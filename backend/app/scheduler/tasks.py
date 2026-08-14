from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
import logging
from datetime import datetime

from app.services.data_collector import collect_all_fashion_data
from app.services.trend_analyzer import analyze_trends
from app.services.demand_predictor import generate_predictions
from app.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

scheduler = AsyncIOScheduler()


async def collect_fashion_data_job():
    """Background job to collect fashion data"""
    try:
        logger.info("Starting fashion data collection job...")
        start_time = datetime.now()
        
        # Collect data from all sources
        results = await collect_all_fashion_data()
        
        elapsed = (datetime.now() - start_time).total_seconds()
        logger.info(f"Fashion data collection completed in {elapsed:.2f} seconds. Collected {results.get('total_products', 0)} products.")
        
    except Exception as e:
        logger.error(f"Error in fashion data collection job: {e}", exc_info=True)


async def analyze_trends_job():
    """Background job to analyze trends"""
    try:
        logger.info("Starting trend analysis job...")
        start_time = datetime.now()
        
        # Analyze trends
        results = await analyze_trends()
        
        elapsed = (datetime.now() - start_time).total_seconds()
        logger.info(f"Trend analysis completed in {elapsed:.2f} seconds. Analyzed {results.get('trends_updated', 0)} trends.")
        
    except Exception as e:
        logger.error(f"Error in trend analysis job: {e}", exc_info=True)


async def generate_predictions_job():
    """Background job to generate demand predictions"""
    try:
        logger.info("Starting demand prediction job...")
        start_time = datetime.now()
        
        # Generate predictions
        results = await generate_predictions()
        
        elapsed = (datetime.now() - start_time).total_seconds()
        logger.info(f"Demand prediction completed in {elapsed:.2f} seconds. Generated {results.get('predictions_created', 0)} predictions.")
        
    except Exception as e:
        logger.error(f"Error in demand prediction job: {e}", exc_info=True)


def start_scheduler():
    """Start the background scheduler"""
    try:
        # Schedule data collection job
        scheduler.add_job(
            collect_fashion_data_job,
            trigger=CronTrigger(hour=f'*/{settings.DATA_COLLECTION_INTERVAL_HOURS}'),
            id='collect_fashion_data',
            name='Collect fashion data from all sources',
            replace_existing=True
        )
        
        # Schedule trend analysis job (runs hourly)
        scheduler.add_job(
            analyze_trends_job,
            trigger=CronTrigger(hour='*'),
            id='analyze_trends',
            name='Analyze fashion trends',
            replace_existing=True
        )
        
        # Schedule prediction job (runs every 3 hours)
        scheduler.add_job(
            generate_predictions_job,
            trigger=CronTrigger(hour='*/3'),
            id='generate_predictions',
            name='Generate demand predictions',
            replace_existing=True
        )
        
        # Start scheduler
        scheduler.start()
        logger.info("Scheduler started successfully")
        
        # Run initial data collection
        scheduler.add_job(
            collect_fashion_data_job,
            id='initial_collection',
            name='Initial data collection',
        )
        
    except Exception as e:
        logger.error(f"Error starting scheduler: {e}", exc_info=True)


def stop_scheduler():
    """Stop the background scheduler"""
    try:
        scheduler.shutdown()
        logger.info("Scheduler stopped")
    except Exception as e:
        logger.error(f"Error stopping scheduler: {e}")
