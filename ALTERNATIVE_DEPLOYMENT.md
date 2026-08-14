# Alternative Deployment Options

If Render deployment is taking too long or failing, here are **3 alternative options** to deploy your backend quickly.

---

## Option 1: Railway (Easiest Alternative)

### Why Railway?
- Similar to Render (free tier available)
- Better dependency handling
- Faster builds
- Simple setup

### Quick Deploy:

```bash
# Install Railway CLI
npm i -g @railway/cli

# Login
railway login

# Link to project
railway link

# Deploy
cd backend
railway up
```

### Via Dashboard:
1. Go to https://railway.app
2. Click **"New Project"**
3. Select **"Deploy from GitHub repo"**
4. Choose `trendloom-og`
5. Set root directory: `backend`
6. Railway auto-detects Python and deploys

**Environment Variables to Add:**
```
ENVIRONMENT=production
SCHEDULER_ENABLED=False
DATABASE_URL=sqlite+aiosqlite:///./trendloom.db
```

### Get Your URL:
Railway provides: `https://trendloom-production.up.railway.app`

---

## Option 2: Fly.io (Fast & Reliable)

### Why Fly.io?
- Better performance on free tier
- No cold starts
- Global edge network

### Quick Deploy:

```bash
# Install Fly CLI
powershell -Command "iwr https://fly.io/install.ps1 -useb | iex"

# Login
fly auth login

# Create app
cd backend
fly launch --name trendloom-backend --region sin

# Deploy
fly deploy
```

### Configuration:
Fly creates `fly.toml` automatically. Update if needed:

```toml
app = "trendloom-backend"

[build]
  builder = "paketobuildpacks/builder:base"

[env]
  PORT = "8080"
  ENVIRONMENT = "production"

[[services]]
  http_checks = []
  internal_port = 8080
  processes = ["app"]
  protocol = "tcp"

  [[services.ports]]
    port = 80
    handlers = ["http"]

  [[services.ports]]
    port = 443
    handlers = ["tls", "http"]

[http_service]
  internal_port = 8080
  force_https = true
  auto_stop_machines = true
  auto_start_machines = true
```

---

## Option 3: Vercel Backend (Serverless)

### Why Vercel?
- Frontend already on Vercel
- Everything in one place
- Instant deployment

### Steps:

1. **Create `vercel.json` in project root:**

```json
{
  "version": 2,
  "builds": [
    {
      "src": "backend/app/main.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/api/(.*)",
      "dest": "backend/app/main.py"
    }
  ]
}
```

2. **Install Vercel CLI:**
```bash
npm i -g vercel
```

3. **Deploy:**
```bash
vercel --prod
```

**Note:** Serverless has limitations:
- No background tasks
- 10-second timeout per request
- SQLite won't persist (need external DB)

---

## Option 4: PythonAnywhere (No CLI Needed)

### Why PythonAnywhere?
- Web-based setup
- No CLI installation
- Good for Python apps

### Steps:

1. Go to https://www.pythonanywhere.com
2. Create free account
3. Upload code via web interface
4. Set up WSGI configuration
5. Install dependencies via web console

**Pros:** Simple web interface  
**Cons:** Manual setup, slower

---

## Option 5: Heroku (Classic)

### Why Heroku?
- Industry standard
- Reliable
- Good documentation

### Steps:

```bash
# Install Heroku CLI
winget install Heroku.HerokuCLI

# Login
heroku login

# Create app
heroku create trendloom-backend

# Set buildpack
heroku buildpacks:set heroku/python

# Deploy
cd backend
git push heroku main
```

**Note:** Heroku removed free tier, but has free trial credits.

---

## Option 6: Local Ngrok Tunnel (For Demo Only)

### Why Ngrok?
- Instant (no build time)
- Perfect for demos
- Runs on your machine

### Steps:

1. **Download ngrok:** https://ngrok.com/download
2. **Start backend locally:**
```bash
cd backend
uvicorn app.main:app --reload
```

3. **Expose via ngrok:**
```bash
ngrok http 8000
```

4. **Get public URL:**
```
https://abcd1234.ngrok.io
```

5. **Update frontend** `api.js` with ngrok URL

**Pros:** 
- Instant (0 build time)
- Works with local backend
- Perfect for demos

**Cons:**
- Must keep laptop running
- URL changes each time (unless paid plan)
- Not for production

---

## Comparison Table

| Platform | Setup Time | Free Tier | Cold Start | Best For |
|----------|-----------|-----------|------------|----------|
| **Render** | 5 min | ✅ 750h/mo | 30-60s | Production |
| **Railway** | 3 min | ✅ 500h/mo | 10s | Fast deploy |
| **Fly.io** | 5 min | ✅ 3 apps | None | Performance |
| **Vercel** | 2 min | ✅ Unlimited | None | Serverless |
| **Ngrok** | 1 min | ✅ Limited | None | Demos |
| **PythonAnywhere** | 10 min | ✅ 1 app | None | Web-based |
| **Heroku** | 5 min | ❌ Trial only | 30s | Enterprise |

---

## Recommended Strategy

### For Hackathon Demo (Time-Sensitive):

**Option 1: Ngrok (Fastest)**
```bash
# Start backend
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload

# In another terminal
ngrok http 8000
```
→ **Ready in 2 minutes**

**Option 2: Railway (Best Free Tier)**
```bash
npm i -g @railway/cli
railway login
cd backend
railway up
```
→ **Ready in 5 minutes**

### For Production:

**Option 1: Render** (Already configured)  
**Option 2: Fly.io** (Better performance)  
**Option 3: Railway** (Simpler setup)

---

## Quick Decision Matrix

**Use Render if:**
- You want free tier
- You're okay with cold starts
- You have 5 minutes

**Use Railway if:**
- Render is failing
- You want faster builds
- You need simpler setup

**Use Ngrok if:**
- Demo is in <5 minutes
- You can't wait for deployment
- Backend works locally

**Use Vercel if:**
- Frontend already on Vercel
- You want everything together
- You're okay with serverless limits

---

## Emergency Demo Setup (2 Minutes)

If you need to demo **RIGHT NOW**:

```bash
# 1. Start local backend
cd backend
uvicorn app.main:app --reload

# 2. In new terminal, install ngrok
# Download from https://ngrok.com/download

# 3. Expose backend
ngrok http 8000

# 4. Copy ngrok URL (https://xxxx.ngrok.io)

# 5. Update frontend/js/api.js line 9:
BASE_URL: 'https://xxxx.ngrok.io/api',

# 6. Open frontend in browser
# It works!
```

---

## Files to Update for Each Platform

### Railway:
- Add `railway.json` (optional)
- No changes to code needed

### Fly.io:
- Update `fly.toml` (auto-generated)
- No changes to code needed

### Vercel:
- Add root `vercel.json`
- Update ASGI to WSGI (if needed)

### Ngrok:
- No changes needed
- Just update frontend API URL

---

## Environment Variables for All Platforms

```bash
ENVIRONMENT=production
DATABASE_URL=sqlite+aiosqlite:///./trendloom.db
SCHEDULER_ENABLED=False
DEBUG=False
CORS_ORIGINS=*
HOST=0.0.0.0
PORT=8000  # or $PORT for cloud platforms
```

---

## 🆘 Still Having Issues?

### Last Resort: Frontend-Only Demo

Make frontend work without backend:

1. **Mock API responses** in `frontend/js/api.js`
2. **Return sample data** for all endpoints
3. **Demo just the UI** with static data

This isn't ideal, but shows your UI/UX work.

---

## ✅ Best Recommendation

**For your hackathon:**

1. **Try Render first** (already configured)
2. **If failing, use Railway** (install CLI, `railway up`)
3. **If time-critical, use Ngrok** (instant)

**For production after hackathon:**

1. **Fly.io** (best performance)
2. **Railway** (best developer experience)
3. **Render** (most features on free tier)

---

## 📞 Support Commands

### Check what's running locally:
```bash
# Windows
netstat -ano | findstr :8000

# Check if backend is running
curl http://localhost:8000/health
```

### Kill process on port 8000:
```bash
# Windows PowerShell
$port = 8000
Get-NetTCPConnection -LocalPort $port | Stop-Process -Force
```

---

**Choose your path and let's get deployed!** 🚀
