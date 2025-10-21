/**
 * Brüggen Innovation Catalogue - Co-Creation Lab
 * Handles interactive product building with drag-and-drop functionality
 */

document.addEventListener('DOMContentLoaded', function() {

    // Initialize co-creation functionality
    const coCreationLab = new CoCreationLab();
    coCreationLab.init();

    // Make it globally available for onclick handlers
    window.coCreationLab = coCreationLab;
});

class CoCreationLab {
    constructor() {
        this.currentStep = 1;
        this.maxStepReached = 1; // Track highest step user has reached for bidirectional navigation
        this.cameFromBaseProduct = false;
        this.totalSteps = 5;
        this.sessionId = document.getElementById('session-id')?.value;

        // Product configuration state
        this.config = {
            baseProduct: null,
            baseProductName: '',
            baseProductImage: '',
            customIngredients: [],
            ingredientPercentages: {}, // Legacy: Store percentage for each ingredient
            ingredientRatios: {}, // NEW: Store ratios per ingredient: {ingredient: {percent: val, gram: val, activeUnit: 'percent'}}
            nutritionalClaims: [],
            certifications: [],
            packaging: '',
            clientName: '',
            clientEmail: '',
            notes: ''
        };

        // Ingredient data
        this.ingredientData = {
            fruits: [
                'Dried Strawberries', 'Blueberries', 'Cranberries', 'Raspberries',
                'Dried Mango', 'Banana Chips', 'Dried Apricots', 'Raisins',
                'Goji Berries', 'Dried Cherries', 'Freeze-dried Kiwi', 'Dried Pineapple'
            ],
            nuts: [
                'Almonds', 'Walnuts', 'Pecans', 'Cashews', 'Hazelnuts',
                'Pistachios', 'Brazil Nuts', 'Macadamia', 'Pine Nuts',
                'Sunflower Seeds', 'Pumpkin Seeds', 'Chia Seeds', 'Flax Seeds'
            ],
            grains: [
                'Quinoa', 'Amaranth', 'Buckwheat', 'Millet', 'Spelt',
                'Kamut', 'Teff', 'Brown Rice', 'Wild Rice', 'Barley'
            ],
            extras: [
                'Coconut Flakes', 'Cocoa Nibs', 'Dark Chocolate', 'Honey',
                'Maple Syrup', 'Vanilla Extract', 'Cinnamon', 'Turmeric',
                'Spirulina', 'Matcha', 'Protein Powder', 'Collagen'
            ]
        };
    }

    init() {
        this.bindEvents();
        this.updateProgress();
        this.loadURLParameters();
        this.checkForBaseProduct();

        // Ensure PDF button is enabled if we have a base product
        setTimeout(() => {
            const generateBtn = document.getElementById('generate-concept');
            if (generateBtn && this.config.baseProduct) {
                generateBtn.disabled = false;
            }
        }, 100);
    }

    bindEvents() {
        // Step navigation
        this.bindStepNavigation();

        // Step 1: Base product selection
        this.bindBaseProductSelection();

        // Product search functionality
        this.bindProductSearch();

        // Step 2: Ingredient selection
        this.bindIngredientSelection();

        // Step 3: Ingredient percentages
        this.bindIngredientPercentages();

        // Step 4: Claims and certifications
        this.bindClaimsSelection();

        // Step 5: Final review and submission (packaging step removed)
        this.bindFinalSubmission();

        // Draft management
        this.bindDraftManagement();

        // Preview updates
        this.bindPreviewUpdates();

        // Reset configuration
        this.bindResetConfiguration();

        // Summary modal
        this.bindSummaryModal();
    }

    loadURLParameters() {
        const urlParams = new URLSearchParams(window.location.search);
        const draftId = urlParams.get('draft_id');
        const baseProductId = urlParams.get('base_product') || urlParams.get('base_product_id');

        // Check if loading from a draft
        if (draftId) {
            this.loadDraftConfiguration(draftId);
            return; // Don't proceed with regular base product selection
        }

        if (baseProductId) {
            // Auto-select base product if provided in URL
            const productCard = document.querySelector(`[data-product-id="${baseProductId}"]`);
            if (productCard) {
                setTimeout(() => {
                    productCard.click();
                }, 500);
            }
        }
    }
    
    async loadDraftConfiguration(draftId) {
        try {
            console.log('Loading draft configuration:', draftId);
            
            const response = await fetch(`/cocreation/load-draft/${draftId}`);
            const data = await response.json();
            
            if (!data.success || !data.draft) {
                console.error('Failed to load draft:', data.error);
                alert('Failed to load draft: ' + (data.error || 'Unknown error'));
                return;
            }
            
            // Parse the configuration
            const config = JSON.parse(data.draft.product_config);
            console.log('Loaded draft configuration:', config);
            
            // Restore base product
            if (config.baseProduct) {
                this.config.baseProduct = config.baseProduct;
                this.config.baseProductName = config.baseProductName || '';
                this.config.baseProductImage = config.baseProductImage || '';
                
                // Select the base product card
                const productCard = document.querySelector(`[data-product-id="${config.baseProduct}"]`);
                if (productCard) {
                    document.querySelectorAll('.base-product-card').forEach(c => c.classList.remove('selected'));
                    productCard.classList.add('selected');
                }
            }
            
            // Restore custom ingredients
            if (config.customIngredients && Array.isArray(config.customIngredients)) {
                this.config.customIngredients = [...config.customIngredients];
            }
            
            // Restore nutritional claims
            if (config.nutritionalClaims && Array.isArray(config.nutritionalClaims)) {
                this.config.nutritionalClaims = [...config.nutritionalClaims];
            }
            
            // Restore certifications
            if (config.certifications && Array.isArray(config.certifications)) {
                this.config.certifications = [...config.certifications];
            }
            
            // Restore ingredient ratios
            if (config.ingredientRatios && typeof config.ingredientRatios === 'object') {
                this.config.ingredientRatios = {...config.ingredientRatios};
            }
            
            // Restore client information
            if (config.clientName) {
                this.config.clientName = config.clientName;
                const clientNameInput = document.getElementById('client-name');
                if (clientNameInput) clientNameInput.value = config.clientName;
            }
            
            if (config.clientEmail) {
                this.config.clientEmail = config.clientEmail;
                const clientEmailInput = document.getElementById('client-email');
                if (clientEmailInput) clientEmailInput.value = config.clientEmail;
            }
            
            if (config.notes) {
                this.config.notes = config.notes;
                const notesInput = document.getElementById('special-notes');
                if (notesInput) notesInput.value = config.notes;
            }
            
            // Update the UI to reflect the loaded configuration
            this.restoreUIFromConfig();
            
            // Update preview
            this.updatePreview();
            
            // Show success message
            this.showSuccessMessage(`Draft "${data.draft.draft_name}" loaded successfully!`);
            
            // Navigate to step 2 (Add Ingredients) to show the loaded configuration
            this.currentStep = 2;
            this.maxStepReached = 5; // Allow navigation to all steps since draft was saved from a complete state
            this.updateProgress();
            document.getElementById('step-1').classList.remove('active');
            document.getElementById('step-2').classList.add('active');
            
        } catch (error) {
            console.error('Error loading draft configuration:', error);
            alert('An error occurred while loading the draft.');
        }
    }
    
    restoreUIFromConfig() {
        // Restore custom ingredients in the UI
        if (this.config.customIngredients.length > 0) {
            const customIngredientsDiv = document.getElementById('custom-ingredients-list');
            if (customIngredientsDiv) {
                customIngredientsDiv.innerHTML = '';
                this.config.customIngredients.forEach(ingredient => {
                    const ingredientTag = document.createElement('span');
                    ingredientTag.className = 'ingredient-tag custom';
                    ingredientTag.innerHTML = `
                        ${ingredient}
                        <button class="remove-ingredient" onclick="window.coCreationLab.removeCustomIngredient('${ingredient.replace(/'/g, "\\'")}')">
                            <i class="fas fa-times"></i>
                        </button>
                    `;
                    customIngredientsDiv.appendChild(ingredientTag);
                });
            }
        }
        
        // Restore selected claims
        if (this.config.nutritionalClaims.length > 0) {
            document.querySelectorAll('.claim-option').forEach(option => {
                const claim = option.dataset.claim;
                if (this.config.nutritionalClaims.includes(claim)) {
                    option.classList.add('selected');
                }
            });
        }
        
        // Restore selected certifications
        if (this.config.certifications.length > 0) {
            document.querySelectorAll('.certification-option').forEach(option => {
                const cert = option.dataset.cert;
                if (this.config.certifications.includes(cert)) {
                    option.classList.add('selected');
                }
            });
        }
        
        // Restore ingredient percentages if needed
        if (Object.keys(this.config.ingredientRatios).length > 0) {
            // The percentages will be restored when navigating to step 3
            console.log('Ingredient ratios restored:', this.config.ingredientRatios);
        }
    }

    checkForBaseProduct() {
        // Check if base product is already selected via URL parameters
        const baseProductId = document.getElementById('base-product-id')?.value;
        const baseProductName = document.getElementById('base-product-name')?.value;
        const baseProductImage = document.getElementById('base-product-image')?.value;

        if (baseProductId && baseProductName) {
            // Set configuration for pre-selected base product
            this.config.baseProduct = baseProductId;
            this.config.baseProductName = baseProductName;
            this.config.baseProductImage = baseProductImage;

            console.log('Base product configuration:', {
                id: baseProductId,
                name: baseProductName,
                image: baseProductImage
            });

            // Skip to step 2 (Add Ingredients) but allow going back to step 1
            this.currentStep = 2;
            this.updateProgress();
            this.updatePreview();

            // Show step 2 and hide step 1
            document.getElementById('step-1').classList.remove('active');
            document.getElementById('step-2').classList.add('active');

            // Mark that we came from base product selection
            this.cameFromBaseProduct = true;

            console.log('Base product pre-selected:', baseProductName);
        }
    }

    bindStepNavigation() {
        // Global navigation buttons
        document.getElementById('global-next-btn')?.addEventListener('click', () => this.nextStep());
        document.getElementById('global-back-btn')?.addEventListener('click', () => this.previousStep());
        document.getElementById('global-save-draft-btn')?.addEventListener('click', () => {
            document.getElementById('save-draft-btn')?.click();
        });
        document.getElementById('global-generate-btn')?.addEventListener('click', () => this.generateConcept());
        
        // Keep old button bindings for backwards compatibility (though they're now hidden)
        // Next buttons
        document.getElementById('step1-next')?.addEventListener('click', () => this.nextStep());
        document.getElementById('step2-next')?.addEventListener('click', () => this.nextStep());
        document.getElementById('step3-next')?.addEventListener('click', () => this.nextStep());
        document.getElementById('step4-next')?.addEventListener('click', () => this.nextStep());

        // Back buttons
        document.getElementById('step2-back')?.addEventListener('click', () => this.previousStep());
        document.getElementById('step3-back')?.addEventListener('click', () => this.previousStep());
        document.getElementById('step4-back')?.addEventListener('click', () => this.previousStep());
        document.getElementById('step5-back')?.addEventListener('click', () => this.previousStep());
        
        // Special back-to-ingredients button
        document.getElementById('back-to-ingredients')?.addEventListener('click', () => {
            this.currentStep = 2;
            this.showStep(2);
        });

        // Step icon navigation - allow jumping to any previously visited step
        document.querySelectorAll('.progress-step').forEach(stepEl => {
            stepEl.addEventListener('click', (e) => {
                const targetStep = parseInt(stepEl.dataset.step);
                
                // Allow navigation to any step up to maxStepReached (bidirectional)
                if (targetStep <= this.maxStepReached) {
                    // Add visual feedback
                    stepEl.style.cursor = 'pointer';
                    
                    // Navigate to target step
                    this.currentStep = targetStep;
                    this.showStep(targetStep);
                }
            });
            
            // Add visual cues for clickable steps
            stepEl.addEventListener('mouseenter', (e) => {
                const targetStep = parseInt(stepEl.dataset.step);
                if (targetStep <= this.maxStepReached) {
                    stepEl.style.cursor = 'pointer';
                    stepEl.style.opacity = '0.8';
                    stepEl.style.transform = 'scale(1.05)';
                }
            });
            
            stepEl.addEventListener('mouseleave', (e) => {
                stepEl.style.opacity = '1';
                stepEl.style.transform = 'scale(1)';
            });
        });
    }

    bindBaseProductSelection() {
        document.querySelectorAll('.base-product-card').forEach(card => {
            card.addEventListener('click', () => {
                // Remove previous selection
                document.querySelectorAll('.base-product-card').forEach(c => c.classList.remove('selected'));

                // Select current card
                card.classList.add('selected');

                // Update configuration
                this.config.baseProduct = card.dataset.productId;
                this.config.baseProductName = card.dataset.productName;
                this.config.baseProductImage = card.querySelector('img')?.src;

                // Enable next button
                document.getElementById('step1-next').disabled = false;

                // Update preview
                this.updatePreview();

                // Add visual feedback
                this.showSuccessAnimation(card);
            });
        });
    }

    bindProductSearch() {
        const searchInput = document.getElementById('product-search-input');
        const clearBtn = document.getElementById('clear-search');
        const resultsCount = document.getElementById('search-results-count');
        
        if (!searchInput) return;

        const filterProducts = () => {
            const searchTerm = searchInput.value.toLowerCase().trim();
            const productCards = document.querySelectorAll('.product-card-col');
            let visibleCount = 0;

            productCards.forEach(col => {
                const card = col.querySelector('.base-product-card');
                if (!card) return;

                const productName = card.dataset.productName?.toLowerCase() || '';
                const recipeNumber = card.dataset.recipeNumber?.toLowerCase() || '';

                const matches = productName.includes(searchTerm) || recipeNumber.includes(searchTerm);

                if (searchTerm === '' || matches) {
                    col.style.display = '';
                    visibleCount++;
                } else {
                    col.style.display = 'none';
                }
            });

            // Update results count
            if (resultsCount) {
                if (searchTerm === '') {
                    resultsCount.textContent = '';
                } else {
                    resultsCount.textContent = `${visibleCount} product${visibleCount !== 1 ? 's' : ''} found`;
                }
            }

            // Show/hide clear button
            if (clearBtn) {
                clearBtn.style.display = searchTerm ? 'block' : 'none';
            }
        };

        // Bind search input event
        searchInput.addEventListener('input', filterProducts);

        // Bind clear button event
        if (clearBtn) {
            clearBtn.addEventListener('click', () => {
                searchInput.value = '';
                filterProducts();
                searchInput.focus();
            });
        }
    }

    bindDraftManagement() {
        const saveDraftBtn = document.getElementById('save-draft-btn');
        const saveDraftModal = document.getElementById('saveDraftModal');
        const draftNameInput = document.getElementById('draft-name-input');
        const confirmSaveBtn = document.getElementById('confirm-save-draft');

        if (!saveDraftBtn) return;

        // Open save draft modal
        saveDraftBtn.addEventListener('click', () => {
            if (typeof bootstrap !== 'undefined' && saveDraftModal) {
                const modal = new bootstrap.Modal(saveDraftModal);
                modal.show();
                // Clear previous input
                if (draftNameInput) {
                    draftNameInput.value = '';
                    draftNameInput.classList.remove('is-invalid');
                }
            }
        });

        // Confirm save draft
        if (confirmSaveBtn && draftNameInput) {
            confirmSaveBtn.addEventListener('click', () => {
                const draftName = draftNameInput.value.trim();

                if (!draftName) {
                    draftNameInput.classList.add('is-invalid');
                    return;
                }

                draftNameInput.classList.remove('is-invalid');

                // Prepare draft data
                const draftData = {
                    draft_name: draftName,
                    product_config: JSON.stringify(this.config)
                };

                // Send draft to backend
                fetch('/cocreation/save-draft', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(draftData)
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        // Close modal
                        if (typeof bootstrap !== 'undefined' && saveDraftModal) {
                            const modal = bootstrap.Modal.getInstance(saveDraftModal);
                            if (modal) modal.hide();
                        }

                        // Show success message
                        this.showSuccessMessage(`Draft "${draftName}" saved successfully!`);
                    } else {
                        alert('Failed to save draft: ' + (data.error || 'Unknown error'));
                    }
                })
                .catch(error => {
                    console.error('Error saving draft:', error);
                    alert('An error occurred while saving the draft.');
                });
            });
        }
    }

    showSuccessMessage(message) {
        // Simple success notification (can be enhanced with a proper toast/notification system)
        const alertDiv = document.createElement('div');
        alertDiv.className = 'alert alert-success alert-dismissible fade show position-fixed';
        alertDiv.style.cssText = 'top: 100px; right: 20px; z-index: 9999; min-width: 300px;';
        alertDiv.innerHTML = `
            <i class="fas fa-check-circle me-2"></i>${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        document.body.appendChild(alertDiv);

        // Auto-remove after 5 seconds
        setTimeout(() => {
            alertDiv.remove();
        }, 5000);
    }

    bindIngredientPercentages() {
        // This function handles initial setup and event binding for percentage inputs
        // Called during initialization to set up base event structure
        
        // The actual percentage UI setup happens in setupIngredientPercentages()
        // which is called when entering Step 3 via showStep() or nextStep()
        
        // We'll also set up any global percentage-related event handlers here
        // For now, the main logic is in setupIngredientPercentages()
    }

    setupIngredientRatios() {
        const container = document.getElementById('ingredient-ratios');
        const noIngredientsMessage = document.getElementById('no-ingredients-message');
        const ratioSummary = document.getElementById('ratio-summary');
        const step3NextBtn = document.getElementById('step3-next');

        // Initialize ingredientRatios for all selected ingredients
        this.initializeIngredientRatios();

        // Check if any ingredients are selected
        if (this.config.customIngredients.length === 0) {
            noIngredientsMessage.style.display = 'block';
            ratioSummary.style.display = 'none';
            return;
        }

        // Hide no ingredients message and show content
        noIngredientsMessage.style.display = 'none';
        ratioSummary.style.display = 'block';

        // Generate ratio inputs for each selected ingredient with individual unit dropdowns
        const ingredientsHTML = this.config.customIngredients.map(ingredient => {
            const ratioData = this.config.ingredientRatios[ingredient];
            const activeUnit = ratioData.activeUnit;
            const currentValue = ratioData[activeUnit] || 0;
            const unitSymbol = activeUnit === 'percent' ? '%' : 'g';
            const unitLabel = activeUnit === 'percent' ? 'Percentage' : 'Grams';
            const maxValue = activeUnit === 'percent' ? 100 : 1000;
            const stepValue = activeUnit === 'percent' ? 1 : 5;
            const ingredientId = ingredient.replace(/\s+/g, '-');
            
            return `
                <div class="ingredient-ratio-item mb-3" data-ingredient="${ingredient}">
                    <div class="row align-items-center">
                        <div class="col-md-4">
                            <label class="fw-bold text-muted">${ingredient}</label>
                        </div>
                        <div class="col-md-6">
                            <div class="ratio-slider-container">
                                <input type="range" 
                                       class="form-range ratio-slider" 
                                       id="slider-${ingredientId}"
                                       min="0" 
                                       max="${maxValue}" 
                                       step="${stepValue}" 
                                       value="${currentValue}"
                                       data-ingredient="${ingredient}">
                            </div>
                        </div>
                        <div class="col-md-2">
                            <div class="d-flex align-items-center">
                                <input type="number" 
                                       class="form-control ratio-input me-2" 
                                       id="input-${ingredientId}"
                                       min="0" 
                                       max="${maxValue}" 
                                       step="${stepValue}" 
                                       value="${currentValue}"
                                       data-ingredient="${ingredient}"
                                       style="flex: 1; width: 70px; -webkit-appearance: none; -moz-appearance: textfield; text-align: center;"
                                       onwheel="this.blur()">
                                <div class="dropdown">
                                    <button type="button" class="btn btn-sm text-muted unit-dropdown" 
                                            data-bs-toggle="dropdown" 
                                            data-ingredient="${ingredient}"
                                            aria-expanded="false"
                                            id="unit-btn-${ingredientId}"
                                            style="border: none; background: none; font-size: 0.9rem; padding: 2px 4px; min-width: 20px;">
                                        ${unitSymbol} <i class="fas fa-caret-down" style="font-size: 0.7rem; margin-left: 2px;"></i>
                                    </button>
                                    <ul class="dropdown-menu dropdown-menu-end" style="min-width: 120px;">
                                        <li><a class="dropdown-item unit-option" 
                                               data-ingredient="${ingredient}" 
                                               data-unit="percent" 
                                               href="#"
                                               style="font-size: 0.85rem; padding: 4px 8px;">
                                            <i class="fas fa-percentage me-2"></i>Percentage (%)
                                        </a></li>
                                        <li><a class="dropdown-item unit-option" 
                                               data-ingredient="${ingredient}" 
                                               data-unit="gram" 
                                               href="#"
                                               style="font-size: 0.85rem; padding: 4px 8px;">
                                            <i class="fas fa-weight me-2"></i>Grams (g)
                                        </a></li>
                                    </ul>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            `;
        }).join('');

        // Replace the content while preserving the no-ingredients message
        container.innerHTML = `
            <div class="no-ingredients-message text-center py-5" id="no-ingredients-message" style="display: none;">
                <i class="fas fa-exclamation-triangle fa-3x text-muted mb-3"></i>
                <h5 class="text-muted">No ingredients selected</h5>
                <p class="text-muted">Please go back to Step 2 and select some ingredients first.</p>
                <button class="btn btn-outline-secondary rounded-pill px-4" id="back-to-ingredients">
                    <i class="fas fa-arrow-left me-2"></i>Back to Add Ingredients
                </button>
            </div>
            <div class="ingredients-ratio-grid">
                <h6 class="mb-4">
                    <i class="fas fa-sliders-h me-2"></i>Adjust the ratio for each ingredient (click unit to change):
                </h6>
                ${ingredientsHTML}
                <div class="ratio-actions mt-4">
                    <button class="btn btn-outline-info btn-sm me-2" id="distribute-equally">
                        <i class="fas fa-equals me-1"></i>Distribute Equally
                    </button>
                    <button class="btn btn-outline-warning btn-sm" id="reset-ratios">
                        <i class="fas fa-undo me-1"></i>Reset to Zero
                    </button>
                </div>
            </div>
        `;

        // Re-bind the back button since we regenerated the content
        document.getElementById('back-to-ingredients')?.addEventListener('click', () => {
            this.currentStep = 2;
            this.showStep(2);
        });

        // Bind ratio input events
        this.bindRatioInputEvents();
        
        // Bind unit dropdown events
        this.bindUnitDropdowns();

        // Update counts and summary
        this.updateRatioSummary();
    }

    initializeIngredientRatios() {
        // Initialize ratio data structure for all selected ingredients
        this.config.customIngredients.forEach(ingredient => {
            if (!this.config.ingredientRatios[ingredient]) {
                this.config.ingredientRatios[ingredient] = {
                    percent: 0,
                    gram: 0,
                    activeUnit: 'percent'
                };
            }
        });
    }

    bindUnitDropdowns() {
        // Bind individual unit dropdown events
        document.querySelectorAll('.unit-option').forEach(option => {
            option.addEventListener('click', (e) => {
                e.preventDefault();
                const ingredient = e.target.dataset.ingredient;
                const newUnit = e.target.dataset.unit;
                
                // Update the active unit for this ingredient
                this.config.ingredientRatios[ingredient].activeUnit = newUnit;
                
                // Re-setup the ratios to update UI for this ingredient
                this.setupIngredientRatios();
            });
        });
    }

    bindRatioInputEvents() {
        // Bind slider events
        document.querySelectorAll('.ratio-slider').forEach(slider => {
            slider.addEventListener('input', (e) => {
                const ingredient = e.target.dataset.ingredient;
                const value = parseInt(e.target.value);
                const ratioData = this.config.ingredientRatios[ingredient];
                const activeUnit = ratioData.activeUnit;
                
                // Update corresponding input field
                const input = document.getElementById(`input-${ingredient.replace(/\s+/g, '-')}`);
                if (input) input.value = value;

                // Update configuration for active unit
                this.config.ingredientRatios[ingredient][activeUnit] = value;
                
                // Update summary
                this.updateRatioSummary();
            });
        });

        // Bind input field events
        document.querySelectorAll('.ratio-input').forEach(input => {
            input.addEventListener('input', (e) => {
                const ingredient = e.target.dataset.ingredient;
                const ratioData = this.config.ingredientRatios[ingredient];
                const activeUnit = ratioData.activeUnit;
                const maxValue = activeUnit === 'percent' ? 100 : 1000;
                
                let value = parseInt(e.target.value) || 0;
                
                // Clamp value between 0 and max
                value = Math.max(0, Math.min(maxValue, value));
                e.target.value = value;

                // Update corresponding slider
                const slider = document.getElementById(`slider-${ingredient.replace(/\s+/g, '-')}`);
                if (slider) slider.value = value;

                // Update configuration for active unit
                this.config.ingredientRatios[ingredient][activeUnit] = value;
                
                // Update summary
                this.updateRatioSummary();
            });
        });

        // Distribute equally button
        document.getElementById('distribute-equally')?.addEventListener('click', () => {
            this.config.customIngredients.forEach(ingredient => {
                const ratioData = this.config.ingredientRatios[ingredient];
                const activeUnit = ratioData.activeUnit;
                
                // Calculate equal value based on unit
                const equalValue = activeUnit === 'percent' 
                    ? Math.floor(100 / this.config.customIngredients.length)
                    : Math.floor(500 / this.config.customIngredients.length); // Default 500g total for grams

                // Update data
                this.config.ingredientRatios[ingredient][activeUnit] = equalValue;

                // Update UI
                const slider = document.getElementById(`slider-${ingredient.replace(/\s+/g, '-')}`);
                const input = document.getElementById(`input-${ingredient.replace(/\s+/g, '-')}`);
                if (slider) slider.value = equalValue;
                if (input) input.value = equalValue;
            });

            this.updateRatioSummary();
        });

        // Reset ratios button
        document.getElementById('reset-ratios')?.addEventListener('click', () => {
            this.config.customIngredients.forEach(ingredient => {
                const ratioData = this.config.ingredientRatios[ingredient];
                const activeUnit = ratioData.activeUnit;
                
                // Reset data for active unit
                this.config.ingredientRatios[ingredient][activeUnit] = 0;

                // Update UI
                const slider = document.getElementById(`slider-${ingredient.replace(/\s+/g, '-')}`);
                const input = document.getElementById(`input-${ingredient.replace(/\s+/g, '-')}`);
                if (slider) slider.value = 0;
                if (input) input.value = 0;
            });

            this.updateRatioSummary();
        });
    }

    updateRatioSummary() {
        const ingredientCount = this.config.customIngredients.length;
        const ingredientCountEl = document.getElementById('ingredient-count');

        if (ingredientCountEl) {
            ingredientCountEl.textContent = `${ingredientCount} ingredient${ingredientCount !== 1 ? 's' : ''}`;
        }

        // Update preview
        this.updatePreview();
    }

    bindPercentageInputEvents() {
        // Bind slider events
        document.querySelectorAll('.percentage-slider').forEach(slider => {
            slider.addEventListener('input', (e) => {
                const ingredient = e.target.dataset.ingredient;
                const value = parseInt(e.target.value);
                
                // Update corresponding input field
                const input = document.getElementById(`input-${ingredient.replace(/\s+/g, '-')}`);
                if (input) input.value = value;

                // Update configuration
                this.config.ingredientPercentages[ingredient] = value;
                
                // Update summary
                this.updatePercentageSummary();
            });
        });

        // Bind input field events
        document.querySelectorAll('.percentage-input').forEach(input => {
            input.addEventListener('input', (e) => {
                const ingredient = e.target.dataset.ingredient;
                let value = parseInt(e.target.value) || 0;
                
                // Clamp value between 0 and 100
                value = Math.max(0, Math.min(100, value));
                e.target.value = value;

                // Update corresponding slider
                const slider = document.getElementById(`slider-${ingredient.replace(/\s+/g, '-')}`);
                if (slider) slider.value = value;

                // Update configuration
                this.config.ingredientPercentages[ingredient] = value;
                
                // Update summary
                this.updatePercentageSummary();
            });
        });

        // Distribute equally button
        document.getElementById('distribute-equally')?.addEventListener('click', () => {
            const equalPercentage = Math.floor(100 / this.config.customIngredients.length);
            const remainder = 100 % this.config.customIngredients.length;

            this.config.customIngredients.forEach((ingredient, index) => {
                // Give remainder to first ingredients
                const percentage = equalPercentage + (index < remainder ? 1 : 0);
                this.config.ingredientPercentages[ingredient] = percentage;

                // Update UI
                const slider = document.getElementById(`slider-${ingredient.replace(/\s+/g, '-')}`);
                const input = document.getElementById(`input-${ingredient.replace(/\s+/g, '-')}`);
                if (slider) slider.value = percentage;
                if (input) input.value = percentage;
            });

            this.updatePercentageSummary();
        });

        // Reset percentages button
        document.getElementById('reset-percentages')?.addEventListener('click', () => {
            this.config.customIngredients.forEach(ingredient => {
                this.config.ingredientPercentages[ingredient] = 0;

                // Update UI
                const slider = document.getElementById(`slider-${ingredient.replace(/\s+/g, '-')}`);
                const input = document.getElementById(`input-${ingredient.replace(/\s+/g, '-')}`);
                if (slider) slider.value = 0;
                if (input) input.value = 0;
            });

            this.updatePercentageSummary();
        });
    }

    updatePercentageSummary() {
        const totalPercentage = Object.values(this.config.ingredientPercentages).reduce((sum, percentage) => sum + (percentage || 0), 0);
        const ingredientCount = this.config.customIngredients.length;

        // Update progress bar
        const progressBar = document.getElementById('total-percentage-bar');
        const progressText = document.getElementById('total-percentage-text');
        const ingredientCountEl = document.getElementById('ingredient-count');
        const step3NextBtn = document.getElementById('step3-next');

        if (progressBar) {
            progressBar.style.width = `${Math.min(totalPercentage, 100)}%`;
            
            // Color coding: green if 100%, yellow if close, red if far off
            if (totalPercentage === 100) {
                progressBar.className = 'progress-bar bg-success';
            } else if (totalPercentage >= 80 && totalPercentage <= 120) {
                progressBar.className = 'progress-bar bg-warning';
            } else {
                progressBar.className = 'progress-bar bg-danger';
            }
        }

        if (progressText) {
            progressText.textContent = `${totalPercentage}%`;
            progressText.className = totalPercentage === 100 ? 'fw-bold text-success' : 
                                   (totalPercentage >= 80 && totalPercentage <= 120) ? 'fw-bold text-warning' : 
                                   'fw-bold text-danger';
        }

        if (ingredientCountEl) {
            ingredientCountEl.textContent = `${ingredientCount} ingredient${ingredientCount !== 1 ? 's' : ''}`;
        }

        // Enable/disable next button based on total percentage
        if (step3NextBtn) {
            step3NextBtn.disabled = totalPercentage !== 100;
            
            if (totalPercentage === 100) {
                step3NextBtn.innerHTML = 'Continue to Claims <i class="fas fa-arrow-right ms-2"></i>';
            } else {
                step3NextBtn.innerHTML = `Total must be 100% (currently ${totalPercentage}%) <i class="fas fa-arrow-right ms-2"></i>`;
            }
        }

        // Update preview
        this.updatePreview();
    }

    bindIngredientSelection() {
        // Category selection
        document.querySelectorAll('.ingredient-category').forEach(category => {
            category.addEventListener('click', () => {
                // Remove previous selection
                document.querySelectorAll('.ingredient-category').forEach(c => c.classList.remove('active'));

                // Select current category
                category.classList.add('active');

                // Load ingredients for this category
                const categoryName = category.dataset.category;
                this.loadIngredients(categoryName);
            });
        });
    }

    loadIngredients(category) {
        const ingredientSelection = document.getElementById('ingredient-selection');
        const ingredients = this.ingredientData[category] || [];

        ingredientSelection.innerHTML = `
            <h6 class="mb-3">Available ${category.charAt(0).toUpperCase() + category.slice(1)}:</h6>
            <div class="ingredients-grid">
                ${ingredients.map(ingredient => `
                    <div class="ingredient-item" data-ingredient="${ingredient}">
                        <i class="fas fa-plus me-2"></i>
                        ${ingredient}
                    </div>
                `).join('')}
            </div>
        `;

        // Bind ingredient selection events
        ingredientSelection.querySelectorAll('.ingredient-item').forEach(item => {
            item.addEventListener('click', () => {
                const ingredient = item.dataset.ingredient;

                if (item.classList.contains('selected')) {
                    this.removeIngredient(ingredient);
                    item.classList.remove('selected');
                } else {
                    this.addIngredient(ingredient);
                    item.classList.add('selected');
                }
            });
        });

        // Mark already selected ingredients as selected visually
        this.config.customIngredients.forEach(selectedIngredient => {
            const ingredientItem = ingredientSelection.querySelector(`[data-ingredient="${selectedIngredient}"]`);
            if (ingredientItem) {
                ingredientItem.classList.add('selected');
            }
        });
    }

    addIngredient(ingredient) {
        if (!this.config.customIngredients.includes(ingredient)) {
            this.config.customIngredients.push(ingredient);
            this.updateSelectedIngredients();
            this.updatePreview();
        }
    }

    removeIngredient(ingredient) {
        const index = this.config.customIngredients.indexOf(ingredient);
        if (index > -1) {
            this.config.customIngredients.splice(index, 1);
            this.updateSelectedIngredients();
            this.updatePreview();
        }
    }

    updateSelectedIngredients() {
        const container = document.getElementById('selected-ingredients-list');
        
        // Check if container exists, if not try alternative IDs
        if (!container) {
            console.error('selected-ingredients-list container not found');
            const alternativeContainer = document.querySelector('.ingredient-list');
            if (alternativeContainer) {
                this.renderSelectedIngredients(alternativeContainer);
            }
            return;
        }

        if (this.config.customIngredients.length === 0) {
            container.innerHTML = `
                <div class="empty-state text-muted">
                    <i class="fas fa-plus-circle me-2"></i>
                    Select ingredients above to add them to your formula
                </div>
            `;
        } else {
            // Create simple ingredient tags with just the ingredient name
            container.innerHTML = this.config.customIngredients.map(ingredient => `
                <div class="selected-ingredient-tag custom-ingredient" style="display: inline-block; background: #28a745; color: white; padding: 8px 16px; margin: 4px 4px 4px 0; border-radius: 20px; font-size: 14px; font-weight: 500;">
                    ${ingredient}
                    <span class="remove-ingredient" data-ingredient="${ingredient}" style="margin-left: 8px; color: white; cursor: pointer; font-weight: bold;">×</span>
                </div>
            `).join('');

            // Bind remove events
            setTimeout(() => {
                const removeButtons = container.querySelectorAll('.remove-ingredient');
                removeButtons.forEach(btn => {
                    btn.addEventListener('click', (e) => {
                        e.preventDefault();
                        e.stopPropagation();
                        const ingredient = btn.dataset.ingredient;
                        this.removeIngredient(ingredient);

                        // Update visual state in ingredient selection
                        const ingredientItem = document.querySelector(`[data-ingredient="${ingredient}"]`);
                        if (ingredientItem) {
                            ingredientItem.classList.remove('selected');
                        }
                    });
                });
            }, 100);
        }
    }

    renderSelectedIngredients(container) {
        if (this.config.customIngredients.length === 0) {
            container.innerHTML = `
                <div class="empty-state text-muted">
                    <i class="fas fa-plus-circle me-2"></i>
                    Select ingredients above to add them to your formula
                </div>
            `;
        } else {
            container.innerHTML = this.config.customIngredients.map(ingredient => `
                <div class="selected-ingredient-tag custom-ingredient" style="display: inline-block; background: #28a745; color: white; padding: 8px 16px; margin: 4px 4px 4px 0; border-radius: 20px; font-size: 14px; font-weight: 500;">
                    ${ingredient}
                    <span class="remove-ingredient" data-ingredient="${ingredient}" style="margin-left: 8px; color: white; cursor: pointer; font-weight: bold;">×</span>
                </div>
            `).join('');
        }
    }

    bindClaimsSelection() {
        // Nutritional claims
        document.querySelectorAll('.claim-option').forEach(option => {
            option.addEventListener('click', () => {
                const claim = option.dataset.claim;

                if (option.classList.contains('selected')) {
                    option.classList.remove('selected');
                    this.removeClaim(claim);
                } else {
                    option.classList.add('selected');
                    this.addClaim(claim);
                }
            });
        });

        // Certifications
        document.querySelectorAll('.certification-option').forEach(option => {
            option.addEventListener('click', () => {
                const certification = option.dataset.cert;

                if (option.classList.contains('selected')) {
                    option.classList.remove('selected');
                    this.removeCertification(certification);
                } else {
                    option.classList.add('selected');
                    this.addCertification(certification);
                }
            });
        });
    }

    addClaim(claim) {
        if (!this.config.nutritionalClaims.includes(claim)) {
            this.config.nutritionalClaims.push(claim);
            this.updatePreview();
        }
    }

    removeClaim(claim) {
        const index = this.config.nutritionalClaims.indexOf(claim);
        if (index > -1) {
            this.config.nutritionalClaims.splice(index, 1);
            this.updatePreview();
        }
    }

    addCertification(certification) {
        if (!this.config.certifications.includes(certification)) {
            this.config.certifications.push(certification);
            this.updatePreview();
        }
    }

    removeCertification(certification) {
        const index = this.config.certifications.indexOf(certification);
        if (index > -1) {
            this.config.certifications.splice(index, 1);
            this.updatePreview();
        }
    }


    bindFinalSubmission() {
        // Validate client information before enabling buttons
        this.validateClientInfo();

        // Bind input events for real-time validation
        document.getElementById('client-name')?.addEventListener('input', () => this.validateClientInfo());
        document.getElementById('client-email')?.addEventListener('input', () => this.validateClientInfo());

        // Generate PDF
        document.getElementById('generate-concept')?.addEventListener('click', () => {
            this.generateConcept();
        });

        // Ensure PDF button is enabled when step 4 is shown
        document.addEventListener('stepChanged', (e) => {
            if (e.detail.step === 4) {
                // When step 4 is shown, always enable the PDF button if we have a base product
                const generateBtn = document.getElementById('generate-concept');
                if (generateBtn && this.config.baseProduct) {
                    generateBtn.disabled = false;
                }
            }
        });


    }

    validateClientInfo() {
        const clientName = document.getElementById('client-name')?.value.trim();
        const clientEmail = document.getElementById('client-email')?.value.trim();

        const isValidName = clientName && clientName.length > 0;
        const isValidEmailFormat = clientEmail && isValidEmail(clientEmail);

        const isValid = isValidName && isValidEmailFormat;

        // Enable/disable buttons based on validation
        const generateBtn = document.getElementById('generate-concept');

        // Always enable the PDF button if we have a base product - user can generate PDF even without client info
        if (generateBtn) {
            // Enable if we have valid client info OR if we have a base product configured
            const hasBaseProduct = this.config.baseProduct && this.config.baseProductName;
            generateBtn.disabled = !(isValid || hasBaseProduct);
        }

        return isValid;
    }

    bindPreviewUpdates() {
        // Real-time preview updates as user makes selections
        document.addEventListener('configurationChanged', () => {
            this.updatePreview();
        });
    }

    bindResetConfiguration() {
        // Reset configuration button
        document.getElementById('reset-configuration')?.addEventListener('click', () => {
            try {
                // Check if Bootstrap is available
                if (typeof bootstrap !== 'undefined' && bootstrap.Modal) {
                    const resetModalElement = document.getElementById('resetModal');
                    if (resetModalElement) {
                        const resetModal = new bootstrap.Modal(resetModalElement);
                        resetModal.show();
                    } else {
                        console.error('Reset modal element not found');
                        // Fallback: directly call reset with confirmation
                        this.showSimpleResetConfirmation();
                    }
                } else {
                    console.error('Bootstrap not available');
                    // Fallback: use browser confirm dialog
                    this.showSimpleResetConfirmation();
                }
            } catch (error) {
                console.error('Error showing reset modal:', error);
                // Fallback: use browser confirm dialog
                this.showSimpleResetConfirmation();
            }
        });

        // Confirm reset button
        document.getElementById('confirm-reset')?.addEventListener('click', () => {
            // First hide the modal BEFORE calling resetConfiguration
            try {
                const resetModalElement = document.getElementById('resetModal');
                const resetModal = bootstrap.Modal.getInstance(resetModalElement);
                if (resetModal) {
                    resetModal.hide();
                } else {
                    // If no modal instance exists, create one and hide it
                    const newModal = new bootstrap.Modal(resetModalElement);
                    newModal.hide();
                }
            } catch (error) {
                console.error('Error hiding reset modal:', error);
                // Fallback: manually remove modal backdrop and classes
                const modalBackdrop = document.querySelector('.modal-backdrop');
                if (modalBackdrop) {
                    modalBackdrop.remove();
                }
                document.body.classList.remove('modal-open');
                document.body.style.removeProperty('overflow');
                document.body.style.removeProperty('padding-right');
            }

            // Then call reset configuration
            this.resetConfiguration();
        });
    }

    showSimpleResetConfirmation() {
        // Fallback confirmation using browser confirm dialog
        const confirmed = confirm(
            'Are you sure you want to reset your entire configuration?\n\n' +
            'This will clear all selected ingredients, claims, certifications, and packaging options. ' +
            'You will need to start from the beginning.\n\n' +
            'This action cannot be undone.'
        );
        
        if (confirmed) {
            this.resetConfiguration();
        }
    }

    bindSummaryModal() {
        // Expand summary button
        document.getElementById('expand-summary')?.addEventListener('click', () => {
            this.showDetailedSummary();
        });

        // Print summary button
        document.getElementById('print-summary')?.addEventListener('click', () => {
            this.printSummary();
        });
    }

    resetConfiguration() {
        // Reset all configuration data
        this.config = {
            baseProduct: null,
            baseProductName: '',
            baseProductImage: '',
            customIngredients: [],
            ingredientPercentages: {},  // Legacy: Reset ingredient percentages
            ingredientRatios: {}, // NEW: Reset ingredient ratios
            nutritionalClaims: [],
            certifications: [],
            packaging: '',
            clientName: '',
            clientEmail: '',
            notes: ''
        };

        // Reset current step to 1 and max reached step
        this.currentStep = 1;
        this.maxStepReached = 1;
        this.cameFromBaseProduct = false;

        // Hide all steps and show step 1
        document.querySelectorAll('.creation-step').forEach(step => {
            step.classList.remove('active');
        });
        document.getElementById('step-1').classList.add('active');

        // Clear all selections
        document.querySelectorAll('.base-product-card').forEach(card => {
            card.classList.remove('selected');
        });
        document.querySelectorAll('.ingredient-category').forEach(cat => {
            cat.classList.remove('active');
        });
        document.querySelectorAll('.ingredient-item').forEach(item => {
            item.classList.remove('selected');
        });
        document.querySelectorAll('.claim-option').forEach(claim => {
            claim.classList.remove('selected');
        });
        document.querySelectorAll('.certification-option').forEach(cert => {
            cert.classList.remove('selected');
        });

        // Clear form fields
        const clientNameField = document.getElementById('client-name');
        if (clientNameField) clientNameField.value = '';
        
        const clientEmailField = document.getElementById('client-email');
        if (clientEmailField) clientEmailField.value = '';
        
        const specialNotesField = document.getElementById('special-notes');
        if (specialNotesField) specialNotesField.value = '';

        // Clear ingredient selection area
        const ingredientSelection = document.getElementById('ingredient-selection');
        if (ingredientSelection) {
            ingredientSelection.innerHTML = '';
        }
        
        const selectedIngredientsList = document.getElementById('selected-ingredients-list');
        if (selectedIngredientsList) {
            selectedIngredientsList.innerHTML = `
                <div class="empty-state text-muted">
                    <i class="fas fa-plus-circle me-2"></i>
                    Select ingredients above to add them to your formula
                </div>
            `;
        }

        // Clear Step 3 ratio inputs
        const ingredientRatiosContainer = document.getElementById('ingredient-ratios');
        if (ingredientRatiosContainer) {
            ingredientRatiosContainer.innerHTML = `
                <div class="no-ingredients-message text-center py-5" id="no-ingredients-message">
                    <i class="fas fa-exclamation-triangle fa-3x text-muted mb-3"></i>
                    <h5 class="text-muted">No ingredients selected</h5>
                    <p class="text-muted">Please go back to Step 2 and select some ingredients first.</p>
                    <button class="btn btn-outline-secondary rounded-pill px-4" id="back-to-ingredients">
                        <i class="fas fa-arrow-left me-2"></i>Back to Add Ingredients
                    </button>
                </div>
            `;
        }

        // Reset ratio summary display
        const ratioSummary = document.getElementById('ratio-summary');
        if (ratioSummary) {
            ratioSummary.style.display = 'none';
        }

        // Reset all percentage sliders and inputs
        document.querySelectorAll('.percentage-slider').forEach(slider => {
            slider.value = 0;
        });
        document.querySelectorAll('.percentage-input').forEach(input => {
            input.value = 0;
        });

        // Reset percentage progress bar
        const progressBar = document.getElementById('total-percentage-bar');
        const progressText = document.getElementById('total-percentage-text');
        if (progressBar) {
            progressBar.style.width = '0%';
            progressBar.className = 'progress-bar bg-danger';
        }
        if (progressText) {
            progressText.textContent = '0%';
            progressText.className = 'fw-bold text-danger';
        }

        // Reset button states for all steps
        const step1NextBtn = document.getElementById('step1-next');
        if (step1NextBtn) step1NextBtn.disabled = true;
        
        const step2NextBtn = document.getElementById('step2-next');
        if (step2NextBtn) step2NextBtn.disabled = false; // Enable for demo
        
        const step3NextBtn = document.getElementById('step3-next');
        if (step3NextBtn) step3NextBtn.disabled = true;
        
        const step4NextBtn = document.getElementById('step4-next');
        if (step4NextBtn) step4NextBtn.disabled = false; // Enable for demo
        
        const sendConceptBtn = document.getElementById('send-concept');
        if (sendConceptBtn) sendConceptBtn.disabled = true;

        // Remove all progress-step CSS classes before updateProgress()
        document.querySelectorAll('.progress-step').forEach(step => {
            step.classList.remove('active', 'completed', 'current', 'done', 'finished');
        });

        // Update progress and preview AFTER explicit reset
        this.updateProgress();
        this.updatePreview();

        // Show success message
        this.showResetSuccess();

        // Scroll to top
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }

    showResetSuccess() {
        // Create temporary success notification
        const notification = document.createElement('div');
        notification.className = 'alert alert-success alert-dismissible fade show position-fixed';
        notification.style.cssText = 'top: 20px; right: 20px; z-index: 1050; min-width: 300px;';
        notification.innerHTML = `
            <i class="fas fa-check-circle me-2"></i>
            Configuration reset successfully!
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;

        document.body.appendChild(notification);

        // Auto-remove after 3 seconds
        setTimeout(() => {
            if (notification.parentNode) {
                notification.remove();
            }
        }, 3000);
    }

    updatePreview() {
        const preview = document.getElementById('live-preview');
        const configSummary = document.getElementById('config-summary');

        if (this.config.baseProduct) {
            // Get base product details
            const baseCard = document.querySelector(`[data-product-id="${this.config.baseProduct}"]`);
            let baseImage = this.config.baseProductImage;

            // If no image in config, try to get it from the card
            if (!baseImage && baseCard) {
                baseImage = baseCard.querySelector('img')?.src;
            }

            // Show professional product preview
            // Note: ingredients will be loaded asynchronously for popup
            preview.innerHTML = `
                <div class="professional-preview" style="
                    background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%);
                    border-radius: 16px;
                    padding: 24px;
                    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
                    border: 1px solid rgba(102, 28, 49, 0.1);
                ">
                    <!-- Product Hero Section -->
                    <div class="product-hero text-center mb-4" style="
                        background: white;
                        border-radius: 12px;
                        padding: 20px;
                        margin-bottom: 24px;
                        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.05);
                    ">
                        <img src="${baseImage}" alt="${this.config.baseProductName}" 
                             style="
                                width: 100%;
                                max-width: 240px;
                                height: 160px;
                                object-fit: cover;
                                border-radius: 12px;
                                margin-bottom: 16px;
                                box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
                             "
                             onerror="console.error('Failed to load image:', this.src)">
                        
                        <!-- Product Name with Hover Popup -->
                        <h4 class="product-name mb-1" style="
                            color: #661c31;
                            font-weight: 700;
                            font-size: 1.3rem;
                            margin-bottom: 8px;
                            position: relative;
                            display: inline-block;
                        ">
                            <span class="hover-trigger" 
                                  style="cursor: help; border-bottom: 2px dotted rgba(102, 28, 49, 0.4);">
                                ${this.config.baseProductName}
                            </span>
                        </h4>
                        
                        ${this.config.customIngredients.length > 0 ? 
                            `<div class="customization-note" style="
                                color: #6c757d;
                                font-size: 0.9rem;
                                font-style: italic;
                            ">Enhanced with ${this.config.customIngredients.length} custom ingredient${this.config.customIngredients.length !== 1 ? 's' : ''}</div>` : ''
                        }
                    </div>

                    <!-- Configuration Sections -->
                    <div class="configuration-sections">
                        <!-- Added Ingredients -->
                        ${this.config.customIngredients.length > 0 ? `
                            <div class="config-section" style="
                                background: white;
                                border-radius: 12px;
                                padding: 20px;
                                margin-bottom: 16px;
                                border-left: 4px solid #28a745;
                                box-shadow: 0 2px 8px rgba(40, 167, 69, 0.1);
                            ">
                                <h6 style="
                                    color: #28a745;
                                    font-weight: 600;
                                    font-size: 1rem;
                                    margin-bottom: 16px;
                                    display: flex;
                                    align-items: center;
                                ">
                                    <i class="fas fa-plus-circle me-2"></i>
                                    Added Ingredients
                                </h6>
                                <div class="ingredient-pills" style="display: flex; flex-wrap: wrap; gap: 8px;">
                                    ${this.config.customIngredients.map(ingredient => {
                                        const ratioData = this.config.ingredientRatios?.[ingredient];
                                        let ratioText = '';
                                        if (ratioData) {
                                            const activeUnit = ratioData.activeUnit || 'percent';
                                            const value = ratioData[activeUnit] || 0;
                                            const unitSymbol = activeUnit === 'percent' ? '%' : 'g';
                                            if (value > 0) {
                                                ratioText = ` (${value}${unitSymbol})`;
                                            }
                                        }
                                        return `<span style="
                                            background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
                                            color: white;
                                            padding: 8px 16px;
                                            border-radius: 20px;
                                            font-size: 0.85rem;
                                            font-weight: 500;
                                            box-shadow: 0 2px 8px rgba(40, 167, 69, 0.3);
                                            border: 1px solid rgba(255, 255, 255, 0.2);
                                        ">${ingredient}${ratioText}</span>`;
                                    }).join('')}
                                </div>
                            </div>
                        ` : ''}

                        <!-- Nutritional Claims -->
                        ${this.config.nutritionalClaims.length > 0 ? `
                            <div class="config-section" style="
                                background: white;
                                border-radius: 12px;
                                padding: 20px;
                                margin-bottom: 16px;
                                border-left: 4px solid #ffc107;
                                box-shadow: 0 2px 8px rgba(255, 193, 7, 0.1);
                            ">
                                <h6 style="
                                    color: #f57c00;
                                    font-weight: 600;
                                    font-size: 1rem;
                                    margin-bottom: 16px;
                                    display: flex;
                                    align-items: center;
                                ">
                                    <i class="fas fa-award me-2"></i>
                                    Nutritional Claims
                                </h6>
                                <div class="claim-pills" style="display: flex; flex-wrap: wrap; gap: 8px;">
                                    ${this.config.nutritionalClaims.map(claim => `
                                        <span style="
                                            background: linear-gradient(135deg, #ffc107 0%, #ffca2c 100%);
                                            color: #212529;
                                            padding: 8px 16px;
                                            border-radius: 20px;
                                            font-size: 0.85rem;
                                            font-weight: 600;
                                            box-shadow: 0 2px 8px rgba(255, 193, 7, 0.3);
                                        ">${claim}</span>
                                    `).join('')}
                                </div>
                            </div>
                        ` : ''}

                        <!-- Certifications -->
                        ${this.config.certifications.length > 0 ? `
                            <div class="config-section" style="
                                background: white;
                                border-radius: 12px;
                                padding: 20px;
                                margin-bottom: 16px;
                                border-left: 4px solid #17a2b8;
                                box-shadow: 0 2px 8px rgba(23, 162, 184, 0.1);
                            ">
                                <h6 style="
                                    color: #17a2b8;
                                    font-weight: 600;
                                    font-size: 1rem;
                                    margin-bottom: 16px;
                                    display: flex;
                                    align-items: center;
                                ">
                                    <i class="fas fa-certificate me-2"></i>
                                    Certifications
                                </h6>
                                <div class="cert-pills" style="display: flex; flex-wrap: wrap; gap: 8px;">
                                    ${this.config.certifications.map(cert => `
                                        <span style="
                                            background: linear-gradient(135deg, #17a2b8 0%, #20c997 100%);
                                            color: white;
                                            padding: 8px 16px;
                                            border-radius: 20px;
                                            font-size: 0.85rem;
                                            font-weight: 500;
                                            box-shadow: 0 2px 8px rgba(23, 162, 184, 0.3);
                                            border: 1px solid rgba(255, 255, 255, 0.2);
                                        ">${cert}</span>
                                    `).join('')}
                                </div>
                            </div>
                        ` : ''}
                    </div>
                </div>
            `;

            // Hide the duplicate configuration summary section
            configSummary.style.display = 'none';
            
            // Create and setup global popup with async ingredients loading
            this.createGlobalPopupAsync();
            
            // Setup popup handlers after DOM update
            this.setupPopupHandlers();
        } else {
            preview.innerHTML = `
                <div class="preview-placeholder">
                    <i class="fas fa-image fa-3x text-muted mb-3"></i>
                    <p class="text-muted">Select a base product to see your creation come to life</p>
                </div>
            `;
            configSummary.style.display = 'none';
        }
    }

    async createGlobalPopupAsync() {
        console.log('=== DEBUG: Creating popup with async ingredient loading');
        console.log('=== DEBUG: Base product ID:', this.config.baseProduct);
        
        // Remove existing popup if present
        const existingPopup = document.getElementById('global-ingredients-popup');
        if (existingPopup) {
            existingPopup.remove();
        }
        
        // Create new popup element with loading state
        const popup = document.createElement('div');
        popup.id = 'global-ingredients-popup';
        popup.className = 'ingredients-tooltip';
        
        popup.style.cssText = `
            display: none;
            position: fixed;
            z-index: 99999;
            background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
            color: white;
            padding: 20px;
            border-radius: 12px;
            font-size: 0.9rem;
            min-width: 400px;
            max-width: 500px;
            line-height: 1.6;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5), 0 0 0 1px rgba(255, 255, 255, 0.1);
            word-wrap: break-word;
            white-space: normal;
            pointer-events: none;
            backdrop-filter: blur(10px);
            font-family: 'Montserrat', sans-serif;
        `;
        
        popup.innerHTML = `
            <div style="font-weight: 700; margin-bottom: 12px; color: #ff4143; font-size: 1rem;">
                <i class="fas fa-list-ul" style="margin-right: 8px;"></i>Base Ingredients:
            </div>
            <div class="ingredients-content" style="color: rgba(255, 255, 255, 0.95); font-weight: 400;">
                <i class="fas fa-spinner fa-spin me-2"></i>Loading ingredients...
            </div>
        `;
        
        // Append to document body
        document.body.appendChild(popup);
        
        // Load ingredients asynchronously
        try {
            const ingredients = await this.getBaseProductIngredients();
            console.log('=== DEBUG: Async loaded ingredients:', ingredients);
            
            const content = popup.querySelector('.ingredients-content');
            if (content) {
                content.innerHTML = ingredients.length > 0 
                    ? ingredients.map(ing => ing.display || ing).join(', ')
                    : 'No ingredients available';
            }
        } catch (error) {
            console.error('=== DEBUG: Failed to load ingredients for popup:', error);
            const content = popup.querySelector('.ingredients-content');
            if (content) {
                content.innerHTML = 'Failed to load ingredients';
            }
        }
        
        console.log('=== DEBUG: Popup created and ingredients loading started');
    }

    setupPopupHandlers() {
        // Add event listeners for hover popup after DOM update
        setTimeout(() => {
            const trigger = document.querySelector('.hover-trigger');
            const popup = document.getElementById('global-ingredients-popup');
            
            if (trigger && popup) {
                console.log('Setting up popup handlers');
                
                trigger.addEventListener('mouseenter', (e) => {
                    console.log('Mouse enter - showing popup');
                    this.showIngredientsPopup(e.target, popup);
                });
                
                trigger.addEventListener('mouseleave', () => {
                    console.log('Mouse leave - hiding popup');
                    popup.style.display = 'none';
                });
            } else {
                console.log('Popup elements not found:', { trigger, popup });
            }
        }, 100);
    }
    
    showIngredientsPopup(triggerElement, popup) {
        // Get trigger element position
        const rect = triggerElement.getBoundingClientRect();
        const popupWidth = 500; // max width
        const popupHeight = 120; // estimated height
        
        // Calculate position - prefer below the element, but adjust if needed
        let left = rect.left + (rect.width / 2) - (popupWidth / 2);
        let top = rect.bottom + 10;
        
        // Prevent horizontal cutoff
        if (left < 10) {
            left = 10;
        } else if (left + popupWidth > window.innerWidth - 10) {
            left = window.innerWidth - popupWidth - 10;
        }
        
        // Prevent vertical cutoff - show above if needed
        if (top + popupHeight > window.innerHeight - 10) {
            top = rect.top - popupHeight - 10;
        }
        
        // Position and show popup
        popup.style.left = left + 'px';
        popup.style.top = top + 'px';
        popup.style.display = 'block';
        
        console.log('Popup positioned at:', { left, top });
    }

    showBaseProductPopup(event) {
        const popup = document.getElementById('global-ingredients-popup');
        if (popup && event && event.target) {
            this.showIngredientsPopup(event.target, popup);
            console.log('Showing popup manually');
        }
    }

    hideBaseProductPopup() {
        const popup = document.getElementById('global-ingredients-popup');
        if (popup) {
            popup.style.display = 'none';
            console.log('Hiding popup manually');
        }
    }

    updateConfigurationSummary() {
        // Base product
        const summaryBase = document.getElementById('summary-base');
        const summaryBaseName = document.getElementById('summary-base-name');
        if (this.config.baseProduct && summaryBase && summaryBaseName) {
            summaryBase.style.display = 'block';
            summaryBaseName.textContent = this.config.baseProductName;
        } else if (summaryBase) {
            summaryBase.style.display = 'none';
        }

        // Custom Ingredients
        const summaryIngredients = document.getElementById('summary-ingredients');
        const summaryIngredientsList = document.getElementById('summary-ingredients-list');
        if (this.config.customIngredients.length > 0 && summaryIngredients && summaryIngredientsList) {
            summaryIngredients.style.display = 'block';
            summaryIngredientsList.innerHTML = this.config.customIngredients.map(ingredient => 
                `<span class="badge bg-success me-1 mb-1">${ingredient}</span>`
            ).join('');
        } else if (summaryIngredients) {
            summaryIngredients.style.display = 'none';
        }

        // Claims
        const summaryClaims = document.getElementById('summary-claims');
        const summaryClaimsList = document.getElementById('summary-claims-list');
        if (this.config.nutritionalClaims.length > 0 && summaryClaims && summaryClaimsList) {
            summaryClaims.style.display = 'block';
            summaryClaimsList.innerHTML = this.config.nutritionalClaims.map(claim => 
                `<span class="badge bg-warning me-1 mb-1">${claim}</span>`
            ).join('');
        } else if (summaryClaims) {
            summaryClaims.style.display = 'none';
        }

        // Certifications
        const summaryCertifications = document.getElementById('summary-certifications');
        const summaryCertificationsList = document.getElementById('summary-certifications-list');
        if (this.config.certifications.length > 0 && summaryCertifications && summaryCertificationsList) {
            summaryCertifications.style.display = 'block';
            summaryCertificationsList.innerHTML = this.config.certifications.map(cert => 
                `<span class="badge bg-info me-1 mb-1">${cert}</span>`
            ).join('');
        } else if (summaryCertifications) {
            summaryCertifications.style.display = 'none';
        }

        // Packaging
    }

    getFallbackIngredients() {
        // Try to fetch ingredients from the product details or a known list
        console.log('=== DEBUG: Attempting fallback ingredient loading');
        
        // Common fallback ingredients for different product types
        const fallbackIngredientsByName = {
            'classic': ['Oats', 'Wheat flakes', 'Raisins', 'Sunflower seeds', 'Hazelnuts'],
            'muesli': ['Rolled oats', 'Dried fruits', 'Nuts', 'Seeds'],
            'granola': ['Oats', 'Honey', 'Nuts', 'Dried berries'],
            'overnight': ['Oats', 'Chia seeds', 'Dried fruits', 'Coconut'],
            'protein': ['Oats', 'Protein powder', 'Nuts', 'Seeds']
        };
        
        const productName = this.config.baseProductName?.toLowerCase() || '';
        
        // Try to match product name to fallback ingredients
        for (const [key, ingredients] of Object.entries(fallbackIngredientsByName)) {
            if (productName.includes(key)) {
                console.log('=== DEBUG: Using fallback ingredients for', key, ':', ingredients);
                return ingredients;
            }
        }
        
        // Default fallback
        const defaultIngredients = ['Rolled oats', 'Mixed dried fruits', 'Nuts and seeds', 'Natural flavors'];
        console.log('=== DEBUG: Using default fallback ingredients:', defaultIngredients);
        return defaultIngredients;
    }

    async getBaseProductIngredients() {
        console.log('=== DEBUG: Getting base product ingredients for:', this.config.baseProduct);
        if (!this.config.baseProduct) {
            console.log('=== DEBUG: No base product selected');
            return [];
        }

        // Try to fetch real ingredients from backend API
        try {
            const response = await fetch(`/api/product/${this.config.baseProduct}/ingredients`);
            if (response.ok) {
                const data = await response.json();
                console.log('=== DEBUG: Backend API response:', data);
                
                if (data.success && data.ingredients && Array.isArray(data.ingredients)) {
                    const realIngredients = data.ingredients.map(ingredient => {
                        if (typeof ingredient === 'object' && ingredient.name) {
                            // Keep structured data with status field for PDF generation
                            const structuredIngredient = {
                                name: ingredient.name,
                                percentage: ingredient.percentage || 0,
                                recipe_number: ingredient.recipe_number || null,
                                status: ingredient.status || null
                            };
                            // Also create display string for UI
                            structuredIngredient.display = ingredient.name + (ingredient.percentage > 0 ? ` (${ingredient.percentage}%)` : '');
                            return structuredIngredient;
                        } else if (typeof ingredient === 'string') {
                            return { name: ingredient, display: ingredient, status: null };
                        }
                        return null;
                    }).filter(Boolean);
                    
                    console.log('=== DEBUG: Successfully loaded real ingredients from API:', realIngredients);
                    return realIngredients;
                }
            }
        } catch (error) {
            console.error('=== DEBUG: Failed to fetch ingredients from API:', error);
        }

        // Fallback to HTML data-attributes
        const baseCard = document.querySelector(`[data-product-id="${this.config.baseProduct}"]`);
        if (baseCard) {
            const ingredientsData = baseCard.getAttribute('data-ingredients');
            console.log('=== DEBUG: Fallback to HTML data:', ingredientsData);
            
            if (ingredientsData && ingredientsData.trim() && ingredientsData !== 'null') {
                const htmlIngredients = this.parseIngredientsData(ingredientsData);
                if (htmlIngredients.length > 0) {
                    console.log('=== DEBUG: Using HTML fallback ingredients:', htmlIngredients);
                    return htmlIngredients;
                }
            }
        }

        console.log('=== DEBUG: All methods failed, using default fallback');
        return this.getFallbackIngredients();
    }

    parseIngredientsData(ingredientsData) {
        console.log('=== DEBUG: Parsing ingredients data:', ingredientsData);

        if (ingredientsData && ingredientsData !== '[]' && ingredientsData !== 'null' && ingredientsData !== 'undefined') {
            try {
                console.log('=== DEBUG: Attempting to parse ingredients data');
                // Handle malformed JSON by fixing common issues
                let cleanedData = ingredientsData;

                // Fix incomplete JSON strings
                if (cleanedData.startsWith('[{') && !cleanedData.endsWith('}]')) {
                    // Try to complete the JSON structure
                    cleanedData = cleanedData + '"}]';
                    console.log('=== DEBUG: Fixed incomplete JSON:', cleanedData);
                }

                const parsed = JSON.parse(cleanedData);
                console.log('=== DEBUG: Successfully parsed ingredients:', parsed);

                // Handle both array of objects and array of strings - RETURN ALL INGREDIENTS
                if (Array.isArray(parsed) && parsed.length > 0) {
                    const result = parsed.map(ingredient => {
                        if (typeof ingredient === 'object' && ingredient.name) {
                            return ingredient.name + (ingredient.percentage && ingredient.percentage > 0 ? ` (${ingredient.percentage}%)` : '');
                        } else if (typeof ingredient === 'string') {
                            return ingredient;
                        }
                        return 'Unknown ingredient';
                    }).filter(ing => ing && ing !== 'Unknown ingredient');

                    console.log('=== DEBUG: Successfully returning', result.length, 'ingredients:', result);
                    return result;
                }
            } catch (e) {
                console.error('=== DEBUG: Error parsing base product ingredients:', e);
                console.log('=== DEBUG: Problematic data:', ingredientsData);
            }
        }

        // Fallback: Try to extract from the card's ingredient display
        const ingredientElement = baseCard.querySelector('.product-ingredients .ingredient-item');
        if (ingredientElement) {
            const ingredientText = ingredientElement.textContent.trim();
            console.log('=== DEBUG: Fallback - extracted ingredient text:', ingredientText);

            if (ingredientText && ingredientText !== '...') {
                // Split by comma and clean up, remove ellipsis
                const ingredients = ingredientText.split(',')
                    .map(ing => ing.trim())
                    .filter(ing => ing && ing !== '...' && ing !== '…' && ing.length > 0);
                console.log('=== DEBUG: Fallback ingredients:', ingredients);
                return ingredients;
            }
        }

        console.log('=== DEBUG: No ingredients found, using fallback method');
        return this.getFallbackIngredients();
    }

    getBaseProductClaims() {
        if (!this.config.baseProduct) return [];

        const baseCard = document.querySelector(`[data-product-id="${this.config.baseProduct}"]`);
        const claimsData = baseCard?.getAttribute('data-claims');

        if (claimsData) {
            try {
                return JSON.parse(claimsData);
            } catch (e) {
                console.error('Error parsing base product claims:', e);
                return [];
            }
        }

        return [];
    }

    getBaseProductCertifications() {
        if (!this.config.baseProduct) return [];

        const baseCard = document.querySelector(`[data-product-id="${this.config.baseProduct}"]`);
        const certificationsData = baseCard?.getAttribute('data-certifications');

        if (certificationsData) {
            try {
                return JSON.parse(certificationsData);
            } catch (e) {
                console.error('Error parsing base product certifications:', e);
                return [];
            }
        }

        return [];
    }

    showStep(stepNumber) {
        // Hide all steps
        document.querySelectorAll('.creation-step').forEach(step => {
            step.classList.remove('active');
        });

        // Show target step
        document.getElementById(`step-${stepNumber}`).classList.add('active');

        // Update current step
        this.currentStep = stepNumber;

        // Update progress
        this.updateProgress();

        // Special handling for different steps
        if (this.currentStep === 3) {
            // Step 3: Setup ingredient percentages
            this.setupIngredientRatios();
        } else if (this.currentStep === 5) {
            // Step 5: Review & Send
            this.validateClientInfo();

            // Always enable PDF button if we have a base product
            const generateBtn = document.getElementById('generate-concept');
            if (generateBtn && this.config.baseProduct) {
                generateBtn.disabled = false;
            }
        }

        // Scroll to top
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }

    nextStep() {
        if (this.currentStep < this.totalSteps) {
            // Hide current step
            document.getElementById(`step-${this.currentStep}`).classList.remove('active');

            // Show next step
            this.currentStep++;
            
            // Update maxStepReached if we're progressing forward
            if (this.currentStep > this.maxStepReached) {
                this.maxStepReached = this.currentStep;
            }
            
            document.getElementById(`step-${this.currentStep}`).classList.add('active');

            // Update progress
            this.updateProgress();

            // Special handling for different steps
            if (this.currentStep === 3) {
                // Step 3: Setup ingredient percentages
                this.setupIngredientRatios();
            } else if (this.currentStep === 5) {
                // Step 5: Review & Send (formerly step 4)
                this.validateClientInfo();

                // Always enable PDF button if we have a base product
                const generateBtn = document.getElementById('generate-concept');
                if (generateBtn && this.config.baseProduct) {
                    generateBtn.disabled = false;
                }
            }

            // Scroll to top
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }
    }

    previousStep() {
        if (this.currentStep > 1) {
            // Hide current step
            document.getElementById(`step-${this.currentStep}`).classList.remove('active');

            // Show previous step
            this.currentStep--;
            document.getElementById(`step-${this.currentStep}`).classList.add('active');

            // If going back to step 1, show current selection but allow changing it
            if (this.currentStep === 1) {
                // Show current selection if any
                if (this.config.baseProduct) {
                    const currentCard = document.querySelector(`[data-product-id="${this.config.baseProduct}"]`);
                    if (currentCard) {
                        document.querySelectorAll('.base-product-card').forEach(card => {
                            card.classList.remove('selected');
                        });
                        currentCard.classList.add('selected');
                        document.getElementById('step1-next').disabled = false;
                    }
                }
                this.cameFromBaseProduct = false;
            }

            // Update progress
            this.updateProgress();

            // Scroll to top
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }
    }

    updateProgress() {
        document.querySelectorAll('.progress-step').forEach((step, index) => {
            // Remove ALL possible state classes first (including template-added ones)
            step.classList.remove('active', 'completed', 'current', 'done', 'finished');

            // currentStep is 1-based, but index is 0-based
            // So we need to compare with index + 1
            const stepNumber = index + 1;

            const stepCircle = step.querySelector('.step-circle');
            const stepLabel = step.querySelector('.step-label');

            // Reset all steps to default state first
            if (stepCircle) {
                stepCircle.style.background = '#e9ecef';
                stepCircle.style.color = '#6c757d';
                stepCircle.style.borderColor = '#e9ecef';
                stepCircle.style.transform = 'scale(1)';
            }
            if (stepLabel) {
                stepLabel.style.color = '#6c757d';
                stepLabel.style.fontWeight = 'normal';
            }

            // Mark current step as active
            if (stepNumber === this.currentStep) {
                step.classList.add('active');
                if (stepCircle) {
                    stepCircle.style.background = '#ff4143';
                    stepCircle.style.color = '#661c31';
                    stepCircle.style.borderColor = '#ff4143';
                    stepCircle.style.transform = 'scale(1.1)';
                }
                if (stepLabel) {
                    stepLabel.style.color = '#ff4143';
                    stepLabel.style.fontWeight = '600';
                }
            }

            // Mark previous steps as completed
            if (stepNumber < this.currentStep) {
                step.classList.add('completed');
                if (stepCircle) {
                    stepCircle.style.background = '#28a745';
                    stepCircle.style.color = 'white';
                    stepCircle.style.borderColor = '#28a745';
                }
                if (stepLabel) {
                    stepLabel.style.color = '#28a745';
                    stepLabel.style.fontWeight = '600';
                }
                // Change icon to checkmark for completed steps
                const icon = step.querySelector('.step-circle i');
                if (icon) {
                    icon.className = 'fas fa-check';
                }
            } 
            // Mark future visited steps as clickable/accessible
            else if (stepNumber > this.currentStep && stepNumber <= this.maxStepReached) {
                step.classList.add('visited');
                if (stepCircle) {
                    stepCircle.style.background = '#6f42c1'; // Purple for visited but not current
                    stepCircle.style.color = 'white';
                    stepCircle.style.borderColor = '#6f42c1';
                    stepCircle.style.cursor = 'pointer';
                }
                if (stepLabel) {
                    stepLabel.style.color = '#6f42c1';
                    stepLabel.style.fontWeight = '500';
                }
                // Keep original icons for visited future steps
                const icon = step.querySelector('.step-circle i');
                if (icon) {
                    switch(index) {
                        case 0: // Step 1: Choose Base
                            icon.className = 'fas fa-cogs';
                            break;
                        case 1: // Step 2: Add Ingredients
                            icon.className = 'fas fa-plus';
                            break;
                        case 2: // Step 3: Ingredient Ratios
                            icon.className = 'fas fa-percentage';
                            break;
                        case 3: // Step 4: Select Claims
                            icon.className = 'fas fa-award';
                            break;
                        case 4: // Step 5: Review & Send
                            icon.className = 'fas fa-check';
                            break;
                    }
                }
            } else {
                // Restore original icon for non-completed steps
                const icon = step.querySelector('.step-circle i');
                if (icon) {
                    switch(index) {
                        case 0: // Step 1: Choose Base
                            icon.className = 'fas fa-cogs';
                            break;
                        case 1: // Step 2: Add Ingredients
                            icon.className = 'fas fa-plus';
                            break;
                        case 2: // Step 3: Ingredient Ratios
                            icon.className = 'fas fa-percentage';
                            break;
                        case 3: // Step 4: Select Claims
                            icon.className = 'fas fa-award';
                            break;
                        case 4: // Step 5: Review & Send
                            icon.className = 'fas fa-check';
                            break;
                    }
                }
            }
        });

        // Update progress lines
        document.querySelectorAll('.progress-line').forEach((line, index) => {
            // Line connects step (index + 1) to step (index + 2)
            const lineConnectsToStep = index + 2;
            
            if (lineConnectsToStep <= this.currentStep) {
                // Line to completed or current step - green
                line.style.backgroundColor = '#28a745';
            } else if (lineConnectsToStep <= this.maxStepReached) {
                // Line to previously visited step - purple
                line.style.backgroundColor = '#6f42c1';
            } else {
                // Line to unvisited step - gray
                line.style.backgroundColor = '#e9ecef';
            }
        });

        // Update layout based on current step
        this.updateLayoutForStep();
        
        // Update global navigation buttons
        this.updateGlobalNavigation();
    }

    updateGlobalNavigation() {
        const globalBackBtn = document.getElementById('global-back-btn');
        const globalNextBtn = document.getElementById('global-next-btn');
        const globalNextText = document.getElementById('global-next-text');
        const globalSaveDraftBtn = document.getElementById('global-save-draft-btn');
        const globalGenerateBtn = document.getElementById('global-generate-btn');
        
        // Show/hide back button (not shown on step 1)
        if (globalBackBtn) {
            globalBackBtn.style.display = this.currentStep > 1 ? 'inline-flex' : 'none';
        }
        
        // Update next button text and visibility based on current step
        if (globalNextBtn && globalNextText) {
            if (this.currentStep === 1) {
                globalNextText.textContent = 'Continue to Ingredients';
                globalNextBtn.style.display = 'inline-flex';
                globalNextBtn.disabled = !this.config.baseProduct;
            } else if (this.currentStep === 2) {
                globalNextText.textContent = 'Continue to Ratios';
                globalNextBtn.style.display = 'inline-flex';
                globalNextBtn.disabled = false;
            } else if (this.currentStep === 3) {
                globalNextText.textContent = 'Continue to Claims';
                globalNextBtn.style.display = 'inline-flex';
                globalNextBtn.disabled = false;
            } else if (this.currentStep === 4) {
                globalNextText.textContent = 'Review & Finalize';
                globalNextBtn.style.display = 'inline-flex';
                globalNextBtn.disabled = false;
            } else if (this.currentStep === 5) {
                // Step 5: Show save draft and generate buttons, hide next
                globalNextBtn.style.display = 'none';
                if (globalSaveDraftBtn) globalSaveDraftBtn.style.display = 'inline-flex';
                if (globalGenerateBtn) {
                    globalGenerateBtn.style.display = 'inline-flex';
                    globalGenerateBtn.disabled = !this.config.baseProduct;
                }
            }
        }
        
        // Hide save draft and generate buttons on steps 1-4
        if (this.currentStep < 5) {
            if (globalSaveDraftBtn) globalSaveDraftBtn.style.display = 'none';
            if (globalGenerateBtn) globalGenerateBtn.style.display = 'none';
        }
    }

    updateLayoutForStep() {
        const leftPanel = document.getElementById('left-panel');
        const rightPanel = document.getElementById('right-panel');

        if (this.currentStep === 4) {
            // Review & Send step: 50/50 layout
            leftPanel.className = 'col-lg-6';
            rightPanel.className = 'col-lg-6';
        } else {
            // All other steps: 2/3 to 1/3 layout
            leftPanel.className = 'col-lg-8';
            rightPanel.className = 'col-lg-4';
        }
    }



    showDetailedSummary() {
        const detailedSummary = document.getElementById('detailed-summary');

        const baseProductIngredients = this.getBaseProductIngredients();
        const baseProductClaims = this.getBaseProductClaims();
        const baseProductCertifications = this.getBaseProductCertifications();

        detailedSummary.innerHTML = `
            <div class="summary-section">
                <h6><i class="fas fa-box-open me-2"></i>Base Product Information</h6>
                <div class="summary-highlight">
                    <h6>Selected Base Product</h6>
                    <div class="component-list">
                        <span class="component-item base">${this.config.baseProductName}</span>
                    </div>
                </div>

                ${baseProductIngredients.length > 0 ? `
                    <div class="mb-3">
                        <strong>Base Ingredients (${baseProductIngredients.length}):</strong>
                        <div class="component-list">
                            ${baseProductIngredients.map(ingredient => 
                                `<span class="component-item base">${ingredient.display || ingredient}</span>`
                            ).join('')}
                        </div>
                    </div>
                ` : ''}

                ${baseProductClaims.length > 0 ? `
                    <div class="mb-3">
                        <strong>Base Claims (${baseProductClaims.length}):</strong>
                        <div class="component-list">
                            ${baseProductClaims.map(claim => 
                                `<span class="component-item base">${claim}</span>`
                            ).join('')}
                        </div>
                    </div>
                ` : ''}

                ${baseProductCertifications.length > 0 ? `
                    <div class="mb-3">
                        <strong>Base Certifications (${baseProductCertifications.length}):</strong>
                        <div class="component-list">
                            ${baseProductCertifications.map(cert => 
                                `<span class="component-item base">${cert}</span>`
                            ).join('')}
                        </div>
                    </div>
                ` : ''}
            </div>

            ${this.config.customIngredients.length > 0 ? `
                <div class="summary-section">
                    <h6><i class="fas fa-plus me-2"></i>Custom Ingredients</h6>
                    <div class="component-list">
                        ${this.config.customIngredients.map(ingredient => 
                            `<span class="component-item ingredient">${ingredient}</span>`
                        ).join('')}
                    </div>
                    <p class="text-muted mt-2">Added ${this.config.customIngredients.length} custom ingredients to enhance the base recipe.</p>
                </div>
            ` : ''}

            ${this.config.nutritionalClaims.length > 0 ? `
                <div class="summary-section">
                    <h6><i class="fas fa-award me-2"></i>Additional Claims</h6>
                    <div class="component-list">
                        ${this.config.nutritionalClaims.map(claim => 
                            `<span class="component-item claim">${claim}</span>`
                        ).join('')}
                    </div>
                    <p class="text-muted mt-2">Selected ${this.config.nutritionalClaims.length} additional nutritional claims.</p>
                </div>
            ` : ''}

            ${this.config.certifications.length > 0 ? `
                <div class="summary-section">
                    <h6><i class="fas fa-certificate me-2"></i>Additional Certifications</h6>
                    <div class="component-list">
                        ${this.config.certifications.map(cert => 
                            `<span class="component-item certification">${cert}</span>`
                        ).join('')}
                    </div>
                    <p class="text-muted mt-2">Added ${this.config.certifications.length} additional certifications.</p>
                </div>
            ` : ''}


            <div class="summary-section">
                <h6><i class="fas fa-chart-bar me-2"></i>Configuration Summary</h6>
                <div class="row">
                    <div class="col-md-3">
                        <div class="text-center">
                            <div class="h4 text-primary">${baseProductIngredients.length + this.config.customIngredients.length}</div>
                            <div class="text-muted">Total Ingredients</div>
                        </div>
                    </div>
                    <div class="col-md-3">
                        <div class="text-center">
                            <div class="h4 text-success">${baseProductClaims.length + this.config.nutritionalClaims.length}</div>
                            <div class="text-muted">Total Claims</div>
                        </div>
                    </div>
                    <div class="col-md-3">
                        <div class="text-center">
                            <div class="h4 text-info">${baseProductCertifications.length + this.config.certifications.length}</div>
                            <div class="text-muted">Total Certifications</div>
                        </div>
                    </div>
                </div>
            </div>
        `;

        const summaryModal = new bootstrap.Modal(document.getElementById('summaryModal'));
        summaryModal.show();
    }

    printSummary() {
        const printContent = document.getElementById('detailed-summary').innerHTML;
        const printWindow = window.open('', '_blank');

        printWindow.document.write(`
            <html>
                <head>
                    <title>Product Configuration Summary</title>
                    <style>
                        body { font-family: Arial, sans-serif; margin: 20px; }
                        .summary-section { margin-bottom: 20px; border: 1px solid #ddd; padding: 15px; border-radius: 5px; }
                        .component-item { display: inline-block; margin: 2px; padding: 5px 10px; background: #f0f0f0; border-radius: 15px; font-size: 12px; }
                        .component-item.base { background: #007bff; color: white; }
                        .component-item.ingredient { background: #28a745; color: white; }
                        .component-item.claim { background: #ffc107; color: black; }
                        .component-item.certification { background: #17a2b8; color: white; }
                        h6 { color: #333; border-bottom: 1px solid #ddd; padding-bottom: 5px; }
                        @media print { .no-print { display: none; } }
                    </style>
                </head>
                <body>
                    <h2>Brüggen Co-Creation Lab - Product Configuration Summary</h2>
                    <div class="print-date">Generated on: ${new Date().toLocaleDateString()}</div>
                    <hr>
                    ${printContent}
                </body>
            </html>
        `);

        printWindow.document.close();
        printWindow.print();
    }

    async generateConcept() {
        const generateBtn = document.getElementById('generate-concept');
        const sendBtn = document.getElementById('send-concept');

        // Ensure we have the latest client information
        const clientName = document.getElementById('client-name');
        const clientEmail = document.getElementById('client-email');
        const specialNotes = document.getElementById('special-notes');

        this.config.clientName = clientName?.value || 'Draft Concept';
        this.config.clientEmail = clientEmail?.value || 'draft@example.com';
        this.config.notes = specialNotes?.value || '';

        // Get base product details to include in PDF
        const baseProductIngredients = this.getBaseProductIngredients();
        const baseProductClaims = this.getBaseProductClaims();
        const baseProductCertifications = this.getBaseProductCertifications();

        // Create enhanced config with base product details for PDF
        const enhancedConfig = {
            ...this.config,
            baseProductName: this.config.baseProductName,
            baseProductImage: this.config.baseProductImage,
            baseIngredients: baseProductIngredients,
            baseClaims: baseProductClaims,
            baseCertifications: baseProductCertifications,
            customIngredients: this.config.customIngredients || [],
            nutritionalClaims: this.config.nutritionalClaims || [],
            certifications: this.config.certifications || [],
            notes: this.config.notes || ''
        };

        try {
            showLoading(generateBtn);

            const response = await fetch('/cocreation/save_concept', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    session_id: this.sessionId,
                    client_name: this.config.clientName,
                    client_email: this.config.clientEmail,
                    product_config: enhancedConfig
                })
            });

            const result = await response.json();

            if (result.success) {
                showToast('PDF wird heruntergeladen...', 'success');

                // Automatically trigger download immediately
                const link = document.createElement('a');
                link.href = result.pdf_url;
                link.download = 'bruggen_concept.pdf';
                link.target = '_blank';
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);

                // Update download link for manual access if needed
                const downloadBtn = document.getElementById('download-pdf-btn');
                if (downloadBtn) {
                    downloadBtn.href = result.pdf_url;
                    downloadBtn.download = 'bruggen_concept.pdf';
                }
            } else {
                throw new Error(result.message || 'Failed to generate PDF');
            }

        } catch (error) {
            console.error('Error generating concept:', error);
            showToast('Error generating PDF: ' + error.message, 'danger');
        } finally {
            hideLoading(generateBtn);
        }
    }

    async sendConcept() {
        const sendBtn = document.getElementById('send-concept');

        try {
            showLoading(sendBtn);

            const response = await fetch('/cocreation/send_email', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    session_id: this.sessionId
                })
            });

            const result = await response.json();

            if (result.success) {
                showToast(result.message, 'success');
                this.showSuccessModal('Concept sent successfully to your client!');
            } else {
                throw new Error(result.message || 'Failed to send email');
            }

        } catch (error) {
            console.error('Error sending concept:', error);
            showToast('Error sending email: ' + error.message, 'danger');
        } finally {
            hideLoading(sendBtn);
        }
    }

    showSuccessAnimation(element) {
        element.style.transform = 'scale(1.1)';
        element.style.transition = 'all 0.2s ease';

        setTimeout(() => {
            element.style.transform = 'scale(1)';
        }, 200);
    }

    showSuccessModal(message) {
        document.getElementById('success-message').textContent = message;
        new bootstrap.Modal(document.getElementById('successModal')).show();
    }
}

// Utility function for email validation (if not already defined)
function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

// Custom drag and drop functionality for touch devices
class TouchDragDrop {
    constructor() {
        this.draggedElement = null;
        this.touchStartPos = { x: 0, y: 0 };
        this.dragThreshold = 10;
    }

    init() {
        this.bindTouchEvents();
    }

    bindTouchEvents() {
        document.addEventListener('touchstart', this.handleTouchStart.bind(this), { passive: false });
        document.addEventListener('touchmove', this.handleTouchMove.bind(this), { passive: false });
        document.addEventListener('touchend', this.handleTouchEnd.bind(this), { passive: false });
    }

    handleTouchStart(e) {
        const touch = e.touches[0];
        this.touchStartPos = { x: touch.clientX, y: touch.clientY };

        // Check if touch started on a draggable element
        const draggable = e.target.closest('.draggable');
        if (draggable) {
            this.draggedElement = draggable;
            draggable.classList.add('dragging');
        }
    }

    handleTouchMove(e) {
        if (!this.draggedElement) return;

        e.preventDefault();
        const touch = e.touches[0];
        const deltaX = touch.clientX - this.touchStartPos.x;
        const deltaY = touch.clientY - this.touchStartPos.y;

        // Only start visual dragging if moved beyond threshold
        if (Math.abs(deltaX) > this.dragThreshold || Math.abs(deltaY) > this.dragThreshold) {
            this.draggedElement.style.transform = `translate(${deltaX}px, ${deltaY}px)`;
            this.draggedElement.style.zIndex = '1000';
            this.draggedElement.style.opacity = '0.8';
        }
    }

    handleTouchEnd(e) {
        if (!this.draggedElement) return;

        const touch = e.changedTouches[0];
        const elementBelow = document.elementFromPoint(touch.clientX, touch.clientY);
        const dropZone = elementBelow?.closest('.drop-zone');

        if (dropZone) {
            // Handle drop
            this.handleDrop(this.draggedElement, dropZone);
        }

        // Reset dragged element
        this.draggedElement.style.transform = '';
        this.draggedElement.style.zIndex = '';
        this.draggedElement.style.opacity = '';
        this.draggedElement.classList.remove('dragging');
        this.draggedElement = null;
    }

    handleDrop(element, dropZone) {
        // Implement drop logic based on your needs
        const ingredient = element.dataset.ingredient;
        if (ingredient && dropZone.classList.contains('ingredient-drop-zone')) {
            // Add ingredient to selection
            coCreationLab.addIngredient(ingredient);
        }
    }
}

// Initialize touch drag and drop for tablet support
const touchDragDrop = new TouchDragDrop();
touchDragDrop.init();