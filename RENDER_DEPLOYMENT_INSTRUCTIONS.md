# Render Deployment Instructions

## 🚀 Step-by-Step Guide to Deploy Backend on Render

### Prerequisites
- GitHub repository with your code (✅ Already done)
- Render account (free): https://render.com

---

## Option 1: Deploy via Render Dashboard (Recommended)

### Step 1: Create New Web Service

1. Go to https://dashboard.render.com
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository:
   - Click **"Connect account"** if not connected
   - Search for: `trendloom-og`
   - Click **"Connect"**

### Step 2: Configure Service

**Basic Settings:**
```
Name: trendloom-backend
Region: Singapore (or closest to you)
Branch: main
Root Directory: backend
```

**Build Settings:**
```
Runtime: Python 3
Build Command: pip install -r requirements.txt
Start Command: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

**Plan:**
```
Instance Type: Free
```

### Step 3: Environment Variables

Add these environment variables:

```
ENVIRONMENT=production
DATABASE_URL=sqlite+aiosqlite:///./trendloom.db
SCHEDULER_ENABLED=False
DEBUG=False
CORS_ORIGINS=*
HUGGINGFACE_API_KEY=(leave empty - optional)
```

### Step 4: Advanced Settings

**Health Check Path:**
```
/api/health
```

**Auto-Deploy:**
```
✓ Enable (auto-deploy from GitHub)
```

### Step 5: Create Web Service

1. Click **"Create Web Service"**
2. Wait 3-5 minutes for build
3. Monitor logs for any errors

### Step 6: Get Your URL

Once deployed, you'll see:
```
https://trendloom-backend-xxxx.onrender.com
```

**Save this URL!** You'll need it to connect the frontend.

---

## Option 2: Deploy via render.yaml (Automatic)

### Already Configured! ✅

Your `render.yaml` file is ready. Render should automatically detect it.

**If it doesn't:**
1. In Render Dashboard → **"Blueprint"**
2. Connect repository
3. Render will use `render.yaml` configuration
4. Click **"Apply"**

---

## Option 3: Deploy via Render CLI

```bash
# Install Render CLI
npm install -g @render-cli/cli

# Login
render login

# Deploy
render deploy
```

---

## 🐛 Common Build Issues & Solutions

### Issue 1: "Build Failed - Out of Memory"

**Solution:** Your requirements are already minimal. This shouldn't happen.

If it does:
```bash
# Further reduce requirements.txt to absolute minimum:
fastapi==0.109.0
uvicorn[standard]==0.27.0
aiosqlite==0.19.0
pytrends==4.9.2
pillow>=10.0.0
```

### Issue 2: "Module not found: app"

**Solution:** Check Root Directory

1. In Render Dashboard → **Service Settings**
2. Set **Root Directory** to: `backend`
3. Redeploy

### Issue 3: "Port binding failed"

**Solution:** Your Procfile is correct. Make sure:
- Start Command uses `$PORT` variable
- Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### Issue 4: "Health check failing"

**Solution:** Wait 2-3 minutes after deploy

Health check hits `/api/health`. First request may be slow.

### Issue 5: "Dependencies taking too long"

**Solution:** Render free tier has a 15-minute build timeout

Your minimal requirements should build in ~3-5 minutes.

If timeout occurs:
- Remove `pandas` (only needed for advanced analytics)
- Remove `beautifulsoup4` and `lxml` (only for scraping)

---

## 📋 Minimal Requirements (If Build Fails)

**Absolute minimum to get image analysis working:**

```
fastapi==0.109.0
uvicorn[standard]==0.27.0
aiosqlite==0.19.0
pillow>=10.0.0
requests==2.31.0
python-multipart==0.0.6
python-dotenv==1.0.1
```

**This removes:**
- PyTrends (live trends won't work, but image analysis will)
- Pandas (analytics endpoints will fail)
- BeautifulSoup/lxml (scraping won't work)

**But keeps:**
- Image analysis ✅ (your main feature)
- Basic API ✅
- Health checks ✅

---

## 🔍 How to Monitor Deployment

### View Logs

1. In Render Dashboard
2. Select your service
3. Click **"Logs"** tab
4. Watch for:
   ```
   Installing dependencies...
   Building...
   Starting server...
   Application startup complete
   ```

### Check Health

Once "Deploy succeeded" appears:

```bash
curl https://trendloom-backend-xxxx.onrender.com/api/health
```

**Expected Response:**
```json
{
  "status": "healthy",
  "app": "TrendLoom",
  "version": "1.0.0",
  "environment": "production"
}
```

---

## ⚡ Speed Up Deployment

### 1. Disable Scheduler

Already done in `.env.example`:
```
SCHEDULER_ENABLED=False
```

This prevents background tasks from running on free tier.

### 2. Use SQLite (Not PostgreSQL)

Already configured:
```
DATABASE_URL=sqlite+aiosqlite:///./trendloom.db
```

No external database needed.

### 3. Minimal Dependencies

Already stripped down in `requirements.txt`.

---

## 🎯 Post-Deployment Checklist

After successful deployment:

- [ ] Service shows "Live" status
- [ ] Health check returns 200 OK
- [ ] `/api/health` endpoint responds
- [ ] Copy backend URL
- [ ] Update `frontend/js/api.js` with URL
- [ ] Push frontend changes
- [ ] Test image upload

---

## 🔄 Redeploy After Changes

### Automatic Redeploy:
- Push to GitHub → Render auto-deploys
- No manual action needed

### Manual Redeploy:
1. Render Dashboard
2. Select service
3. Click **"Manual Deploy"** → **"Deploy latest commit"**

---

## 📊 What to Expect

### Build Time:
```
Installing dependencies: ~2-3 minutes
Building application: ~30 seconds
Starting server: ~10 seconds
──────────────────────────────────
Total: ~3-5 minutes
```

### First Request:
```
Cold start: ~30-60 seconds (free tier)
Subsequent: <1 second
```

### Health Check:
```
Render checks /api/health every 5 minutes
If fails 3 times → marks as unhealthy
```

---

## 🆘 If Deployment Fails

### Check These:

1. **Build Logs** - What's the actual error?
2. **Root Directory** - Set to `backend`
3. **Start Command** - Should be: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4. **Python Version** - Should auto-detect 3.11

### Alternative: Use Railway

If Render fails completely, try Railway:

```bash
# Install Railway CLI
npm i -g @railway/cli

# Login
railway login

# Deploy
cd backend
railway up
```

**Railway also has a free tier** and might handle dependencies better.

---

## ✅ Success Indicators

You'll know it's working when you see:

```
✓ Build completed successfully
✓ Service is live
✓ Health check passing
✓ URL is accessible
```

**In logs:**
```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:PORT
```

---

## 📞 Need Help?

If deployment fails:

1. **Check Render Logs** - Usually shows the exact issue
2. **Verify `requirements.txt`** - Should be minimal
3. **Check Root Directory** - Must be `backend`
4. **Review error message** - Often very specific

**Common fixes:**
- Wrong root directory
- Missing environment variable
- Dependency conflict
- Port binding issue

---

## 🎉 Once Deployed Successfully

**You'll have:**
- ✅ Live backend API
- ✅ Image analysis endpoint
- ✅ Live Google Trends data
- ✅ Health monitoring
- ✅ Auto-deploy from GitHub

**Next step:**
→ See `CONNECT_FRONTEND_BACKEND.md` to connect frontend

---

**Your backend URL will look like:**
```
https://trendloom-backend-[random-id].onrender.com
```

**Save it** - you'll need it for the frontend connection!
