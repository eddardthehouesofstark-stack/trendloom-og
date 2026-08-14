# Deploy to Railway (Render Alternative)

Render is having build issues. Railway handles Python dependencies better.

## 🚀 Quick Railway Deployment

### Step 1: Install Railway CLI

```bash
npm install -g @railway/cli
```

### Step 2: Login to Railway

```bash
railway login
```

This opens your browser - sign in with GitHub.

### Step 3: Initialize Project

```bash
cd "d:\srcas hackathon 14 15"
railway init
```

Choose:
- Create new project: **Yes**
- Project name: **trendloom-backend**

### Step 4: Deploy

```bash
railway up
```

Railway will:
1. Detect Python automatically
2. Find your requirements.txt
3. Build and deploy
4. Give you a URL

### Step 5: Set Root Directory

In Railway dashboard:
1. Go to your service settings
2. Set **Root Directory** to: `backend`
3. Redeploy

### Step 6: Get Your URL

Railway gives you: `https://trendloom-backend-production.up.railway.app`

---

## ✅ Why Railway Works Better

- ✅ Better Python dependency handling
- ✅ Pre-built binary packages
- ✅ More build memory
- ✅ Faster builds
- ✅ Free tier: 500 hours/month

---

## 🔄 Alternative: If Railway CLI Doesn't Work

Use Railway Dashboard:

1. Go to https://railway.app
2. Click **"New Project"**
3. **"Deploy from GitHub repo"**
4. Select: `trendloom-og`
5. **Settings** → **Root Directory** → `backend`
6. Railway auto-deploys!

---

**This should work where Render failed!**
