from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime


class RecommendationResponse(BaseModel):
    product_id: int
    product_name: Optional[str] = None
    recommendation_type: str
    confidence_score: float
    category: str
    color: Optional[str] = None
    material: Optional[str] = None
    style: Optional[str] = None
    image_url: Optional[str] = None
    price: Optional[float] = None
    trend_score: Optional[float] = None
    
    class Config:
        from_attributes = True


class ImageAnalysisRequest(BaseModel):
    image_url: Optional[str] = None
    image_base64: Optional[str] = None


class ImageAnalysisResponse(BaseModel):
    category: str
    confidence: float
    colors: List[Dict[str, Any]]
    detected_attributes: Dict[str, Any]
    style: Optional[str] = None
    pattern: Optional[str] = None
    material: Optional[str] = None
    similar_products: List[Dict[str, Any]]
    recommendations: List[RecommendationResponse]
    ai_tags: List[str]


class DashboardResponse(BaseModel):
    # KPIs
    market_coverage: float
    trend_accuracy: float
    signal_strength: str
    active_signals: int
    
    # Trending data
    trending_products: List[Dict[str, Any]]
    trending_categories: List[Dict[str, Any]]
    trending_colors: List[Dict[str, Any]]
    trending_materials: List[Dict[str, Any]]
    
    # Action board
    action_items: List[Dict[str, Any]]
    
    # Regional preview
    regional_data: Dict[str, Any]
    
    # Metadata
    state: str
    last_updated: datetime
    data_freshness: str


class WeeklyAnalyticsResponse(BaseModel):
    week_start: datetime
    week_end: datetime
    total_products_tracked: int
    new_trends_identified: int
    top_growing_categories: List[Dict[str, Any]]
    top_growing_colors: List[Dict[str, Any]]
    top_searches: List[Dict[str, Any]]
    demand_changes: List[Dict[str, Any]]
    state: str


class MonthlyAnalyticsResponse(BaseModel):
    month: str
    year: int
    total_products_tracked: int
    trends_emerged: int
    trends_declined: int
    seasonal_insights: Dict[str, Any]
    top_performers: List[Dict[str, Any]]
    market_summary: Dict[str, Any]
    state: str
