import asyncio
import logging
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.base import AsyncSessionLocal
from app.models import Product
from app.services.web_scraper import scraper_service
from app.services.google_trends import trends_service
from app.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


async def collect_all_fashion_data() -> dict:
    """Collect fashion data from all sources"""
    try:
        logger.info("Starting comprehensive fashion data collection...")
        
        # Categories to collect
        categories = [
            'shirts', 'dresses', 'sarees', 'jeans', 'kurtas',
            'lehengas', 'kurtis', 't-shirts', 'tops', 'palazzo'
        ]
        
        # Collect from web sources
        products = await scraper_service.collect_products_from_all_sources(
            categories=categories,
            products_per_category=20
        )
        
        # Collect Google Trends data
        trends_data = await trends_service.analyze_fashion_keywords(
            state_code='IN-TN',
            timeframe='today 3-m'
        )
        
        # Save products to database
        products_saved = await _save_products_to_db(products)
        
        # Update trends data
        trends_updated = await _save_trends_to_db(trends_data)
        
        logger.info(f"Data collection completed: {products_saved} products saved, {trends_updated} trends updated")
        
        return {
            'total_products': products_saved,
            'trends_updated': trends_updated,
            'status': 'success'
        }
        
    except Exception as e:
        logger.error(f"Error in collect_all_fashion_data: {e}", exc_info=True)
        return {
            'total_products': 0,
            'trends_updated': 0,
            'status': 'error',
            'error': str(e)
        }


async def _save_products_to_db(products: list) -> int:
    """Save collected products to database"""
    saved_count = 0
    
    try:
        async with AsyncSessionLocal() as db:
            for product_data in products:
                try:
                    # Check if product already exists
                    from sqlalchemy import select
                    query = select(Product).where(
                        Product.source == product_data.get('source'),
                        Product.name == product_data.get('name')
                    )
                    result = await db.execute(query)
                    existing = result.scalar_one_or_none()
                    
                    if existing:
                        # Update existing product
                        existing.price = product_data.get('price', existing.price)
                        existing.last_scraped_at = datetime.now()
                        existing.view_count += 1
                    else:
                        # Create new product
                        product = Product(
                            name=product_data.get('name', 'Unknown Product'),
                            category=product_data.get('category', 'clothing'),
                            source=product_data.get('source', 'unknown'),
                            source_url=product_data.get('source_url'),
                            brand=product_data.get('brand'),
                            price=product_data.get('price', 0.0),
                            image_url=product_data.get('image_url'),
                            state=settings.DEFAULT_STATE,
                            trend_score=50.0,  # Initial score
                            popularity_score=50.0,
                            last_scraped_at=datetime.now()
                        )
                        db.add(product)
                        saved_count += 1
                    
                except Exception as e:
                    logger.error(f"Error saving product: {e}")
                    continue
            
            await db.commit()
            logger.info(f"Saved {saved_count} new products to database")
            
    except Exception as e:
        logger.error(f"Error in _save_products_to_db: {e}", exc_info=True)
    
    return saved_count


async def _save_trends_to_db(trends_data: dict) -> int:
    """Save trends data to database"""
    updated_count = 0
    
    try:
        from app.models import Trend
        from sqlalchemy import select
        
        async with AsyncSessionLocal() as db:
            for keyword, data in trends_data.items():
                try:
                    # Check if trend exists
                    query = select(Trend).where(
                        Trend.keyword == keyword,
                        Trend.state == settings.DEFAULT_STATE
                    )
                    result = await db.execute(query)
                    existing = result.scalar_one_or_none()
                    
                    current_score = data.get('current_score', 0)
                    avg_score = data.get('avg_score', 0)
                    
                    if existing:
                        # Update existing trend
                        existing.interest_score = current_score
                        existing.search_volume = int(current_score * 1000)  # Approximate
                        existing.data_date = datetime.now()
                        existing.is_rising = data.get('trend') == 'rising'
                    else:
                        # Create new trend
                        trend = Trend(
                            keyword=keyword,
                            category='fashion',
                            trend_type='keyword',
                            interest_score=current_score,
                            search_volume=int(current_score * 1000),
                            state=settings.DEFAULT_STATE,
                            data_date=datetime.now(),
                            is_rising=data.get('trend') == 'rising',
                            momentum_score=avg_score
                        )
                        db.add(trend)
                        updated_count += 1
                    
                except Exception as e:
                    logger.error(f"Error saving trend {keyword}: {e}")
                    continue
            
            await db.commit()
            logger.info(f"Updated {updated_count} trends in database")
            
    except Exception as e:
        logger.error(f"Error in _save_trends_to_db: {e}", exc_info=True)
    
    return updated_count
