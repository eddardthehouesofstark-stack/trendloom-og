# Fix Render Deployment

## What's Happening

Render keeps failing on the build step. Let's try alternative approaches:

---

## Option 1: Use Railway Instead (Recommended)

Railway handles Python dependencies better than Render.

### Quick Deploy:

```bash
# Install Railway CLI
npm i -g @railway/cli

# Login
railway login

# Deploy (from project root)
cd "d:\srcas hackathon 14 15"
railway init
railway up

# Set root directory in Railway dashboard to: backend
```

**Railway will:**
- Auto-detect Python
- Install dependencies correctly
- Deploy in ~3 minutes
- Give you a URL

---

## Option 2: Fix Render Configuration

The issue might be the root directory setting. Try:

### In Render Dashboard:

1. **Service Settings**
2. **Build & Deploy**
3. Change:
   - Root Directory: `backend`
   - Build Command: `pip install --upgrade pip && pip install -r requirements.txt`
   - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

4. **Environment Variables** - Add:
```
PYTHON_VERSION=3.11.0
PIP_NO_CACHE_DIR=1
```

5. **Manual Deploy** → Deploy latest commit

---

## Option 3: Even More Minimal Requirements

If still failing, try ultra-minimal:

### Edit `backend/requirements.txt`:

```
fastapi==0.109.0
uvicorn==0.27.0
sqlalchemy==2.0.25
aiosqlite==0.19.0
pillow==10.0.0
python-multipart==0.0.6
python-dotenv==1.0.1
httpx==0.26.0
requests==2.31.0
pydantic==2.5.3
pydantic-settings==2.1.0
```

(Remove `uvicorn[standard]` - use plain `uvicorn`)

---

## Option 4: Use Fly.io

Fly.io has better Python support:

```bash
# Install Fly CLI (PowerShell as Admin)
powershell -Command "iwr https://fly.io/install.ps1 -useb | iex"

# Login
fly auth login

# Deploy
cd "d:\srcas hackathon 14 15\backend"
fly launch --name trendloom-backend
fly deploy
```

---

## Option 5: Just Use Ngrok for Demo

Honestly, for a hackathon demo, ngrok is:
- ✅ Instant (2 minutes)
- ✅ Reliable
- ✅ No build issues
- ✅ Shows you can deploy to production later

See: `DEMO_NOW_NGROK.md`

---

## Recommended Path

1. **Right now:** Use ngrok to get demo working (2 min)
2. **Later:** Try Railway (better Python support)
3. **After hackathon:** Fix Render or use Fly.io for production

**Don't waste time on Render right now** - get the demo working with ngrok!
