from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc
from typing import Optional
from datetime import datetime, timedelta

from app.database.base import get_db
from app.models import Product, Trend, SearchLog
from app.config import get_settings

router = APIRouter(prefix="/api/analytics", tags=["analytics"])
settings = get_settings()


@router.get("/weekly")
async def get_weekly_analytics(
    state: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db)
):
    """Get weekly analytics"""
    try:
        state_filter = state or settings.DEFAULT_STATE
        
        # Calculate date range
        end_date = datetime.now()
        start_date = end_date - timedelta(days=7)
        
        # Total products tracked
        total_query = select(func.count(Product.id)).where(
            Product.is_active == True,
            Product.state == state_filter
        )
        total_result = await db.execute(total_query)
        total_products = total_result.scalar() or 0
        
        # New trends identified
        new_trends_query = select(func.count(Trend.id)).where(
            Trend.state == state_filter,
            Trend.created_at >= start_date
        )
        new_trends_result = await db.execute(new_trends_query)
        new_trends = new_trends_result.scalar() or 0
        
        # Top growing categories
        growing_categories_query = select(
            Product.category,
            func.avg(Product.weekly_growth).label('avg_growth'),
            func.count(Product.id).label('count')
        ).where(
            Product.is_active == True,
            Product.state == state_filter,
            Product.weekly_growth > 0
        ).group_by(Product.category).order_by(desc('avg_growth')).limit(5)
        
        growing_result = await db.execute(growing_categories_query)
        growing_categories = [
            {
                'category': row.category,
                'growth': round(float(row.avg_growth), 2),
                'product_count': row.count
            }
            for row in growing_result.all()
        ]
        
        # Top searches
        search_query = select(
            SearchLog.query,
            func.count(SearchLog.id).label('count')
        ).where(
            SearchLog.state == state_filter,
            SearchLog.created_at >= start_date
        ).group_by(SearchLog.query).order_by(desc('count')).limit(10)
        
        search_result = await db.execute(search_query)
        top_searches = [
            {'query': row.query, 'count': row.count}
            for row in search_result.all()
        ]
        
        return {
            'week_start': start_date.isoformat(),
            'week_end': end_date.isoformat(),
            'total_products_tracked': total_products,
            'new_trends_identified': new_trends,
            'top_growing_categories': growing_categories,
            'top_growing_colors': [],  # Would calculate from color trends
            'top_searches': top_searches,
            'demand_changes': [],
            'state': state_filter
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching weekly analytics: {str(e)}")


@router.get("/monthly")
async def get_monthly_analytics(
    state: Optional[str] = Query(None),
    month: Optional[int] = Query(None, ge=1, le=12),
    year: Optional[int] = Query(None),
    db: AsyncSession = Depends(get_db)
):
    """Get monthly analytics"""
    try:
        state_filter = state or settings.DEFAULT_STATE
        
        # Default to current month
        if not month:
            month = datetime.now().month
        if not year:
            year = datetime.now().year
        
        # Calculate date range
        start_date = datetime(year, month, 1)
        if month == 12:
            end_date = datetime(year + 1, 1, 1)
        else:
            end_date = datetime(year, month + 1, 1)
        
        # Total products
        total_query = select(func.count(Product.id)).where(
            Product.is_active == True,
            Product.state == state_filter
        )
        total_result = await db.execute(total_query)
        total_products = total_result.scalar() or 0
        
        # Trends emerged
        emerged_query = select(func.count(Trend.id)).where(
            Trend.state == state_filter,
            Trend.created_at >= start_date,
            Trend.created_at < end_date,
            Trend.is_rising == True
        )
        emerged_result = await db.execute(emerged_query)
        trends_emerged = emerged_result.scalar() or 0
        
        # Trends declined
        declined_query = select(func.count(Trend.id)).where(
            Trend.state == state_filter,
            Trend.created_at >= start_date,
            Trend.created_at < end_date,
            Trend.is_declining == True
        )
        declined_result = await db.execute(declined_query)
        trends_declined = declined_result.scalar() or 0
        
        # Top performers
        top_performers_query = select(Product).where(
            Product.is_active == True,
            Product.state == state_filter,
            Product.is_trending == True
        ).order_by(desc(Product.trend_score)).limit(10)
        
        top_result = await db.execute(top_performers_query)
        top_performers = [
            {
                'id': p.id,
                'name': p.name,
                'category': p.category,
                'trend_score': round(p.trend_score, 2),
                'weekly_growth': round(p.weekly_growth, 2)
            }
            for p in top_result.scalars().all()
        ]
        
        month_name = datetime(year, month, 1).strftime('%B')
        
        return {
            'month': month_name,
            'year': year,
            'total_products_tracked': total_products,
            'trends_emerged': trends_emerged,
            'trends_declined': trends_declined,
            'seasonal_insights': {
                'season': _get_season_from_month(month),
                'dominant_colors': [],
                'popular_materials': []
            },
            'top_performers': top_performers,
            'market_summary': {
                'overall_growth': 12.5,  # Would calculate from data
                'market_momentum': 'positive',
                'volatility': 'low'
            },
            'state': state_filter
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching monthly analytics: {str(e)}")


def _get_season_from_month(month: int) -> str:
    """Get season from month"""
    if month in [12, 1, 2]:
        return 'winter'
    elif month in [3, 4, 5]:
        return 'spring'
    elif month in [6, 7, 8]:
        return 'monsoon'
    elif month in [9, 10, 11]:
        return 'festive'
    return 'general'
