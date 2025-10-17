// Visibility Settings JavaScript
// Handles toggle functionality for ingredient percentages and unapproved recipes

document.addEventListener('DOMContentLoaded', function() {
    const hidePercentagesToggle = document.getElementById('hidePercentagesToggle');
    const hideUnapprovedToggle = document.getElementById('hideUnapprovedToggle');
    
    // Get CSRF token from meta tag
    const csrfToken = document.querySelector('meta[name="csrf-token"]')?.content;
    
    // Handle Percentages Toggle
    if (hidePercentagesToggle) {
        hidePercentagesToggle.addEventListener('change', function() {
            updateVisibilitySettings({
                hide_percentages: this.checked
            });
        });
    }
    
    // Handle Unapproved Recipes Toggle
    if (hideUnapprovedToggle) {
        hideUnapprovedToggle.addEventListener('change', function() {
            updateVisibilitySettings({
                hide_unapproved_recipes: this.checked
            });
        });
    }
    
    // Function to update visibility settings via AJAX
    function updateVisibilitySettings(settings) {
        fetch('/visibility-settings', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify(settings)
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Reload the page to apply changes
                window.location.reload();
            } else {
                console.error('Failed to update visibility settings:', data.error);
                showNotification('Error updating settings. Please try again.', 'error');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showNotification('Error updating settings. Please try again.', 'error');
        });
    }
    
    // Show notification (if not already defined in main.js)
    function showNotification(message, type = 'info') {
        // Create toast notification
        const toastContainer = document.querySelector('.toast-container') || createToastContainer();
        
        const toastHtml = `
            <div class="toast align-items-center text-white bg-${type === 'error' ? 'danger' : 'success'} border-0" role="alert" aria-live="assertive" aria-atomic="true">
                <div class="d-flex">
                    <div class="toast-body">
                        ${message}
                    </div>
                    <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
                </div>
            </div>
        `;
        
        toastContainer.insertAdjacentHTML('beforeend', toastHtml);
        const toastElement = toastContainer.lastElementChild;
        const toast = new bootstrap.Toast(toastElement, { delay: 3000 });
        toast.show();
        
        // Remove toast element after it's hidden
        toastElement.addEventListener('hidden.bs.toast', function() {
            toastElement.remove();
        });
    }
    
    // Create toast container if it doesn't exist
    function createToastContainer() {
        const container = document.createElement('div');
        container.className = 'toast-container position-fixed top-0 end-0 p-3';
        container.style.zIndex = '9999';
        document.body.appendChild(container);
        return container;
    }
});
