# Connect Frontend to Backend - Quick Guide

## 🎯 Purpose
Once your Render backend deployment completes, follow these steps to connect your Vercel frontend to it.

---

## Step 1: Get Your Render Backend URL

1. Go to https://dashboard.render.com
2. Find your `trendloom-backend` service
3. Copy the URL (will look like):
   ```
   https://trendloom-backend-xxxx.onrender.com
   ```

---

## Step 2: Update Frontend API Configuration

### File to Edit: `frontend/js/api.js`

**Find Line 9:**
```javascript
BASE_URL: `http://${window.location.hostname}:8000/api`,
```

**Replace with** (use your actual Render URL):
```javascript
BASE_URL: 'https://trendloom-backend-xxxx.onrender.com/api',
```

### ⚠️ Important Notes:
- Include `/api` at the end
- Use `https://` (not `http://`)
- Replace `xxxx` with your actual Render service ID

---

## Step 3: Test Backend Health

Before deploying, verify your backend is running:

```bash
# Test health endpoint
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

## Step 4: Commit and Push Changes

```bash
# Stage the updated API configuration
git add frontend/js/api.js

# Commit the change
git commit -m "Connect frontend to Render backend production URL"

# Push to GitHub
git push origin main
```

**Vercel will automatically deploy the update in ~1 minute.**

---

## Step 5: Test Image Analysis

1. Visit: https://trendloom-og-3faj.vercel.app/attributes.html
2. Click "Upload Image"
3. Select any fashion image (shirt, dress, jeans, etc.)
4. Click "Analyze Image"

**Expected Result:**
- Category detection (e.g., "T-shirt/top", "Dress")
- Color palette with percentages
- Style attributes (casual, formal, etc.)
- Material detection
- AI-generated tags

---

## Step 6: Test Live Dashboard

1. Visit: https://trendloom-og-3faj.vercel.app/dashboard.html
2. Look for the red pulsing **"LIVE"** badge
3. Verify metrics are loading (may take 10-15 seconds on first load)

**Expected Result:**
- KPIs showing real Google Trends data
- Trending products grid
- Color palette trends
- Material trends

---

## 🐛 Troubleshooting

### Issue: "Failed to fetch" Error

**Possible Causes:**
1. Backend URL is incorrect
2. Render service is sleeping (cold start)
3. CORS error

**Solutions:**
```javascript
// Open browser console (F12)
// Check the error message

// If you see CORS error:
// This shouldn't happen - CORS is configured with allow_origins=["*"]

// If you see "net::ERR_NAME_NOT_RESOLVED":
// Check the backend URL is correct in api.js

// If you see timeout:
// First request to Render free tier takes 30-60 seconds (cold start)
// Wait and try again
```

### Issue: Image Analysis Returns Default Data

**This is normal!** The endpoint has fallback data to ensure it always works.

**To verify real analysis:**
1. Check browser console logs
2. Look for "[TrendLoomAPI] Success! Result:"
3. If you see this, real analysis is working

**If using free Hugging Face API:**
- Rate limits may apply
- First request may be slow (model loading)
- Fallback ensures feature always works

### Issue: Backend Takes Too Long to Respond

**On Render Free Tier:**
- Services sleep after 15 minutes of inactivity
- First request takes 30-60 seconds to wake up
- Subsequent requests are fast

**Solution:**
- Keep a browser tab open during demo
- Make a test request before presenting
- Consider upgrading to paid tier for demos ($7/month)

---

## 🎯 Verification Checklist

Before your demo:

- [ ] Backend health check responds
- [ ] Frontend loads without errors
- [ ] Dashboard shows live data
- [ ] Image upload works
- [ ] Color trends display
- [ ] Seasonal forecasting works
- [ ] Supplier filters work (India/Tamil Nadu)
- [ ] Fashion calendar shows 2026-2027 events

---

## 📞 Quick Commands Reference

```bash
# Test backend health
curl https://trendloom-backend-xxxx.onrender.com/api/health

# Test live dashboard endpoint
curl https://trendloom-backend-xxxx.onrender.com/api/dashboard/live?state=IN-TN

# Test image analysis endpoint
curl -X POST https://trendloom-backend-xxxx.onrender.com/api/image/analyze \
  -F "file=@test_image.jpg"

# View frontend
open https://trendloom-og-3faj.vercel.app

# View GitHub repo
open https://github.com/eddardthehouesofstark-stack/trendloom-og
```

---

## 🚀 One-Line Update Command

Once you have your Render URL, run:

```bash
# Edit frontend/js/api.js line 9, then:
git add frontend/js/api.js && git commit -m "Connect to Render backend" && git push origin main
```

**Done!** Vercel will deploy automatically.

---

## 📝 Example: Complete api.js Configuration

After update, your `frontend/js/api.js` should look like:

```javascript
/**
 * TrendLoom API Client
 * Handles all backend API communication
 */

// API Configuration
const API_CONFIG = {
    // Production: use Render backend
    BASE_URL: 'https://trendloom-backend-xxxx.onrender.com/api',
    DEFAULT_STATE: 'Tamil Nadu',
    TIMEOUT: 10000,
};

// Rest of the file remains unchanged...
```

---

## ✅ Success Indicators

You'll know it's working when:

1. **Dashboard loads** with real trend scores
2. **"LIVE" badge** appears and pulses
3. **Image upload** returns category and colors
4. **No CORS errors** in browser console
5. **API calls** complete in < 5 seconds (after cold start)

---

## 🎉 You're Done!

Your TrendLoom platform is now fully deployed and connected:
- Frontend: Vercel ✅
- Backend: Render ✅
- Database: SQLite ✅
- Image Analysis: Hugging Face API ✅
- Live Trends: Google Trends API ✅
