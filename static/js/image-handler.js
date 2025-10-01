/**
 * Brüggen Innovation Catalogue - Image Loading Handler
 * Handles image loading, error states, and lazy loading
 */

document.addEventListener('DOMContentLoaded', function() {
    // Only initialize if we're sure the page has loaded completely
    if (document.readyState === 'complete') {
        initializeImageHandling();
    } else {
        window.addEventListener('load', initializeImageHandling);
    }
});

function initializeImageHandling() {
    // Handle all product and trend images with safety checks
    const images = document.querySelectorAll('.product-image, .trend-image, .hero-product-image, .card-img-top img, img[id*="Preview"]');
    
    images.forEach(img => {
        // Only process valid img elements with more thorough checks
        if (img && 
            img.tagName === 'IMG' && 
            img.classList && 
            typeof img.classList.add === 'function' &&
            img.style && 
            typeof img.addEventListener === 'function') {
            try {
                setupImageHandlers(img);
            } catch (error) {
                console.warn('Error setting up image handlers for:', img, error);
            }
        }
    });
    
    // Setup lazy loading for images that aren't immediately visible
    if ('IntersectionObserver' in window) {
        setupLazyLoading();
    }
}

function setupImageHandlers(img) {
    // Safety check - ensure img element exists and has classList
    if (!img || !img.classList || !img.style || img.tagName !== 'IMG') {
        console.warn('Invalid image element passed to setupImageHandlers:', img);
        return;
    }
    
    // Add loading class initially
    try {
        img.classList.add('loading');
    } catch (error) {
        console.warn('Could not add loading class to image:', error);
        return;
    }
    
    // Handle successful load
    img.addEventListener('load', function() {
        if (img && img.classList) {
            img.classList.remove('loading', 'error');
            if (img.style) {
                img.style.opacity = '1';
            }
        }
    });
    
    // Handle load errors
    img.addEventListener('error', function() {
        if (!img || !img.classList) return;
        
        img.classList.remove('loading');
        img.classList.add('error');
        
        // Try to reload once with a fallback URL
        if (!img.dataset.retried) {
            img.dataset.retried = 'true';
            
            // If the original URL was a static file, try to reload it once
            if (img.src.includes('/static/images/') || img.src.includes('/api/image/')) {
                setTimeout(() => {
                    if (img) {
                        // Force reload the same URL
                        const originalSrc = img.src;
                        img.src = '';
                        img.src = originalSrc + '?retry=' + Date.now();
                    }
                }, 500);
                return;
            }
            
            // Use a more reliable food image as fallback for external URLs
            const fallbackUrls = [
                'https://images.unsplash.com/photo-1574323347407-f5e1ad6d020b?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
                'https://images.unsplash.com/photo-1517686469429-8bdb88b9f907?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
                'https://images.unsplash.com/photo-1593560708920-61dd98c46a4e?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80'
            ];
            
            const randomFallback = fallbackUrls[Math.floor(Math.random() * fallbackUrls.length)];
            
            setTimeout(() => {
                if (img) {
                    img.src = randomFallback;
                }
            }, 1000);
        } else {
            // Final fallback - show placeholder
            showImagePlaceholder(img);
        }
    });
    
    // Set initial opacity for smooth loading
    if (img.style) {
        img.style.opacity = '0';
        img.style.transition = 'opacity 0.3s ease-in-out';
    }
}

function showImagePlaceholder(img) {
    // Safety check
    if (!img || !img.classList || !img.style) {
        return;
    }
    
    try {
        // Create a canvas with a placeholder
        const canvas = document.createElement('canvas');
        const ctx = canvas.getContext('2d');
        canvas.width = 400;
        canvas.height = 300;
        
        // Draw placeholder background
        ctx.fillStyle = '#f8f9fa';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        
        // Draw border
        ctx.strokeStyle = '#dee2e6';
        ctx.lineWidth = 2;
        ctx.strokeRect(0, 0, canvas.width, canvas.height);
        
        // Draw icon
        ctx.fillStyle = '#6c757d';
        ctx.font = '48px Arial';
        ctx.textAlign = 'center';
        ctx.fillText('🥣', canvas.width/2, canvas.height/2 + 16);
        
        // Draw text
        ctx.fillStyle = '#6c757d';
        ctx.font = '16px Arial';
        ctx.fillText('Product Image', canvas.width/2, canvas.height/2 + 50);
        
        // Convert to data URL and set as src
        img.src = canvas.toDataURL();
        img.classList.remove('loading', 'error');
        img.style.opacity = '1';
    } catch (error) {
        console.warn('Could not create image placeholder:', error);
        // Fallback - just remove the loading states
        if (img.classList) {
            img.classList.remove('loading', 'error');
        }
        if (img.style) {
            img.style.opacity = '1';
        }
    }
}

function setupLazyLoading() {
    try {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    
                    // Safety check
                    if (!img || !img.dataset) {
                        return;
                    }
                    
                    // Load the image if it has a data-src attribute
                    if (img.dataset.src) {
                        img.src = img.dataset.src;
                        img.removeAttribute('data-src');
                    }
                    
                    observer.unobserve(img);
                }
            });
        }, {
            rootMargin: '50px 0px',
            threshold: 0.01
        });
        
        // Observe images with data-src attribute
        const lazyImages = document.querySelectorAll('img[data-src]');
        lazyImages.forEach(img => {
            if (img && img.tagName === 'IMG') {
                imageObserver.observe(img);
            }
        });
    } catch (error) {
        console.warn('Lazy loading setup failed:', error);
    }
}

// Helper function to preload critical images
function preloadCriticalImages() {
    const criticalImages = [
        'https://images.unsplash.com/photo-1574323347407-f5e1ad6d020b?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
        'https://images.unsplash.com/photo-1517686469429-8bdb88b9f907?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
        'https://images.unsplash.com/photo-1593560708920-61dd98c46a4e?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80'
    ];
    
    criticalImages.forEach(src => {
        const img = new Image();
        img.src = src;
    });
}

// Preload critical images on page load
preloadCriticalImages();