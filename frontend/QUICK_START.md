# Frontend Integration - Quick Start

## 1. Start the Backend

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
copy .env.example .env

# Start server
python -m app.main
```

Backend will start on: **http://localhost:8000**

Verify it's running: http://localhost:8000/docs

## 2. Test Integration Example

Open in browser: `INTEGRATION_EXAMPLE.html`

This simple page shows:
- ✓ Live KPIs from backend
- ✓ Trending products
- ✓ Real-time search
- ✓ API connection status

If you see live data → Backend is connected! ✅

## 3. Add Scripts to Your Pages

Add these two lines before `</body>` in each HTML file:

```html
<!-- Add before closing </body> tag -->
<script src="js/api.js"></script>
<script src="js/dashboard.js"></script>  <!-- Change per page -->
</body>
</html>
```

### Script Mapping

| Page | Script to Use |
|------|---------------|
| dashboard.html | js/dashboard.js |
| explore.html | js/explore.js |
| seasonal.html | js/seasonal.js |
| regional.html | js/explore.js |
| competitor.html | js/explore.js |
| recommendation.html | js/recommendations.js |
| attributes.html | js/explore.js |

## 4. Add Data Attributes

Add data attributes to elements that should show live data:

### Example: Dashboard KPIs

```html
<!-- Before (static) -->
<span>78%</span>

<!-- After (dynamic) -->
<span data-kpi="market-coverage">78%</span>
```

### Common Data Attributes

```html
<!-- Dashboard -->
<span data-kpi="market-coverage">--</span>
<span data-kpi="trend-accuracy">--</span>
<span data-kpi="signal-strength">--</span>
<span data-kpi="active-signals">--</span>

<!-- Trending Products Container -->
<div data-trending-products>
    <!-- Cards here -->
</div>

<!-- Action Board Container -->
<div data-action-board>
    <!-- Action items here -->
</div>
```

## 5. Open Your Pages

Open any HTML file in browser. The JavaScript will:
1. Connect to backend
2. Fetch live data
3. Update the UI automatically

## 6. Check Console

Open browser console (F12) to see:
- "Loading dashboard data..."
- "Dashboard data loaded: {...}"
- Any errors

## Troubleshooting

### Backend Not Running?
```bash
# Check if backend is running
curl http://localhost:8000

# Or open in browser:
http://localhost:8000/docs
```

### CORS Error?
Update backend `.env`:
```env
ALLOWED_ORIGINS=http://localhost:5500,http://127.0.0.1:5500,file://
```

Then restart backend.

### No Data Showing?
1. Check browser console for errors
2. Verify backend has data (may take 5-10 min on first run)
3. Check data attributes are added to HTML elements

### Wrong API URL?
Edit `js/api.js`:
```javascript
const API_CONFIG = {
    BASE_URL: 'http://localhost:8000/api',  // Change if needed
    ...
};
```

## Testing API Directly

Open browser console and test:

```javascript
// Test connection
const data = await TrendLoomAPI.getDashboard();
console.log(data);

// Search products
const products = await TrendLoomAPI.searchProducts({ query: 'shirt' });
console.log(products);

// Get trending colors
const colors = await TrendLoomAPI.getTrendingColors();
console.log(colors);
```

## File Checklist

Make sure you have:
- ✓ `js/api.js` - API client
- ✓ `js/dashboard.js` - Dashboard logic
- ✓ `js/explore.js` - Explore page logic
- ✓ `js/seasonal.js` - Seasonal page logic
- ✓ `js/recommendations.js` - Recommendations logic

## What Happens Next?

1. Backend collects data automatically every 6 hours
2. Frontend fetches latest data on page load
3. Search and filters work in real-time
4. All mock data is replaced with live data

## Need Help?

- **Integration Guide**: Read `INTEGRATION_GUIDE.md` for detailed instructions
- **API Docs**: Visit http://localhost:8000/docs
- **Example Page**: Open `INTEGRATION_EXAMPLE.html` for a working demo

---

**That's it!** Your frontend now displays live fashion trend data! 🎉
