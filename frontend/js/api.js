/**
 * TrendLoom API Client
 * Handles all backend API communication
 */

// API Configuration
const API_CONFIG = {
    // Auto-detect: use same hostname as the page (localhost or 127.0.0.1)
    BASE_URL: `http://${window.location.hostname}:8000/api`,
    DEFAULT_STATE: 'Tamil Nadu',
    TIMEOUT: 10000,
};

// API Client Class
class TrendLoomAPI {
    constructor(baseUrl = API_CONFIG.BASE_URL) {
        this.baseUrl = baseUrl;
        this.defaultState = API_CONFIG.DEFAULT_STATE;
    }

    /**
     * Generic fetch wrapper with error handling
     */
    async fetch(endpoint, options = {}) {
        const url = `${this.baseUrl}${endpoint}`;
        
        try {
            const response = await fetch(url, {
                ...options,
                headers: {
                    'Content-Type': 'application/json',
                    ...options.headers,
                },
            });

            if (!response.ok) {
                throw new Error(`API Error: ${response.status} ${response.statusText}`);
            }

            return await response.json();
        } catch (error) {
            console.error('API Fetch Error:', error);
            throw error;
        }
    }

    /**
     * Dashboard Endpoints
     */
    async getDashboard(state = this.defaultState) {
        return this.fetch(`/dashboard?state=${encodeURIComponent(state)}`);
    }
    
    async getLiveDashboard(stateCode = 'IN-TN') {
        return this.fetch(`/dashboard/live?state=${encodeURIComponent(stateCode)}`);
    }

    /**
     * Trending Endpoints
     */
    async getTrendingProducts(params = {}) {
        const {
            state = this.defaultState,
            category = null,
            limit = 20
        } = params;

        let url = `/trending/products?state=${encodeURIComponent(state)}&limit=${limit}`;
        if (category) url += `&category=${encodeURIComponent(category)}`;

        return this.fetch(url);
    }

    async getTrendingCategories(state = this.defaultState) {
        return this.fetch(`/trending/categories?state=${encodeURIComponent(state)}`);
    }

    async getTrendingColors(state = this.defaultState, limit = 10) {
        return this.fetch(`/trending/colors?state=${encodeURIComponent(state)}&limit=${limit}`);
    }

    async getTrendingMaterials(state = this.defaultState, limit = 10) {
        return this.fetch(`/trending/materials?state=${encodeURIComponent(state)}&limit=${limit}`);
    }

    async getTrendingStyles(state = this.defaultState, limit = 10) {
        return this.fetch(`/trending/styles?state=${encodeURIComponent(state)}&limit=${limit}`);
    }

    async getTrendingKeywords(state = this.defaultState, limit = 20) {
        return this.fetch(`/trending/keywords?state=${encodeURIComponent(state)}&limit=${limit}`);
    }

    /**
     * Search Endpoints
     */
    async searchProducts(params = {}) {
        const {
            query,
            category = null,
            color = null,
            material = null,
            style = null,
            minPrice = null,
            maxPrice = null,
            state = this.defaultState,
            limit = 20
        } = params;

        let url = `/search?q=${encodeURIComponent(query)}&state=${encodeURIComponent(state)}&limit=${limit}`;
        if (category) url += `&category=${encodeURIComponent(category)}`;
        if (color) url += `&color=${encodeURIComponent(color)}`;
        if (material) url += `&material=${encodeURIComponent(material)}`;
        if (style) url += `&style=${encodeURIComponent(style)}`;
        if (minPrice !== null) url += `&min_price=${minPrice}`;
        if (maxPrice !== null) url += `&max_price=${maxPrice}`;

        return this.fetch(url);
    }

    async getAutocomplete(query, limit = 10) {
        return this.fetch(`/search/autocomplete?q=${encodeURIComponent(query)}&limit=${limit}`);
    }

    async getSearchFilters(state = this.defaultState) {
        return this.fetch(`/search/filters?state=${encodeURIComponent(state)}`);
    }

    /**
     * Recommendations Endpoints
     */
    async getRecommendations(params = {}) {
        const {
            state = this.defaultState,
            category = null,
            style = null,
            limit = 10
        } = params;

        let url = `/recommendations?state=${encodeURIComponent(state)}&limit=${limit}`;
        if (category) url += `&category=${encodeURIComponent(category)}`;
        if (style) url += `&style=${encodeURIComponent(style)}`;

        return this.fetch(url);
    }

    async analyzeImage(file) {
        console.log('[TrendLoomAPI] analyzeImage called with file:', file);
        const formData = new FormData();
        formData.append('file', file);

        const url = `${this.baseUrl}/image/analyze`;
        console.log('[TrendLoomAPI] Uploading to:', url);
        
        try {
            const response = await fetch(url, {
                method: 'POST',
                body: formData,
            });

            console.log('[TrendLoomAPI] Response status:', response.status);

            if (!response.ok) {
                const errorText = await response.text();
                console.error('[TrendLoomAPI] Error response:', errorText);
                throw new Error(`Image Analysis Error: ${response.status} - ${errorText}`);
            }

            const result = await response.json();
            console.log('[TrendLoomAPI] Success! Result:', result);
            return result;
        } catch (error) {
            console.error('[TrendLoomAPI] Exception:', error);
            throw error;
        }
    }

    /**
     * Demand Prediction Endpoints
     */
    async getDemandPredictions(params = {}) {
        const {
            state = this.defaultState,
            category = null,
            timeHorizon = 30,
            limit = 20
        } = params;

        let url = `/demand?state=${encodeURIComponent(state)}&time_horizon=${timeHorizon}&limit=${limit}`;
        if (category) url += `&category=${encodeURIComponent(category)}`;

        return this.fetch(url);
    }

    async getCategoryForecast(category, days = 30, state = this.defaultState) {
        return this.fetch(`/demand/forecast/${encodeURIComponent(category)}?state=${encodeURIComponent(state)}&days=${days}`);
    }

    async getSeasonalPredictions(state = this.defaultState) {
        return this.fetch(`/demand/seasonal?state=${encodeURIComponent(state)}`);
    }

    /**
     * Analytics Endpoints
     */
    async getWeeklyAnalytics(state = this.defaultState) {
        return this.fetch(`/analytics/weekly?state=${encodeURIComponent(state)}`);
    }

    async getMonthlyAnalytics(month = null, year = null, state = this.defaultState) {
        let url = `/analytics/monthly?state=${encodeURIComponent(state)}`;
        if (month) url += `&month=${month}`;
        if (year) url += `&year=${year}`;

        return this.fetch(url);
    }
}

// Create global API instance
const api = new TrendLoomAPI();

// Utility Functions
const ApiUtils = {
    /**
     * Show loading state
     */
    showLoading(elementId) {
        const element = document.getElementById(elementId);
        if (element) {
            element.innerHTML = `
                <div class="flex items-center justify-center py-12">
                    <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-brand-teal"></div>
                </div>
            `;
        }
    },

    /**
     * Show error message
     */
    showError(elementId, message = 'Failed to load data. Please try again.') {
        const element = document.getElementById(elementId);
        if (element) {
            element.innerHTML = `
                <div class="bg-red-50 border border-red-200 rounded-lg p-4 text-red-800">
                    <p class="font-semibold">Error</p>
                    <p class="text-sm">${message}</p>
                </div>
            `;
        }
    },

    /**
     * Format currency
     */
    formatCurrency(amount, currency = 'INR') {
        if (!amount) return 'N/A';
        return new Intl.NumberFormat('en-IN', {
            style: 'currency',
            currency: currency,
            maximumFractionDigits: 0
        }).format(amount);
    },

    /**
     * Format percentage
     */
    formatPercentage(value) {
        if (value === null || value === undefined) return 'N/A';
        return `${value >= 0 ? '+' : ''}${value.toFixed(1)}%`;
    },

    /**
     * Format date
     */
    formatDate(dateString) {
        if (!dateString) return 'N/A';
        const date = new Date(dateString);
        return date.toLocaleDateString('en-IN', {
            year: 'numeric',
            month: 'short',
            day: 'numeric'
        });
    },

    /**
     * Get recommendation badge class
     */
    getRecommendationClass(recommendation) {
        const classes = {
            'PRODUCE NOW': 'bg-brand-sage text-brand-navy',
            'PRODUCE': 'bg-brand-sage text-brand-navy',
            'WAIT': 'bg-yellow-400 text-brand-navy',
            'WAIT / MONITOR': 'bg-yellow-400 text-brand-navy',
            'AVOID': 'bg-brand-coral text-white',
            'MONITOR': 'bg-gray-400 text-white'
        };
        return classes[recommendation] || 'bg-gray-400 text-white';
    },

    /**
     * Get momentum badge class
     */
    getMomentumClass(momentum) {
        const classes = {
            'high': 'bg-green-500 text-white',
            'medium': 'bg-yellow-500 text-white',
            'low': 'bg-gray-400 text-white'
        };
        return classes[momentum] || 'bg-gray-400 text-white';
    },

    /**
     * Debounce function
     */
    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }
};

// Export for use in HTML files
if (typeof window !== 'undefined') {
    window.TrendLoomAPI = api;
    window.ApiUtils = ApiUtils;
}
