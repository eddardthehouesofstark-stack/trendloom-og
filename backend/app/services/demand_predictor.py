import logging
from datetime import datetime, timedelta
from sqlalchemy import select, func
from typing import Dict, List
import numpy as np

from app.database.base import AsyncSessionLocal
from app.models import Product, Trend, DemandPrediction
from app.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


async def generate_predictions() -> Dict:
    """Generate demand predictions for categories"""
    try:
        logger.info("Starting demand prediction generation...")
        
        # Get categories to predict
        categories = await _get_active_categories()
        
        predictions_created = 0
        
        for category in categories:
            try:
                # Generate predictions for different time horizons
                for days in [7, 14, 30, 90]:
                    prediction = await _predict_category_demand(category, days)
                    if prediction:
                        await _save_prediction(prediction)
                        predictions_created += 1
                
            except Exception as e:
                logger.error(f"Error predicting for category {category}: {e}")
                continue
        
        return {
            'predictions_created': predictions_created,
            'categories_predicted': len(categories),
            'status': 'success'
        }
        
    except Exception as e:
        logger.error(f"Error in generate_predictions: {e}", exc_info=True)
        return {
            'predictions_created': 0,
            'categories_predicted': 0,
            'status': 'error',
            'error': str(e)
        }


async def _get_active_categories() -> List[str]:
    """Get active product categories"""
    try:
        async with AsyncSessionLocal() as db:
            query = select(Product.category).where(
                Product.is_active == True,
                Product.state == settings.DEFAULT_STATE
            ).distinct()
            
            result = await db.execute(query)
            categories = [row[0] for row in result.all()]
            
            return categories
            
    except Exception as e:
        logger.error(f"Error getting categories: {e}")
        return []


async def _predict_category_demand(category: str, days: int) -> Dict:
    """Predict demand for a category"""
    try:
        async with AsyncSessionLocal() as db:
            # Get current metrics for category
            query = select(
                func.count(Product.id).label('product_count'),
                func.avg(Product.trend_score).label('avg_trend'),
                func.avg(Product.weekly_growth).label('avg_growth'),
                func.avg(Product.popularity_score).label('avg_popularity')
            ).where(
                Product.category == category,
                Product.is_active == True,
                Product.state == settings.DEFAULT_STATE
            )
            
            result = await db.execute(query)
            row = result.one()
            
            if not row.product_count:
                return None
            
            # Get trend data for category
            trend_query = select(Trend).where(
                Trend.category == category,
                Trend.state == settings.DEFAULT_STATE
            ).order_by(Trend.interest_score.desc()).limit(1)
            
            trend_result = await db.execute(trend_query)
            trend = trend_result.scalar_one_or_none()
            
            # Calculate prediction
            base_score = float(row.avg_trend or 50)
            growth_rate = float(row.avg_growth or 0)
            
            # Simple linear prediction (in production, use Prophet or ML models)
            predicted_score = base_score + (growth_rate * (days / 7))
            predicted_score = max(0, min(100, predicted_score))
            
            # Calculate growth percentage
            growth_percentage = ((predicted_score - base_score) / base_score * 100) if base_score > 0 else 0
            
            # Calculate confidence based on data quality
            confidence = 0.70  # Base confidence
            if row.product_count > 50:
                confidence += 0.10
            if trend:
                confidence += 0.10
            if abs(growth_rate) < 20:
                confidence += 0.10
            
            confidence = min(confidence, 0.95)
            
            # Generate prediction graph data
            graph_data = _generate_prediction_graph(base_score, predicted_score, days)
            
            # Seasonal and trend factors
            seasonal_factor = _calculate_seasonal_factor(category)
            trend_factor = 1.0 + (growth_rate / 100) if growth_rate else 1.0
            
            return {
                'category': category,
                'state': settings.DEFAULT_STATE,
                'predicted_demand_score': round(predicted_score, 2),
                'growth_percentage': round(growth_percentage, 2),
                'confidence': round(confidence, 2),
                'prediction_for_date': datetime.now() + timedelta(days=days),
                'time_horizon_days': days,
                'seasonal_factor': seasonal_factor,
                'trend_factor': trend_factor,
                'prediction_graph_data': graph_data,
                'model_used': 'linear_trend',
                'model_version': '1.0'
            }
            
    except Exception as e:
        logger.error(f"Error predicting demand for {category}: {e}")
        return None


def _generate_prediction_graph(start_score: float, end_score: float, days: int) -> List[Dict]:
    """Generate graph data points for prediction"""
    graph_data = []
    
    try:
        # Generate daily points
        step = (end_score - start_score) / days
        
        for i in range(days + 1):
            date = datetime.now() + timedelta(days=i)
            value = start_score + (step * i)
            
            # Add uncertainty bounds
            uncertainty = abs(step) * 0.3 * i  # Uncertainty increases over time
            
            graph_data.append({
                'date': date.isoformat(),
                'value': round(value, 2),
                'lower_bound': round(max(0, value - uncertainty), 2),
                'upper_bound': round(min(100, value + uncertainty), 2)
            })
        
    except Exception as e:
        logger.error(f"Error generating prediction graph: {e}")
    
    return graph_data


def _calculate_seasonal_factor(category: str) -> float:
    """Calculate seasonal factor for category"""
    current_month = datetime.now().month
    
    # Define seasonal categories
    summer_categories = ['t-shirt', 'shorts', 'dress', 'linen']
    winter_categories = ['jacket', 'sweater', 'coat', 'hoodie']
    festive_categories = ['saree', 'lehenga', 'kurta', 'ethnic']
    
    category_lower = category.lower()
    
    # Summer months (March-June)
    if current_month in [3, 4, 5, 6]:
        if any(cat in category_lower for cat in summer_categories):
            return 1.3
        elif any(cat in category_lower for cat in winter_categories):
            return 0.7
    
    # Monsoon months (July-September)
    elif current_month in [7, 8, 9]:
        return 1.0
    
    # Festive season (October-November)
    elif current_month in [10, 11]:
        if any(cat in category_lower for cat in festive_categories):
            return 1.5
    
    # Winter months (December-February)
    elif current_month in [12, 1, 2]:
        if any(cat in category_lower for cat in winter_categories):
            return 1.4
        elif any(cat in category_lower for cat in summer_categories):
            return 0.6
    
    return 1.0


async def _save_prediction(prediction: Dict):
    """Save prediction to database"""
    try:
        async with AsyncSessionLocal() as db:
            # Check if prediction exists for this category and time horizon
            query = select(DemandPrediction).where(
                DemandPrediction.category == prediction['category'],
                DemandPrediction.state == prediction['state'],
                DemandPrediction.time_horizon_days == prediction['time_horizon_days']
            )
            
            result = await db.execute(query)
            existing = result.scalar_one_or_none()
            
            if existing:
                # Update existing prediction
                for key, value in prediction.items():
                    if key not in ['category', 'state', 'time_horizon_days']:
                        setattr(existing, key, value)
                existing.updated_at = datetime.now()
            else:
                # Create new prediction
                demand_prediction = DemandPrediction(**prediction)
                db.add(demand_prediction)
            
            await db.commit()
            
    except Exception as e:
        logger.error(f"Error saving prediction: {e}")
