from sqlalchemy import Column, Integer, String, Float, DateTime, Text, JSON
from sqlalchemy.sql import func
from app.database.base import Base


class SearchLog(Base):
    __tablename__ = "search_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    query = Column(String(500), nullable=False, index=True)
    category = Column(String(100))
    
    # Filters used
    filters = Column(JSON)
    
    # Results
    results_count = Column(Integer, default=0)
    
    # User context
    state = Column(String(100))
    ip_address = Column(String(50))
    user_agent = Column(Text)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Recommendation(Base):
    __tablename__ = "recommendations"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Recommendation details
    product_id = Column(Integer, index=True)
    recommendation_type = Column(String(100))  # trending, seasonal, similar, ai_based
    
    # Context
    based_on = Column(String(200))  # what triggered this recommendation
    confidence_score = Column(Float, default=0.0)
    
    # Attributes
    category = Column(String(100))
    color = Column(String(100))
    material = Column(String(100))
    style = Column(String(100))
    season = Column(String(50))
    
    # Location
    state = Column(String(100), index=True)
    
    # Metrics
    relevance_score = Column(Float, default=0.0)
    trend_alignment = Column(Float, default=0.0)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True))


class DemandPrediction(Base):
    __tablename__ = "demand_predictions"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # What we're predicting
    category = Column(String(100), nullable=False, index=True)
    keyword = Column(String(200))
    
    # Location
    state = Column(String(100), index=True)
    
    # Prediction
    predicted_demand_score = Column(Float)  # 0-100
    growth_percentage = Column(Float)
    confidence = Column(Float)
    
    # Time horizon
    prediction_for_date = Column(DateTime(timezone=True))
    time_horizon_days = Column(Integer)  # 7, 14, 30, 90
    
    # Model info
    model_used = Column(String(100))
    model_version = Column(String(50))
    
    # Historical context
    historical_data = Column(JSON)
    features_used = Column(JSON)
    
    # Factors
    seasonal_factor = Column(Float)
    trend_factor = Column(Float)
    market_factor = Column(Float)
    
    # Graph data
    prediction_graph_data = Column(JSON)  # [{date, value, lower_bound, upper_bound}]
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def to_dict(self):
        return {
            "id": self.id,
            "category": self.category,
            "keyword": self.keyword,
            "state": self.state,
            "predicted_demand_score": self.predicted_demand_score,
            "growth_percentage": self.growth_percentage,
            "confidence": self.confidence,
            "prediction_for_date": self.prediction_for_date.isoformat() if self.prediction_for_date else None,
            "time_horizon_days": self.time_horizon_days,
            "seasonal_factor": self.seasonal_factor,
            "trend_factor": self.trend_factor,
            "prediction_graph_data": self.prediction_graph_data,
        }
