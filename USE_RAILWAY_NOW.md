# 🚂 DEPLOY TO RAILWAY NOW (Render Keeps Failing)

Render's having metadata generation issues. Railway will work.

## ⚡ FASTEST WAY - Railway Dashboard (No CLI needed)

### Step 1: Go to Railway
https://railway.app

### Step 2: Sign in with GitHub
Click "Login" → "Login with GitHub"

### Step 3: Deploy
1. Click **"New Project"**
2. Select **"Deploy from GitHub repo"**
3. Choose: **`trendloom-og`**
4. Railway auto-detects Python and deploys!

### Step 4: Configure Root Directory
1. Click on your service
2. Go to **"Settings"**
3. Under **"Root Directory"**, enter: `backend`
4. Click **"Redeploy"**

### Step 5: Get Your URL
Once deployed, Railway gives you a URL like:
```
https://trendloom-backend-production.up.railway.app
```

**Copy this URL!**

---

## 🔗 Connect Frontend

Edit `frontend/js/api.js` line 9:

```javascript
BASE_URL: 'https://trendloom-backend-production.up.railway.app/api',
```

Push to GitHub:
```bash
git add frontend/js/api.js
git commit -m "Connect to Railway backend"
git push origin main
```

**Vercel auto-deploys in 1 minute!**

---

## ✅ Why Railway Works

- ✅ Better Python environment
- ✅ Pre-compiled binary wheels
- ✅ No metadata generation errors
- ✅ Free tier: 500 hours/month
- ✅ Fast deploys (2-3 minutes)

---

## 🎯 DONE!

Your full stack will be live:
- Frontend: Vercel ✅
- Backend: Railway ✅
- Demo ready: ✅

**Total time: 5 minutes**
