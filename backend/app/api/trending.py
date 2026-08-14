from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc, func
from typing import List, Optional
from datetime import datetime, timedelta

from app.database.base import get_db
from app.models import Product, Trend, ColorTrend, MaterialTrend
from app.schemas import ProductResponse, TrendResponse, ColorTrendResponse, MaterialTrendResponse
from app.config import get_settings

router = APIRouter(prefix="/api/trending", tags=["trending"])
settings = get_settings()


@router.get("/products", response_model=List[ProductResponse])
async def get_trending_products(
    state: Optional[str] = Query(None, description="State name (default: Tamil Nadu)"),
    category: Optional[str] = Query(None, description="Product category filter"),
    limit: int = Query(20, le=100),
    db: AsyncSession = Depends(get_db)
):
    """Get trending products"""
    try:
        query = select(Product).where(
            Product.is_trending == True,
            Product.is_active == True
        )
        
        # Apply filters
        if state:
            query = query.where(Product.state == state)
        else:
            query = query.where(Product.state == settings.DEFAULT_STATE)
        
        if category:
            query = query.where(Product.category == category)
        
        # Order by trend score
        query = query.order_by(desc(Product.trend_score)).limit(limit)
        
        result = await db.execute(query)
        products = result.scalars().all()
        
        return [ProductResponse.model_validate(p) for p in products]
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching trending products: {str(e)}")


@router.get("/categories")
async def get_trending_categories(
    state: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db)
):
    """Get trending categories with product counts"""
    try:
        state_filter = state or settings.DEFAULT_STATE
        
        query = select(
            Product.category,
            func.count(Product.id).label('product_count'),
            func.avg(Product.trend_score).label('avg_trend_score'),
            func.avg(Product.weekly_growth).label('avg_growth')
        ).where(
            Product.is_active == True,
            Product.state == state_filter
        ).group_by(
            Product.category
        ).order_by(
            desc('avg_trend_score')
        ).limit(10)
        
        result = await db.execute(query)
        rows = result.all()
        
        categories = []
        for row in rows:
            categories.append({
                'category': row.category,
                'product_count': row.product_count,
                'avg_trend_score': round(float(row.avg_trend_score or 0), 2),
                'avg_growth': round(float(row.avg_growth or 0), 2),
                'is_rising': (row.avg_growth or 0) > 5.0
            })
        
        return {
            'state': state_filter,
            'categories': categories,
            'updated_at': datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching trending categories: {str(e)}")


@router.get("/colors", response_model=List[ColorTrendResponse])
async def get_trending_colors(
    state: Optional[str] = Query(None),
    limit: int = Query(10, le=50),
    db: AsyncSession = Depends(get_db)
):
    """Get trending colors"""
    try:
        state_filter = state or settings.DEFAULT_STATE
        
        query = select(ColorTrend).where(
            ColorTrend.state == state_filter
        ).order_by(
            desc(ColorTrend.popularity)
        ).limit(limit)
        
        result = await db.execute(query)
        colors = result.scalars().all()
        
        return [ColorTrendResponse.model_validate(c) for c in colors]
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching trending colors: {str(e)}")


@router.get("/materials", response_model=List[MaterialTrendResponse])
async def get_trending_materials(
    state: Optional[str] = Query(None),
    limit: int = Query(10, le=50),
    db: AsyncSession = Depends(get_db)
):
    """Get trending materials/fabrics"""
    try:
        state_filter = state or settings.DEFAULT_STATE
        
        query = select(MaterialTrend).where(
            MaterialTrend.state == state_filter
        ).order_by(
            desc(MaterialTrend.popularity)
        ).limit(limit)
        
        result = await db.execute(query)
        materials = result.scalars().all()
        
        return [MaterialTrendResponse.model_validate(m) for m in materials]
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching trending materials: {str(e)}")


@router.get("/styles")
async def get_trending_styles(
    state: Optional[str] = Query(None),
    limit: int = Query(10, le=50),
    db: AsyncSession = Depends(get_db)
):
    """Get trending styles"""
    try:
        state_filter = state or settings.DEFAULT_STATE
        
        query = select(
            Product.style,
            func.count(Product.id).label('product_count'),
            func.avg(Product.trend_score).label('avg_trend_score'),
            func.avg(Product.weekly_growth).label('avg_growth')
        ).where(
            Product.is_active == True,
            Product.state == state_filter,
            Product.style.isnot(None)
        ).group_by(
            Product.style
        ).order_by(
            desc('avg_trend_score')
        ).limit(limit)
        
        result = await db.execute(query)
        rows = result.all()
        
        styles = []
        for row in rows:
            styles.append({
                'style': row.style,
                'product_count': row.product_count,
                'avg_trend_score': round(float(row.avg_trend_score or 0), 2),
                'avg_growth': round(float(row.avg_growth or 0), 2),
                'momentum': 'high' if (row.avg_growth or 0) > 10 else 'medium' if (row.avg_growth or 0) > 5 else 'low'
            })
        
        return {
            'state': state_filter,
            'styles': styles,
            'updated_at': datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching trending styles: {str(e)}")


@router.get("/keywords")
async def get_trending_keywords(
    state: Optional[str] = Query(None),
    limit: int = Query(20, le=100),
    db: AsyncSession = Depends(get_db)
):
    """Get most searched fashion keywords"""
    try:
        state_filter = state or settings.DEFAULT_STATE
        
        query = select(Trend).where(
            Trend.state == state_filter,
            Trend.interest_score > 0
        ).order_by(
            desc(Trend.interest_score)
        ).limit(limit)
        
        result = await db.execute(query)
        trends = result.scalars().all()
        
        keywords = []
        for trend in trends:
            keywords.append({
                'keyword': trend.keyword,
                'category': trend.category,
                'interest_score': trend.interest_score,
                'growth_rate': trend.growth_rate,
                'search_volume': trend.search_volume,
                'is_rising': trend.is_rising,
                'related_keywords': trend.related_keywords or []
            })
        
        return {
            'state': state_filter,
            'keywords': keywords,
            'total': len(keywords),
            'updated_at': datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching trending keywords: {str(e)}")
