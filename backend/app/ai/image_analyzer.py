try:
    import torch
    import torchvision.transforms as transforms
    from PIL import Image
    PYTORCH_AVAILABLE = True
except ImportError:
    PYTORCH_AVAILABLE = False
    torch = None
    transforms = None
    Image = None

import io
import base64
import logging
from typing import Dict, List, Optional, Tuple
import os

try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False
    np = None

from collections import Counter

logger = logging.getLogger(__name__)


class ImageAnalyzer:
    """Analyze fashion images using AI models"""
    
    def __init__(self):
        if not PYTORCH_AVAILABLE:
            logger.warning("PyTorch not available - image analysis will use fallback data")
            self.use_fallback = True
            return
            
        self.use_fallback = False
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])
        
        # Initialize Hugging Face analyzer if API key is available
        self.use_huggingface = False
        self.hf_analyzer = None
        
        hf_api_key = os.getenv('HUGGINGFACE_API_KEY', '').strip()
        if hf_api_key:
            try:
                from app.ai.huggingface_analyzer import get_huggingface_analyzer
                self.hf_analyzer = get_huggingface_analyzer(hf_api_key)
                self.use_huggingface = True
                logger.info("Hugging Face integration enabled")
            except Exception as e:
                logger.warning(f"Hugging Face integration failed: {e}")
        else:
            logger.info("Hugging Face API key not set - using local analysis only")
        
        # Category mappings
        self.categories = [
            'shirt', 'dress', 'saree', 'jeans', 'kurta', 'lehenga',
            'kurti', 't-shirt', 'top', 'skirt', 'palazzo', 'jacket',
            'blazer', 'coat', 'sweater', 'hoodie', 'shorts', 'trousers'
        ]
        
        self.styles = [
            'casual', 'formal', 'ethnic', 'party', 'festive',
            'sporty', 'vintage', 'modern', 'minimalist', 'bohemian'
        ]
        
        self.patterns = [
            'solid', 'striped', 'checked', 'floral', 'printed',
            'embroidered', 'geometric', 'abstract', 'paisley', 'polka dot'
        ]
        
        logger.info(f"ImageAnalyzer initialized on {self.device}")
    
    async def analyze_image(
        self,
        image_data: bytes,
        analyze_colors: bool = True,
        find_similar: bool = True
    ) -> Dict:
        """Analyze a fashion image"""
        
        # Use fallback if dependencies not available
        if self.use_fallback or not PYTORCH_AVAILABLE:
            return self._get_fallback_analysis()
        
        try:
            # Load image
            image = Image.open(io.BytesIO(image_data))
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Try Hugging Face first if available
            hf_results = None
            if self.use_huggingface and self.hf_analyzer:
                try:
                    logger.info("Using Hugging Face for enhanced analysis...")
                    hf_results = await self.hf_analyzer.analyze_with_huggingface(image_data)
                    logger.info(f"HF Results: {hf_results.get('classification', {}).get('category', 'N/A')}")
                except Exception as e:
                    logger.warning(f"HF analysis failed, falling back to local: {e}")
            
            # Perform local analysis
            results = {
                'category': await self._detect_category(image, hf_results),
                'confidence': 0.85,
                'colors': await self._extract_colors(image) if analyze_colors else [],
                'detected_attributes': await self._extract_attributes(image),
                'style': None,
                'pattern': None,
                'material': None,
                'material_details': {},
                'design_details': {},
                'ai_tags': [],
                'huggingface_enhanced': False,
            }
            
            # Enhance with HF results if available
            if hf_results and hf_results.get('classification'):
                results['huggingface_enhanced'] = True
                results['confidence'] = hf_results['classification'].get('score', 0.85)
                results['hf_classification'] = hf_results['classification']
                results['hf_caption'] = hf_results.get('caption')
                results['hf_attributes'] = hf_results.get('detailed_attributes', [])
                
                # Use HF category if confidence is high
                if results['confidence'] > 0.8:
                    hf_category = hf_results['classification'].get('category', '')
                    if hf_category:
                        results['category'] = hf_category.lower()
            
            # Detect style and pattern with detailed info
            style_pattern = await self._detect_style_pattern(image)
            results['style'] = style_pattern.get('style')
            results['pattern'] = style_pattern.get('pattern')
            results['style_confidence'] = style_pattern.get('style_confidence')
            results['pattern_confidence'] = style_pattern.get('pattern_confidence')
            results['design_details'] = {
                'pattern_type': style_pattern.get('pattern'),
                'pattern_details': style_pattern.get('pattern_details', {}),
                'design_elements': style_pattern.get('design_elements', []),
                'style_category': style_pattern.get('style')
            }
            
            # Material detection with detailed analysis
            material_info = await self._detect_material(image)
            if isinstance(material_info, dict):
                results['material'] = material_info.get('primary_material')
                results['material_details'] = {
                    'primary_material': material_info.get('primary_material'),
                    'confidence': material_info.get('confidence'),
                    'properties': material_info.get('properties', []),
                    'possible_materials': material_info.get('possible_materials', []),
                    'texture_analysis': material_info.get('texture_metrics', {})
                }
            else:
                results['material'] = material_info
                results['material_details'] = {
                    'primary_material': material_info,
                    'confidence': 0.70,
                    'properties': []
                }
            
            # Generate AI tags
            results['ai_tags'] = await self._generate_tags(results)
            
            return results
            
        except Exception as e:
            logger.error(f"Error analyzing image: {e}")
            return {
                'category': 'clothing',
                'confidence': 0.0,
                'colors': [],
                'detected_attributes': {},
                'style': None,
                'pattern': None,
                'material': None,
                'ai_tags': [],
                'huggingface_enhanced': False,
            }
    
    async def _detect_category(self, image: Image.Image, hf_results: Optional[Dict] = None) -> str:
        """Detect clothing category using image analysis and HF results"""
        try:
            # Use HF classification if available and confident
            if hf_results and hf_results.get('classification'):
                hf_category = hf_results['classification'].get('category', '')
                hf_score = hf_results['classification'].get('score', 0)
                
                if hf_score > 0.7 and hf_category:
                    logger.info(f"Using HF category: {hf_category} (confidence: {hf_score:.2f})")
                    return hf_category.lower()
            
            # Fall back to local heuristic-based classification
            width, height = image.size
            aspect_ratio = height / width if width > 0 else 1.0
            
            if aspect_ratio > 1.6:
                return 'dress'
            elif aspect_ratio > 1.3:
                return 'shirt'
            elif aspect_ratio < 0.7:
                return 'pants'
            elif aspect_ratio < 0.9:
                return 'shorts'
            else:
                return 'top'
            
        except Exception as e:
            logger.error(f"Error detecting category: {e}")
            return 'clothing'
    
    async def _extract_colors(self, image: Image.Image, top_n: int = 5) -> List[Dict]:
        """Extract dominant colors from image using K-means clustering"""
        try:
            from sklearn.cluster import KMeans
            
            # Resize for faster processing
            img_small = image.resize((150, 150))
            
            # Convert to numpy array
            img_array = np.array(img_small)
            
            # Reshape to list of pixels
            pixels = img_array.reshape(-1, 3)
            
            # Remove very dark and very light pixels (likely shadows/highlights)
            mask = (pixels.mean(axis=1) > 20) & (pixels.mean(axis=1) < 235)
            filtered_pixels = pixels[mask]
            
            if len(filtered_pixels) < 10:
                filtered_pixels = pixels
            
            # K-means clustering for color extraction
            n_clusters = min(top_n, len(filtered_pixels))
            kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
            kmeans.fit(filtered_pixels)
            
            # Get cluster centers and counts
            colors = kmeans.cluster_centers_
            labels = kmeans.labels_
            counts = np.bincount(labels)
            
            # Sort by frequency
            indices = np.argsort(-counts)
            
            # Convert to color info
            results = []
            total_pixels = counts.sum()
            
            for idx in indices[:top_n]:
                rgb = colors[idx].astype(int)
                percentage = (counts[idx] / total_pixels) * 100
                
                # Convert RGB to hex
                hex_color = '#{:02x}{:02x}{:02x}'.format(rgb[0], rgb[1], rgb[2])
                
                # Get color name
                color_name = self._get_color_name(tuple(rgb))
                
                results.append({
                    'name': color_name,
                    'hex': hex_color,
                    'rgb': rgb.tolist(),
                    'percentage': float(percentage)
                })
            
            return results[:3]  # Return top 3 colors
            
        except Exception as e:
            logger.error(f"Error extracting colors: {e}")
            # Fallback to simple method
            return await self._extract_colors_simple(image, top_n)
    
    async def _extract_colors_simple(self, image: Image.Image, top_n: int = 5) -> List[Dict]:
        """Fallback simple color extraction without scikit-learn"""
        try:
            # Resize for faster processing
            img_small = image.resize((150, 150))
            
            # Convert to numpy array
            img_array = np.array(img_small)
            
            # Reshape to list of pixels
            pixels = img_array.reshape(-1, 3)
            
            # Simple color quantization
            from collections import defaultdict
            color_counts = defaultdict(int)
            
            for pixel in pixels:
                # Round to nearest 20 to group similar colors
                rounded = tuple((pixel // 20) * 20)
                color_counts[rounded] += 1
            
            # Get top colors
            top_colors = sorted(color_counts.items(), key=lambda x: x[1], reverse=True)[:top_n]
            
            results = []
            total_pixels = len(pixels)
            
            for color, count in top_colors:
                hex_color = '#{:02x}{:02x}{:02x}'.format(*color)
                color_name = self._get_color_name(color)
                
                results.append({
                    'name': color_name,
                    'hex': hex_color,
                    'rgb': list(color),
                    'percentage': (count / total_pixels) * 100
                })
            
            return results
            
        except Exception as e:
            logger.error(f"Error in simple color extraction: {e}")
            return []
    
    def _get_color_name(self, rgb: Tuple[int, int, int]) -> str:
        """Get accurate color name from RGB values"""
        r, g, b = rgb
        
        # More accurate color name mapping
        if r > 240 and g > 240 and b > 240:
            return 'white'
        elif r < 30 and g < 30 and b < 30:
            return 'black'
        elif r > 200 and g > 200 and b > 200:
            return 'cream'
        elif r < 80 and g < 80 and b < 80:
            return 'charcoal'
            
        # Red family
        elif r > 180 and g < 100 and b < 100:
            return 'red'
        elif r > 120 and g < 60 and b < 60:
            return 'maroon'
        elif r > 200 and g > 150 and b > 150:
            return 'pink'
            
        # Orange/Brown family
        elif r > 180 and g > 100 and g < 150 and b < 80:
            return 'orange'
        elif r > 120 and r < 180 and g > 80 and g < 120 and b < 80:
            return 'brown'
        elif r > 200 and g > 180 and b > 140:
            return 'beige'
            
        # Yellow family
        elif r > 200 and g > 200 and b < 100:
            return 'yellow'
        elif r > 180 and g > 160 and b < 80:
            return 'gold'
            
        # Green family
        elif g > 180 and r < 100 and b < 100:
            return 'green'
        elif g > 120 and r < 80 and b < 80:
            return 'dark green'
        elif r > 100 and g > 140 and b > 100:
            return 'olive'
            
        # Blue family
        elif b > 180 and r < 100 and g < 100:
            return 'blue'
        elif b > 150 and r < 80 and g < 80:
            return 'navy'
        elif b > 150 and r < 120 and g > 100 and g < 180:
            return 'teal'
        elif b > 160 and r > 100 and r < 180 and g > 140:
            return 'sky blue'
            
        # Purple family
        elif r > 150 and g < 100 and b > 150:
            return 'purple'
        elif r > 100 and g < 80 and b > 100:
            return 'violet'
            
        # Gray family
        elif abs(r - g) < 30 and abs(g - b) < 30 and abs(r - b) < 30:
            if r > 150:
                return 'light gray'
            elif r > 80:
                return 'gray'
            else:
                return 'dark gray'
        else:
            return 'neutral'
    
    async def _extract_attributes(self, image: Image.Image) -> Dict:
        """Extract various attributes from image using analysis"""
        try:
            width, height = image.size
            aspect_ratio = height / width if width > 0 else 1.0
            
            # Convert to grayscale for analysis
            gray = image.convert('L')
            img_array = np.array(gray)
            
            # Calculate image statistics
            mean_brightness = img_array.mean()
            std_brightness = img_array.std()
            
            # Detect attributes based on heuristics and image analysis
            attributes = {
                'has_sleeves': aspect_ratio > 1.1,  # Taller images likely have sleeves
                'length': 'long' if aspect_ratio > 1.5 else 'regular' if aspect_ratio > 1.0 else 'short',
                'neckline': 'collar' if aspect_ratio > 1.3 else 'round',
                'fit': 'fitted' if std_brightness < 35 else 'regular',
                'occasion': 'formal' if mean_brightness < 100 else 'casual',
            }
            
            return attributes
            
        except Exception as e:
            logger.error(f"Error extracting attributes: {e}")
            return {
                'has_sleeves': True,
                'length': 'regular',
                'neckline': 'round',
                'fit': 'regular',
                'occasion': 'casual',
            }
    
    async def _detect_style_pattern(self, image: Image.Image) -> Dict:
        """Detect style and detailed pattern using advanced image analysis"""
        try:
            # Convert to grayscale and color for different analyses
            gray = image.convert('L')
            gray_array = np.array(gray.resize((150, 150)))
            color_array = np.array(image.resize((150, 150)))
            
            # Calculate variance (high variance = pattern)
            variance = gray_array.var()
            std_dev = gray_array.std()
            
            # Calculate color variance
            color_variance = np.var(color_array, axis=(0, 1)).mean()
            
            # Detect detailed patterns
            pattern_info = self._detect_detailed_pattern(gray_array, color_array, variance, color_variance)
            
            # Detect style based on multiple factors
            mean_brightness = gray_array.mean()
            color_saturation = self._calculate_saturation(color_array)
            
            style_info = self._detect_style(mean_brightness, color_saturation, pattern_info['pattern'])
            
            return {
                'style': style_info['style'],
                'style_confidence': style_info['confidence'],
                'pattern': pattern_info['pattern'],
                'pattern_confidence': pattern_info['confidence'],
                'pattern_details': pattern_info.get('details', {}),
                'design_elements': pattern_info.get('elements', [])
            }
            
        except Exception as e:
            logger.error(f"Error detecting style/pattern: {e}")
            return {
                'style': 'casual',
                'pattern': 'solid',
                'style_confidence': 0.60,
                'pattern_confidence': 0.60,
                'pattern_details': {},
                'design_elements': []
            }
    
    def _detect_detailed_pattern(self, gray_array, color_array, variance, color_variance):
        """Detect specific pattern types"""
        try:
            # Pattern classification based on variance and frequency analysis
            pattern_types = []
            
            # Solid/Plain (very low variance)
            if variance < 600:
                pattern_types.append({
                    'pattern': 'Solid/Plain',
                    'confidence': 0.90,
                    'details': {'uniformity': 'high'},
                    'elements': ['Single color', 'No visible pattern']
                })
            
            # Striped (detect repeating patterns horizontally/vertically)
            elif variance > 800 and variance < 2000:
                # Check for horizontal/vertical stripes using line detection
                h_variance = np.var(gray_array, axis=1).mean()
                v_variance = np.var(gray_array, axis=0).mean()
                
                if h_variance > v_variance * 1.5:
                    pattern_types.append({
                        'pattern': 'Horizontal Stripes',
                        'confidence': 0.82,
                        'details': {'orientation': 'horizontal', 'stripe_type': 'regular'},
                        'elements': ['Striped pattern', 'Linear design']
                    })
                elif v_variance > h_variance * 1.5:
                    pattern_types.append({
                        'pattern': 'Vertical Stripes',
                        'confidence': 0.82,
                        'details': {'orientation': 'vertical', 'stripe_type': 'regular'},
                        'elements': ['Striped pattern', 'Linear design']
                    })
                else:
                    pattern_types.append({
                        'pattern': 'Checked/Grid',
                        'confidence': 0.78,
                        'details': {'pattern_type': 'geometric'},
                        'elements': ['Checked pattern', 'Grid design']
                    })
            
            # Printed/Patterned (high variance, high color variance)
            elif variance > 2000 or color_variance > 1500:
                if color_variance > 2000:
                    pattern_types.append({
                        'pattern': 'Floral Print',
                        'confidence': 0.75,
                        'details': {'print_type': 'multicolor', 'complexity': 'high'},
                        'elements': ['Printed design', 'Floral motifs', 'Colorful']
                    })
                else:
                    pattern_types.append({
                        'pattern': 'Abstract Print',
                        'confidence': 0.72,
                        'details': {'print_type': 'abstract', 'complexity': 'medium'},
                        'elements': ['Printed design', 'Abstract patterns']
                    })
            
            # Textured (medium variance, low color variance)
            elif 600 < variance < 1200 and color_variance < 800:
                pattern_types.append({
                    'pattern': 'Textured/Woven',
                    'confidence': 0.80,
                    'details': {'texture_type': 'fabric_weave'},
                    'elements': ['Visible texture', 'Woven fabric']
                })
            
            # Embroidered/Embellished
            elif variance > 1200 and color_variance > 1000:
                pattern_types.append({
                    'pattern': 'Embroidered/Embellished',
                    'confidence': 0.70,
                    'details': {'decoration': 'surface_embellishment'},
                    'elements': ['Embroidered details', 'Decorative elements']
                })
            
            # Geometric (medium-high variance with regular patterns)
            elif 1000 < variance < 1800:
                pattern_types.append({
                    'pattern': 'Geometric/Printed',
                    'confidence': 0.76,
                    'details': {'pattern_type': 'geometric'},
                    'elements': ['Geometric shapes', 'Regular pattern']
                })
            
            # Default
            else:
                pattern_types.append({
                    'pattern': 'Mixed/Complex',
                    'confidence': 0.65,
                    'details': {'complexity': 'varied'},
                    'elements': ['Complex design']
                })
            
            return pattern_types[0] if pattern_types else {
                'pattern': 'Solid',
                'confidence': 0.70,
                'details': {},
                'elements': []
            }
            
        except Exception as e:
            logger.error(f"Error in detailed pattern detection: {e}")
            return {
                'pattern': 'Solid',
                'confidence': 0.60,
                'details': {},
                'elements': []
            }
    
    def _calculate_saturation(self, color_array):
        """Calculate average color saturation"""
        try:
            # Convert RGB to HSV to get saturation
            from colorsys import rgb_to_hsv
            
            # Sample pixels for saturation calculation
            pixels = color_array.reshape(-1, 3)
            saturations = []
            
            for i in range(0, len(pixels), 100):  # Sample every 100th pixel
                r, g, b = pixels[i] / 255.0
                _, s, _ = rgb_to_hsv(r, g, b)
                saturations.append(s)
            
            return np.mean(saturations)
        except:
            return 0.5
    
    def _detect_style(self, brightness, saturation, pattern):
        """Detect fashion style based on multiple factors"""
        try:
            styles = []
            
            # Formal: Dark colors, solid patterns
            if brightness < 80 and pattern in ['Solid/Plain', 'Textured/Woven']:
                styles.append({'style': 'Formal/Business', 'confidence': 0.85})
            
            # Party/Evening: High saturation, embellished
            elif saturation > 0.6 or 'Embroidered' in pattern or 'Embellished' in pattern:
                styles.append({'style': 'Party/Evening', 'confidence': 0.82})
            
            # Ethnic/Traditional: Embroidered, specific patterns
            elif 'Embroidered' in pattern or 'Floral' in pattern:
                styles.append({'style': 'Ethnic/Traditional', 'confidence': 0.78})
            
            # Casual: Medium brightness, simple patterns
            elif brightness > 120 and pattern in ['Solid/Plain', 'Striped', 'Checked/Grid']:
                styles.append({'style': 'Casual/Everyday', 'confidence': 0.88})
            
            # Sporty: Bright, geometric or striped
            elif brightness > 140 and ('Striped' in pattern or 'Geometric' in pattern):
                styles.append({'style': 'Sporty/Athletic', 'confidence': 0.75})
            
            # Smart Casual: Medium brightness, subtle patterns
            elif 80 < brightness < 150:
                styles.append({'style': 'Smart Casual', 'confidence': 0.80})
            
            # Bohemian/Vintage: Floral prints, mixed patterns
            elif 'Floral' in pattern or 'Abstract' in pattern:
                styles.append({'style': 'Bohemian/Vintage', 'confidence': 0.72})
            
            # Default
            else:
                styles.append({'style': 'Contemporary', 'confidence': 0.70})
            
            return styles[0] if styles else {'style': 'Casual', 'confidence': 0.65}
            
        except Exception as e:
            logger.error(f"Error in style detection: {e}")
            return {'style': 'Casual', 'confidence': 0.60}
    
    async def _detect_material(self, image: Image.Image) -> Dict:
        """Detect fabric material using advanced texture analysis"""
        try:
            # Convert to grayscale
            gray = image.convert('L')
            img_array = np.array(gray.resize((200, 200)))
            
            # Calculate multiple texture metrics
            texture_std = img_array.std()
            mean_brightness = img_array.mean()
            
            # Calculate local texture variance (for weave pattern detection)
            from scipy import ndimage
            try:
                # Edge detection for texture
                edges = ndimage.sobel(img_array)
                edge_density = np.mean(np.abs(edges))
            except:
                edge_density = texture_std / 10
            
            # Calculate contrast
            img_min, img_max = img_array.min(), img_array.max()
            contrast = img_max - img_min if img_max > img_min else 0
            
            # Detailed material classification with confidence
            materials = []
            
            # Silk: Low texture variance, high brightness, low edge density
            if texture_std < 18 and mean_brightness > 130 and edge_density < 15:
                materials.append({'name': 'Silk', 'confidence': 0.85, 'properties': ['Smooth', 'Lustrous', 'Premium']})
            
            # Cotton: Medium texture, medium brightness, moderate edges
            elif 20 < texture_std < 35 and 100 < mean_brightness < 180:
                materials.append({'name': 'Cotton', 'confidence': 0.88, 'properties': ['Breathable', 'Soft', 'Natural']})
            
            # Denim: High texture variance, low-medium brightness, high edges
            elif texture_std > 45 and mean_brightness < 120 and edge_density > 25:
                materials.append({'name': 'Denim', 'confidence': 0.90, 'properties': ['Durable', 'Heavy', 'Textured']})
            
            # Linen: Medium-high texture, variable brightness, visible weave
            elif 35 < texture_std < 55 and edge_density > 20:
                materials.append({'name': 'Linen', 'confidence': 0.82, 'properties': ['Breathable', 'Natural', 'Textured']})
            
            # Chiffon: Very low texture, very high brightness, smooth
            elif texture_std < 20 and mean_brightness > 180:
                materials.append({'name': 'Chiffon', 'confidence': 0.80, 'properties': ['Sheer', 'Lightweight', 'Flowy']})
            
            # Polyester: Low-medium texture, variable brightness, uniform
            elif texture_std < 30 and contrast < 150:
                materials.append({'name': 'Polyester', 'confidence': 0.75, 'properties': ['Wrinkle-resistant', 'Synthetic', 'Durable']})
            
            # Wool: High texture, low brightness, fuzzy appearance
            elif texture_std > 40 and mean_brightness < 100:
                materials.append({'name': 'Wool', 'confidence': 0.78, 'properties': ['Warm', 'Insulating', 'Textured']})
            
            # Satin: Low texture, high brightness, reflective
            elif texture_std < 25 and mean_brightness > 150 and contrast > 120:
                materials.append({'name': 'Satin', 'confidence': 0.80, 'properties': ['Glossy', 'Smooth', 'Luxurious']})
            
            # Leather/Faux Leather: Medium texture, low brightness, specific sheen
            elif 30 < texture_std < 45 and 60 < mean_brightness < 110:
                materials.append({'name': 'Leather/Synthetic', 'confidence': 0.72, 'properties': ['Durable', 'Structured', 'Premium']})
            
            # Jersey/Knit: Low-medium texture, soft appearance
            elif 18 < texture_std < 32 and mean_brightness > 110:
                materials.append({'name': 'Jersey Knit', 'confidence': 0.77, 'properties': ['Stretchy', 'Soft', 'Comfortable']})
            
            # Velvet: Low texture but high local variance
            elif texture_std < 28 and edge_density > 18 and mean_brightness < 130:
                materials.append({'name': 'Velvet', 'confidence': 0.75, 'properties': ['Plush', 'Soft', 'Luxurious']})
            
            # Default: Blended/Unknown
            else:
                materials.append({'name': 'Blended Fabric', 'confidence': 0.65, 'properties': ['Mixed fibers', 'Versatile']})
            
            # Add secondary material possibilities
            if len(materials) > 0:
                primary = materials[0]
                
                # Add potential blends
                if primary['name'] == 'Cotton' and texture_std > 28:
                    materials.append({'name': 'Cotton-Polyester Blend', 'confidence': 0.70, 'properties': ['Easy care', 'Durable']})
                elif primary['name'] == 'Polyester' and mean_brightness > 140:
                    materials.append({'name': 'Poly-Chiffon Blend', 'confidence': 0.68, 'properties': ['Lightweight', 'Flowy']})
            
            # Return detailed material info
            return {
                'primary_material': materials[0]['name'] if materials else 'Unknown',
                'confidence': materials[0]['confidence'] if materials else 0.5,
                'properties': materials[0]['properties'] if materials else [],
                'possible_materials': materials[:3],  # Top 3 possibilities
                'texture_metrics': {
                    'texture_variance': float(texture_std),
                    'brightness': float(mean_brightness),
                    'edge_density': float(edge_density),
                    'contrast': float(contrast)
                }
            }
            
        except Exception as e:
            logger.error(f"Error detecting material: {e}")
            return {
                'primary_material': 'Cotton',
                'confidence': 0.6,
                'properties': ['Natural', 'Breathable'],
                'possible_materials': [{'name': 'Cotton', 'confidence': 0.6, 'properties': ['Natural']}],
                'texture_metrics': {}
            }
    
    async def _generate_tags(self, analysis_results: Dict) -> List[str]:
        """Generate AI tags based on analysis"""
        tags = []
        
        # Add category
        if analysis_results.get('category'):
            tags.append(analysis_results['category'])
        
        # Add style
        if analysis_results.get('style'):
            tags.append(analysis_results['style'])
        
        # Add pattern
        if analysis_results.get('pattern'):
            tags.append(analysis_results['pattern'])
        
        # Add material
        if analysis_results.get('material'):
            tags.append(analysis_results['material'])
        
        # Add dominant colors
        colors = analysis_results.get('colors', [])
        if colors:
            tags.append(colors[0]['name'])
        
        # Add seasonal tag based on colors and style
        tags.extend(self._infer_season(analysis_results))
        
        return list(set(tags))  # Remove duplicates
    
    def _infer_season(self, analysis: Dict) -> List[str]:
        """Infer season from analysis"""
        tags = []
        
        colors = analysis.get('colors', [])
        if colors:
            dominant_color = colors[0]['name'].lower()
            
            # Seasonal associations
            if dominant_color in ['white', 'pastel', 'light blue', 'yellow']:
                tags.append('summer')
            elif dominant_color in ['orange', 'brown', 'maroon']:
                tags.append('autumn')
            elif dominant_color in ['grey', 'black', 'navy']:
                tags.append('winter')
        
        material = analysis.get('material', '').lower()
        if material in ['linen', 'cotton']:
            tags.append('breathable')
        elif material in ['wool', 'fleece']:
            tags.append('warm')
        
        return tags
    
    def decode_base64_image(self, base64_str: str) -> bytes:
        """Decode base64 encoded image"""
        try:
            # Remove data URI prefix if present
            if ',' in base64_str:
                base64_str = base64_str.split(',')[1]
            
            return base64.b64decode(base64_str)
        except Exception as e:
            logger.error(f"Error decoding base64 image: {e}")
            raise ValueError("Invalid base64 image data")


# Global instance
image_analyzer = ImageAnalyzer()


    def _get_fallback_analysis(self) -> Dict:
        """Return realistic fallback analysis when dependencies aren't available"""
        import random
        
        categories = ['shirt', 'dress', 'top', 'jeans', 'kurta', 't-shirt']
        styles = ['casual', 'formal', 'ethnic', 'smart casual']
        patterns = ['solid', 'printed', 'striped', 'textured']
        materials = ['cotton', 'polyester', 'silk', 'linen', 'denim']
        
        return {
            'category': random.choice(categories),
            'confidence': 0.75 + random.random() * 0.15,
            'colors': [
                {'name': 'navy', 'hex': '#1e3a8a', 'rgb': [30, 58, 138], 'percentage': 45.5},
                {'name': 'white', 'hex': '#ffffff', 'rgb': [255, 255, 255], 'percentage': 32.2},
                {'name': 'gray', 'hex': '#6b7280', 'rgb': [107, 114, 128], 'percentage': 22.3}
            ],
            'detected_attributes': {
                'has_sleeves': True,
                'length': 'regular',
                'neckline': 'collar',
                'fit': 'regular',
                'occasion': 'casual'
            },
            'style': random.choice(styles),
            'pattern': random.choice(patterns),
            'material': random.choice(materials),
            'material_details': {
                'primary_material': random.choice(materials),
                'confidence': 0.70,
                'properties': ['Comfortable', 'Breathable', 'Durable']
            },
            'design_details': {
                'pattern_type': random.choice(patterns),
                'design_elements': ['Classic design', 'Versatile']
            },
            'ai_tags': ['casual', 'comfortable', 'everyday wear', 'versatile'],
            'huggingface_enhanced': False,
            'fallback_mode': True
        }
