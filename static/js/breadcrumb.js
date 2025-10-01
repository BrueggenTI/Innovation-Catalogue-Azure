/**
 * Brüggen Innovation Catalogue - Dynamic Breadcrumb Navigation
 * Manages dynamic back navigation based on the current page context
 */

document.addEventListener('DOMContentLoaded', function() {
    initializeBreadcrumbNavigation();
});

function initializeBreadcrumbNavigation() {
    const backButton = document.getElementById('breadcrumb-back');
    if (!backButton) return;
    
    const currentPath = window.location.pathname;
    const urlParams = new URLSearchParams(window.location.search);
    
    // Define navigation structure
    const navigationMap = {
        '/': { text: 'Dashboard', url: '/', icon: 'fa-home' },
        '/catalog': { text: 'Dashboard', url: '/', icon: 'fa-home' },
        '/trends': { text: 'Dashboard', url: '/', icon: 'fa-home' },
        '/cocreation': { text: 'Dashboard', url: '/', icon: 'fa-home' },
        '/product/': { text: 'Innovation Catalog', url: '/catalog', icon: 'fa-cogs' },
        '/trend/': { text: 'Trends & Insights', url: '/trends', icon: 'fa-chart-line' }
    };
    
    // Determine the appropriate back navigation
    let backNavigation = null;
    
    // Check for specific product detail pages
    if (currentPath.startsWith('/product/')) {
        // If we came from co-creation, go back to co-creation
        if (urlParams.get('from') === 'cocreation') {
            backNavigation = { text: 'Co-Creation Lab', url: '/cocreation', icon: 'fa-lightbulb' };
        } else {
            backNavigation = navigationMap['/product/'];
        }
    }
    // Check for trend detail pages
    else if (currentPath.startsWith('/trend/')) {
        backNavigation = navigationMap['/trend/'];
    }
    // Check for co-creation with base product
    else if (currentPath === '/cocreation' && urlParams.get('base_product_id')) {
        backNavigation = { text: 'Innovation Catalog', url: '/catalog', icon: 'fa-cogs' };
    }
    // Default mappings for main sections
    else {
        backNavigation = navigationMap[currentPath];
    }
    
    // Update the back button if navigation is defined
    if (backNavigation) {
        updateBackButton(backButton, backNavigation);
    } else {
        // Hide the back button if we're on the dashboard
        if (currentPath === '/') {
            backButton.style.display = 'none';
        }
    }
    
    // Store navigation history for better back navigation
    storeNavigationHistory(currentPath);
}

function updateBackButton(backButton, navigation) {
    // Update button text and icon
    const icon = backButton.querySelector('i');
    const text = backButton.querySelector('.breadcrumb-text');
    
    if (icon) {
        icon.className = `fas fa-arrow-left me-2`;
    }
    
    if (text) {
        text.textContent = `Back to ${navigation.text}`;
    } else {
        // If no text element exists, update the entire button content
        backButton.innerHTML = `
            <i class="fas fa-arrow-left me-2"></i>
            <span class="breadcrumb-text">Back to ${navigation.text}</span>
        `;
    }
    
    // Update the click handler
    backButton.onclick = function(e) {
        e.preventDefault();
        navigateBack(navigation.url);
    };
    
    // Update href for right-click context menu
    backButton.href = navigation.url;
    
    // Show the button
    backButton.style.display = 'inline-flex';
}

function navigateBack(url) {
    // Add a small delay to show the click animation
    setTimeout(() => {
        window.location.href = url;
    }, 100);
}

function storeNavigationHistory(currentPath) {
    // Store the current path in session storage for better navigation
    const navigationHistory = JSON.parse(sessionStorage.getItem('navigationHistory') || '[]');
    
    // Add current path to history (avoid duplicates)
    if (navigationHistory[navigationHistory.length - 1] !== currentPath) {
        navigationHistory.push(currentPath);
        
        // Keep only the last 10 pages in history
        if (navigationHistory.length > 10) {
            navigationHistory.shift();
        }
        
        sessionStorage.setItem('navigationHistory', JSON.stringify(navigationHistory));
    }
}

// Enhanced navigation with referrer support
function getSmartBackNavigation() {
    const currentPath = window.location.pathname;
    const referrer = document.referrer;
    const navigationHistory = JSON.parse(sessionStorage.getItem('navigationHistory') || '[]');
    
    // If we have a referrer from the same domain, use it
    if (referrer && referrer.includes(window.location.origin)) {
        const referrerPath = new URL(referrer).pathname;
        
        // Map common referrer patterns
        if (referrerPath === '/catalog' && currentPath.startsWith('/product/')) {
            return { text: 'Innovation Catalog', url: '/catalog', icon: 'fa-cogs' };
        } else if (referrerPath === '/trends' && currentPath.startsWith('/trend/')) {
            return { text: 'Trends & Insights', url: '/trends', icon: 'fa-chart-line' };
        } else if (referrerPath === '/cocreation' && currentPath.startsWith('/product/')) {
            return { text: 'Co-Creation Lab', url: '/cocreation', icon: 'fa-lightbulb' };
        }
    }
    
    // Fallback to navigation history
    if (navigationHistory.length > 1) {
        const previousPath = navigationHistory[navigationHistory.length - 2];
        
        if (previousPath === '/catalog') {
            return { text: 'Innovation Catalog', url: '/catalog', icon: 'fa-cogs' };
        } else if (previousPath === '/trends') {
            return { text: 'Trends & Insights', url: '/trends', icon: 'fa-chart-line' };
        } else if (previousPath === '/cocreation') {
            return { text: 'Co-Creation Lab', url: '/cocreation', icon: 'fa-lightbulb' };
        }
    }
    
    // Default fallback
    return { text: 'Dashboard', url: '/', icon: 'fa-home' };
}