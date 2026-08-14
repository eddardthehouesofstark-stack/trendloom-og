/**
 * Recommendations Page Logic
 */

// Load recommendations
async function loadRecommendations(filters = {}) {
    try {
        console.log('Loading recommendations...');
        
        const recommendations = await TrendLoomAPI.getRecommendations({
            limit: 20,
            ...filters
        });
        
        displayRecommendations(recommendations);
    } catch (error) {
        console.error('Error loading recommendations:', error);
        ApiUtils.showError('recommendations-container', 'Failed to load recommendations');
    }
}

// Display recommendations
function displayRecommendations(recommendations) {
    const container = document.querySelector('[data-recommendations-grid]') ||
                     document.querySelector('.grid');
    
    if (!container) return;
    
    if (!recommendations || recommendations.length === 0) {
        container.innerHTML = '<p class="col-span-full text-center py-12">No recommendations available</p>';
        return;
    }
    
    const cards = container.querySelectorAll('.product-card, .group');
    
    recommendations.forEach((rec, index) => {
        if (cards[index]) {
            updateRecommendationCard(cards[index], rec);
        }
    });
}

// Update recommendation card
function updateRecommendationCard(card, recommendation) {
    // Update image
    const img = card.querySelector('img');
    if (img && recommendation.image_url) {
        img.src = recommendation.image_url;
        img.alt = recommendation.product_name;
    }
    
    // Update title
    const title = card.querySelector('h4, h3');
    if (title) {
        title.textContent = recommendation.product_name;
    }
    
    // Update category
    const category = card.querySelector('.category');
    if (category) {
        category.textContent = recommendation.category;
    }
    
    // Update confidence score
    const confidence = card.querySelector('[data-confidence]');
    if (confidence) {
        confidence.textContent = `${(recommendation.confidence_score * 100).toFixed(0)}% Match`;
    }
}

// Handle image upload
function setupImageUpload() {
    const uploadInput = document.querySelector('#image-upload, input[type="file"]');
    const uploadButton = document.querySelector('[data-upload-trigger]');
    
    if (uploadInput) {
        uploadInput.addEventListener('change', async (e) => {
            const file = e.target.files[0];
            if (file) {
                await analyzeUploadedImage(file);
            }
        });
    }
    
    if (uploadButton) {
        uploadButton.addEventListener('click', () => {
            uploadInput?.click();
        });
    }
}

// Analyze uploaded image
async function analyzeUploadedImage(file) {
    try {
        console.log('Analyzing image...');
        
        // Show loading state
        ApiUtils.showLoading('analysis-results');
        
        const analysis = await TrendLoomAPI.analyzeImage(file);
        
        console.log('Image analysis complete:', analysis);
        
        // Display analysis results
        displayImageAnalysis(analysis);
        
        // Display similar products
        if (analysis.similar_products) {
            displaySimilarProducts(analysis.similar_products);
        }
        
        // Display recommendations
        if (analysis.recommendations) {
            displayRecommendations(analysis.recommendations);
        }
        
    } catch (error) {
        console.error('Error analyzing image:', error);
        ApiUtils.showError('analysis-results', 'Failed to analyze image');
    }
}

// Display image analysis results
function displayImageAnalysis(analysis) {
    const container = document.getElementById('analysis-results');
    if (!container) return;
    
    container.innerHTML = `
        <div class="bg-white rounded-xl p-6 space-y-4">
            <h3 class="text-xl font-semibold">Analysis Results</h3>
            
            <div class="grid grid-cols-2 gap-4">
                <div>
                    <p class="text-sm text-gray-600">Category</p>
                    <p class="font-semibold">${analysis.category}</p>
                </div>
                <div>
                    <p class="text-sm text-gray-600">Confidence</p>
                    <p class="font-semibold">${(analysis.confidence * 100).toFixed(0)}%</p>
                </div>
                ${analysis.style ? `
                <div>
                    <p class="text-sm text-gray-600">Style</p>
                    <p class="font-semibold">${analysis.style}</p>
                </div>
                ` : ''}
                ${analysis.pattern ? `
                <div>
                    <p class="text-sm text-gray-600">Pattern</p>
                    <p class="font-semibold">${analysis.pattern}</p>
                </div>
                ` : ''}
            </div>
            
            ${analysis.colors && analysis.colors.length > 0 ? `
            <div>
                <p class="text-sm text-gray-600 mb-2">Detected Colors</p>
                <div class="flex gap-2">
                    ${analysis.colors.slice(0, 5).map(color => `
                        <div class="flex items-center gap-2">
                            <div class="w-8 h-8 rounded-full border" style="background: ${color.hex}"></div>
                            <span class="text-sm">${color.name}</span>
                        </div>
                    `).join('')}
                </div>
            </div>
            ` : ''}
            
            ${analysis.ai_tags && analysis.ai_tags.length > 0 ? `
            <div>
                <p class="text-sm text-gray-600 mb-2">Tags</p>
                <div class="flex flex-wrap gap-2">
                    ${analysis.ai_tags.map(tag => `
                        <span class="px-3 py-1 bg-gray-100 rounded-full text-sm">${tag}</span>
                    `).join('')}
                </div>
            </div>
            ` : ''}
        </div>
    `;
}

// Display similar products
function displaySimilarProducts(products) {
    const container = document.querySelector('[data-similar-products]');
    if (!container || !products || products.length === 0) return;
    
    // Similar logic to displayRecommendations
}

// Initialize page
async function initializeRecommendationsPage() {
    await loadRecommendations();
    setupImageUpload();
}

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializeRecommendationsPage);
} else {
    initializeRecommendationsPage();
}
