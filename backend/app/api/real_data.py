"""
Real Fashion Data API Endpoints
"""
from fastapi import APIRouter, HTTPException
from typing import List, Dict
import logging

from app.services.fashion_data_api import fashion_data_collector

router = APIRouter(prefix="/api/real-data", tags=["real-data"])
logger = logging.getLogger(__name__)


@router.get("/color-trends")
async def get_color_trends() -> List[Dict]:
    """Get real 2024 color trends from Pantone and fashion authorities"""
    try:
        trends = await fashion_data_collector.get_color_trends_2024()
        return trends
    except Exception as e:
        logger.error(f"Error fetching color trends: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/material-trends")
async def get_material_trends() -> List[Dict]:
    """Get real 2024 material trends from industry reports"""
    try:
        trends = await fashion_data_collector.get_material_trends_2024()
        return trends
    except Exception as e:
        logger.error(f"Error fetching material trends: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/style-trends")
async def get_style_trends() -> List[Dict]:
    """Get real 2024 style trends from fashion authorities"""
    try:
        trends = await fashion_data_collector.get_style_trends_2024()
        return trends
    except Exception as e:
        logger.error(f"Error fetching style trends: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/trending-items")
async def get_trending_items(source: str = "etsy", limit: int = 20) -> List[Dict]:
    """
    Get trending fashion items from various sources
    
    Sources:
    - etsy: Etsy trending items (FREE)
    - reddit: Reddit fashion discussions (FREE)
    """
    try:
        if source == "etsy":
            items = await fashion_data_collector.get_etsy_trending(limit=limit)
        elif source == "reddit":
            items = await fashion_data_collector.get_fashion_trends_from_reddit()
        else:
            raise HTTPException(status_code=400, detail="Invalid source. Use 'etsy' or 'reddit'")
        
        return items
    except Exception as e:
        logger.error(f"Error fetching trending items: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/datasets")
async def get_fashion_datasets() -> Dict:
    """Get available fashion datasets information"""
    try:
        datasets = await fashion_data_collector.get_github_fashion_datasets()
        return datasets
    except Exception as e:
        logger.error(f"Error fetching datasets: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/summary")
async def get_real_data_summary() -> Dict:
    """Get summary of all available real fashion data"""
    try:
        color_trends = await fashion_data_collector.get_color_trends_2024()
        material_trends = await fashion_data_collector.get_material_trends_2024()
        style_trends = await fashion_data_collector.get_style_trends_2024()
        
        return {
            'color_trends': {
                'count': len(color_trends),
                'top_3': color_trends[:3]
            },
            'material_trends': {
                'count': len(material_trends),
                'top_3': material_trends[:3]
            },
            'style_trends': {
                'count': len(style_trends),
                'top_3': style_trends[:3]
            },
            'data_sources': [
                'Pantone Color of the Year 2024',
                'Fashion Week Trend Reports',
                'Textile Exchange Report 2024',
                'McKinsey Fashion Report',
                'Street Style Analysis',
                'Reddit Fashion Communities',
                'Etsy Marketplace Data'
            ]
        }
    except Exception as e:
        logger.error(f"Error fetching summary: {e}")
        raise HTTPException(status_code=500, detail=str(e))
