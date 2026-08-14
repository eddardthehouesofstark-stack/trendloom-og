# TrendLoom Backend

A production-ready Python backend for TrendLoom fashion trend analytics platform. Provides real-time fashion trend data using free and open-source technologies.

## Features

- **Live Product Tracking**: Collect fashion products from multiple e-commerce sources
- **Google Trends Integration**: Real-time search trend analysis
- **AI Image Analysis**: Analyze clothing images and detect attributes
- **Demand Prediction**: Forecast future demand using ML models
- **Seasonal Trend Detection**: Identify seasonal fashion patterns
- **Color & Material Analysis**: Track trending colors and fabrics
- **Product Recommendations**: AI-powered product suggestions
- **Search & Autocomplete**: Fast fuzzy search with suggestions
- **Regional Analytics**: State-specific fashion insights
- **Automated Data Collection**: Background scheduler for data updates

## Technology Stack

- **Framework**: FastAPI
- **Database**: SQLite (PostgreSQL ready)
- **AI/ML**: PyTorch, Transformers, Scikit-learn
- **Data Collection**: PyTrends, BeautifulSoup, Requests
- **Scheduling**: APScheduler
- **Caching**: Redis (optional)

## Installation

### Prerequisites

- Python 3.11 or higher
- pip or poetry

### Setup

1. **Clone the repository**
```bash
cd backend
```

2. **Create virtual environment**
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment**
```bash
copy .env.example .env
# Edit .env with your settings
```

5. **Initialize database**
```bash
# Database tables will be created automatically on first run
```

6. **Run the server**
```bash
# Development
python -m app.main

# OR with uvicorn
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### Dashboard
- `GET /api/dashboard` - Complete dashboard data
- `GET /api/info` - API information

### Trending
- `GET /api/trending/products` - Trending products
- `GET /api/trending/categories` - Trending categories
- `GET /api/trending/colors` - Trending colors
- `GET /api/trending/materials` - Trending materials
- `GET /api/trending/styles` - Trending styles
- `GET /api/trending/keywords` - Trending search keywords

### Demand Prediction
- `GET /api/demand` - Demand predictions
- `GET /api/demand/forecast/{category}` - Category-specific forecast
- `GET /api/demand/seasonal` - Seasonal predictions

### Recommendations
- `GET /api/recommendations` - Product recommendations
- `POST /api/image/analyze` - Analyze fashion image

### Search
- `GET /api/search?q=` - Search products
- `GET /api/search/autocomplete?q=` - Autocomplete suggestions
- `GET /api/search/filters` - Available filters

### Analytics
- `GET /api/analytics/weekly` - Weekly analytics
- `GET /api/analytics/monthly` - Monthly analytics

## Configuration

### Environment Variables

Key configuration options in `.env`:

```env
# Application
APP_NAME=TrendLoom
DEBUG=True

# Server
HOST=0.0.0.0
PORT=8000

# Database
DATABASE_URL=sqlite+aiosqlite:///./trendloom.db

# Region
DEFAULT_STATE=Tamil Nadu

# Scheduler
SCHEDULER_ENABLED=True
DATA_COLLECTION_INTERVAL_HOURS=6

# CORS
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5500
```

## Data Sources

The backend collects data from:

### Free Sources
- **Google Trends**: Fashion search trends
- **Google Shopping**: Product data
- **E-commerce Sites**: Myntra, Ajio, Flipkart (when available)
- **Public Datasets**: Fashion datasets from Kaggle

### AI Models (Free)
- **Hugging Face Models**: Image classification, embeddings
- **Scikit-learn**: Trend analysis
- **PyTorch**: Image processing

## Background Jobs

The system runs automated background jobs:

1. **Data Collection** (Every 6 hours)
   - Scrapes products from e-commerce sites
   - Collects Google Trends data
   - Updates product database

2. **Trend Analysis** (Every hour)
   - Calculates trend scores
   - Updates color/material trends
   - Identifies rising/declining trends

3. **Demand Prediction** (Every 3 hours)
   - Generates demand forecasts
   - Updates prediction models
   - Calculates seasonal factors

## Database Schema

### Main Tables
- `products`: Fashion products with attributes
- `trends`: Trend data from various sources
- `color_trends`: Color popularity tracking
- `material_trends`: Material popularity tracking
- `demand_predictions`: Demand forecasts
- `recommendations`: Product recommendations
- `search_logs`: Search analytics

## State Support

Currently supports:
- Tamil Nadu (default)

### Adding New States

The architecture is scalable. To add a new state:

1. Update `DEFAULT_STATE` in configuration
2. Data collection will automatically start for the new state
3. No frontend changes required

## AI Features

### Image Analysis
Upload images for:
- Category detection
- Color extraction
- Attribute identification
- Style/pattern recognition
- Similar product search

### Demand Forecasting
- Linear trend analysis
- Seasonal adjustment
- Growth rate calculation
- Confidence scoring

### Recommendations
- Trend-based suggestions
- Image similarity matching
- Category-specific recommendations

## Performance

- API response time: < 500ms (cached)
- Async endpoints for better concurrency
- Background processing for heavy tasks
- Database query optimization

## Caching

Optional Redis caching for:
- Frequently requested data
- Dashboard metrics
- Trending products
- Search results

Enable by setting `REDIS_ENABLED=True` in `.env`

## Logging

Logs are written to:
- Console (stdout)
- File: `logs/trendloom.log`

Log level can be configured via `LOG_LEVEL` environment variable.

## Testing

```bash
# Run tests (when available)
pytest

# With coverage
pytest --cov=app
```

## Docker Support (Optional)

```dockerfile
# Dockerfile provided separately
docker build -t trendloom-backend .
docker run -p 8000:8000 trendloom-backend
```

## Production Deployment

### Using Uvicorn

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Using Gunicorn + Uvicorn Workers

```bash
gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### PostgreSQL Setup

Update `DATABASE_URL` in `.env`:
```env
DATABASE_URL=postgresql+asyncpg://user:password@localhost/trendloom
```

## Frontend Integration

The backend is designed to work seamlessly with the existing frontend. Simply update the frontend API calls to point to:

```javascript
const API_BASE_URL = 'http://localhost:8000/api';
```

All endpoints return JSON in a format compatible with the frontend components.

## Troubleshooting

### Database Connection Issues
- Check `DATABASE_URL` in `.env`
- Ensure database file has write permissions

### Scheduler Not Starting
- Check `SCHEDULER_ENABLED=True` in `.env`
- Review logs for errors

### Data Collection Failing
- Check network connectivity
- Review scraping service logs
- Ensure user-agent is valid

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes
4. Add tests
5. Submit pull request

## License

MIT License

## Support

For issues and questions:
- Check API documentation at `/docs`
- Review logs in `logs/` directory
- Open an issue on GitHub

## Roadmap

- [ ] Add more e-commerce sources
- [ ] Implement advanced ML models
- [ ] Add user authentication
- [ ] Support all Indian states
- [ ] Real-time WebSocket updates
- [ ] Export reports feature
- [ ] A/B testing framework
- [ ] Performance monitoring

---

**Note**: This backend uses only free and open-source technologies. No paid APIs are required for full functionality.
