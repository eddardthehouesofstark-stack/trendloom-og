import logging
from datetime import datetime
from sqlalchemy import select, func, desc
from typing import Dict

from app.database.base import AsyncSessionLocal
from app.models import Product, Trend, ColorTrend, MaterialTrend
from app.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


async def analyze_trends() -> Dict:
    """Analyze and update trend scores"""
    try:
        logger.info("Starting trend analysis...")
        
        # Update product trend scores
        products_updated = await _update_product_trend_scores()
        
        # Analyze color trends
        colors_updated = await _analyze_color_trends()
        
        # Analyze material trends
        materials_updated = await _analyze_material_trends()
        
        # Update trend statuses
        trends_updated = await _update_trend_statuses()
        
        return {
            'products_updated': products_updated,
            'colors_updated': colors_updated,
            'materials_updated': materials_updated,
            'trends_updated': trends_updated,
            'status': 'success'
        }
        
    except Exception as e:
        logger.error(f"Error in analyze_trends: {e}", exc_info=True)
        return {
            'products_updated': 0,
            'colors_updated': 0,
            'materials_updated': 0,
            'trends_updated': 0,
            'status': 'error',
            'error': str(e)
        }


async def _update_product_trend_scores() -> int:
    """Calculate and update trend scores for products"""
    updated_count = 0
    
    try:
        async with AsyncSessionLocal() as db:
            # Get all active products
            query = select(Product).where(Product.is_active == True)
            result = await db.execute(query)
            products = result.scalars().all()
            
            for product in products:
                try:
                    # Calculate trend score based on multiple factors
                    score = _calculate_trend_score(product)
                    
                    # Update product
                    product.trend_score = score
                    product.is_trending = score >= 70.0
                    product.updated_at = datetime.now()
                    
                    updated_count += 1
                    
                except Exception as e:
                    logger.error(f"Error updating product {product.id}: {e}")
                    continue
            
            await db.commit()
            logger.info(f"Updated trend scores for {updated_count} products")
            
    except Exception as e:
        logger.error(f"Error in _update_product_trend_scores: {e}")
    
    return updated_count


def _calculate_trend_score(product: Product) -> float:
    """Calculate trend score for a product"""
    # Base score
    score = 50.0
    
    # Popularity factor
    if product.popularity_score:
        score += (product.popularity_score / 10)
    
    # Weekly growth factor
    if product.weekly_growth:
        score += min(product.weekly_growth, 20)
    
    # View count factor
    if product.view_count:
        score += min(product.view_count / 100, 10)
    
    # Search count factor
    if product.search_count:
        score += min(product.search_count / 50, 10)
    
    # Recency factor
    if product.created_at:
        days_old = (datetime.now() - product.created_at).days
        if days_old < 7:
            score += 10
        elif days_old < 30:
            score += 5
    
    return min(score, 100.0)


async def _analyze_color_trends() -> int:
    """Analyze and update color trends"""
    updated_count = 0
    
    try:
        async with AsyncSessionLocal() as db:
            # Get color distribution from products
            query = select(
                Product.color,
                Product.color_hex,
                func.count(Product.id).label('product_count'),
                func.avg(Product.trend_score).label('avg_trend'),
                func.avg(Product.weekly_growth).label('avg_growth')
            ).where(
                Product.is_active == True,
                Product.color.isnot(None),
                Product.state == settings.DEFAULT_STATE
            ).group_by(Product.color, Product.color_hex)
            
            result = await db.execute(query)
            rows = result.all()
            
            for row in rows:
                try:
                    # Check if color trend exists
                    color_query = select(ColorTrend).where(
                        ColorTrend.color_name == row.color,
                        ColorTrend.state == settings.DEFAULT_STATE
                    )
                    color_result = await db.execute(color_query)
                    existing = color_result.scalar_one_or_none()
                    
                    popularity = float(row.avg_trend or 0)
                    weekly_growth = float(row.avg_growth or 0)
                    
                    if existing:
                        existing.product_count = row.product_count
                        existing.popularity = popularity
                        existing.weekly_growth = weekly_growth
                        existing.updated_at = datetime.now()
                    else:
                        color_trend = ColorTrend(
                            color_name=row.color,
                            hex_code=row.color_hex,
                            product_count=row.product_count,
                            popularity=popularity,
                            weekly_growth=weekly_growth,
                            state=settings.DEFAULT_STATE
                        )
                        db.add(color_trend)
                        updated_count += 1
                    
                except Exception as e:
                    logger.error(f"Error analyzing color {row.color}: {e}")
                    continue
            
            await db.commit()
            logger.info(f"Updated {updated_count} color trends")
            
    except Exception as e:
        logger.error(f"Error in _analyze_color_trends: {e}")
    
    return updated_count


async def _analyze_material_trends() -> int:
    """Analyze and update material trends"""
    updated_count = 0
    
    try:
        async with AsyncSessionLocal() as db:
            # Get material distribution from products
            query = select(
                Product.material,
                func.count(Product.id).label('product_count'),
                func.avg(Product.trend_score).label('avg_trend'),
                func.avg(Product.weekly_growth).label('avg_growth')
            ).where(
                Product.is_active == True,
                Product.material.isnot(None),
                Product.state == settings.DEFAULT_STATE
            ).group_by(Product.material)
            
            result = await db.execute(query)
            rows = result.all()
            
            for row in rows:
                try:
                    # Check if material trend exists
                    material_query = select(MaterialTrend).where(
                        MaterialTrend.material_name == row.material,
                        MaterialTrend.state == settings.DEFAULT_STATE
                    )
                    material_result = await db.execute(material_query)
                    existing = material_result.scalar_one_or_none()
                    
                    popularity = float(row.avg_trend or 0)
                    weekly_growth = float(row.avg_growth or 0)
                    
                    if existing:
                        existing.product_count = row.product_count
                        existing.popularity = popularity
                        existing.weekly_growth = weekly_growth
                        existing.updated_at = datetime.now()
                    else:
                        material_trend = MaterialTrend(
                            material_name=row.material,
                            product_count=row.product_count,
                            popularity=popularity,
                            weekly_growth=weekly_growth,
                            state=settings.DEFAULT_STATE
                        )
                        db.add(material_trend)
                        updated_count += 1
                    
                except Exception as e:
                    logger.error(f"Error analyzing material {row.material}: {e}")
                    continue
            
            await db.commit()
            logger.info(f"Updated {updated_count} material trends")
            
    except Exception as e:
        logger.error(f"Error in _analyze_material_trends: {e}")
    
    return updated_count


async def _update_trend_statuses() -> int:
    """Update trend statuses (rising, declining, stable)"""
    updated_count = 0
    
    try:
        async with AsyncSessionLocal() as db:
            # Get all trends
            query = select(Trend).where(Trend.state == settings.DEFAULT_STATE)
            result = await db.execute(query)
            trends = result.scalars().all()
            
            for trend in trends:
                try:
                    # Determine status based on growth rate
                    if trend.growth_rate and trend.growth_rate > 10:
                        trend.is_rising = True
                        trend.is_declining = False
                        trend.is_stable = False
                    elif trend.growth_rate and trend.growth_rate < -10:
                        trend.is_rising = False
                        trend.is_declining = True
                        trend.is_stable = False
                    else:
                        trend.is_rising = False
                        trend.is_declining = False
                        trend.is_stable = True
                    
                    trend.updated_at = datetime.now()
                    updated_count += 1
                    
                except Exception as e:
                    logger.error(f"Error updating trend {trend.id}: {e}")
                    continue
            
            await db.commit()
            logger.info(f"Updated status for {updated_count} trends")
            
    except Exception as e:
        logger.error(f"Error in _update_trend_statuses: {e}")
    
    return updated_count
