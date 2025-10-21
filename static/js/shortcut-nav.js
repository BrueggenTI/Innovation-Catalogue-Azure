/**
 * Shortcut Navigation Circle - Interactive Behavior
 * Modern 2025 Design with smooth animations
 */

document.addEventListener('DOMContentLoaded', function() {
    const shortcutCircle = document.getElementById('shortcutCircle');
    const wrapper = document.querySelector('.shortcut-nav-wrapper');
    
    if (!shortcutCircle || !wrapper) return;
    
    // Make wrapper visible immediately
    wrapper.style.opacity = '1';
    wrapper.style.visibility = 'visible';
    
    // Handle scroll event to adjust position
    // Button bleibt bei 125px bis scrollY >= 95px (dann 30px Abstand zum oberen Rand)
    let scrollTimeout;
    window.addEventListener('scroll', function() {
        clearTimeout(scrollTimeout);
        scrollTimeout = setTimeout(function() {
            if (window.scrollY >= 95) {
                wrapper.classList.add('scrolled');
            } else {
                wrapper.classList.remove('scrolled');
            }
        }, 10);
    });
    
    // Add pulse animation on first load to attract attention
    setTimeout(() => {
        shortcutCircle.classList.add('pulse');
    }, 1000);
    
    // Remove pulse animation after a few cycles
    setTimeout(() => {
        shortcutCircle.classList.remove('pulse');
    }, 7000);
    
    // Re-add pulse when user hasn't interacted in a while
    let interactionTimer;
    
    function resetInteractionTimer() {
        clearTimeout(interactionTimer);
        interactionTimer = setTimeout(() => {
            if (!shortcutCircle.classList.contains('pulse')) {
                shortcutCircle.classList.add('pulse');
                setTimeout(() => {
                    shortcutCircle.classList.remove('pulse');
                }, 4000);
            }
        }, 30000); // Pulse again after 30 seconds of no interaction
    }
    
    // Track interactions
    wrapper.addEventListener('mouseenter', () => {
        shortcutCircle.classList.remove('pulse');
        clearTimeout(interactionTimer);
    });
    
    wrapper.addEventListener('mouseleave', resetInteractionTimer);
    
    // Initial timer
    resetInteractionTimer();
    
    // Add smooth transitions for shortcuts
    const shortcuts = document.querySelectorAll('.shortcut-btn');
    shortcuts.forEach((btn, index) => {
        btn.addEventListener('click', function(e) {
            // Add click ripple effect
            const ripple = document.createElement('span');
            ripple.style.cssText = `
                position: absolute;
                width: 100%;
                height: 100%;
                top: 0;
                left: 0;
                background: radial-gradient(circle, rgba(102, 28, 49, 0.3) 0%, transparent 70%);
                border-radius: 20px;
                pointer-events: none;
                animation: ripple 0.6s ease-out;
            `;
            this.appendChild(ripple);
            
            setTimeout(() => ripple.remove(), 600);
        });
    });
});

// Add ripple animation to CSS dynamically
const style = document.createElement('style');
style.textContent = `
    @keyframes ripple {
        from {
            transform: scale(0);
            opacity: 1;
        }
        to {
            transform: scale(2);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);
