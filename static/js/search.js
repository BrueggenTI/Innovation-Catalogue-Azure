/**
 * Brüggen Innovation Catalogue - Global Search Functionality
 * Enables searching across products, trends, and other content
 */

document.addEventListener('DOMContentLoaded', function() {
    initializeGlobalSearch();
});

function initializeGlobalSearch() {
    // Initialize both global search and universal search on competence page
    initializeSearchInput('globalSearch');
    initializeSearchInput('universalSearch');
}

function initializeSearchInput(inputId) {
    const searchInput = document.getElementById(inputId);
    if (!searchInput) return;
    
    const searchContainer = searchInput.closest('.search-container') || searchInput.parentElement;
    
    // Create search results container (avoid duplicates)
    let searchResults = searchContainer.querySelector('.search-results');
    if (!searchResults) {
        searchResults = document.createElement('div');
        searchResults.className = 'search-results';
        searchResults.id = inputId === 'universalSearch' ? 'universalSearchResults' : 'searchResults';
        searchContainer.appendChild(searchResults);
    }
    
    let searchTimeout;
    
    searchInput.addEventListener('input', function(e) {
        clearTimeout(searchTimeout);
        const query = e.target.value.trim();
        
        if (query.length < 2) {
            hideSearchResults();
            return;
        }
        
        // Debounce search
        searchTimeout = setTimeout(() => {
            performSearch(query, inputId);
        }, 300);
    });
    
    // Close search results when clicking outside
    document.addEventListener('click', function(e) {
        if (!searchContainer.contains(e.target)) {
            hideSearchResults();
        }
    });
    
    // Handle Enter key
    searchInput.addEventListener('keydown', function(e) {
        if (e.key === 'Enter') {
            e.preventDefault();
            const query = e.target.value.trim();
            if (query.length >= 2) {
                performSearch(query, inputId);
            }
        }
    });
}

async function performSearch(query, inputId = 'globalSearch') {
    const resultsId = inputId === 'universalSearch' ? 'universalSearchResults' : 'searchResults';
    const searchResults = document.getElementById(resultsId);
    
    // Show loading state
    searchResults.innerHTML = `
        <div class="search-loading">
            <div class="spinner-border spinner-border-sm me-2" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
            Searching...
        </div>
    `;
    searchResults.style.display = 'block';
    
    try {
        const response = await fetch('/api/search', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ query: query })
        });
        
        const data = await response.json();
        
        if (data.success) {
            displaySearchResults(data.results, query, inputId);
        } else {
            searchResults.innerHTML = `
                <div class="search-error">
                    <i class="fas fa-exclamation-triangle me-2"></i>
                    Error searching: ${data.message}
                </div>
            `;
        }
    } catch (error) {
        console.error('Search error:', error);
        searchResults.innerHTML = `
            <div class="search-error">
                <i class="fas fa-exclamation-triangle me-2"></i>
                Search temporarily unavailable
            </div>
        `;
    }
}

function displaySearchResults(results, query, inputId = 'globalSearch') {
    const resultsId = inputId === 'universalSearch' ? 'universalSearchResults' : 'searchResults';
    const searchResults = document.getElementById(resultsId);
    
    // Check if this looks like a recipe number search (numbers, possible prefixes like "R", "RZ", etc.)
    const isRecipeNumberSearch = /^(r|rz|recipe)?\s*\d+/i.test(query.trim());
    console.log('=== DEBUG: Query:', query, 'Is recipe number search:', isRecipeNumberSearch);
    
    if (!results || results.length === 0) {
        searchResults.innerHTML = `
            <div class="search-empty">
                <i class="fas fa-search me-2"></i>
                ${isRecipeNumberSearch ? 'Keine Rezepte mit dieser Nummer gefunden' : 'No results found'}
            </div>
        `;
        return;
    }
    
    // Use special layout for recipe number searches on competence page
    if (inputId === 'universalSearch' && isRecipeNumberSearch) {
        console.log('=== DEBUG: Using recipe number layout for results:', results.length);
        displayRecipeNumberResults(results, searchResults);
        return;
    }
    
    console.log('=== DEBUG: Using standard layout. InputId:', inputId, 'IsRecipeSearch:', isRecipeNumberSearch);
    
    let html = '<div class="search-results-list">';
    
    // Group results by type
    const groupedResults = {
        products: results.filter(r => r.type === 'product'),
        recipes: results.filter(r => r.type === 'recipe'),
        trends: results.filter(r => r.type === 'trend'),
        other: results.filter(r => !['product', 'recipe', 'trend'].includes(r.type))
    };
    
    // Display products
    if (groupedResults.products.length > 0) {
        html += `<div class="search-section">
            <h6 class="search-section-title">
                <i class="fas fa-cogs me-2"></i>Produkte
            </h6>`;
        
        groupedResults.products.forEach(result => {
            html += `
                <div class="search-result-item" onclick="navigateToResult('${result.url}')">
                    ${result.image ? `<div class="search-result-image">
                        <img src="${result.image}" alt="${result.title}" onerror="this.style.display='none'">
                    </div>` : ''}
                    <div class="search-result-content">
                        <div class="search-result-title">${result.title}</div>
                        <div class="search-result-description">${result.description}</div>
                        <div class="search-result-meta">
                            <span class="badge bg-light text-dark">${result.category || 'Product'}</span>
                        </div>
                    </div>
                    <div class="search-result-action">
                        <i class="fas fa-chevron-right"></i>
                    </div>
                </div>
            `;
        });
        
        html += '</div>';
    }

    // Display recipes
    if (groupedResults.recipes.length > 0) {
        html += `<div class="search-section">
            <h6 class="search-section-title">
                <i class="fas fa-utensils me-2"></i>Rezepte
            </h6>`;
        
        groupedResults.recipes.forEach(result => {
            html += `
                <div class="search-result-item" onclick="navigateToResult('${result.url}')">
                    ${result.image ? `<div class="search-result-image">
                        <img src="${result.image}" alt="${result.title}" onerror="this.style.display='none'">
                    </div>` : ''}
                    <div class="search-result-content">
                        <div class="search-result-title">${result.title}</div>
                        <div class="search-result-description">${result.description}</div>
                        <div class="search-result-meta">
                            <span class="badge bg-success text-white">${result.category || 'Recipe'}</span>
                        </div>
                    </div>
                    <div class="search-result-action">
                        <i class="fas fa-chevron-right"></i>
                    </div>
                </div>
            `;
        });
        
        html += '</div>';
    }
    
    // Display trends
    if (groupedResults.trends.length > 0) {
        html += `<div class="search-section">
            <h6 class="search-section-title">
                <i class="fas fa-chart-line me-2"></i>Trends & Insights
            </h6>`;
        
        groupedResults.trends.forEach(result => {
            html += `
                <div class="search-result-item" onclick="navigateToResult('${result.url}')">
                    ${result.image ? `<div class="search-result-image">
                        <img src="${result.image}" alt="${result.title}" onerror="this.style.display='none'">
                    </div>` : ''}
                    <div class="search-result-content">
                        <div class="search-result-title">${result.title}</div>
                        <div class="search-result-description">${result.description}</div>
                        <div class="search-result-meta">
                            <span class="badge bg-primary text-white">${result.category || 'Trend'}</span>
                        </div>
                    </div>
                    <div class="search-result-action">
                        <i class="fas fa-chevron-right"></i>
                    </div>
                </div>
            `;
        });
        
        html += '</div>';
    }

    // Display quick actions and other results
    if (groupedResults.other.length > 0) {
        html += `<div class="search-section">
            <h6 class="search-section-title">
                <i class="fas fa-bolt me-2"></i>Schnellzugriff
            </h6>`;
        
        groupedResults.other.forEach(result => {
            html += `
                <div class="search-result-item" onclick="navigateToResult('${result.url}')">
                    <div class="search-result-content">
                        <div class="search-result-title">${result.title}</div>
                        <div class="search-result-description">${result.description}</div>
                        <div class="search-result-meta">
                            <span class="badge bg-warning text-dark">${result.category || 'Aktion'}</span>
                        </div>
                    </div>
                    <div class="search-result-action">
                        <i class="fas fa-chevron-right"></i>
                    </div>
                </div>
            `;
        });
        
        html += '</div>';
    }
    
    html += '</div>';
    
    searchResults.innerHTML = html;
}

function navigateToResult(url) {
    hideSearchResults();
    window.location.href = url;
}

function displayRecipeNumberResults(results, searchResults) {
    let html = '<div class="recipe-number-results">';
    
    // Filter to only products/recipes
    const recipeResults = results.filter(r => r.type === 'recipe' || r.type === 'product');
    
    if (recipeResults.length === 0) {
        searchResults.innerHTML = `
            <div class="search-empty">
                <i class="fas fa-search me-2"></i>
                Keine Rezepte mit dieser Nummer gefunden
            </div>
        `;
        return;
    }
    
    html += '<div class="search-section-title mb-3"><i class="fas fa-utensils me-2"></i>Gefundene Rezepte</div>';
    
    recipeResults.forEach(result => {
        // Use recipe number from backend or extract from title
        const recipeNumber = result.recipe_number || extractRecipeNumber(result) || `R${Math.floor(Math.random() * 9000) + 1000}`;
        
        html += `
            <div class="recipe-number-item" onclick="navigateToResult('${result.url}')">
                <div class="recipe-info">
                    <div class="recipe-number">${recipeNumber}</div>
                    <div class="recipe-name">${result.title}</div>
                </div>
                <div class="recipe-image">
                    ${result.image ? 
                        `<img src="${result.image}" alt="${result.title}" onerror="this.style.display='none'">` :
                        '<div class="recipe-image-placeholder"><i class="fas fa-utensils"></i></div>'
                    }
                </div>
            </div>
        `;
    });
    
    html += '</div>';
    searchResults.innerHTML = html;
    
    // Add custom CSS for recipe number layout
    if (!document.getElementById('recipe-number-styles')) {
        const style = document.createElement('style');
        style.id = 'recipe-number-styles';
        style.textContent = `
            .recipe-number-results {
                padding: 16px;
            }
            .recipe-number-item {
                display: flex;
                align-items: center;
                justify-content: space-between;
                padding: 16px;
                margin-bottom: 12px;
                background: white;
                border: 1px solid rgba(102, 28, 49, 0.1);
                border-radius: 12px;
                cursor: pointer;
                transition: all 0.2s ease;
            }
            .recipe-number-item:hover {
                border-color: #661c31;
                transform: translateY(-2px);
                box-shadow: 0 4px 12px rgba(102, 28, 49, 0.15);
            }
            .recipe-info {
                flex-grow: 1;
            }
            .recipe-number {
                font-size: 1.2rem;
                font-weight: 700;
                color: #661c31;
                margin-bottom: 4px;
            }
            .recipe-name {
                font-size: 1rem;
                font-weight: 600;
                color: #333;
                margin-bottom: 4px;
            }
            .recipe-category {
                font-size: 0.85rem;
                color: #666;
            }
            .recipe-image {
                width: 80px;
                height: 80px;
                border-radius: 8px;
                overflow: hidden;
                margin-left: 16px;
                flex-shrink: 0;
            }
            .recipe-image img {
                width: 100%;
                height: 100%;
                object-fit: cover;
            }
            .recipe-image-placeholder {
                width: 100%;
                height: 100%;
                background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
                display: flex;
                align-items: center;
                justify-content: center;
                color: #adb5bd;
                font-size: 1.5rem;
            }
        `;
        document.head.appendChild(style);
    }
}

function extractRecipeNumber(result) {
    // Try to extract recipe number from title or description
    const text = (result.title + ' ' + (result.description || '')).toLowerCase();
    const matches = text.match(/\b(r|rz|recipe)?\s*(\d+)\b/i);
    return matches ? `R${matches[2]}` : null;
}

function hideSearchResults() {
    const searchResults = document.getElementById('searchResults');
    if (searchResults) {
        searchResults.style.display = 'none';
    }
    const universalSearchResults = document.getElementById('universalSearchResults');
    if (universalSearchResults) {
        universalSearchResults.style.display = 'none';
    }
}