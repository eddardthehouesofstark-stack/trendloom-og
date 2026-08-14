# 🚀 GET DEMO WORKING RIGHT NOW - Use Ngrok

Render keeps failing, so let's use **Ngrok** to get your demo working in **2 minutes**.

## ⚡ INSTANT SOLUTION

### Step 1: Start Backend Locally (1 minute)

Open a terminal and run:

```bash
cd "d:\srcas hackathon 14 15\backend"

# If you don't have venv yet:
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# Start backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Wait for:** "Application startup complete"

### Step 2: Install and Run Ngrok (1 minute)

1. **Download Ngrok:**
   - Go to: https://ngrok.com/download
   - Download Windows version
   - Extract `ngrok.exe` somewhere

2. **Run Ngrok** (new terminal):
```bash
# Navigate to where you extracted ngrok.exe
cd path\to\ngrok

# Expose your local backend
ngrok http 8000
```

3. **Copy the URL** that appears:
```
Forwarding: https://abcd-1234-5678.ngrok-free.app -> http://localhost:8000
```

Copy the `https://abcd-1234-5678.ngrok-free.app` URL

### Step 3: Update Frontend (30 seconds)

1. Open: `d:\srcas hackathon 14 15\frontend\js\api.js`

2. Find line 9 (BASE_URL)

3. Change to your ngrok URL:
```javascript
BASE_URL: 'https://abcd-1234-5678.ngrok-free.app/api',
```

4. Save the file

### Step 4: Push to Vercel (30 seconds)

```bash
cd "d:\srcas hackathon 14 15"
git add frontend/js/api.js
git commit -m "Connect to ngrok backend for demo"
git push origin main
```

**Vercel auto-deploys in ~1 minute**

---

## ✅ DONE!

Your demo is now live at:
```
https://trendloom-og-3faj.vercel.app
```

With backend running through ngrok on your laptop!

---

## 📝 IMPORTANT NOTES

### Keep Terminal Open:
- **Terminal 1:** Backend must stay running
- **Terminal 2:** Ngrok must stay running
- Close either = demo stops working

### Before Demo:
- Start backend: `uvicorn app.main:app --reload --host 0.0.0.0 --port 8000`
- Start ngrok: `ngrok http 8000`
- Wait 30 seconds for Vercel to deploy
- Test image upload

### Ngrok Free Tier:
- URL changes each time you restart ngrok
- Need to update frontend and redeploy each time
- Max 1 hour sessions (restart if needed)

---

## 🎯 FOR PRODUCTION LATER

Once demo is done, we'll fix Render properly. For now, this works!

---

## 🆘 IF BACKEND WON'T START

Check if requirements installed:
```bash
cd backend
pip install fastapi uvicorn sqlalchemy aiosqlite pillow python-multipart python-dotenv httpx requests
```

Then start again:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
