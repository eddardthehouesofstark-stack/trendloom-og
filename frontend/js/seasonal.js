/**
 * Seasonal Intelligence Page Logic
 */

// Load seasonal trends
async function loadSeasonalTrends() {
    try {
        console.log('Loading seasonal trends...');
        
        const data = await TrendLoomAPI.getSeasonalPredictions();
        
        console.log('Seasonal data loaded:', data);
        
        updateSeasonInfo(data);
        updateSeasonalColors(data.top_colors);
        updateSeasonalMaterials(data.top_materials);
        updateSeasonalCategories(data.top_categories);
        
    } catch (error) {
        console.error('Error loading seasonal trends:', error);
        ApiUtils.showError('seasonal-container', 'Failed to load seasonal data');
    }
}

// Update season information
function updateSeasonInfo(data) {
    const seasonEl = document.querySelector('[data-season]');
    if (seasonEl) {
        seasonEl.textContent = data.season.charAt(0).toUpperCase() + data.season.slice(1);
    }
    
    const confidenceEl = document.querySelector('[data-season-confidence]');
    if (confidenceEl) {
        confidenceEl.textContent = `${(data.confidence * 100).toFixed(0)}% Confidence`;
    }
}

// Update seasonal colors
function updateSeasonalColors(colors) {
    if (!colors || colors.length === 0) return;
    
    const container = document.querySelector('[data-seasonal-colors]');
    if (!container) return;
    
    // Get existing color cards
    const cards = container.querySelectorAll('.color-card, .rounded-xl');
    
    colors.slice(0, 5).forEach((color, index) => {
        if (cards[index]) {
            const card = cards[index];
            
            // Update color swatch
            const swatch = card.querySelector('[class*="bg-"]');
            if (swatch && color.hex) {
                swatch.style.backgroundColor = color.hex;
            }
            
            // Update color name
            const nameEl = card.querySelector('h4, h3, .color-name');
            if (nameEl) {
                nameEl.textContent = color.name;
            }
            
            // Update score
            const scoreEl = card.querySelector('[data-score], .score');
            if (scoreEl) {
                scoreEl.textContent = `Score: ${color.score}`;
            }
            
            // Update growth
            const growthEl = card.querySelector('[data-growth], .growth');
            if (growthEl) {
                growthEl.textContent = `Growth: ${ApiUtils.formatPercentage(color.growth)}`;
            }
        }
    });
}

// Update seasonal materials
function updateSeasonalMaterials(materials) {
    if (!materials || materials.length === 0) return;
    
    const container = document.querySelector('[data-seasonal-materials]');
    if (!container) return;
    
    const cards = container.querySelectorAll('.material-card, .rounded-xl');
    
    materials.slice(0, 5).forEach((material, index) => {
        if (cards[index]) {
            const card = cards[index];
            
            const nameEl = card.querySelector('h4, h3');
            if (nameEl) {
                nameEl.textContent = material.name;
            }
            
            const scoreEl = card.querySelector('[data-score]');
            if (scoreEl) {
                scoreEl.textContent = material.score;
            }
        }
    });
}

// Update seasonal categories
function updateSeasonalCategories(categories) {
    if (!categories || categories.length === 0) return;
    
    const container = document.querySelector('[data-seasonal-categories]');
    if (!container) return;
    
    const cards = container.querySelectorAll('.category-card');
    
    categories.slice(0, 5).forEach((category, index) => {
        if (cards[index]) {
            const card = cards[index];
            
            const nameEl = card.querySelector('h4, h3');
            if (nameEl) {
                nameEl.textContent = category.name;
            }
        }
    });
}

// Initialize page
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', loadSeasonalTrends);
} else {
    loadSeasonalTrends();
}
