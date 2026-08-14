/**
 * Explore Trends Page Logic
 */

let currentFilters = {
    category: null,
    color: null,
    material: null,
    style: null
};

// Load trending products
async function loadTrendingProducts(filters = {}) {
    try {
        console.log('Loading trending products with filters:', filters);
        
        const products = await TrendLoomAPI.getTrendingProducts({
            ...currentFilters,
            ...filters,
            limit: 20
        });
        
        displayProducts(products);
    } catch (error) {
        console.error('Error loading trending products:', error);
        ApiUtils.showError('products-container', 'Failed to load products');
    }
}

// Display products
function displayProducts(products) {
    const container = document.querySelector('[data-products-grid]') || 
                     document.querySelector('.grid');
    
    if (!container) {
        console.warn('Products container not found');
        return;
    }
    
    if (!products || products.length === 0) {
        container.innerHTML = '<p class="col-span-full text-center py-12 text-gray-500">No products found</p>';
        return;
    }
    
    // Update existing product cards with live data
    const cards = container.querySelectorAll('.group, .product-card');
    
    products.forEach((product, index) => {
        if (cards[index]) {
            updateProductCard(cards[index], product);
        }
    });
}

// Update individual product card
function updateProductCard(card, product) {
    // Update image
    const img = card.querySelector('img');
    if (img && product.image_url) {
        img.src = product.image_url;
        img.alt = product.name;
    }
    
    // Update title
    const title = card.querySelector('h4, h3, .product-name');
    if (title) {
        title.textContent = product.name;
    }
    
    // Update price
    const priceEl = card.querySelector('[data-price], .price');
    if (priceEl && product.price) {
        priceEl.textContent = ApiUtils.formatCurrency(product.price);
    }
    
    // Update trend score
    const scoreEl = card.querySelector('[data-trend-score], .trend-score');
    if (scoreEl && product.trend_score) {
        scoreEl.textContent = product.trend_score.toFixed(1);
    }
    
    // Update category badge
    const categoryEl = card.querySelector('[data-category], .category');
    if (categoryEl && product.category) {
        categoryEl.textContent = product.category;
    }
}

// Search functionality
function setupSearch() {
    const searchInput = document.querySelector('#search-input, [data-search-input]');
    
    if (searchInput) {
        const debouncedSearch = ApiUtils.debounce(async (query) => {
            if (query.length < 2) return;
            
            try {
                const results = await TrendLoomAPI.searchProducts({ query });
                displayProducts(results);
            } catch (error) {
                console.error('Search error:', error);
            }
        }, 300);
        
        searchInput.addEventListener('input', (e) => {
            debouncedSearch(e.target.value);
        });
    }
}

// Load categories for filters
async function loadFilters() {
    try {
        const filters = await TrendLoomAPI.getSearchFilters();
        
        // Populate category filter
        populateFilterDropdown('category-filter', filters.categories);
        populateFilterDropdown('color-filter', filters.colors);
        populateFilterDropdown('material-filter', filters.materials);
        populateFilterDropdown('style-filter', filters.styles);
    } catch (error) {
        console.error('Error loading filters:', error);
    }
}

// Populate dropdown
function populateFilterDropdown(id, options) {
    const dropdown = document.getElementById(id);
    if (!dropdown || !options) return;
    
    // Keep first option (usually "All")
    const firstOption = dropdown.querySelector('option');
    dropdown.innerHTML = '';
    if (firstOption) dropdown.appendChild(firstOption);
    
    options.slice(0, 10).forEach(option => {
        const opt = document.createElement('option');
        opt.value = option.value;
        opt.textContent = `${option.value} (${option.count})`;
        dropdown.appendChild(opt);
    });
}

// Initialize page
async function initializeExplorePage() {
    await loadTrendingProducts();
    setupSearch();
    await loadFilters();
}

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializeExplorePage);
} else {
    initializeExplorePage();
}
