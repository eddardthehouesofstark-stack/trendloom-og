from app.schemas.product import (
    ProductBase,
    ProductCreate,
    ProductUpdate,
    ProductResponse,
    TrendingProductsResponse,
    ProductSearchRequest,
)
from app.schemas.trend import (
    TrendBase,
    TrendResponse,
    ColorTrendResponse,
    MaterialTrendResponse,
    DemandPredictionResponse,
    SeasonalTrendResponse,
)
from app.schemas.analytics import (
    RecommendationResponse,
    ImageAnalysisRequest,
    ImageAnalysisResponse,
    DashboardResponse,
)

__all__ = [
    "ProductBase",
    "ProductCreate",
    "ProductUpdate",
    "ProductResponse",
    "TrendingProductsResponse",
    "ProductSearchRequest",
    "TrendBase",
    "TrendResponse",
    "ColorTrendResponse",
    "MaterialTrendResponse",
    "DemandPredictionResponse",
    "SeasonalTrendResponse",
    "RecommendationResponse",
    "ImageAnalysisRequest",
    "ImageAnalysisResponse",
    "DashboardResponse",
]
