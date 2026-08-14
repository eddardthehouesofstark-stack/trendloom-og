# TrendLoom Backend - Quick Start Guide

Get the backend running in 5 minutes!

## Prerequisites

- Python 3.11+ installed
- Internet connection

## Quick Install

### Windows

```cmd
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python -m app.main
```

### Linux/Mac

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python -m app.main
```

## Verify Installation

Open your browser and visit:
- **API**: http://localhost:8000
- **Docs**: http://localhost:8000/docs

You should see the API documentation!

## Test the API

### Using Browser

Visit: http://localhost:8000/api/dashboard

### Using curl

```bash
curl http://localhost:8000/api/trending/products
```

### Using Python

```python
import requests

response = requests.get('http://localhost:8000/api/dashboard')
print(response.json())
```

## Connect Frontend

Update your frontend JavaScript to use the API:

```javascript
const API_BASE_URL = 'http://localhost:8000/api';

// Example: Fetch dashboard data
fetch(`${API_BASE_URL}/dashboard`)
    .then(res => res.json())
    .then(data => console.log(data));
```

## What Happens on First Run?

1. **Database Creation**: SQLite database is created automatically
2. **Initial Data Collection**: Background job starts collecting fashion data
3. **API Ready**: All endpoints become available immediately

## Data Collection

The system automatically collects data every 6 hours. You can also trigger it manually:

1. The scheduler runs in the background
2. Data is collected from Google Trends and e-commerce sites
3. Trends are analyzed and predictions are generated

Initial data collection may take 5-10 minutes. The API works even while data is being collected.

## Common Issues

### Port Already in Use

Change the port in `.env`:
```env
PORT=8001
```

### Module Not Found Error

Make sure you're in the virtual environment:
```bash
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

### Database Permission Error

Make sure you have write permissions in the backend directory.

## Next Steps

1. Review API documentation at http://localhost:8000/docs
2. Test endpoints with your frontend
3. Check logs in `logs/trendloom.log`
4. Configure settings in `.env`

## Production Deployment

For production, use:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## Need Help?

- Check the full README.md for detailed documentation
- Review API docs at `/docs` endpoint
- Check logs for errors

## Stopping the Server

Press `Ctrl+C` in the terminal where the server is running.

---

That's it! You're ready to go! 🚀
