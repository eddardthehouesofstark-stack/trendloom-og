import asyncio
import aiohttp
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
import logging
import re
from urllib.parse import urljoin, quote_plus
from app.config import get_settings

settings = get_settings()
logger = logging.getLogger(__name__)


class WebScraperService:
    """Service to scrape fashion data from multiple sources"""
    
    def __init__(self):
        self.headers = {
            'User-Agent': settings.USER_AGENT,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        }
    
    async def fetch_page(self, url: str, session: aiohttp.ClientSession) -> Optional[str]:
        """Fetch a web page"""
        try:
            async with session.get(url, headers=self.headers, timeout=aiohttp.ClientTimeout(total=15)) as response:
                if response.status == 200:
                    return await response.text()
                logger.warning(f"Failed to fetch {url}: Status {response.status}")
                return None
        except Exception as e:
            logger.error(f"Error fetching {url}: {e}")
            return None
    
    async def scrape_myntra_products(self, category: str = "casual-shirts", limit: int = 20) -> List[Dict]:
        """Scrape products from Myntra (simplified - use their API if available)"""
        products = []
        
        try:
            # Note: Real implementation would use Myntra's API or proper scraping with Selenium
            # This is a simplified example
            async with aiohttp.ClientSession() as session:
                url = f"https://www.myntra.com/{category}"
                html = await self.fetch_page(url, session)
                
                if not html:
                    return products
                
                soup = BeautifulSoup(html, 'html.parser')
                
                # Example selectors (these would need to be updated based on actual site structure)
                product_cards = soup.find_all('li', class_='product-base', limit=limit)
                
                for card in product_cards:
                    try:
                        product = self._extract_myntra_product(card, url)
                        if product:
                            products.append(product)
                    except Exception as e:
                        logger.error(f"Error extracting Myntra product: {e}")
                        continue
                
        except Exception as e:
            logger.error(f"Error scraping Myntra: {e}")
        
        return products
    
    def _extract_myntra_product(self, card, base_url: str) -> Optional[Dict]:
        """Extract product data from Myntra card"""
        try:
            # Example extraction (adjust selectors based on actual HTML)
            name_elem = card.find('h3', class_='product-product')
            price_elem = card.find('span', class_='product-discountedPrice')
            brand_elem = card.find('h4', class_='product-brand')
            image_elem = card.find('img', class_='img-responsive')
            link_elem = card.find('a')
            
            if not name_elem:
                return None
            
            product = {
                'name': name_elem.get_text(strip=True) if name_elem else '',
                'brand': brand_elem.get_text(strip=True) if brand_elem else '',
                'price': self._extract_price(price_elem.get_text() if price_elem else '0'),
                'image_url': image_elem.get('src', '') if image_elem else '',
                'source': 'myntra',
                'source_url': urljoin(base_url, link_elem.get('href', '')) if link_elem else '',
                'category': 'shirt',
            }
            
            return product
            
        except Exception as e:
            logger.error(f"Error in _extract_myntra_product: {e}")
            return None
    
    async def scrape_ajio_products(self, category: str = "shirts", limit: int = 20) -> List[Dict]:
        """Scrape products from Ajio"""
        products = []
        
        try:
            async with aiohttp.ClientSession() as session:
                url = f"https://www.ajio.com/s/{category}-4461"
                html = await self.fetch_page(url, session)
                
                if not html:
                    return products
                
                soup = BeautifulSoup(html, 'html.parser')
                
                # Example selectors (adjust based on actual site)
                product_items = soup.find_all('div', class_='item', limit=limit)
                
                for item in product_items:
                    try:
                        product = self._extract_ajio_product(item, url)
                        if product:
                            products.append(product)
                    except Exception as e:
                        logger.error(f"Error extracting Ajio product: {e}")
                        continue
                
        except Exception as e:
            logger.error(f"Error scraping Ajio: {e}")
        
        return products
    
    def _extract_ajio_product(self, item, base_url: str) -> Optional[Dict]:
        """Extract product data from Ajio item"""
        try:
            name_elem = item.find('div', class_='nameCls')
            price_elem = item.find('span', class_='price')
            brand_elem = item.find('div', class_='brand')
            image_elem = item.find('img')
            link_elem = item.find('a', class_='rilrtl-products-list__link')
            
            if not name_elem:
                return None
            
            product = {
                'name': name_elem.get_text(strip=True) if name_elem else '',
                'brand': brand_elem.get_text(strip=True) if brand_elem else '',
                'price': self._extract_price(price_elem.get_text() if price_elem else '0'),
                'image_url': image_elem.get('src', '') if image_elem else '',
                'source': 'ajio',
                'source_url': urljoin(base_url, link_elem.get('href', '')) if link_elem else '',
                'category': 'shirt',
            }
            
            return product
            
        except Exception as e:
            logger.error(f"Error in _extract_ajio_product: {e}")
            return None
    
    async def scrape_google_shopping(self, query: str, limit: int = 20) -> List[Dict]:
        """Scrape Google Shopping results (simplified)"""
        products = []
        
        try:
            async with aiohttp.ClientSession() as session:
                # Note: Real implementation would need proper Google Shopping API or scraping
                encoded_query = quote_plus(f"{query} fashion india")
                url = f"https://www.google.com/search?q={encoded_query}&tbm=shop"
                
                html = await self.fetch_page(url, session)
                
                if not html:
                    return products
                
                soup = BeautifulSoup(html, 'html.parser')
                
                # Example extraction (Google's HTML structure changes frequently)
                product_divs = soup.find_all('div', class_='sh-dgr__content', limit=limit)
                
                for div in product_divs:
                    try:
                        product = self._extract_google_shopping_product(div)
                        if product:
                            products.append(product)
                    except Exception as e:
                        logger.error(f"Error extracting Google Shopping product: {e}")
                        continue
                
        except Exception as e:
            logger.error(f"Error scraping Google Shopping: {e}")
        
        return products
    
    def _extract_google_shopping_product(self, div) -> Optional[Dict]:
        """Extract product from Google Shopping result"""
        try:
            title_elem = div.find('h3')
            price_elem = div.find('span', class_='a8Pemb')
            seller_elem = div.find('div', class_='aULzUe')
            image_elem = div.find('img')
            link_elem = div.find('a')
            
            if not title_elem:
                return None
            
            product = {
                'name': title_elem.get_text(strip=True) if title_elem else '',
                'brand': seller_elem.get_text(strip=True) if seller_elem else '',
                'price': self._extract_price(price_elem.get_text() if price_elem else '0'),
                'image_url': image_elem.get('src', '') if image_elem else '',
                'source': 'google_shopping',
                'source_url': link_elem.get('href', '') if link_elem else '',
                'category': 'clothing',
            }
            
            return product
            
        except Exception as e:
            logger.error(f"Error in _extract_google_shopping_product: {e}")
            return None
    
    def _extract_price(self, price_str: str) -> float:
        """Extract numeric price from string"""
        try:
            # Remove currency symbols and commas
            price_clean = re.sub(r'[₹$,\s]', '', price_str)
            # Extract first number
            match = re.search(r'\d+\.?\d*', price_clean)
            if match:
                return float(match.group())
            return 0.0
        except:
            return 0.0
    
    async def collect_products_from_all_sources(
        self,
        categories: List[str],
        products_per_category: int = 20
    ) -> List[Dict]:
        """Collect products from all available sources"""
        all_products = []
        
        tasks = []
        
        for category in categories:
            # Add tasks for each source
            tasks.append(self.scrape_myntra_products(category, products_per_category))
            tasks.append(self.scrape_ajio_products(category, products_per_category))
            tasks.append(self.scrape_google_shopping(category, products_per_category))
            
            # Add delay between batches
            await asyncio.sleep(1)
        
        # Execute all tasks
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        for result in results:
            if isinstance(result, list):
                all_products.extend(result)
            elif isinstance(result, Exception):
                logger.error(f"Task failed: {result}")
        
        logger.info(f"Collected {len(all_products)} products from all sources")
        
        return all_products


# Global instance
scraper_service = WebScraperService()
