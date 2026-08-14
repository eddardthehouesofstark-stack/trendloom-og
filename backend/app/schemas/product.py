from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, List
from datetime import datetime


class ProductBase(BaseModel):
    name: str
    category: str
    sub_category: Optional[str] = None
    source: str
    source_url: Optional[str] = None
    brand: Optional[str] = None
    price: Optional[float] = None
    image_url: Optional[str] = None
    description: Optional[str] = None
    color: Optional[str] = None
    color_hex: Optional[str] = None
    material: Optional[str] = None
    pattern: Optional[str] = None
    style: Optional[str] = None
    state: Optional[str] = None


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    trend_score: Optional[float] = None
    popularity_score: Optional[float] = None
    weekly_growth: Optional[float] = None
    is_trending: Optional[bool] = None


class ProductResponse(ProductBase):
    id: int
    trend_score: float
    popularity_score: float
    weekly_growth: float
    is_trending: bool
    ai_tags: Optional[List[str]] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class TrendingProductsResponse(BaseModel):
    total: int
    products: List[ProductResponse]
    state: str
    updated_at: Optional[datetime] = None


class ProductSearchRequest(BaseModel):
    query: str
    category: Optional[str] = None
    color: Optional[str] = None
    material: Optional[str] = None
    style: Optional[str] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    state: Optional[str] = None
    limit: int = Field(default=20, le=100)
