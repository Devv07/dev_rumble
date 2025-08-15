document.addEventListener('DOMContentLoaded', function() {
    // Add hover effect to cards
    const cards = document.querySelectorAll('.card');
    cards.forEach(card => {
        card.addEventListener('mouseenter', () => {
            card.style.transform = 'translateY(-5px)';
        });
        
        card.addEventListener('mouseleave', () => {
            card.style.transform = 'translateY(0)';
        });
    });
    
    // Notification badge interaction
    const notificationBtn = document.querySelector('.icon-btn:nth-child(1)');
    notificationBtn.addEventListener('click', function() {
        const badge = this.querySelector('.notification-badge');
        badge.textContent = '0';
        badge.style.backgroundColor = '#4CAF50';
    });
    
    // CTA button animation
    const ctaButton = document.querySelector('.cta-button');
    ctaButton.addEventListener('click', function() {
        this.innerHTML = 'Redirecting... <i class="fas fa-spinner fa-spin"></i>';
        setTimeout(() => {
            this.innerHTML = 'Explore Courses';
            alert('Course catalog page would open here in a real application');
        }, 1500);
    });
});