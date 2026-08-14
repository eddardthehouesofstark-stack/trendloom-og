# 🚀 Quick Deploy - 3 Steps

## Prerequisites
- GitHub account
- 15 minutes

---

## Step 1: Database (Supabase) - 3 minutes

1. Go to **https://supabase.com** → Sign up with GitHub
2. **New Project** → Name: `trendloom` → Set password → Create
3. **Settings** → **Database** → Copy **Connection Pooling** string
4. Convert to: `postgresql+asyncpg://postgres.[ref]:[password]@aws-0-[region].pooler.supabase.com:5432/postgres`
5. Save this - you'll need it in Step 2

---

## Step 2: Backend (Render) - 5 minutes

1. Push code to GitHub:
```bash
cd "d:\srcas hackathon 14 15"
git init
git add .
git commit -m "TrendLoom - Fashion Intelligence Platform"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/trendloom.git
git push -u origin main
```

2. Go to **https://render.com** → Sign up with GitHub
3. **New +** → **Web Service** → Connect repo
4. Configure:
   - Name: `trendloom-backend`
   - Runtime: **Python 3**
   - Build: `pip install -r backend/requirements.txt`
   - Start: `cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - Plan: **Free**

5. **Environment Variables** (click Advanced):
```
DATABASE_URL = [paste your Supabase connection string from Step 1]
ENVIRONMENT = production
ALLOWED_ORIGINS = *
```

6. **Create Web Service** → Wait 5-10 min
7. Copy URL: `https://trendloom-backend.onrender.com`

---

## Step 3: Frontend (Vercel) - 5 minutes

1. Update API URL in `frontend/js/api.js`:
```javascript
const API_CONFIG = {
    BASE_URL: 'https://trendloom-backend.onrender.com/api',  // ← Your Render URL
    DEFAULT_STATE: 'Tamil Nadu',
    TIMEOUT: 10000,
};
```

2. Commit:
```bash
git add frontend/js/api.js
git commit -m "Update API URL for production"
git push
```

3. Go to **https://vercel.com** → Sign up with GitHub
4. **Add New** → **Project** → Import your repo
5. **Root Directory**: `frontend`
6. **Deploy** → Wait 2 minutes
7. Copy URL: `https://trendloom.vercel.app`

---

## ✅ Done!

**Your Live URLs:**
- Frontend: `https://trendloom.vercel.app`
- Backend API: `https://trendloom-backend.onrender.com`
- API Docs: `https://trendloom-backend.onrender.com/docs`

**Test It:**
1. Visit your frontend URL
2. Dashboard should load with data
3. Navigate to Explore Trends
4. Try Attribute Analyzer (upload image)

**Note:** First load may take 30-60 seconds (Render cold start). After that, it's instant!

---

## Troubleshooting

**Frontend loads but no data?**
- Check browser console (F12) for errors
- Verify backend URL in `api.js` is correct
- Visit backend `/docs` to test API directly

**Backend 502 error?**
- Check Render logs
- Verify `DATABASE_URL` environment variable
- Wait a few minutes (might still be deploying)

**CORS errors?**
- Update `ALLOWED_ORIGINS` in Render environment variables
- Include your Vercel URL
- Save changes (triggers redeploy)

---

## Keep Backend Awake (Optional)

Render free tier sleeps after 15 min inactivity. To prevent:

1. Go to **https://uptimerobot.com** (free)
2. Add Monitor → **HTTP(s)**
3. URL: `https://trendloom-backend.onrender.com/api/health`
4. Interval: **5 minutes**
5. Save

Your backend will now stay warm 24/7!

---

## Total Cost: **$0**
## Total Time: **15 minutes**
## Hackathon Ready: **✅**
