from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging
import sys
from pathlib import Path

from app.config import get_settings
from app.database.base import init_db
from app.api import trending, dashboard, recommendations, search, analytics, demand, real_data
from app.scheduler.tasks import start_scheduler, stop_scheduler

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
    ]
)

logger = logging.getLogger(__name__)
settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown"""
    # Startup
    logger.info("Starting TrendLoom Backend...")
    
    # Initialize database
    await init_db()
    logger.info("Database initialized")
    
    # Start scheduler
    if settings.SCHEDULER_ENABLED:
        start_scheduler()
        logger.info("Scheduler started")
    
    yield
    
    # Shutdown
    logger.info("Shutting down TrendLoom Backend...")
    
    # Stop scheduler
    if settings.SCHEDULER_ENABLED:
        stop_scheduler()
        logger.info("Scheduler stopped")


# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Live Fashion Trend Analytics Backend",
    lifespan=lifespan
)

# Configure CORS - Allow all origins for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=False,  # Must be False when using allow_origins=["*"]
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(trending.router)
app.include_router(dashboard.router)
app.include_router(recommendations.router)
app.include_router(search.router)
app.include_router(analytics.router)
app.include_router(demand.router)
app.include_router(real_data.router)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
        "environment": settings.ENVIRONMENT,
        "default_state": settings.DEFAULT_STATE,
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT
    }


@app.get("/api/health")
async def api_health_check():
    """Health check endpoint for monitoring"""
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT
    }


@app.get("/api/info")
async def api_info():
    """API information endpoint"""
    return {
        "app_name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "features": [
            "Live Product Tracking",
            "Google Trends Integration",
            "AI Image Analysis",
            "Demand Prediction",
            "Seasonal Trend Detection",
            "Color & Material Analysis",
            "Product Recommendations",
            "Search & Autocomplete",
            "Regional Analytics"
        ],
        "data_sources": [
            "Google Trends",
            "E-commerce Platforms",
            "Social Media Trends",
            "Fashion Blogs"
        ],
        "ai_models": [
            "Image Classification",
            "Color Detection",
            "Attribute Extraction",
            "Demand Forecasting"
        ],
        "supported_regions": [
            settings.DEFAULT_STATE
        ],
        "update_frequency": f"Every {settings.DATA_COLLECTION_INTERVAL_HOURS} hours"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )
