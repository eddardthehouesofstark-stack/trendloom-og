/**
 * Dashboard Page Logic
 * Loads and displays LIVE dashboard data from Google Trends + backend
 */

// Dashboard data loader
async function loadDashboardData() {
    try {
        console.log('Loading LIVE dashboard data...');
        
        // Show loading state
        showLoadingStates();
        
        // Fetch LIVE dashboard data from API (Google Trends + Database)
        const data = await TrendLoomAPI.getLiveDashboard('IN-TN');
        
        console.log('LIVE Dashboard data loaded:', data);
        console.log('Data source:', data.data_source);
        console.log('Data freshness:', data.data_freshness);
        
        // Update all dashboard sections with live data
        updateKPIs(data);
        updateLiveTrendsIndicator(data);
        updateTrendingProducts(data.trending_products);
        updateActionBoard(data.action_items);
        updateTrendingCategories(data.trending_categories);
        
    } catch (error) {
        console.error('Error loading dashboard:', error);
        console.log('Falling back to database-only data...');
        
        // Fallback to regular dashboard if live fails
        try {
            const fallbackData = await TrendLoomAPI.getDashboard();
            updateKPIs(fallbackData);
            updateTrendingProducts(fallbackData.trending_products);
            updateActionBoard(fallbackData.action_items);
        } catch (fallbackError) {
            showErrorStates();
        }
    }
}

// Update live trends indicator
function updateLiveTrendsIndicator(data) {
    // Add "LIVE" badge near title if we have live data
    if (data.data_freshness === 'live' && data.live_trends) {
        const heroTitle = document.querySelector('h2.font-display-lg');
        if (heroTitle && !document.querySelector('[data-live-indicator]')) {
            const liveBadge = document.createElement('span');
            liveBadge.setAttribute('data-live-indicator', 'true');
            liveBadge.className = 'inline-flex items-center gap-1 bg-red-500 text-white text-xs px-2 py-1 rounded-full ml-3 animate-pulse';
            liveBadge.innerHTML = '<span class="w-2 h-2 bg-white rounded-full"></span> LIVE DATA';
            heroTitle.appendChild(liveBadge);
        }
        
        console.log('Live Google Trends data available:', Object.keys(data.live_trends).length, 'keywords');
        
        // Log some live trend data
        if (data.trending_searches && data.trending_searches.length > 0) {
            console.log('Trending searches:', data.trending_searches.slice(0, 5));
        }
    }
}

// Show loading states
function showLoadingStates() {
    // KPIs will show default values until loaded
    console.log('Showing loading states...');
}

// Show error states
function showErrorStates() {
    document.querySelectorAll('[data-api-content]').forEach(el => {
        el.innerHTML = '<p class="text-red-500 text-sm">Failed to load data</p>';
    });
}

// Update KPI cards
function updateKPIs(data) {
    // Market Coverage
    const marketCoverageEl = document.querySelector('[data-kpi="market-coverage"]');
    if (marketCoverageEl) {
        marketCoverageEl.textContent = `${data.market_coverage}%`;
    }
    
    // Trend Accuracy
    const trendAccuracyEl = document.querySelector('[data-kpi="trend-accuracy"]');
    if (trendAccuracyEl) {
        trendAccuracyEl.textContent = `${data.trend_accuracy}%`;
    }
    
    // Signal Strength
    const signalStrengthEl = document.querySelector('[data-kpi="signal-strength"]');
    if (signalStrengthEl) {
        signalStrengthEl.textContent = data.signal_strength;
    }
    
    // Active Signals
    const activeSignalsEl = document.querySelector('[data-kpi="active-signals"]');
    if (activeSignalsEl) {
        activeSignalsEl.textContent = data.active_signals;
    }
}

// Update trending products section
function updateTrendingProducts(products) {
    if (!products || products.length === 0) return;
    
    console.log('Updating trending products:', products.length);
    
    // Find the trending products container
    const container = document.querySelector('[data-trending-products]');
    if (!container) {
        console.warn('Trending products container not found');
        return;
    }
    
    // Keep the first 2 cards (they have custom styling), update the rest
    const existingCards = container.querySelectorAll('.group');
    
    products.slice(0, 2).forEach((product, index) => {
        if (existingCards[index]) {
            const card = existingCards[index];
            
            // Update image
            const img = card.querySelector('img');
            if (img && product.image_url) {
                img.src = product.image_url;
                img.alt = product.name;
            }
            
            // Update badge
            const badge = card.querySelector('[class*="bg-brand"]');
            if (badge) {
                badge.textContent = product.recommendation || 'TRENDING';
                badge.className = `${ApiUtils.getRecommendationClass(product.recommendation)} font-bold text-[10px] px-2 py-1 rounded-sm tracking-wider mb-2 inline-block`;
            }
            
            // Update title
            const title = card.querySelector('h4');
            if (title) {
                title.textContent = product.name;
            }
        }
    });
    
    console.log('Trending products updated');
}

// Update action board
function updateActionBoard(actionItems) {
    if (!actionItems || actionItems.length === 0) return;
    
    console.log('Updating action board:', actionItems.length);
    
    // Find action board container
    const container = document.querySelector('[data-action-board]');
    if (!container) {
        console.warn('Action board container not found');
        return;
    }
    
    // Get existing action cards
    const existingCards = container.querySelectorAll('[class*="bg-surface"]');
    
    // Update up to 3 cards (PRODUCE, WAIT, AVOID)
    const produceItems = actionItems.filter(item => item.status === 'produce').slice(0, 1);
    const waitItems = actionItems.filter(item => item.status === 'wait').slice(0, 1);
    const avoidItems = actionItems.filter(item => item.status === 'avoid').slice(0, 1);
    
    const itemsToShow = [...produceItems, ...waitItems, ...avoidItems];
    
    itemsToShow.forEach((item, index) => {
        if (existingCards[index]) {
            const card = existingCards[index];
            
            // Update badge
            const badge = card.querySelector('span[class*="bg-"]');
            if (badge) {
                badge.textContent = item.action;
            }
            
            // Update certainty
            const certainty = card.querySelector('.font-label-sm');
            if (certainty) {
                certainty.textContent = item.certainty;
            }
            
            // Update title
            const title = card.querySelector('h4');
            if (title) {
                title.textContent = item.product_name;
            }
            
            // Update momentum score
            const progressBar = card.querySelector('[class*="w-["]');
            if (progressBar) {
                progressBar.style.width = `${item.momentum_score}%`;
            }
        }
    });
    
    console.log('Action board updated');
}

// Update trending categories
function updateTrendingCategories(categories) {
    if (!categories || categories.length === 0) return;
    
    console.log('Updating trending categories:', categories.length);
    
    // This would update a categories section if it exists
    // Implementation depends on your exact HTML structure
}

// Initialize dashboard when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', loadDashboardData);
} else {
    loadDashboardData();
}

// Refresh dashboard data every 5 minutes
setInterval(loadDashboardData, 5 * 60 * 1000);
