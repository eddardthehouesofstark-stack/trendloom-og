from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class TrendBase(BaseModel):
    keyword: str
    category: str
    trend_type: str
    interest_score: float
    growth_rate: float
    state: Optional[str] = None


class TrendResponse(BaseModel):
    id: int
    keyword: str
    category: str
    trend_type: str
    search_volume: int
    interest_score: float
    growth_rate: float
    momentum_score: float
    week_over_week_change: Optional[float] = None
    month_over_month_change: Optional[float] = None
    state: str
    related_keywords: Optional[List[str]] = None
    related_products_count: int
    predicted_demand: Optional[float] = None
    prediction_confidence: Optional[float] = None
    season: Optional[str] = None
    is_rising: bool
    is_declining: bool
    is_stable: bool
    data_date: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class ColorTrendResponse(BaseModel):
    id: int
    color_name: str
    hex_code: Optional[str] = None
    popularity: float
    weekly_growth: float
    product_count: int
    state: str
    season: Optional[str] = None
    
    class Config:
        from_attributes = True


class MaterialTrendResponse(BaseModel):
    id: int
    material_name: str
    popularity: float
    weekly_growth: float
    product_count: int
    state: str
    season: Optional[str] = None
    properties: Optional[List[str]] = None
    
    class Config:
        from_attributes = True


class DemandPredictionResponse(BaseModel):
    category: str
    keyword: Optional[str] = None
    state: str
    predicted_demand_score: float
    growth_percentage: float
    confidence: float
    prediction_for_date: Optional[datetime] = None
    time_horizon_days: int
    seasonal_factor: Optional[float] = None
    trend_factor: Optional[float] = None
    prediction_graph_data: Optional[List[Dict]] = None
    
    class Config:
        from_attributes = True


class SeasonalTrendResponse(BaseModel):
    season: str
    confidence: float
    top_colors: List[Dict[str, Any]]
    top_materials: List[Dict[str, Any]]
    top_categories: List[Dict[str, Any]]
    state: str
    
    class Config:
        from_attributes = True
