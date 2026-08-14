from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from typing import Optional, List
from datetime import datetime, timedelta

from app.database.base import get_db
from app.models import DemandPrediction, Trend
from app.schemas.trend import DemandPredictionResponse
from app.config import get_settings

router = APIRouter(prefix="/api/demand", tags=["demand"])
settings = get_settings()


@router.get("", response_model=List[DemandPredictionResponse])
async def get_demand_predictions(
    state: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    time_horizon: int = Query(30, description="Prediction horizon in days"),
    limit: int = Query(20, le=100),
    db: AsyncSession = Depends(get_db)
):
    """Get demand predictions"""
    try:
        state_filter = state or settings.DEFAULT_STATE
        
        query = select(DemandPrediction).where(
            DemandPrediction.state == state_filter,
            DemandPrediction.time_horizon_days == time_horizon
        )
        
        if category:
            query = query.where(DemandPrediction.category == category)
        
        query = query.order_by(desc(DemandPrediction.predicted_demand_score)).limit(limit)
        
        result = await db.execute(query)
        predictions = result.scalars().all()
        
        return [DemandPredictionResponse.model_validate(p) for p in predictions]
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching demand predictions: {str(e)}")


@router.get("/forecast/{category}")
async def get_category_forecast(
    category: str,
    state: Optional[str] = Query(None),
    days: int = Query(30, le=90),
    db: AsyncSession = Depends(get_db)
):
    """Get detailed forecast for a specific category"""
    try:
        state_filter = state or settings.DEFAULT_STATE
        
        query = select(DemandPrediction).where(
            DemandPrediction.category == category,
            DemandPrediction.state == state_filter,
            DemandPrediction.time_horizon_days == days
        ).order_by(desc(DemandPrediction.created_at)).limit(1)
        
        result = await db.execute(query)
        prediction = result.scalar_one_or_none()
        
        if not prediction:
            # Generate basic forecast if not available
            return _generate_basic_forecast(category, state_filter, days)
        
        return {
            'category': prediction.category,
            'state': prediction.state,
            'predicted_demand_score': prediction.predicted_demand_score,
            'growth_percentage': prediction.growth_percentage,
            'confidence': prediction.confidence,
            'prediction_for_date': prediction.prediction_for_date,
            'time_horizon_days': prediction.time_horizon_days,
            'seasonal_factor': prediction.seasonal_factor,
            'trend_factor': prediction.trend_factor,
            'prediction_graph_data': prediction.prediction_graph_data or [],
            'model_used': prediction.model_used,
            'created_at': prediction.created_at
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching forecast: {str(e)}")


@router.get("/seasonal")
async def get_seasonal_predictions(
    state: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db)
):
    """Get seasonal trend predictions"""
    try:
        state_filter = state or settings.DEFAULT_STATE
        
        # Get current season
        current_month = datetime.now().month
        season = _get_season_from_month(current_month)
        
        # Get trends for current season
        query = select(Trend).where(
            Trend.state == state_filter,
            Trend.season == season
        ).order_by(desc(Trend.interest_score)).limit(20)
        
        result = await db.execute(query)
        trends = result.scalars().all()
        
        # Aggregate by type
        colors = [t for t in trends if t.trend_type == 'color']
        materials = [t for t in trends if t.trend_type == 'material']
        categories = [t for t in trends if t.trend_type == 'category']
        
        return {
            'season': season,
            'confidence': 0.85,
            'state': state_filter,
            'top_colors': [
                {
                    'name': t.keyword,
                    'score': t.interest_score,
                    'growth': t.growth_rate
                }
                for t in colors[:5]
            ],
            'top_materials': [
                {
                    'name': t.keyword,
                    'score': t.interest_score,
                    'growth': t.growth_rate
                }
                for t in materials[:5]
            ],
            'top_categories': [
                {
                    'name': t.keyword,
                    'score': t.interest_score,
                    'growth': t.growth_rate
                }
                for t in categories[:5]
            ],
            'recommendations': _get_seasonal_recommendations(season)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching seasonal predictions: {str(e)}")


def _get_season_from_month(month: int) -> str:
    """Determine season from month"""
    if month in [12, 1, 2]:
        return 'winter'
    elif month in [3, 4, 5]:
        return 'spring'
    elif month in [6, 7, 8]:
        return 'monsoon'
    elif month in [9, 10, 11]:
        return 'festive'
    return 'general'


def _generate_basic_forecast(category: str, state: str, days: int) -> dict:
    """Generate a basic forecast when no prediction exists"""
    # This would use historical data and simple models
    # For now, return a placeholder
    
    base_score = 65.0
    growth = 5.5
    
    graph_data = []
    current_date = datetime.now()
    
    for i in range(days):
        date = current_date + timedelta(days=i)
        # Simple linear growth
        value = base_score + (growth * i / days)
        
        graph_data.append({
            'date': date.isoformat(),
            'value': round(value, 2),
            'lower_bound': round(value - 10, 2),
            'upper_bound': round(value + 10, 2)
        })
    
    return {
        'category': category,
        'state': state,
        'predicted_demand_score': base_score + growth,
        'growth_percentage': growth,
        'confidence': 0.70,
        'prediction_for_date': (datetime.now() + timedelta(days=days)).isoformat(),
        'time_horizon_days': days,
        'seasonal_factor': 1.0,
        'trend_factor': 1.05,
        'prediction_graph_data': graph_data,
        'model_used': 'basic_forecast',
        'created_at': datetime.now().isoformat()
    }


def _get_seasonal_recommendations(season: str) -> List[dict]:
    """Get recommendations for a season"""
    recommendations = {
        'winter': [
            'Focus on warm fabrics like wool and fleece',
            'Dark colors and earth tones perform well',
            'Layering pieces are in high demand'
        ],
        'summer': [
            'Light, breathable fabrics like cotton and linen',
            'Bright and pastel colors are popular',
            'Loose, comfortable fits are preferred'
        ],
        'monsoon': [
            'Quick-dry and water-resistant materials',
            'Darker colors that hide stains',
            'Practical, functional designs'
        ],
        'festive': [
            'Ethnic and traditional styles spike',
            'Rich colors and embellishments',
            'Premium materials like silk'
        ]
    }
    
    return recommendations.get(season, ['General fashion trends apply'])
