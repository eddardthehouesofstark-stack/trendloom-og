# TrendLoom Backend - Project Structure

## Directory Tree

```
backend/
│
├── app/
│   ├── __init__.py                 # Application initialization
│   ├── main.py                     # FastAPI app & startup/shutdown
│   ├── config.py                   # Configuration management
│   │
│   ├── models/                     # SQLAlchemy models
│   │   ├── __init__.py
│   │   ├── product.py              # Product model
│   │   ├── trend.py                # Trend, ColorTrend, MaterialTrend models
│   │   └── analytics.py            # SearchLog, Recommendation, DemandPrediction
│   │
│   ├── schemas/                    # Pydantic schemas
│   │   ├── __init__.py
│   │   ├── product.py              # Product request/response schemas
│   │   ├── trend.py                # Trend schemas
│   │   └── analytics.py            # Analytics schemas
│   │
│   ├── api/                        # API endpoints
│   │   ├── __init__.py
│   │   ├── dashboard.py            # Dashboard endpoint
│   │   ├── trending.py             # Trending products, colors, materials
│   │   ├── recommendations.py      # Recommendations & image analysis
│   │   ├── search.py               # Search & autocomplete
│   │   ├── demand.py               # Demand predictions
│   │   └── analytics.py            # Weekly/monthly analytics
│   │
│   ├── services/                   # Business logic services
│   │   ├── __init__.py
│   │   ├── google_trends.py        # Google Trends integration
│   │   ├── web_scraper.py          # Web scraping service
│   │   ├── data_collector.py       # Data collection orchestration
│   │   ├── trend_analyzer.py       # Trend analysis logic
│   │   └── demand_predictor.py     # Demand prediction logic
│   │
│   ├── ai/                         # AI/ML models
│   │   ├── __init__.py
│   │   └── image_analyzer.py       # Image analysis with PyTorch
│   │
│   ├── scheduler/                  # Background jobs
│   │   ├── __init__.py
│   │   └── tasks.py                # APScheduler tasks
│   │
│   ├── database/                   # Database configuration
│   │   └── base.py                 # SQLAlchemy setup
│   │
│   └── utils/                      # Utility functions
│       └── __init__.py
│
├── logs/                           # Application logs
│   └── trendloom.log
│
├── models_cache/                   # AI model cache
│
├── requirements.txt                # Python dependencies
├── .env.example                    # Environment variables template
├── .env                            # Environment variables (gitignored)
├── .gitignore                      # Git ignore rules
├── Dockerfile                      # Docker container definition
├── docker-compose.yml              # Docker Compose configuration
├── README.md                       # Full documentation
├── QUICKSTART.md                   # Quick start guide
├── PROJECT_STRUCTURE.md            # This file
└── trendloom.db                    # SQLite database (created at runtime)
```

## Module Descriptions

### Core Application (`app/`)

#### `main.py`
- FastAPI application instance
- CORS middleware configuration
- Router registration
- Lifespan events (startup/shutdown)
- Database initialization
- Scheduler startup

#### `config.py`
- Settings management using Pydantic
- Environment variable handling
- Application configuration
- Default values

### Models (`app/models/`)

#### `product.py`
- **Product**: Fashion products with all attributes
  - Basic info: name, category, brand, price
  - Source tracking: source, source_url, source_id
  - Attributes: color, material, pattern, style
  - Metrics: trend_score, popularity_score, weekly_growth
  - AI features: ai_tags, ai_confidence

#### `trend.py`
- **Trend**: General trend tracking
  - Keyword, category, trend_type
  - Metrics: interest_score, growth_rate, momentum_score
  - Status: is_rising, is_declining, is_stable
- **ColorTrend**: Color popularity tracking
- **MaterialTrend**: Material/fabric popularity tracking

#### `analytics.py`
- **SearchLog**: Search query logging
- **Recommendation**: Product recommendations
- **DemandPrediction**: Demand forecasts

### Schemas (`app/schemas/`)

Pydantic models for:
- Request validation
- Response serialization
- Data transformation
- Type safety

### API Endpoints (`app/api/`)

#### `dashboard.py`
- `GET /api/dashboard` - Complete dashboard data
  - KPIs
  - Trending products
  - Categories, colors, materials
  - Action board
  - Regional preview

#### `trending.py`
- `GET /api/trending/products` - Trending products
- `GET /api/trending/categories` - Trending categories
- `GET /api/trending/colors` - Trending colors
- `GET /api/trending/materials` - Trending materials
- `GET /api/trending/styles` - Trending styles
- `GET /api/trending/keywords` - Trending keywords

#### `recommendations.py`
- `GET /api/recommendations` - Get recommendations
- `POST /api/image/analyze` - Analyze fashion image
  - Upload file or provide URL
  - AI-powered analysis
  - Similar product search

#### `search.py`
- `GET /api/search` - Search products
- `GET /api/search/autocomplete` - Autocomplete suggestions
- `GET /api/search/filters` - Available filters

#### `demand.py`
- `GET /api/demand` - Demand predictions
- `GET /api/demand/forecast/{category}` - Category forecast
- `GET /api/demand/seasonal` - Seasonal predictions

#### `analytics.py`
- `GET /api/analytics/weekly` - Weekly analytics
- `GET /api/analytics/monthly` - Monthly analytics

### Services (`app/services/`)

#### `google_trends.py`
- Google Trends integration using PyTrends
- Fetch interest over time
- Get related queries
- Analyze fashion keywords
- Trending searches

#### `web_scraper.py`
- Web scraping from e-commerce sites
- Myntra, Ajio, Google Shopping
- Product data extraction
- Async scraping with aiohttp

#### `data_collector.py`
- Orchestrates data collection
- Collects from all sources
- Saves to database
- Error handling and logging

#### `trend_analyzer.py`
- Calculate trend scores
- Analyze color trends
- Analyze material trends
- Update trend statuses
- Rising/declining detection

#### `demand_predictor.py`
- Generate demand predictions
- Linear trend analysis
- Seasonal adjustment
- Confidence scoring
- Graph data generation

### AI/ML (`app/ai/`)

#### `image_analyzer.py`
- Image analysis using PyTorch
- Category detection
- Color extraction
- Attribute detection
- Style and pattern recognition
- Material detection
- Tag generation

### Scheduler (`app/scheduler/`)

#### `tasks.py`
- Background job definitions
- Data collection job (every 6 hours)
- Trend analysis job (hourly)
- Prediction job (every 3 hours)
- Scheduler management

### Database (`app/database/`)

#### `base.py`
- SQLAlchemy async engine
- Session management
- Database initialization
- Connection pooling

## Data Flow

### 1. Data Collection Flow

```
Scheduler Trigger
    ↓
Data Collector Service
    ↓
├─→ Web Scraper → E-commerce Sites → Products
├─→ Google Trends → Fashion Keywords → Trends
    ↓
Database (Products, Trends)
```

### 2. Trend Analysis Flow

```
Scheduler Trigger
    ↓
Trend Analyzer
    ↓
├─→ Calculate Product Scores
├─→ Analyze Colors
├─→ Analyze Materials
└─→ Update Statuses
    ↓
Database (Updated Trends)
```

### 3. Prediction Flow

```
Scheduler Trigger
    ↓
Demand Predictor
    ↓
├─→ Get Historical Data
├─→ Calculate Predictions
├─→ Generate Graph Data
└─→ Apply Seasonal Factors
    ↓
Database (Predictions)
```

### 4. API Request Flow

```
Frontend Request
    ↓
FastAPI Router
    ↓
API Endpoint
    ↓
├─→ Query Database
├─→ Apply Filters
├─→ Calculate Metrics
└─→ Format Response
    ↓
JSON Response to Frontend
```

### 5. Image Analysis Flow

```
Image Upload
    ↓
Image Analyzer
    ↓
├─→ Detect Category
├─→ Extract Colors
├─→ Detect Attributes
└─→ Generate Tags
    ↓
├─→ Find Similar Products
└─→ Generate Recommendations
    ↓
JSON Response
```

## Key Features by Module

### Data Collection
- **Sources**: Multiple e-commerce platforms
- **Frequency**: Every 6 hours
- **Data**: Products, prices, images, attributes
- **Storage**: SQLite database

### Trend Analysis
- **Metrics**: Trend score, popularity, growth
- **Colors**: Dominant color tracking
- **Materials**: Fabric popularity
- **Status**: Rising, declining, stable

### AI Analysis
- **Image**: Category, color, style detection
- **Text**: Keyword extraction
- **Prediction**: Demand forecasting
- **Recommendation**: Personalized suggestions

### API Services
- **Fast**: < 500ms response time
- **Async**: Concurrent request handling
- **Cached**: Frequently accessed data
- **Documented**: Swagger/OpenAPI

## Database Schema Summary

### Tables
1. **products**: Fashion product catalog
2. **trends**: Trend tracking
3. **color_trends**: Color popularity
4. **material_trends**: Material popularity
5. **demand_predictions**: Forecasts
6. **recommendations**: Suggestions
7. **search_logs**: Search analytics

### Relationships
- Products ← Recommendations
- Products → ColorTrends (aggregated)
- Products → MaterialTrends (aggregated)
- Trends → DemandPredictions

## Configuration

### Environment Variables
All configuration in `.env`:
- Application settings
- Database connection
- Scheduler settings
- Regional defaults
- API keys (optional)

### Defaults
- State: Tamil Nadu
- Collection: Every 6 hours
- Analysis: Every hour
- Predictions: Every 3 hours

## Technology Choices

### Why FastAPI?
- Fast, modern Python web framework
- Automatic API documentation
- Type checking with Pydantic
- Async support

### Why SQLite?
- No server setup required
- File-based, portable
- Good performance for moderate load
- Easy PostgreSQL migration

### Why APScheduler?
- Pure Python scheduler
- No external dependencies
- Async job support
- Flexible triggers

### Why Free Tools?
- No API costs
- No vendor lock-in
- Full control
- Open-source community

## Extending the System

### Add New Data Source
1. Create scraper in `services/web_scraper.py`
2. Add to collection in `services/data_collector.py`
3. Map fields to Product model

### Add New State
1. Update `DEFAULT_STATE` in config
2. Data collection auto-adapts
3. No code changes needed

### Add New AI Model
1. Add model in `ai/` directory
2. Integrate in `image_analyzer.py`
3. Update schemas if needed

### Add New Endpoint
1. Create router in `api/`
2. Register in `main.py`
3. Document in schemas

## Performance Optimization

### Current
- Async database operations
- Connection pooling
- Background processing
- Efficient queries

### Future
- Redis caching
- Query optimization
- Response compression
- CDN for images

## Security

### Implemented
- CORS protection
- Input validation
- SQL injection prevention (SQLAlchemy)
- Error handling

### Production Recommendations
- Add authentication
- Rate limiting
- API keys
- HTTPS only

---

This structure provides a solid foundation for a scalable, maintainable fashion trend analytics backend!
