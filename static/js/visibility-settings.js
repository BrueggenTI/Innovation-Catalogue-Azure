/**
 * Visibility Settings Manager
 * Handles toggling visibility of ingredient percentages and recipes with unapproved materials
 */

(function() {
    'use strict';

    // Storage keys
    const STORAGE_KEYS = {
        HIDE_PERCENTAGES: 'brg_hide_percentages',
        HIDE_UNAPPROVED: 'brg_hide_unapproved'
    };

    // State
    let hidePercentages = false;
    let hideUnapproved = false;

    /**
     * Initialize visibility settings
     */
    function initVisibilitySettings() {
        // Load saved settings from localStorage
        loadSettings();

        // Setup toggle switches
        setupToggleSwitches();

        // Apply initial visibility settings
        applyVisibilitySettings();
    }

    /**
     * Load settings from localStorage
     */
    function loadSettings() {
        hidePercentages = localStorage.getItem(STORAGE_KEYS.HIDE_PERCENTAGES) === 'true';
        hideUnapproved = localStorage.getItem(STORAGE_KEYS.HIDE_UNAPPROVED) === 'true';

        // Update toggle states
        const percentageToggle = document.getElementById('hidePercentagesToggle');
        const unapprovedToggle = document.getElementById('hideUnapprovedToggle');

        if (percentageToggle) percentageToggle.checked = hidePercentages;
        if (unapprovedToggle) unapprovedToggle.checked = hideUnapproved;
    }

    /**
     * Save settings to localStorage
     */
    function saveSettings() {
        localStorage.setItem(STORAGE_KEYS.HIDE_PERCENTAGES, hidePercentages.toString());
        localStorage.setItem(STORAGE_KEYS.HIDE_UNAPPROVED, hideUnapproved.toString());
    }

    /**
     * Setup toggle switch event listeners
     */
    function setupToggleSwitches() {
        const percentageToggle = document.getElementById('hidePercentagesToggle');
        const unapprovedToggle = document.getElementById('hideUnapprovedToggle');

        if (percentageToggle) {
            percentageToggle.addEventListener('change', function() {
                hidePercentages = this.checked;
                saveSettings();
                applyPercentageVisibility();
            });
        }

        if (unapprovedToggle) {
            unapprovedToggle.addEventListener('change', function() {
                hideUnapproved = this.checked;
                saveSettings();
                applyUnapprovedVisibility();
            });
        }
    }

    /**
     * Apply all visibility settings
     */
    function applyVisibilitySettings() {
        applyPercentageVisibility();
        applyUnapprovedVisibility();
    }

    /**
     * Apply percentage visibility setting
     * Hides/shows percentage values in ingredient lists
     */
    function applyPercentageVisibility() {
        // Handle ingredient percentage table cells
        const percentageCells = document.querySelectorAll('.ingredient-percentage');
        percentageCells.forEach(cell => {
            if (hidePercentages) {
                cell.style.display = 'none';
            } else {
                cell.style.display = '';
            }
        });

        // Hide/show the percentage header column by checking text content
        const allHeaders = document.querySelectorAll('th');
        allHeaders.forEach(header => {
            const headerText = (header.textContent || header.innerText || '').toLowerCase();
            if (headerText.includes('percentage') || headerText.includes('prozent')) {
                if (hidePercentages) {
                    header.style.display = 'none';
                } else {
                    header.style.display = '';
                }
            }
        });
        
        // Find all elements with percentage patterns in text
        const ingredientElements = document.querySelectorAll('.ingredient-item, .ingredient-list li, .ingredients-list li, .ingredients-preview-text, [class*="ingredient"]');
        
        ingredientElements.forEach(element => {
            const text = element.textContent || element.innerText;
            
            // Pattern to match percentages like (45%) or (20%)
            const percentagePattern = /\s*\((\d+(?:\.\d+)?)\s*%\)/g;
            
            if (percentagePattern.test(text)) {
                if (hidePercentages) {
                    // Store original text if not already stored
                    if (!element.dataset.originalText) {
                        element.dataset.originalText = element.innerHTML;
                    }
                    // Remove percentages from display
                    element.innerHTML = element.innerHTML.replace(/\s*\((\d+(?:\.\d+)?)\s*%\)/g, '');
                } else {
                    // Restore original text if available
                    if (element.dataset.originalText) {
                        element.innerHTML = element.dataset.originalText;
                    }
                }
            }
        });

        // Also handle text nodes in product cards and recipe details
        const productCards = document.querySelectorAll('.product-card, .recipe-card, .product-detail');
        productCards.forEach(card => {
            processTextNodes(card);
        });
    }

    /**
     * Process text nodes to hide/show percentages
     */
    function processTextNodes(element) {
        if (!element) return;

        const walker = document.createTreeWalker(
            element,
            NodeFilter.SHOW_TEXT,
            null,
            false
        );

        const textNodes = [];
        let node;
        while (node = walker.nextNode()) {
            if (node.nodeValue && /\(\d+(?:\.\d+)?\s*%\)/.test(node.nodeValue)) {
                textNodes.push(node);
            }
        }

        textNodes.forEach(textNode => {
            const parent = textNode.parentElement;
            if (!parent) return;

            if (hidePercentages) {
                if (!parent.dataset.originalText) {
                    parent.dataset.originalText = parent.innerHTML;
                }
                parent.innerHTML = parent.innerHTML.replace(/\s*\((\d+(?:\.\d+)?)\s*%\)/g, '');
            } else {
                if (parent.dataset.originalText) {
                    parent.innerHTML = parent.dataset.originalText;
                }
            }
        });
    }

    /**
     * Apply unapproved material visibility setting
     * Hides/shows recipes that contain unapproved raw materials
     */
    function applyUnapprovedVisibility() {
        // Find all recipe/product cards with unapproved material flag
        const recipeCards = document.querySelectorAll('[data-has-unapproved="true"]');
        
        recipeCards.forEach(card => {
            if (hideUnapproved) {
                // Hide the card
                card.style.display = 'none';
                card.classList.add('visibility-hidden');
            } else {
                // Show the card
                card.style.display = '';
                card.classList.remove('visibility-hidden');
            }
        });

        // Update results count if available
        updateResultsCount();
    }

    /**
     * Update the results count display
     */
    function updateResultsCount() {
        const resultCountElements = document.querySelectorAll('.results-count, .product-count');
        
        resultCountElements.forEach(element => {
            const totalCards = document.querySelectorAll('.product-card, .recipe-card').length;
            const visibleCards = document.querySelectorAll('.product-card:not(.visibility-hidden), .recipe-card:not(.visibility-hidden)').length;
            
            if (element.dataset.originalCount === undefined) {
                element.dataset.originalCount = totalCards;
            }
            
            // Update the count text
            const countText = element.textContent.replace(/\d+/, visibleCards);
            element.textContent = countText;
        });
    }

    /**
     * Public API - Apply settings when new content is loaded dynamically
     */
    window.BruggenVisibility = {
        refresh: function() {
            applyVisibilitySettings();
        },
        hidePercentages: function(hide) {
            hidePercentages = hide;
            const toggle = document.getElementById('hidePercentagesToggle');
            if (toggle) toggle.checked = hide;
            saveSettings();
            applyPercentageVisibility();
        },
        hideUnapproved: function(hide) {
            hideUnapproved = hide;
            const toggle = document.getElementById('hideUnapprovedToggle');
            if (toggle) toggle.checked = hide;
            saveSettings();
            applyUnapprovedVisibility();
        }
    };

    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initVisibilitySettings);
    } else {
        initVisibilitySettings();
    }

    // Re-apply settings when page becomes visible (e.g., tab switching)
    document.addEventListener('visibilitychange', function() {
        if (!document.hidden) {
            applyVisibilitySettings();
        }
    });

})();
