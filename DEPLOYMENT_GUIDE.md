# 🚀 TrendLoom Deployment Guide

## Stack Overview
- **Frontend**: Vercel (Static hosting)
- **Backend**: Render (Python/FastAPI)
- **Database**: Supabase (PostgreSQL)

All services have generous free tiers perfect for hackathon demos!

---

## Step 1: Database Setup (Supabase) ☁️

### 1.1 Create Supabase Project
1. Go to https://supabase.com
2. Click "Start your project"
3. Sign up with GitHub
4. Click "New Project"
5. Fill in:
   - Name: `trendloom`
   - Database Password: (save this securely!)
   - Region: Choose closest to you
6. Click "Create new project" (takes ~2 minutes)

### 1.2 Get Database Connection String
1. In your Supabase dashboard, click "Project Settings" (gear icon)
2. Go to "Database" section
3. Scroll to "Connection string"
4. Copy the "Connection pooling" URI (it starts with `postgresql://`)
5. Replace `[YOUR-PASSWORD]` with your database password

**Your connection string looks like:**
```
postgresql://postgres.xxxxx:password@aws-0-region.pooler.supabase.com:5432/postgres
```

### 1.3 For SQLAlchemy (Async)
Convert the connection string for asyncpg:
```
postgresql+asyncpg://postgres.xxxxx:password@aws-0-region.pooler.supabase.com:5432/postgres
```

---

## Step 2: Backend Deployment (Render) 🔧

### 2.1 Push Code to GitHub
```bash
cd "d:\srcas hackathon 14 15"
git init
git add .
git commit -m "Initial commit - TrendLoom hackathon project"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/trendloom.git
git push -u origin main
```

### 2.2 Deploy to Render
1. Go to https://render.com
2. Sign up with GitHub
3. Click "New +" → "Web Service"
4. Connect your GitHub repository
5. Select your `trendloom` repo
6. Fill in:
   - **Name**: `trendloom-backend`
   - **Region**: Singapore (or closest)
   - **Branch**: main
   - **Root Directory**: (leave empty)
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r backend/requirements.txt`
   - **Start Command**: `cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Plan**: Free

### 2.3 Add Environment Variables
Click "Advanced" → "Add Environment Variable":

```
DATABASE_URL = postgresql+asyncpg://postgres.xxxxx:password@aws-0-region.pooler.supabase.com:5432/postgres
ENVIRONMENT = production
ALLOWED_ORIGINS = https://your-frontend.vercel.app,https://*.vercel.app
SCHEDULER_ENABLED = true
LOG_LEVEL = INFO
```

7. Click "Create Web Service"
8. Wait 5-10 minutes for deployment
9. Copy your backend URL: `https://trendloom-backend.onrender.com`

### 2.4 Test Backend
Visit: `https://trendloom-backend.onrender.com/docs`

You should see the FastAPI Swagger documentation!

---

## Step 3: Frontend Deployment (Vercel) 🌐

### 3.1 Update API Base URL
Edit `frontend/js/api.js`:

```javascript
const API_CONFIG = {
    // Update this to your Render backend URL
    BASE_URL: 'https://trendloom-backend.onrender.com/api',
    DEFAULT_STATE: 'Tamil Nadu',
    TIMEOUT: 10000,
};
```

### 3.2 Commit the change
```bash
git add frontend/js/api.js
git commit -m "Update API URL for production"
git push
```

### 3.3 Deploy to Vercel
1. Go to https://vercel.com
2. Sign up with GitHub
3. Click "Add New" → "Project"
4. Import your `trendloom` repository
5. Configure:
   - **Framework Preset**: Other
   - **Root Directory**: `frontend`
   - **Build Command**: (leave empty)
   - **Output Directory**: (leave empty)
6. Click "Deploy"
7. Wait 2-3 minutes
8. Copy your frontend URL: `https://trendloom.vercel.app`

### 3.4 Update CORS on Backend
Go back to Render dashboard:
1. Go to your backend service
2. Environment → Edit `ALLOWED_ORIGINS`
3. Add your Vercel URL:
   ```
   https://trendloom.vercel.app,https://*.vercel.app
   ```
4. Save (triggers redeploy)

---

## Step 4: Initialize Database 🗄️

### 4.1 Run Database Migrations
In your Render service dashboard:
1. Go to "Shell" tab
2. Run:
```bash
cd backend
python -c "from app.database.base import init_db; import asyncio; asyncio.run(init_db())"
```

Or, use Supabase SQL Editor:
1. Go to Supabase dashboard → SQL Editor
2. Create tables using SQLAlchemy models (auto-creates on first API call)

---

## Step 5: Verify Deployment ✅

### 5.1 Test Backend
Visit: `https://trendloom-backend.onrender.com/docs`
- Try the `/api/health` endpoint
- Try `/api/trending/keywords?state=Tamil Nadu`

### 5.2 Test Frontend
Visit: `https://trendloom.vercel.app`
- Dashboard should load
- Check browser console (F12) for API calls
- Verify data is loading

### 5.3 Test Full Flow
1. Open dashboard
2. Navigate to "Explore Trends"
3. Upload an image to "Attribute Analyzer"
4. Check "Seasonal Intelligence"

---

## Troubleshooting 🔧

### Backend Issues

**502 Bad Gateway on Render:**
- Check backend logs in Render dashboard
- Verify `DATABASE_URL` is correct
- Check if database tables exist

**CORS Errors:**
- Update `ALLOWED_ORIGINS` in Render
- Include your Vercel URL
- Redeploy backend

**Database Connection Failed:**
- Verify Supabase connection string
- Check if Supabase project is active
- Try using "Transaction pooling" mode instead of "Session pooling"

### Frontend Issues

**API Calls Failing:**
- Check `frontend/js/api.js` has correct backend URL
- Verify CORS is configured
- Check browser console for errors

**Images Not Loading:**
- Pexels API key is embedded in code (should work)
- Check browser console for API errors
- Verify network tab shows successful requests

---

## Free Tier Limits

### Supabase (Free)
- ✅ 500 MB database
- ✅ Unlimited API requests
- ✅ 2 GB bandwidth/month
- ✅ 50 MB file storage

### Render (Free)
- ✅ 750 hours/month (enough for 24/7)
- ✅ Sleeps after 15 min inactivity
- ✅ 512 MB RAM
- ✅ Shared CPU
- ⚠️ Cold starts (~30 seconds)

### Vercel (Free)
- ✅ 100 GB bandwidth/month
- ✅ Unlimited deployments
- ✅ Automatic HTTPS
- ✅ Edge network (fast worldwide)

---

## Production Optimization

### For Render Cold Starts
Add a "keep-alive" service:
1. Use UptimeRobot (free) to ping your backend every 5 minutes
2. Visit: https://uptimerobot.com
3. Add monitor: `https://trendloom-backend.onrender.com/api/health`

### For Supabase Performance
Enable connection pooling:
1. Use "Transaction pooling" mode
2. Add `?pgbouncer=true` to connection string
3. Set `pool_pre_ping=True` in SQLAlchemy

---

## Environment Variables Reference

### Backend (Render)

**Required:**
```
DATABASE_URL = postgresql+asyncpg://...
ENVIRONMENT = production
ALLOWED_ORIGINS = https://trendloom.vercel.app
```

**Optional:**
```
SCHEDULER_ENABLED = true
DATA_COLLECTION_INTERVAL_HOURS = 6
LOG_LEVEL = INFO
CACHE_TTL_SHORT = 300
DEFAULT_STATE = Tamil Nadu
```

---

## Custom Domain (Optional)

### Add Custom Domain to Vercel
1. Go to Project Settings → Domains
2. Add your domain
3. Update DNS records as instructed

### Add Custom Domain to Render
1. Go to Service Settings → Custom Domains
2. Add your API subdomain (e.g., api.yourdomain.com)
3. Update DNS records

---

## Monitoring & Logs

### Backend Logs (Render)
- Dashboard → Logs tab
- Real-time streaming
- Search functionality

### Frontend Errors (Vercel)
- Dashboard → Deployments → View Function Logs
- Or use browser DevTools (F12)

### Database Metrics (Supabase)
- Dashboard → Database
- Shows connections, queries, size

---

## Cost Estimate

**For Hackathon Demo:**
- **Cost**: $0 (100% free)
- **Deployment Time**: ~30 minutes
- **Maintenance**: Zero

**For Production (if scaling):**
- Render Pro: $7/month (no cold starts)
- Supabase Pro: $25/month (8 GB database)
- Vercel Pro: $20/month (more bandwidth)

---

## Quick Deploy Checklist

- [ ] Create Supabase project
- [ ] Get database connection string
- [ ] Push code to GitHub
- [ ] Deploy backend to Render
- [ ] Add environment variables
- [ ] Update frontend API URL
- [ ] Deploy frontend to Vercel
- [ ] Update CORS on backend
- [ ] Test full application
- [ ] Add UptimeRobot monitor (optional)

---

## Support

**Issues?**
- Check backend logs in Render
- Check browser console (F12)
- Verify environment variables
- Test API endpoints at `/docs`

**Demo URLs:**
- Frontend: https://trendloom.vercel.app
- Backend API: https://trendloom-backend.onrender.com
- API Docs: https://trendloom-backend.onrender.com/docs

---

**Deployment Status**: ✅ Production Ready
**Free Tier**: ✅ Sufficient for hackathon
**Scalability**: ✅ Easy to upgrade
