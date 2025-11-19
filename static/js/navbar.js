document.addEventListener('DOMContentLoaded', function() {
    const navbar = document.querySelector('.navbar');
    const logoImg = document.querySelector('.logo-img');
    const originalLogoSrc = logoImg.dataset.originalLogo;
    const scrolledLogoSrc = logoImg.dataset.scrolledLogo;

    // Función para manejar el estado del navbar al desplazarse
    function handleScroll() {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    }

    // Función para resaltar el enlace activo
    function highlightActiveLink() {
        const navLinks = document.querySelectorAll('.navbar-nav .nav-link');
        const currentPath = window.location.pathname;

        navLinks.forEach(link => {
            // Comprueba si el href del enlace coincide con la ruta actual.
            // Para la página de inicio, la ruta es "/" y el enlace puede ser "/".
            // Para otras páginas, como "/eventos/", la coincidencia debe ser exacta.
            if (link.getAttribute('href') === currentPath) {
                link.classList.add('active');
            } else {
                link.classList.remove('active');
            }
        });
    }

    // Ejecutar al cargar y al desplazarse
    handleScroll();
    highlightActiveLink();
    window.addEventListener('scroll', handleScroll);
});