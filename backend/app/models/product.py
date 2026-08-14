from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Boolean, JSON
from sqlalchemy.sql import func
from app.database.base import Base


class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(500), nullable=False)
    category = Column(String(100), index=True)
    sub_category = Column(String(100))
    
    # Source info
    source = Column(String(100), index=True)  # myntra, ajio, flipkart, etc.
    source_url = Column(Text)
    source_id = Column(String(200))
    
    # Product details
    brand = Column(String(200))
    price = Column(Float)
    currency = Column(String(10), default="INR")
    image_url = Column(Text)
    description = Column(Text)
    
    # Attributes
    color = Column(String(100))
    color_hex = Column(String(7))
    material = Column(String(100))
    pattern = Column(String(100))
    style = Column(String(100))
    
    # Location
    state = Column(String(100), index=True)
    country = Column(String(100), default="India")
    
    # Trend metrics
    trend_score = Column(Float, default=0.0, index=True)
    popularity_score = Column(Float, default=0.0)
    weekly_growth = Column(Float, default=0.0)
    view_count = Column(Integer, default=0)
    search_count = Column(Integer, default=0)
    
    # AI extracted features
    ai_tags = Column(JSON)  # ["casual", "summer", "lightweight"]
    ai_confidence = Column(Float)
    
    # Status
    is_trending = Column(Boolean, default=False, index=True)
    is_active = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_scraped_at = Column(DateTime(timezone=True))
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "sub_category": self.sub_category,
            "source": self.source,
            "source_url": self.source_url,
            "brand": self.brand,
            "price": self.price,
            "currency": self.currency,
            "image_url": self.image_url,
            "description": self.description,
            "color": self.color,
            "color_hex": self.color_hex,
            "material": self.material,
            "pattern": self.pattern,
            "style": self.style,
            "state": self.state,
            "trend_score": self.trend_score,
            "popularity_score": self.popularity_score,
            "weekly_growth": self.weekly_growth,
            "is_trending": self.is_trending,
            "ai_tags": self.ai_tags,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
