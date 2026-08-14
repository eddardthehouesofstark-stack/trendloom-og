# Frontend-Backend Integration Guide

## Quick Integration Steps

### 1. Add API Scripts to Each HTML File

Add these two script tags before the closing `</body>` tag in each HTML file:

```html
<!-- Before closing </body> tag -->
<script src="js/api.js"></script>
<script src="js/[page-name].js"></script>
</body>
</html>
```

For each page:
- **dashboard.html**: Use `js/dashboard.js`
- **explore.html**: Use `js/explore.js`
- **seasonal.html**: Use `js/seasonal.js`
- **regional.html**: Use `js/explore.js` (reuse)
- **competitor.html**: Use `js/explore.js` (reuse)
- **recommendation.html**: Use `js/recommendations.js`
- **attributes.html**: Use `js/explore.js` (reuse)

### 2. Add Data Attributes to HTML Elements

Add data attributes to elements that should display live data:

#### Dashboard.html
```html
<!-- KPI Cards -->
<span data-kpi="market-coverage">--</span>
<span data-kpi="trend-accuracy">--</span>
<span data-kpi="signal-strength">--</span>
<span data-kpi="active-signals">--</span>

<!-- Trending Products Container -->
<div data-trending-products>
    <!-- Product cards here -->
</div>

<!-- Action Board Container -->
<div data-action-board>
    <!-- Action items here -->
</div>
```

#### Explore.html
```html
<!-- Products Grid -->
<div data-products-grid>
    <!-- Product cards here -->
</div>

<!-- Search Input -->
<input id="search-input" type="text" placeholder="Search...">
```

#### Seasonal.html
```html
<!-- Season Info -->
<span data-season>--</span>
<span data-season-confidence>--</span>

<!-- Seasonal Colors -->
<div data-seasonal-colors>
    <!-- Color cards here -->
</div>

<!-- Seasonal Materials -->
<div data-seasonal-materials>
    <!-- Material cards here -->
</div>
```

#### Recommendations.html
```html
<!-- File Upload -->
<input id="image-upload" type="file" accept="image/*">

<!-- Analysis Results -->
<div id="analysis-results"></div>

<!-- Recommendations Grid -->
<div data-recommendations-grid>
    <!-- Recommendation cards here -->
</div>
```

### 3. Start Backend Server

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python -m app.main
```

Backend will run on http://localhost:8000

### 4. Open Frontend

Open any HTML file in your browser. The JavaScript will automatically:
- Connect to the backend API
- Fetch live data
- Update the UI

### 5. Verify Integration

1. Open browser console (F12)
2. Look for console logs:
   - "Loading dashboard data..."
   - "Dashboard data loaded: {...}"
3. Check for errors

## API Configuration

If your backend runs on a different URL, update `js/api.js`:

```javascript
const API_CONFIG = {
    BASE_URL: 'http://your-backend-url:8000/api',
    DEFAULT_STATE: 'Tamil Nadu',
    TIMEOUT: 10000,
};
```

## Testing Integration

### Test Dashboard
1. Open dashboard.html
2. Check console for "Loading dashboard data..."
3. Verify KPIs are updated from --% to real values

### Test Search
1. Open explore.html
2. Type in search box
3. See results update in real-time

### Test Image Upload
1. Open recommendation.html
2. Click upload button
3. Select an image
4. See analysis results appear

## Common Issues

### CORS Error
**Problem**: "CORS policy: No 'Access-Control-Allow-Origin'"

**Solution**: Make sure backend `.env` includes your frontend URL:
```env
ALLOWED_ORIGINS=http://localhost:5500,http://127.0.0.1:5500,file://
```

### Connection Refused
**Problem**: "Failed to fetch" or "net::ERR_CONNECTION_REFUSED"

**Solution**: 
1. Check backend is running: http://localhost:8000
2. Verify API_BASE_URL in js/api.js matches backend URL

### No Data Showing
**Problem**: Page loads but shows no data

**Solution**:
1. Check browser console for errors
2. Verify data attributes are added to HTML elements
3. Check backend has collected data (may take 5-10 minutes on first run)

### 404 Errors
**Problem**: "404 Not Found" for API endpoints

**Solution**:
1. Verify backend is running on correct port
2. Check endpoint URLs in browser: http://localhost:8000/docs
3. Ensure API_BASE_URL doesn't have extra slashes

## Data Attributes Reference

### Dashboard
- `data-kpi="market-coverage"` - Market coverage percentage
- `data-kpi="trend-accuracy"` - Trend accuracy percentage
- `data-kpi="signal-strength"` - Signal strength (High/Medium/Low)
- `data-kpi="active-signals"` - Active signals count
- `data-trending-products` - Container for trending products
- `data-action-board` - Container for action items

### Explore/Regional/Competitor
- `data-products-grid` - Container for product grid
- `#search-input` - Search input field
- `#category-filter` - Category dropdown
- `#color-filter` - Color dropdown
- `#material-filter` - Material dropdown

### Seasonal
- `data-season` - Current season name
- `data-season-confidence` - Season confidence
- `data-seasonal-colors` - Seasonal colors container
- `data-seasonal-materials` - Seasonal materials container
- `data-seasonal-categories` - Seasonal categories container

### Recommendations
- `#image-upload` - File input for image upload
- `#analysis-results` - Image analysis results container
- `data-recommendations-grid` - Recommendations grid
- `data-similar-products` - Similar products container

### Attributes
- `data-colors-grid` - Color trends container
- `data-materials-grid` - Material trends container

## Manual API Calls

You can also make manual API calls from browser console:

```javascript
// Get dashboard data
const data = await TrendLoomAPI.getDashboard();
console.log(data);

// Search products
const products = await TrendLoomAPI.searchProducts({ query: 'shirt' });
console.log(products);

// Get trending colors
const colors = await TrendLoomAPI.getTrendingColors();
console.log(colors);

// Get seasonal predictions
const seasonal = await TrendLoomAPI.getSeasonalPredictions();
console.log(seasonal);
```

## Next Steps

1. **Add more data attributes** to elements you want to populate with live data
2. **Customize styling** of dynamically loaded content
3. **Add loading states** with spinners or skeletons
4. **Handle empty states** when no data is available
5. **Add error boundaries** for better error handling

## Support

- Backend API Docs: http://localhost:8000/docs
- Check console logs for debugging
- Verify backend logs in `backend/logs/trendloom.log`

---

**Integration Complete!** Your frontend now displays live fashion trend data from the backend.
