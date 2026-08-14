# Frontend Integration Guide

Complete guide to integrate TrendLoom backend with your HTML/JavaScript frontend.

## Quick Start

### 1. Configure API Base URL

Add this to your JavaScript files:

```javascript
const API_BASE_URL = 'http://localhost:8000/api';
```

### 2. Basic Fetch Example

```javascript
async function fetchDashboard() {
    try {
        const response = await fetch(`${API_BASE_URL}/dashboard`);
        const data = await response.json();
        console.log(data);
        return data;
    } catch (error) {
        console.error('Error fetching dashboard:', error);
    }
}
```

## API Endpoints for Each Frontend Page

### Dashboard Page (`dashboard.html`)

```javascript
// Get complete dashboard data
async function loadDashboard() {
    const data = await fetch(`${API_BASE_URL}/dashboard?state=Tamil Nadu`)
        .then(res => res.json());
    
    // Update KPIs
    document.getElementById('market-coverage').textContent = `${data.market_coverage}%`;
    document.getElementById('trend-accuracy').textContent = `${data.trend_accuracy}%`;
    document.getElementById('signal-strength').textContent = data.signal_strength;
    document.getElementById('active-signals').textContent = data.active_signals;
    
    // Update trending products
    displayTrendingProducts(data.trending_products);
    
    // Update action board
    displayActionItems(data.action_items);
    
    return data;
}

// Helper to display trending products
function displayTrendingProducts(products) {
    const container = document.getElementById('trending-products-grid');
    container.innerHTML = '';
    
    products.forEach(product => {
        const card = `
            <div class="product-card">
                <img src="${product.image_url}" alt="${product.name}">
                <h3>${product.name}</h3>
                <p class="category">${product.category}</p>
                <div class="trend-score">Score: ${product.trend_score}</div>
                <div class="growth">Growth: ${product.weekly_growth}%</div>
                <span class="badge ${product.recommendation.toLowerCase()}">${product.recommendation}</span>
            </div>
        `;
        container.innerHTML += card;
    });
}
```

### Explore Trends Page (`explore.html`)

```javascript
// Get trending products with filters
async function loadTrendingProducts(category = null, limit = 20) {
    let url = `${API_BASE_URL}/trending/products?limit=${limit}`;
    if (category) {
        url += `&category=${category}`;
    }
    
    const products = await fetch(url).then(res => res.json());
    displayProducts(products);
}

// Get trending categories
async function loadTrendingCategories() {
    const data = await fetch(`${API_BASE_URL}/trending/categories`)
        .then(res => res.json());
    
    displayCategories(data.categories);
}

// Search products
async function searchProducts(query) {
    const url = `${API_BASE_URL}/search?q=${encodeURIComponent(query)}`;
    const products = await fetch(url).then(res => res.json());
    displayProducts(products);
}

// Autocomplete
async function getAutocompleteSuggestions(query) {
    if (query.length < 2) return [];
    
    const data = await fetch(`${API_BASE_URL}/search/autocomplete?q=${encodeURIComponent(query)}`)
        .then(res => res.json());
    
    return data.suggestions;
}
```

### Seasonal Intelligence Page (`seasonal.html`)

```javascript
// Get seasonal trends
async function loadSeasonalTrends() {
    const data = await fetch(`${API_BASE_URL}/demand/seasonal`)
        .then(res => res.json());
    
    // Update season info
    document.getElementById('current-season').textContent = data.season;
    document.getElementById('season-confidence').textContent = `${(data.confidence * 100).toFixed(0)}%`;
    
    // Display top colors
    displaySeasonalColors(data.top_colors);
    
    // Display top materials
    displaySeasonalMaterials(data.top_materials);
    
    // Display top categories
    displaySeasonalCategories(data.top_categories);
    
    return data;
}

// Display seasonal colors
function displaySeasonalColors(colors) {
    const container = document.getElementById('seasonal-colors');
    container.innerHTML = '';
    
    colors.forEach(color => {
        const colorCard = `
            <div class="color-card">
                <div class="color-swatch" style="background: ${color.hex || '#ccc'}"></div>
                <h4>${color.name}</h4>
                <p>Score: ${color.score}</p>
                <p>Growth: ${color.growth}%</p>
            </div>
        `;
        container.innerHTML += colorCard;
    });
}
```

### Regional Demand Page (`regional.html`)

```javascript
// Get regional insights (currently Tamil Nadu)
async function loadRegionalData(state = 'Tamil Nadu') {
    // Get trending by region
    const products = await fetch(`${API_BASE_URL}/trending/products?state=${state}`)
        .then(res => res.json());
    
    // Get categories by region
    const categories = await fetch(`${API_BASE_URL}/trending/categories?state=${state}`)
        .then(res => res.json());
    
    displayRegionalProducts(products);
    displayRegionalCategories(categories.categories);
}
```

### Competitor Trends Page (`competitor.html`)

```javascript
// Get trending styles (competitor insights)
async function loadCompetitorTrends() {
    const data = await fetch(`${API_BASE_URL}/trending/styles`)
        .then(res => res.json());
    
    displayStyleTrends(data.styles);
}

// Get trending keywords
async function loadTrendingKeywords() {
    const data = await fetch(`${API_BASE_URL}/trending/keywords?limit=20`)
        .then(res => res.json());
    
    displayKeywordTrends(data.keywords);
}

function displayStyleTrends(styles) {
    const container = document.getElementById('style-trends');
    container.innerHTML = '';
    
    styles.forEach(style => {
        const card = `
            <div class="style-card">
                <h3>${style.style}</h3>
                <p>Products: ${style.product_count}</p>
                <p>Trend Score: ${style.avg_trend_score}</p>
                <p>Growth: ${style.avg_growth}%</p>
                <span class="momentum ${style.momentum}">${style.momentum}</span>
            </div>
        `;
        container.innerHTML += card;
    });
}
```

### Recommendations Page (`recommendation.html`)

```javascript
// Get recommendations
async function loadRecommendations(category = null, style = null) {
    let url = `${API_BASE_URL}/recommendations?limit=20`;
    if (category) url += `&category=${category}`;
    if (style) url += `&style=${style}`;
    
    const recommendations = await fetch(url).then(res => res.json());
    displayRecommendations(recommendations);
}

// Analyze uploaded image
async function analyzeImage(file) {
    const formData = new FormData();
    formData.append('file', file);
    
    const response = await fetch(`${API_BASE_URL}/image/analyze`, {
        method: 'POST',
        body: formData
    });
    
    const analysis = await response.json();
    
    // Display analysis results
    displayImageAnalysis(analysis);
    
    // Display similar products
    displaySimilarProducts(analysis.similar_products);
    
    // Display recommendations
    displayRecommendations(analysis.recommendations);
}

// Image upload handler
document.getElementById('image-upload').addEventListener('change', async (e) => {
    const file = e.target.files[0];
    if (file) {
        await analyzeImage(file);
    }
});
```

### Attributes Page (`attributes.html`)

```javascript
// Get color trends
async function loadColorTrends() {
    const colors = await fetch(`${API_BASE_URL}/trending/colors?limit=20`)
        .then(res => res.json());
    
    displayColorTrends(colors);
}

// Get material trends
async function loadMaterialTrends() {
    const materials = await fetch(`${API_BASE_URL}/trending/materials?limit=20`)
        .then(res => res.json());
    
    displayMaterialTrends(materials);
}

function displayColorTrends(colors) {
    const container = document.getElementById('color-trends');
    container.innerHTML = '';
    
    colors.forEach(color => {
        const card = `
            <div class="color-trend-card">
                <div class="color-swatch" style="background: ${color.hex_code}"></div>
                <h3>${color.color_name}</h3>
                <p>Popularity: ${color.popularity.toFixed(1)}</p>
                <p>Weekly Growth: ${color.weekly_growth.toFixed(1)}%</p>
                <p>Products: ${color.product_count}</p>
            </div>
        `;
        container.innerHTML += card;
    });
}

function displayMaterialTrends(materials) {
    const container = document.getElementById('material-trends');
    container.innerHTML = '';
    
    materials.forEach(material => {
        const card = `
            <div class="material-trend-card">
                <h3>${material.material_name}</h3>
                <p>Popularity: ${material.popularity.toFixed(1)}</p>
                <p>Weekly Growth: ${material.weekly_growth.toFixed(1)}%</p>
                <p>Products: ${material.product_count}</p>
            </div>
        `;
        container.innerHTML += card;
    });
}
```

## Advanced Features

### Demand Prediction with Chart

```javascript
// Get demand prediction for a category
async function loadDemandForecast(category, days = 30) {
    const forecast = await fetch(
        `${API_BASE_URL}/demand/forecast/${category}?days=${days}`
    ).then(res => res.json());
    
    // Use forecast.prediction_graph_data for charting
    renderForecastChart(forecast.prediction_graph_data);
    
    // Display metrics
    document.getElementById('predicted-demand').textContent = 
        forecast.predicted_demand_score.toFixed(1);
    document.getElementById('growth-percentage').textContent = 
        `${forecast.growth_percentage.toFixed(1)}%`;
    document.getElementById('confidence').textContent = 
        `${(forecast.confidence * 100).toFixed(0)}%`;
}

// Render chart using Chart.js or similar
function renderForecastChart(graphData) {
    const labels = graphData.map(d => new Date(d.date).toLocaleDateString());
    const values = graphData.map(d => d.value);
    const lowerBounds = graphData.map(d => d.lower_bound);
    const upperBounds = graphData.map(d => d.upper_bound);
    
    // Use your preferred charting library
    // Chart.js, D3.js, Plotly, etc.
}
```

### Analytics Dashboard

```javascript
// Get weekly analytics
async function loadWeeklyAnalytics() {
    const analytics = await fetch(`${API_BASE_URL}/analytics/weekly`)
        .then(res => res.json());
    
    displayWeeklyStats(analytics);
}

// Get monthly analytics
async function loadMonthlyAnalytics(month, year) {
    const url = `${API_BASE_URL}/analytics/monthly?month=${month}&year=${year}`;
    const analytics = await fetch(url).then(res => res.json());
    
    displayMonthlyStats(analytics);
}
```

### Real-time Search

```javascript
// Implement real-time search with debouncing
let searchTimeout;

function handleSearchInput(query) {
    clearTimeout(searchTimeout);
    
    searchTimeout = setTimeout(async () => {
        if (query.length < 2) return;
        
        // Get autocomplete suggestions
        const suggestions = await getAutocompleteSuggestions(query);
        displaySuggestions(suggestions);
        
        // Perform search
        const results = await searchProducts(query);
        displaySearchResults(results);
    }, 300); // 300ms debounce
}

document.getElementById('search-input').addEventListener('input', (e) => {
    handleSearchInput(e.target.value);
});
```

### Advanced Filtering

```javascript
// Get available filters
async function loadFilterOptions() {
    const filters = await fetch(`${API_BASE_URL}/search/filters`)
        .then(res => res.json());
    
    // Populate filter dropdowns
    populateDropdown('category-filter', filters.categories);
    populateDropdown('color-filter', filters.colors);
    populateDropdown('material-filter', filters.materials);
    populateDropdown('style-filter', filters.styles);
    
    // Set price range
    setPriceRange(filters.price_range.min, filters.price_range.max);
}

// Search with filters
async function searchWithFilters() {
    const params = new URLSearchParams({
        q: document.getElementById('search-input').value,
        category: document.getElementById('category-filter').value,
        color: document.getElementById('color-filter').value,
        material: document.getElementById('material-filter').value,
        min_price: document.getElementById('min-price').value,
        max_price: document.getElementById('max-price').value,
    });
    
    const results = await fetch(`${API_BASE_URL}/search?${params}`)
        .then(res => res.json());
    
    displaySearchResults(results);
}
```

## Error Handling

```javascript
// Robust error handling
async function safeApiFetch(url, options = {}) {
    try {
        const response = await fetch(url, options);
        
        if (!response.ok) {
            throw new Error(`API Error: ${response.status} ${response.statusText}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('API Fetch Error:', error);
        
        // Show user-friendly error message
        showErrorNotification('Unable to load data. Please try again.');
        
        return null;
    }
}

// Usage
const data = await safeApiFetch(`${API_BASE_URL}/dashboard`);
if (data) {
    displayDashboard(data);
}
```

## Loading States

```javascript
// Show loading spinner
function showLoading(containerId) {
    document.getElementById(containerId).innerHTML = `
        <div class="loading-spinner">
            <div class="spinner"></div>
            <p>Loading data...</p>
        </div>
    `;
}

// Hide loading spinner
function hideLoading(containerId) {
    const loader = document.querySelector(`#${containerId} .loading-spinner`);
    if (loader) loader.remove();
}

// Usage
async function loadDashboardWithLoading() {
    showLoading('dashboard-container');
    
    const data = await fetch(`${API_BASE_URL}/dashboard`).then(res => res.json());
    
    hideLoading('dashboard-container');
    displayDashboard(data);
}
```

## Caching Strategy

```javascript
// Simple in-memory cache
const cache = new Map();
const CACHE_DURATION = 5 * 60 * 1000; // 5 minutes

async function fetchWithCache(url) {
    const cached = cache.get(url);
    
    if (cached && Date.now() - cached.timestamp < CACHE_DURATION) {
        return cached.data;
    }
    
    const data = await fetch(url).then(res => res.json());
    
    cache.set(url, {
        data,
        timestamp: Date.now()
    });
    
    return data;
}

// Clear cache when needed
function clearCache() {
    cache.clear();
}
```

## CORS Configuration

If you encounter CORS issues, make sure your backend `.env` includes your frontend URL:

```env
ALLOWED_ORIGINS=http://localhost:5500,http://127.0.0.1:5500,http://localhost:3000
```

## Testing the Integration

```javascript
// Test all major endpoints
async function testBackendConnection() {
    const tests = [
        { name: 'Dashboard', url: `${API_BASE_URL}/dashboard` },
        { name: 'Trending Products', url: `${API_BASE_URL}/trending/products` },
        { name: 'Search', url: `${API_BASE_URL}/search?q=shirt` },
        { name: 'Recommendations', url: `${API_BASE_URL}/recommendations` },
    ];
    
    console.log('Testing backend connection...');
    
    for (const test of tests) {
        try {
            const response = await fetch(test.url);
            const data = await response.json();
            console.log(`✓ ${test.name}: OK`, data);
        } catch (error) {
            console.error(`✗ ${test.name}: FAILED`, error);
        }
    }
}

// Run tests
testBackendConnection();
```

## Complete Integration Example

```html
<!DOCTYPE html>
<html>
<head>
    <title>TrendLoom Dashboard</title>
</head>
<body>
    <div id="dashboard">
        <div class="kpis">
            <div class="kpi">
                <h3>Market Coverage</h3>
                <p id="market-coverage">--</p>
            </div>
            <div class="kpi">
                <h3>Trend Accuracy</h3>
                <p id="trend-accuracy">--</p>
            </div>
        </div>
        
        <div id="trending-products"></div>
    </div>

    <script>
        const API_BASE_URL = 'http://localhost:8000/api';

        async function loadDashboard() {
            try {
                const response = await fetch(`${API_BASE_URL}/dashboard`);
                const data = await response.json();
                
                // Update KPIs
                document.getElementById('market-coverage').textContent = 
                    `${data.market_coverage}%`;
                document.getElementById('trend-accuracy').textContent = 
                    `${data.trend_accuracy}%`;
                
                // Display products
                const container = document.getElementById('trending-products');
                data.trending_products.forEach(product => {
                    const card = document.createElement('div');
                    card.className = 'product-card';
                    card.innerHTML = `
                        <img src="${product.image_url}" alt="${product.name}">
                        <h3>${product.name}</h3>
                        <p>${product.category}</p>
                        <span class="score">${product.trend_score}</span>
                    `;
                    container.appendChild(card);
                });
            } catch (error) {
                console.error('Error loading dashboard:', error);
            }
        }

        // Load on page load
        document.addEventListener('DOMContentLoaded', loadDashboard);
    </script>
</body>
</html>
```

---

This guide covers all the main integration points. All endpoints return JSON that can be directly used in your frontend!
