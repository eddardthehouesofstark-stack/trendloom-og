"""
Hugging Face API Integration for Fashion Analysis
Uses free Inference API - no GPU required!
"""
import requests
import base64
import logging
from typing import Dict, List, Optional
from io import BytesIO
from PIL import Image

logger = logging.getLogger(__name__)


class HuggingFaceAnalyzer:
    """Analyze fashion images using Hugging Face models"""
    
    # Free Hugging Face Inference API endpoints
    FASHION_CLIP_MODEL = "patrickjohncyh/fashion-clip"
    IMAGE_CLASSIFICATION_MODEL = "Matthijs/swin-finetuned-clothing-classification"
    BLIP_CAPTIONING_MODEL = "Salesforce/blip-image-captioning-large"
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self.headers = {}
        if api_key:
            self.headers["Authorization"] = f"Bearer {api_key}"
    
    async def analyze_with_huggingface(self, image_bytes: bytes) -> Dict:
        """
        Analyze fashion image using multiple HuggingFace models
        Returns detailed fashion information including exact categories
        """
        try:
            results = {
                'classification': None,
                'caption': None,
                'detailed_attributes': [],
                'confidence_scores': {}
            }
            
            # 1. Image Classification - Specific clothing categories
            classification = await self._classify_clothing(image_bytes)
            if classification:
                results['classification'] = classification
                results['confidence_scores']['classification'] = classification.get('score', 0)
            
            # 2. Image Captioning - Natural language description
            caption = await self._generate_caption(image_bytes)
            if caption:
                results['caption'] = caption
            
            # 3. Extract detailed attributes from results
            results['detailed_attributes'] = self._extract_attributes_from_results(
                classification, caption
            )
            
            return results
            
        except Exception as e:
            logger.error(f"Hugging Face analysis error: {e}")
            return {
                'classification': None,
                'caption': None,
                'detailed_attributes': [],
                'confidence_scores': {},
                'error': str(e)
            }
    
    async def _classify_clothing(self, image_bytes: bytes) -> Optional[Dict]:
        """Classify clothing into specific categories using Swin transformer"""
        try:
            api_url = f"https://api-inference.huggingface.co/models/{self.IMAGE_CLASSIFICATION_MODEL}"
            
            response = requests.post(
                api_url,
                headers=self.headers,
                data=image_bytes,
                timeout=30
            )
            
            if response.status_code == 200:
                results = response.json()
                # Returns list of [{label: "dress", score: 0.95}, ...]
                if isinstance(results, list) and len(results) > 0:
                    top_result = results[0]
                    logger.info(f"HF Classification: {top_result['label']} ({top_result['score']:.2f})")
                    return {
                        'category': top_result['label'],
                        'score': top_result['score'],
                        'all_predictions': results[:5]  # Top 5 predictions
                    }
            else:
                logger.warning(f"HF Classification API returned {response.status_code}: {response.text}")
            
            return None
            
        except Exception as e:
            logger.error(f"Clothing classification error: {e}")
            return None
    
    async def _generate_caption(self, image_bytes: bytes) -> Optional[str]:
        """Generate natural language description using BLIP"""
        try:
            api_url = f"https://api-inference.huggingface.co/models/{self.BLIP_CAPTIONING_MODEL}"
            
            response = requests.post(
                api_url,
                headers=self.headers,
                data=image_bytes,
                timeout=30
            )
            
            if response.status_code == 200:
                results = response.json()
                # Returns [{"generated_text": "a woman wearing a blue dress"}]
                if isinstance(results, list) and len(results) > 0:
                    caption = results[0].get('generated_text', '')
                    logger.info(f"HF Caption: {caption}")
                    return caption
            else:
                logger.warning(f"HF Captioning API returned {response.status_code}: {response.text}")
            
            return None
            
        except Exception as e:
            logger.error(f"Caption generation error: {e}")
            return None
    
    def _extract_attributes_from_results(
        self, 
        classification: Optional[Dict], 
        caption: Optional[str]
    ) -> List[str]:
        """Extract fashion attributes from HF results"""
        attributes = []
        
        # From classification
        if classification:
            category = classification.get('category', '').lower()
            attributes.append(f"Category: {category}")
            
            # Add confidence info
            score = classification.get('score', 0)
            if score > 0.9:
                attributes.append("High Confidence Detection")
            
        # From caption - extract keywords
        if caption:
            caption_lower = caption.lower()
            
            # Colors
            colors = ['red', 'blue', 'green', 'yellow', 'black', 'white', 'pink', 
                     'purple', 'orange', 'brown', 'grey', 'gray', 'navy', 'beige']
            for color in colors:
                if color in caption_lower:
                    attributes.append(f"Color: {color}")
            
            # Styles
            styles = ['casual', 'formal', 'elegant', 'sporty', 'vintage', 
                     'modern', 'traditional', 'ethnic']
            for style in styles:
                if style in caption_lower:
                    attributes.append(f"Style: {style}")
            
            # Patterns
            patterns = ['striped', 'floral', 'printed', 'solid', 'checked', 
                       'dotted', 'embroidered']
            for pattern in patterns:
                if pattern in caption_lower:
                    attributes.append(f"Pattern: {pattern}")
        
        return attributes
    
    def get_fashion_categories(self) -> List[str]:
        """Get list of all fashion categories the model can detect"""
        # Based on clothing classification model training
        return [
            'T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
            'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot',
            'Blouse', 'Skirt', 'Jacket', 'Sweater', 'Cardigan',
            'Jeans', 'Shorts', 'Suit', 'Tank top', 'Hoodie'
        ]


# Global instance
huggingface_analyzer = None

def get_huggingface_analyzer(api_key: Optional[str] = None) -> HuggingFaceAnalyzer:
    """Get or create HuggingFace analyzer instance"""
    global huggingface_analyzer
    if huggingface_analyzer is None:
        huggingface_analyzer = HuggingFaceAnalyzer(api_key)
    return huggingface_analyzer
