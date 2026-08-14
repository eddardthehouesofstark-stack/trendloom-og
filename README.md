# 🎨 TrendLoom - AI-Powered Fashion Intelligence Platform

> Transforming fashion search data into production decisions with real-time intelligence

[![Deploy](https://img.shields.io/badge/Deploy-Live-success)](https://trendloom.vercel.app)
[![Backend](https://img.shields.io/badge/API-FastAPI-009688)](https://trendloom-backend.onrender.com/docs)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

## 🚀 Live Demo

- **Dashboard**: [trendloom.vercel.app](https://trendloom.vercel.app)
- **API Docs**: [API Documentation](https://trendloom-backend.onrender.com/docs)

---

## 📊 What is TrendLoom?

TrendLoom is an AI-powered fashion intelligence platform that helps manufacturers make data-driven production decisions by analyzing:

- **Real-time Google Trends data** (21+ fashion keywords tracked)
- **Regional demand patterns** across Indian states
- **Seasonal forecasting** for 4 major seasons
- **AI image analysis** using Hugging Face CLIP models
- **Supplier network intelligence** with country/state filtering
- **Competitive insights** from market leaders

**Problem**: Fashion manufacturers waste 30-40% of inventory due to trend misalignment.

**Solution**: Real-time intelligence that shows what to produce, what to wait on, and what to avoid - before you invest in production.

---

## ✨ Key Features

### 1. **Live Data Integration** 🔴
- Real-time Google Trends API integration
- 21 fashion keywords tracked (saree, kurta, jeans, dress, etc.)
- Market coverage calculated from actual search volumes
- Auto-refresh every 5 minutes
- Verifiable data (judges can check Google Trends themselves!)

### 2. **Explore Trends** 🔍
- 42 curated fashion trends with Pexels images
- Separate Men's & Women's categories
- Functional category and momentum filters
- Rising/Peak/Declining trend classification
- Progressive loading (12 trends at a time)

### 3. **Attribute Analyzer** 🤖
- AI-powered image analysis using Hugging Face CLIP
- Detects: colors, patterns, materials, styles, necklines, sleeve types
- Enhanced material detection (11 fabric types)
- Works with any fashion image
- Instant results

### 4. **Seasonal Intelligence** 📅
- 4 season-specific insights (Spring/Summer/Autumn/Winter)
- Pexels API integration for hero images
- Fashion week calendar (2026-2027)
- Global supplier network with country/state filters
- Production planning timeline

### 5. **Regional Intelligence** 🌏
- State-specific demand analysis (India)
- Tamil Nadu focus with 4 local suppliers
- Climate-based recommendations
- Cultural preference mapping

### 6. **Demand Forecasting** 📈
- 6-month demand predictions
- Category-level forecasting
- Peak period identification
- Confidence scores for each prediction

---

## 🛠️ Tech Stack

### Frontend
- **HTML5** + **TailwindCSS** (Material Design 3)
- **Vanilla JavaScript** (no framework overhead)
- **Pexels API** for fashion imagery
- **Vercel** hosting (global CDN)

### Backend
- **FastAPI** (Python async framework)
- **SQLAlchemy** (ORM with async support)
- **PyTrends** (Google Trends unofficial API)
- **Hugging Face Transformers** (CLIP for image analysis)
- **APScheduler** (automated data collection)
- **Render** hosting

### Database
- **Supabase PostgreSQL** (production)
- **SQLite** (local development)

### APIs
- Google Trends (real-time search data)
- Pexels (fashion imagery)
- Hugging Face (AI models)

---

## 📦 Installation

### Prerequisites
- Python 3.11+
- Node.js (optional, for frontend dev server)

### Local Setup

1. **Clone repository**
```bash
git clone https://github.com/YOUR-USERNAME/trendloom.git
cd trendloom
```

2. **Backend setup**
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
copy .env.example .env
python -m app.main
```

Backend runs on: `http://localhost:8000`

3. **Frontend setup**
```bash
cd frontend
# Just open dashboard.html in browser, or use:
python -m http.server 5500
```

Frontend runs on: `http://localhost:5500`

---

## 🚀 Deployment

See [DEPLOY_QUICK_START.md](DEPLOY_QUICK_START.md) for detailed deployment instructions.

**Quick version:**
1. **Database**: Create Supabase project (3 min)
2. **Backend**: Deploy to Render (5 min)
3. **Frontend**: Deploy to Vercel (5 min)

**Total**: 15 minutes, $0 cost

---

## 📁 Project Structure

```
trendloom/
├── backend/
│   ├── app/
│   │   ├── api/          # API endpoints
│   │   ├── models/       # Database models
│   │   ├── schemas/      # Pydantic schemas
│   │   ├── services/     # Business logic
│   │   ├── ai/           # AI/ML models
│   │   ├── scheduler/    # Background jobs
│   │   └── main.py       # FastAPI app
│   ├── requirements.txt
│   ├── Dockerfile
│   └── Procfile
├── frontend/
│   ├── js/
│   │   ├── api.js        # API client
│   │   ├── dashboard.js  # Dashboard logic
│   │   └── ...
│   ├── dashboard.html
│   ├── explore.html
│   ├── seasonal.html
│   └── ...
├── render.yaml           # Render config
├── vercel.json           # Vercel config
└── README.md
```

---

## 🎯 Use Cases

### For Manufacturers
- **What to produce**: See rising trends with high confidence
- **What to wait on**: Monitor emerging patterns
- **What to avoid**: Identify declining trends
- **When to produce**: Align with seasonal demand

### For Retailers
- **Buying decisions**: Know what will sell
- **Inventory planning**: Forecast demand accurately
- **Supplier selection**: Find best sources by region
- **Pricing strategy**: Understand momentum

### For Designers
- **Trend research**: See what's gaining traction
- **Color palettes**: Identify trending color stories
- **Material selection**: Know what fabrics are popular
- **Regional adaptation**: Customize for local markets

---

## 📊 Data Sources

1. **Google Trends** - Real-time search interest (free)
2. **Pexels API** - Fashion imagery (free, 200 requests/hour)
3. **Hugging Face** - AI models (free inference API)
4. **Internal Database** - Historical patterns & products

All APIs are free tier - no costs!

---

## 🔒 Environment Variables

Create `backend/.env`:

```env
# Database
DATABASE_URL=postgresql+asyncpg://postgres:password@host:5432/database

# APIs (optional - features work without these)
HUGGINGFACE_API_KEY=your_key_here

# Config
ENVIRONMENT=production
SCHEDULER_ENABLED=true
ALLOWED_ORIGINS=https://your-frontend.vercel.app
```

---

## 🧪 Testing

### Test Backend
```bash
cd backend
python -m pytest
```

### Test Frontend
Open browser DevTools (F12) and check:
- API calls succeed (Network tab)
- No console errors (Console tab)
- Data loads correctly

### Test API Endpoints
Visit: `http://localhost:8000/docs`

Try:
- `/api/dashboard/live` - Live Google Trends data
- `/api/trending/keywords` - Trending keywords
- `/api/image/analyze` - Upload fashion image

---

## 📈 Performance

- **Dashboard Load**: < 2 seconds
- **API Response**: < 500ms (avg)
- **Image Analysis**: < 3 seconds
- **Google Trends Fetch**: < 5 seconds
- **Database Queries**: < 100ms

**Optimizations:**
- Async/await throughout
- Database connection pooling
- API response caching (TTL: 5-15 min)
- Progressive image loading
- Lazy loading for heavy components

---

## 🤝 Contributing

This is a hackathon project, but contributions are welcome!

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

---

## 📝 License

MIT License - see [LICENSE](LICENSE) file

---

## 👥 Team

Built for **SRCAS Hackathon 14-15**

- Backend & AI Integration
- Frontend Development
- Data Analysis & Forecasting
- API Integration & Deployment

---

## 🙏 Acknowledgments

- **Google Trends** for real-time search data
- **Pexels** for beautiful fashion imagery
- **Hugging Face** for powerful AI models
- **Vercel, Render, Supabase** for free hosting

---

## 📞 Contact

- **Live Demo**: [trendloom.vercel.app](https://trendloom.vercel.app)
- **API Docs**: [API Documentation](https://trendloom-backend.onrender.com/docs)
- **Issues**: [GitHub Issues](https://github.com/YOUR-USERNAME/trendloom/issues)

---

## 🎓 Learn More

- [Deployment Guide](DEPLOYMENT_GUIDE.md) - Full deployment walkthrough
- [Quick Start](DEPLOY_QUICK_START.md) - Deploy in 15 minutes
- [API Documentation](https://trendloom-backend.onrender.com/docs) - Interactive API docs

---

**Built with ❤️ for the fashion industry**

*Making data-driven fashion production accessible to everyone*
