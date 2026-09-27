document.addEventListener('DOMContentLoaded', () => {
    const navbar = document.querySelector('.nav-links');
    const hamburger = document.getElementById('navHamburger');

    if (hamburger && navbar) {
        hamburger.addEventListener('click', () => {
            const isOpen = navbar.classList.toggle('open');
            hamburger.classList.toggle('active', isOpen);
            hamburger.setAttribute('aria-expanded', String(isOpen));
        });

        navbar.querySelectorAll('a').forEach((link) => {
            link.addEventListener('click', () => {
                navbar.classList.remove('open');
                hamburger.classList.remove('active');
                hamburger.setAttribute('aria-expanded', 'false');
            });
        });
    }

    const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            }
        });
    }, { threshold: 0.15 });

    document.querySelectorAll('.animate-on-scroll').forEach((element) => observer.observe(element));
});
