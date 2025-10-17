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
        const resetButton = document.getElementById('resetVisibilitySettings');

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

        if (resetButton) {
            resetButton.addEventListener('click', function() {
                // Reset to defaults
                hidePercentages = false;
                hideUnapproved = false;
                
                // Update toggles
                if (percentageToggle) percentageToggle.checked = false;
                if (unapprovedToggle) unapprovedToggle.checked = false;
                
                // Clear localStorage
                localStorage.removeItem(STORAGE_KEYS.HIDE_PERCENTAGES);
                localStorage.removeItem(STORAGE_KEYS.HIDE_UNAPPROVED);
                
                // Re-apply settings (show everything)
                applyVisibilitySettings();
                
                // Show confirmation
                console.log('Visibility settings reset to defaults');
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
     * Hides/shows the entire percentage column in ingredient tables
     */
    function applyPercentageVisibility() {
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

        // Handle ingredient percentage table cells (entire column)
        const percentageCells = document.querySelectorAll('.ingredient-percentage');
        percentageCells.forEach(cell => {
            if (hidePercentages) {
                cell.style.display = 'none';
            } else {
                cell.style.display = '';
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
            // Find the parent column div (col-lg-4 col-md-6)
            const parentCol = card.closest('.col-lg-4, .col-md-6, .col');
            const elementToHide = parentCol || card;
            
            if (hideUnapproved) {
                // Hide the entire column or card
                elementToHide.style.display = 'none';
                elementToHide.classList.add('visibility-hidden');
            } else {
                // Show the column or card
                elementToHide.style.display = '';
                elementToHide.classList.remove('visibility-hidden');
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
