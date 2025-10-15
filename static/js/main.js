/**
 * Brüggen Innovation Catalogue - Main JavaScript
 * Handles global functionality, animations, and interactions
 */

document.addEventListener('DOMContentLoaded', function() {

    // Initialize global functionality
    initializeAnimations();
    initializeFloatingCards();
    initializeTooltips();
    initializeScrollEffects();
    initializeFormValidation();
    initializeTouchGestures();

    /**
     * Initialize floating cards animation
     */
    function initializeFloatingCards() {
        const floatingCards = document.querySelectorAll('.floating-card');
        console.log(`Found ${floatingCards.length} floating cards to animate`);

        floatingCards.forEach((card, index) => {
            // Ensure the card has the proper animation
            card.style.animation = 'float 4s ease-in-out infinite';

            // Use data attribute for delay or fall back to index-based delay
            const delay = card.dataset.floatDelay || (index * 0.8);
            card.style.animationDelay = `${delay}s`;

            // Add a subtle initial transform to make sure the animation is visible
            card.style.transform = 'translateY(0px)';

            // Add hover interactions
            card.addEventListener('mouseenter', () => {
                card.style.animationPlayState = 'paused';
                card.style.transform = 'translateY(-10px) scale(1.05)';
                card.style.transition = 'transform 0.3s ease';
            });

            card.addEventListener('mouseleave', () => {
                card.style.animationPlayState = 'running';
                card.style.transform = '';
                card.style.transition = '';
            });

            // Force a repaint to ensure animation starts
            card.offsetHeight;
        });

        // Add a debug indicator when animations are active
        if (floatingCards.length > 0) {
            console.log('Floating card animations initialized successfully');
        }
    }

    /**
     * Initialize entrance animations
     */
    function initializeAnimations() {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting && entry.target && entry.target.classList && typeof entry.target.classList.add === 'function') {
                    entry.target.style.animationDelay = `${Math.random() * 0.5}s`;
                    entry.target.classList.add('fade-in-up');
                }
            });
        }, {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        });

        const floatingCards = document.querySelectorAll('.floating-card');
        if (floatingCards.length > 0) {
            floatingCards.forEach(card => {
                if (card) {
                    observer.observe(card);
                }
            });
        }
        console.log(`Found ${floatingCards.length} floating cards to animate`);

        /**
         * Initialize Bootstrap tooltips
         */
    }
    function initializeTooltips() {
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }

    /**
     * Initialize scroll effects
     */
    function initializeScrollEffects() {
        let lastScrollTop = 0;
        const navbar = document.querySelector('.navbar');

        // Safety check for navbar element
        if (!navbar) {
            console.warn('Navbar element not found');
            return;
        }

        window.addEventListener('scroll', function() {
            const scrollTop = window.pageYOffset || document.documentElement.scrollTop;

            // Add shadow to navbar on scroll
            if (scrollTop > 10 && navbar.classList) {
                navbar.classList.add('shadow');
            } else if (navbar.classList) {
                navbar.classList.remove('shadow');
            }

            // Hide/show navbar on scroll (for mobile)
            if (window.innerWidth <= 768 && navbar.style) {
                if (scrollTop > lastScrollTop && scrollTop > 100) {
                    navbar.style.transform = 'translateY(-100%)';
                } else {
                    navbar.style.transform = 'translateY(0)';
                }
            }

            lastScrollTop = scrollTop;
        }, { passive: true });
    }

    /**
     * Initialize form validation
     */
    function initializeFormValidation() {
        const forms = document.querySelectorAll('.needs-validation');

        forms.forEach(form => {
            if (!form || !form.addEventListener) return;

            form.addEventListener('submit', function(event) {
                if (!form.checkValidity()) {
                    event.preventDefault();
                    event.stopPropagation();

                    // Focus on first invalid field
                    const firstInvalid = form.querySelector(':invalid');
                    if (firstInvalid) {
                        firstInvalid.focus();
                        firstInvalid.scrollIntoView({ behavior: 'smooth', block: 'center' });
                    }
                }

                if (form.classList) {
                    form.classList.add('was-validated');
                }
            });
        });
    }

    /**
     * Initialize touch gestures for tablets
     */
    function initializeTouchGestures() {
        let startX, startY, distX, distY;
        const threshold = 150;
        const restraint = 100;
        const allowedTime = 300;
        let elapsedTime, startTime;

        document.addEventListener('touchstart', function(e) {
            const touchobj = e.changedTouches[0];
            startX = touchobj.pageX;
            startY = touchobj.pageY;
            startTime = new Date().getTime();
        }, { passive: true });

        document.addEventListener('touchend', function(e) {
            const touchobj = e.changedTouches[0];
            distX = touchobj.pageX - startX;
            distY = touchobj.pageY - startY;
            elapsedTime = new Date().getTime() - startTime;

            if (elapsedTime <= allowedTime) {
                // Swipe right - go back
                if (distX >= threshold && Math.abs(distY) <= restraint) {
                    const backButton = document.querySelector('[onclick="window.history.back()"]');
                    if (backButton) {
                        backButton.click();
                    }
                }
                // Swipe left - navigate forward (context dependent)
                else if (distX <= -threshold && Math.abs(distY) <= restraint) {
                    handleSwipeLeft();
                }
            }
        }, { passive: true });
    }

    /**
     * Handle swipe left gesture
     */
    function handleSwipeLeft() {
        // Context-dependent forward navigation
        const currentPath = window.location.pathname;

        if (currentPath === '/') {
            window.location.href = '/catalog';
        } else if (currentPath === '/catalog') {
            window.location.href = '/trends';
        } else if (currentPath === '/trends') {
            window.location.href = '/cocreation';
        }
    }

    /**
     * Utility function to show loading state
     */
    window.showLoading = function(element) {
        if (typeof element === 'string') {
            element = document.querySelector(element);
        }
        if (element) {
            element.classList.add('loading');
            element.style.pointerEvents = 'none';
        }
    };

    /**
     * Utility function to hide loading state
     */
    window.hideLoading = function(element) {
        if (typeof element === 'string') {
            element = document.querySelector(element);
        }
        if (element) {
            element.classList.remove('loading');
            element.style.pointerEvents = 'auto';
        }
    };

    /**
     * Utility function to show toast notifications
     */
    window.showToast = function(message, type = 'info', duration = 5000) {
        // Create toast container if it doesn't exist
        let toastContainer = document.querySelector('.toast-container');
        if (!toastContainer) {
            toastContainer = document.createElement('div');
            toastContainer.className = 'toast-container position-fixed top-0 end-0 p-3';
            toastContainer.style.zIndex = '9999';
            document.body.appendChild(toastContainer);
        }

        // Create toast element
        const toastElement = document.createElement('div');
        toastElement.className = `toast align-items-center text-white bg-${type} border-0`;
        toastElement.setAttribute('role', 'alert');
        toastElement.innerHTML = `
            <div class="d-flex">
                <div class="toast-body">${message}</div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        `;

        toastContainer.appendChild(toastElement);

        // Initialize and show toast
        const toast = new bootstrap.Toast(toastElement, {
            autohide: true,
            delay: duration
        });

        toast.show();

        // Remove element after hiding
        toastElement.addEventListener('hidden.bs.toast', function() {
            toastElement.remove();
        });
    };

    /**
     * Utility function to format numbers
     */
    window.formatNumber = function(num) {
        if (num >= 1000000) {
            return (num / 1000000).toFixed(1) + 'M';
        }
        if (num >= 1000) {
            return (num / 1000).toFixed(1) + 'K';
        }
        return num.toString();
    };

    /**
     * Utility function to debounce function calls
     */
    window.debounce = function(func, wait, immediate) {
        let timeout;
        return function executedFunction() {
            const context = this;
            const args = arguments;
            const later = function() {
                timeout = null;
                if (!immediate) func.apply(context, args);
            };
            const callNow = immediate && !timeout;
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
            if (callNow) func.apply(context, args);
        };
    };

    /**
     * Initialize smooth scrolling for anchor links
     */
    function initializeSmoothScrolling() {
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                const href = this.getAttribute('href');
                // Only process valid anchor links (not just "#" or invalid selectors)
                if (href && href.length > 1 && href.startsWith('#')) {
                    try {
                        const target = document.querySelector(href);
                        if (target) {
                            e.preventDefault();
                            target.scrollIntoView({
                                behavior: 'smooth',
                                block: 'start'
                            });
                        }
                    } catch (error) {
                        // Invalid selector, ignore
                        console.debug('Invalid anchor selector:', href);
                    }
                }
            });
        });
    }

    /**
     * Initialize image lazy loading
     */
    function initializeLazyLoading() {
        if ('IntersectionObserver' in window) {
            const imageObserver = new IntersectionObserver((entries, observer) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const img = entry.target;
                        if (img.dataset.src) {
                            img.src = img.dataset.src;
                            img.classList.remove('lazy');
                            imageObserver.unobserve(img);
                        }
                    }
                });
            });

            document.querySelectorAll('img[data-src]').forEach(img => {
                imageObserver.observe(img);
            });
        }
    }

    /**
     * Handle connection status
     */
    function handleConnectionStatus() {
        function updateOnlineStatus() {
            const isOnline = navigator.onLine;
            const statusIndicator = document.querySelector('.connection-status');

            if (!isOnline) {
                showToast('You are currently offline. Some features may not work.', 'warning', 0);
            }
        }

        window.addEventListener('online', updateOnlineStatus);
        window.addEventListener('offline', updateOnlineStatus);
    }

    /**
     * Initialize keyboard shortcuts
     */
    function initializeKeyboardShortcuts() {
        document.addEventListener('keydown', function(e) {
            // Ctrl/Cmd + K for search
            if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
                e.preventDefault();
                const searchInput = document.querySelector('input[type="search"], .search-input');
                if (searchInput) {
                    searchInput.focus();
                }
            }

            // Escape to close modals
            if (e.key === 'Escape') {
                const openModal = document.querySelector('.modal.show');
                if (openModal) {
                    const modal = bootstrap.Modal.getInstance(openModal);
                    if (modal) {
                        modal.hide();
                    }
                }
            }
        });
    }

    /**
     * Initialize accessibility improvements
     */
    function initializeAccessibility() {
        // Skip to main content link
        const skipLink = document.createElement('a');
        skipLink.href = '#main-content';
        skipLink.className = 'skip-link visually-hidden-focusable btn btn-primary position-absolute';
        skipLink.style.top = '10px';
        skipLink.style.left = '10px';
        skipLink.style.zIndex = '9999';
        skipLink.textContent = 'Skip to main content';
        document.body.insertBefore(skipLink, document.body.firstChild);

        // Announce page changes for screen readers
        const pageTitle = document.title;
        const announcement = document.createElement('div');
        announcement.setAttribute('aria-live', 'polite');
        announcement.setAttribute('aria-atomic', 'true');
        announcement.className = 'visually-hidden';
        announcement.textContent = `Page loaded: ${pageTitle}`;
        document.body.appendChild(announcement);

        // Focus management for modals
        document.addEventListener('shown.bs.modal', function(e) {
            const modal = e.target;
            const focusableElements = modal.querySelectorAll(
                'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
            );
            if (focusableElements.length > 0) {
                focusableElements[0].focus();
            }
        });
    }

    /**
     * Performance monitoring
     */
    function initializePerformanceMonitoring() {
        // Log performance metrics
        window.addEventListener('load', function() {
            if ('performance' in window) {
                const perfData = performance.getEntriesByType('navigation')[0];
                console.log('Page load time:', perfData.loadEventEnd - perfData.loadEventStart, 'ms');

                // Log any long tasks (> 50ms)
                if ('PerformanceObserver' in window) {
                    const observer = new PerformanceObserver((list) => {
                        for (const entry of list.getEntries()) {
                            if (entry.duration > 50) {
                                console.warn('Long task detected:', entry.duration, 'ms');
                            }
                        }
                    });
                    observer.observe({ entryTypes: ['longtask'] });
                }
            }
        });
    }

    // Initialize all modules
    initializeSmoothScrolling();
    initializeLazyLoading();
    handleConnectionStatus();
    initializeKeyboardShortcuts();
    initializeAccessibility();
    initializePerformanceMonitoring();

    // Add page-specific initializations
    const currentPage = window.location.pathname;

    if (currentPage === '/catalog') {
        initializeCatalogPage();
    } else if (currentPage === '/trends') {
        initializeTrendsPage();
    } else if (currentPage.startsWith('/product/')) {
        initializeProductDetailPage();
    }

    /**
     * Page-specific initialization functions
     */
    function initializeCatalogPage() {
        // Auto-submit form on filter change (with debounce)
        const filterForm = document.querySelector('form[method="GET"]');
        if (filterForm) {
            const selects = filterForm.querySelectorAll('select');
            const debouncedSubmit = debounce(() => filterForm.submit(), 300);

            selects.forEach(select => {
                select.addEventListener('change', debouncedSubmit);
            });
        }

        // Enhanced product card interactions
        document.querySelectorAll('.product-card').forEach(card => {
            card.addEventListener('mouseenter', function() {
                this.style.transform = 'translateY(-8px) scale(1.02)';
            });

            card.addEventListener('mouseleave', function() {
                this.style.transform = 'translateY(0) scale(1)';
            });
        });
    }

    function initializeTrendsPage() {
        // Trend cards without animations - clean and simple
        document.querySelectorAll('.trend-card').forEach(card => {
            // No hover effects - cards remain static
        });
    }

    function initializeProductDetailPage() {
        // Image zoom functionality
        const productImage = document.querySelector('.product-image-large img');
        if (productImage) {
            productImage.addEventListener('click', function() {
                this.style.transform = this.style.transform === 'scale(1.5)' ? 'scale(1)' : 'scale(1.5)';
            });
        }
    }

    /**
     * Initialize header navigation based on current page
     */
    function initializeHeaderNavigation() {
        const currentPath = window.location.pathname;
        const headerContainer = document.querySelector('.bruggen-header .d-flex.justify-content-between');

        if (!headerContainer) return;

        // Check if we're on a subpage
        const isSubpage = currentPath !== '/' && currentPath !== '/index';

        // Don't override the header - let the base template handle user info with dropdown
    }

    // Initialize header navigation
    initializeHeaderNavigation();

    console.log('Brüggen Innovation Catalogue initialized successfully');
});

/**
 * Global utility functions
 */

// Copy text to clipboard
function copyToClipboard(text) {
    if (navigator.clipboard) {
        navigator.clipboard.writeText(text).then(() => {
            showToast('Copied to clipboard!', 'success');
        }).catch(() => {
            showToast('Failed to copy to clipboard', 'danger');
        });
    } else {
        // Fallback for older browsers
        const textArea = document.createElement('textarea');
        textArea.value = text;
        document.body.appendChild(textArea);
        textArea.select();
        try {
            document.execCommand('copy');
            showToast('Copied to clipboard!', 'success');
        } catch (err) {
            showToast('Failed to copy to clipboard', 'danger');
        }
        document.body.removeChild(textArea);
    }
}

// Share content (if Web Share API is available)
function shareContent(title, text, url) {
    if (navigator.share) {
        navigator.share({
            title: title,
            text: text,
            url: url
        }).catch(console.error);
    } else {
        // Fallback to copying URL
        copyToClipboard(url || window.location.href);
    }
}

// Format currency
function formatCurrency(amount, currency = 'EUR') {
    return new Intl.NumberFormat('de-DE', {
        style: 'currency',
        currency: currency
    }).format(amount);
}

// Format date
function formatDate(date, locale = 'de-DE') {
    return new Intl.DateTimeFormat(locale, {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    }).format(new Date(date));
}

// Validate email
function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

// Add to template filter for JSON parsing
if (typeof Jinja2 !== 'undefined') {
    Jinja2.addFilter('from_json', function(value) {
        try {
            return JSON.parse(value);
        } catch (e) {
            return [];
        }
    });
}

let progressSteps = {};
let progressPhases = [
    { id: 'keyword_strategy', title: 'Keyword-Strategie erstellen', icon: '⏳', status: 'pending' },
    { id: 'data_collection', title: 'Datenquellen durchsuchen', icon: '⏳', status: 'pending' },
    { id: 'ai_analysis', title: 'KI-Analyse durchführen', icon: '⏳', status: 'pending' },
    { id: 'extract_facts', title: 'Key Facts extrahieren', icon: '⏳', status: 'pending' },
    { id: 'generate_pdf', title: 'PDF-Report erstellen', icon: '⏳', status: 'pending' }
];

// Live Logs Management
function initializeLiveLogs() {
    const liveLogsContainer = document.getElementById('liveLogsContainer');
    const liveLogsContent = document.getElementById('liveLogsContent');
    const toggleButton = document.getElementById('toggleLogs');

    if (liveLogsContainer) {
        liveLogsContainer.style.display = 'block';
    }

    if (toggleButton) {
        toggleButton.addEventListener('click', function() {
            const content = document.getElementById('liveLogsContent');
            const icon = this.querySelector('i');

            if (content.style.display === 'none') {
                content.style.display = 'block';
                icon.classList.remove('fa-chevron-down');
                icon.classList.add('fa-chevron-up');
            } else {
                content.style.display = 'none';
                icon.classList.remove('fa-chevron-up');
                icon.classList.add('fa-chevron-down');
            }
        });
    }

    // Clear previous logs
    if (liveLogsContent) {
        liveLogsContent.innerHTML = '';
    }
}

function addLiveLog(message, type = 'info') {
    const liveLogsContent = document.getElementById('liveLogsContent');
    if (!liveLogsContent) return;

    const timestamp = new Date().toLocaleTimeString('de-DE');
    const logEntry = document.createElement('div');
    logEntry.className = 'log-entry mb-1';

    // Color coding based on type
    let color = '#d4d4d4'; // default
    let icon = '•';

    switch(type) {
        case 'success':
            color = '#4ec9b0';
            icon = '✓';
            break;
        case 'warning':
            color = '#dcdcaa';
            icon = '⚠';
            break;
        case 'error':
            color = '#f48771';
            icon = '✗';
            break;
        case 'progress':
            color = '#569cd6';
            icon = '►';
            break;
        case 'data':
            color = '#ce9178';
            icon = '▸';
            break;
    }

    logEntry.innerHTML = `
        <span style="color: #858585;">[${timestamp}]</span>
        <span style="color: ${color}; font-weight: bold;">${icon}</span>
        <span style="color: ${color};">${escapeHtml(message)}</span>
    `;

    liveLogsContent.appendChild(logEntry);

    // Auto-scroll to bottom
    liveLogsContent.scrollTop = liveLogsContent.scrollHeight;
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Placeholder for submitButton, cancelButton, loadingIndicator, keywordsInput, selectedCountries, addProgressStep, initializeProgress
// These are assumed to be defined in the scope where this script is used, likely within a function like 'generateReport' or similar.
// Note: generatedReportData and showReportPreview are declared in trends.html to avoid conflicts
let submitButton, cancelButton, loadingIndicator, keywordsInput, selectedCountries, addProgressStep, initializeProgress;

// Example of how the report generation might be initiated, including the new live log integration.
async function generateReport(event) {
    event.preventDefault();

    submitButton = document.getElementById('submitReportBtn');
    cancelButton = document.getElementById('cancelReportBtn');
    loadingIndicator = document.getElementById('reportLoadingIndicator');
    const keywordsInputEl = document.getElementById('keywords');
    const countriesSelect = document.getElementById('countries');

    // Dummy assignments for demonstration. In a real scenario, these would be actual DOM elements or values.
    keywordsInput = keywordsInputEl ? keywordsInputEl.value : 'default keywords';
    selectedCountries = countriesSelect ? Array.from(countriesSelect.selectedOptions).map(option => option.value) : ['DE'];
    
    // Note: showReportPreview is defined in trends.html
    addProgressStep = (container, data) => console.log("Adding progress step:", data);

    if (submitButton) submitButton.disabled = true;
    if (cancelButton) cancelButton.disabled = true;
    if (loadingIndicator) {
        loadingIndicator.innerHTML = '<div class="analysis-progress-container"></div>';
        loadingIndicator.style.display = 'block';
    }

    // Initialize live logs
    initializeLiveLogs();
    addLiveLog('Deep Research gestartet...', 'progress');
    addLiveLog(`Keywords: ${keywordsInput}`, 'data');
    addLiveLog(`Zielmärkte: ${selectedCountries.join(', ')}`, 'data');

    const progressContainer = document.querySelector('.analysis-progress-container');

    try {
        addLiveLog('Verbinde mit OpenAI GPT-4o...', 'progress');
        const response = await fetch('/api/generate-trend-report-stream', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                keywords: keywordsInput,
                countries: selectedCountries,
            }),
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.message || `HTTP error! status: ${response.status}`);
        }

        const reader = response.body.getReader();
        const decoder = new TextDecoder('utf-8');
        let buffer = '';

        while (true) {
            const { done, value } = await reader.read();
            if (done) break;

            buffer += decoder.decode(value, { stream: true });

            let lines = buffer.split('\n');
            buffer = lines.pop(); // Keep the last partial line

            for (const line of lines) {
                if (line.trim() === '') continue;

                try {
                    const data = JSON.parse(line);
                    if (data.type === 'progress') {
                        addProgressStep(progressContainer, data);

                        // Add to live logs
                        const logType = data.step.includes('error') || data.step.includes('timeout') ? 'warning' : 
                                       data.step.includes('complete') || data.step.includes('success') ? 'success' : 'progress';
                        addLiveLog(data.message, logType);

                    } else if (data.type === 'complete') {
                        addLiveLog('✓ Report erfolgreich generiert!', 'success');
                        addLiveLog(`Titel: ${data.report.title}`, 'data');
                        addLiveLog(`Quellen analysiert: ${data.report.sources ? data.report.sources.length : 'N/A'}`, 'data');

                        if (typeof window.generatedReportData !== 'undefined') {
                            window.generatedReportData = data;
                        }
                        if (typeof showReportPreview === 'function') {
                            showReportPreview(data);
                        }
                        return; // Exit loop and function after completion
                    } else if (data.type === 'error') {
                        addLiveLog(`✗ Fehler: ${data.message}`, 'error');
                        throw new Error(data.message);
                    }
                } catch (e) {
                    console.error("Failed to parse JSON line:", line, e);
                    addLiveLog(`Fehler beim Verarbeiten der Log-Daten: ${escapeHtml(line)}`, 'error');
                }
            }
        }
         // Handle any remaining data in the buffer
        if (buffer.trim()) {
            try {
                const data = JSON.parse(buffer);
                 if (data.type === 'progress') {
                    addProgressStep(progressContainer, data);
                    const logType = data.step.includes('error') || data.step.includes('timeout') ? 'warning' : 
                                   data.step.includes('complete') || data.step.includes('success') ? 'success' : 'progress';
                    addLiveLog(data.message, logType);
                } else if (data.type === 'complete') {
                    addLiveLog('✓ Report erfolgreich generiert!', 'success');
                    if (typeof window.generatedReportData !== 'undefined') {
                        window.generatedReportData = data;
                    }
                    if (typeof showReportPreview === 'function') {
                        showReportPreview(data);
                    }
                } else if (data.type === 'error') {
                    addLiveLog(`✗ Fehler: ${data.message}`, 'error');
                    throw new Error(data.message);
                }
            } catch (e) {
                console.error("Failed to parse final JSON buffer:", buffer, e);
                addLiveLog(`Fehler beim Verarbeiten der finalen Log-Daten: ${escapeHtml(buffer)}`, 'error');
            }
        }


    } catch (error) {
        console.error('Error generating report:', error);
        addLiveLog(`Berichtgenerierung fehlgeschlagen: ${error.message}`, 'error');
        if (loadingIndicator) loadingIndicator.style.display = 'none';
    } finally {
        if (submitButton) submitButton.disabled = false;
        if (cancelButton) cancelButton.disabled = true; // Keep cancel disabled until next attempt
    }
}