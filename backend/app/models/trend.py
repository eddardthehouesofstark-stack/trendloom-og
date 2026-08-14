from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Boolean, JSON
from sqlalchemy.sql import func
from app.database.base import Base


class Trend(Base):
    __tablename__ = "trends"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Trend identification
    keyword = Column(String(200), nullable=False, index=True)
    category = Column(String(100), index=True)
    trend_type = Column(String(50))  # color, material, style, pattern, category
    
    # Metrics
    search_volume = Column(Integer, default=0)
    interest_score = Column(Float, default=0.0)  # 0-100 from Google Trends
    growth_rate = Column(Float, default=0.0)  # percentage
    momentum_score = Column(Float, default=0.0)
    
    # Time-based data
    week_over_week_change = Column(Float)
    month_over_month_change = Column(Float)
    
    # Location
    state = Column(String(100), index=True)
    country = Column(String(100), default="India")
    
    # Related data
    related_keywords = Column(JSON)  # ["linen shirt", "cotton shirt"]
    related_products_count = Column(Integer, default=0)
    
    # Historical data
    historical_data = Column(JSON)  # {date: score}
    
    # Prediction
    predicted_demand = Column(Float)
    prediction_confidence = Column(Float)
    
    # Season
    season = Column(String(50))  # summer, winter, monsoon, festive
    season_confidence = Column(Float)
    
    # Status
    is_rising = Column(Boolean, default=False)
    is_declining = Column(Boolean, default=False)
    is_stable = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    data_date = Column(DateTime(timezone=True))
    
    def to_dict(self):
        return {
            "id": self.id,
            "keyword": self.keyword,
            "category": self.category,
            "trend_type": self.trend_type,
            "search_volume": self.search_volume,
            "interest_score": self.interest_score,
            "growth_rate": self.growth_rate,
            "momentum_score": self.momentum_score,
            "week_over_week_change": self.week_over_week_change,
            "month_over_month_change": self.month_over_month_change,
            "state": self.state,
            "related_keywords": self.related_keywords,
            "related_products_count": self.related_products_count,
            "predicted_demand": self.predicted_demand,
            "prediction_confidence": self.prediction_confidence,
            "season": self.season,
            "is_rising": self.is_rising,
            "is_declining": self.is_declining,
            "is_stable": self.is_stable,
            "data_date": self.data_date.isoformat() if self.data_date else None,
        }


class ColorTrend(Base):
    __tablename__ = "color_trends"
    
    id = Column(Integer, primary_key=True, index=True)
    color_name = Column(String(100), nullable=False, index=True)
    hex_code = Column(String(7))
    rgb = Column(String(50))
    
    popularity = Column(Float, default=0.0)
    weekly_growth = Column(Float, default=0.0)
    product_count = Column(Integer, default=0)
    
    state = Column(String(100), index=True)
    season = Column(String(50))
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class MaterialTrend(Base):
    __tablename__ = "material_trends"
    
    id = Column(Integer, primary_key=True, index=True)
    material_name = Column(String(100), nullable=False, index=True)
    
    popularity = Column(Float, default=0.0)
    weekly_growth = Column(Float, default=0.0)
    product_count = Column(Integer, default=0)
    
    state = Column(String(100), index=True)
    season = Column(String(50))
    
    properties = Column(JSON)  # breathable, warm, lightweight
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
