from app.models.product import Product
from app.models.trend import Trend, ColorTrend, MaterialTrend
from app.models.analytics import SearchLog, Recommendation, DemandPrediction

__all__ = [
    "Product",
    "Trend",
    "ColorTrend",
    "MaterialTrend",
    "SearchLog",
    "Recommendation",
    "DemandPrediction",
]
