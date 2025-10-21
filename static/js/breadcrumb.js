/**
 * Brüggen Innovation Catalogue - Dynamic Breadcrumb Navigation
 * Manages dynamic back navigation based on the current page context
 * Now with smart history tracking that remembers the actual previous page
 */

document.addEventListener('DOMContentLoaded', function() {
    initializeBreadcrumbNavigation();
});

function initializeBreadcrumbNavigation() {
    const backButton = document.getElementById('breadcrumb-back');
    if (!backButton) return;
    
    const currentPath = window.location.pathname;
    const urlParams = new URLSearchParams(window.location.search);
    
    // Get the page title for current page
    const currentPageTitle = getPageTitle();
    
    // Store current page in navigation history
    storeNavigationHistory(currentPath, currentPageTitle);
    
    // Determine the appropriate back navigation using smart history
    let backNavigation = getSmartBackNavigation();
    
    // Update the back button if navigation is defined
    if (backNavigation) {
        updateBackButton(backButton, backNavigation);
    } else {
        // Hide the back button if we're on the dashboard
        if (currentPath === '/') {
            backButton.style.display = 'none';
        }
    }
}

function getPageTitle() {
    // First try to get title from data-page-title attribute on body
    const bodyTitle = document.body.getAttribute('data-page-title');
    if (bodyTitle) {
        return bodyTitle;
    }
    
    // Fallback to h1 text content
    const h1 = document.querySelector('h1');
    if (h1) {
        return h1.textContent.trim();
    }
    
    // Last fallback to document title
    return document.title;
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
    // Remove the current page from history before navigating back
    removeCurrentPageFromHistory();
    
    // Add a small delay to show the click animation
    setTimeout(() => {
        window.location.href = url;
    }, 100);
}

function storeNavigationHistory(currentPath, pageTitle) {
    // Store the current path and title in session storage
    const navigationHistory = JSON.parse(sessionStorage.getItem('navigationHistory') || '[]');
    
    // Create a page entry with path and title
    const pageEntry = {
        path: currentPath,
        title: pageTitle,
        timestamp: Date.now()
    };
    
    // Check if the last entry is the same as current (avoid duplicates on refresh)
    const lastEntry = navigationHistory[navigationHistory.length - 1];
    if (!lastEntry || lastEntry.path !== currentPath) {
        navigationHistory.push(pageEntry);
        
        // Keep only the last 20 pages in history
        if (navigationHistory.length > 20) {
            navigationHistory.shift();
        }
        
        sessionStorage.setItem('navigationHistory', JSON.stringify(navigationHistory));
    }
}

function removeCurrentPageFromHistory() {
    // Remove the current page from history when navigating back
    const navigationHistory = JSON.parse(sessionStorage.getItem('navigationHistory') || '[]');
    
    if (navigationHistory.length > 0) {
        navigationHistory.pop();
        sessionStorage.setItem('navigationHistory', JSON.stringify(navigationHistory));
    }
}

function getSmartBackNavigation() {
    const currentPath = window.location.pathname;
    const urlParams = new URLSearchParams(window.location.search);
    const navigationHistory = JSON.parse(sessionStorage.getItem('navigationHistory') || '[]');
    
    // Priority 1: If we have valid navigation history, use it
    if (navigationHistory.length >= 2) {
        // Get the second-to-last entry (the actual previous page)
        const previousPage = navigationHistory[navigationHistory.length - 2];
        
        // Validate that previousPage has required properties
        if (previousPage && previousPage.path && previousPage.title) {
            return {
                text: previousPage.title,
                url: previousPage.path,
                icon: getIconForPath(previousPage.path)
            };
        }
    }
    
    // Priority 2: Parse hierarchical URL structure to determine parent path
    // This handles direct visits and ensures back button always works
    
    // Match: /custom-pages/view/{page_id}/product/{id}
    const customPageProductMatch = currentPath.match(/^\/custom-pages\/view\/(\d+)\/product\/\d+$/);
    if (customPageProductMatch) {
        const pageId = customPageProductMatch[1];
        return {
            text: 'Custom Page',
            url: `/custom-pages/view/${pageId}`,
            icon: 'fa-folder'
        };
    }
    
    // Match: /catalog/product/{id}
    if (currentPath.match(/^\/catalog\/product\/\d+$/)) {
        return {
            text: 'Innovation Catalog',
            url: '/catalog',
            icon: 'fa-cogs'
        };
    }
    
    // Match: /custom-pages/view/{page_id}
    if (currentPath.match(/^\/custom-pages\/view\/\d+$/)) {
        return {
            text: 'My Custom Pages',
            url: '/custom-pages',
            icon: 'fa-folder'
        };
    }
    
    // Priority 3: Legacy support for old URL structure with query parameters
    if (currentPath.startsWith('/product/') && urlParams.has('from_custom_page')) {
        const customPageId = urlParams.get('from_custom_page');
        return {
            text: 'Custom Page',
            url: `/custom-pages/view/${customPageId}`,
            icon: 'fa-folder'
        };
    }
    
    // Priority 4: Default fallback navigation for when there's no history or context
    if (currentPath.startsWith('/product/')) {
        return { text: 'Innovation Catalog', url: '/catalog', icon: 'fa-cogs' };
    } else if (currentPath.startsWith('/trend/')) {
        return { text: 'Trends & Insights', url: '/trends', icon: 'fa-chart-line' };
    } else if (currentPath === '/cocreation') {
        return { text: 'Dashboard', url: '/', icon: 'fa-home' };
    } else if (currentPath === '/catalog' || currentPath === '/trends' || currentPath === '/custom-pages') {
        return { text: 'Dashboard', url: '/', icon: 'fa-home' };
    }
    
    // Default fallback to dashboard
    return null;
}

function getIconForPath(path) {
    // Return appropriate icon based on path
    if (!path) {
        return 'fa-arrow-left';
    }
    
    if (path === '/') {
        return 'fa-home';
    } else if (path === '/catalog') {
        return 'fa-cogs';
    } else if (path === '/trends') {
        return 'fa-chart-line';
    } else if (path === '/cocreation') {
        return 'fa-lightbulb';
    } else if (path.startsWith('/custom-pages')) {
        return 'fa-folder';
    } else if (path.startsWith('/product/')) {
        return 'fa-box';
    } else if (path.startsWith('/trend/')) {
        return 'fa-chart-bar';
    }
    
    return 'fa-arrow-left';
}
