// Configuración principal y inicialización
document.addEventListener('DOMContentLoaded', function() {
    // Inicializar tooltips de Bootstrap (si los usas)
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    const tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Inicializar popovers (si los usas)
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    const popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
    
    // Manejar formularios de cantidad en el carrito
    this.initQuantityForms();
    
    // Otros inicializaciones generales...
}.bind(this));

function initQuantityForms() {
    const quantityForms = document.querySelectorAll('form[action*="update_cart"]');
    quantityForms.forEach(form => {
        const input = form.querySelector('input[name="quantity"]');
        if (input) {
            input.addEventListener('change', function() {
                // Auto-submit al cambiar cantidad
                form.submit();
            });
        }
    });
}

// Manejar el dropdown de productos (código que ya tenías)
function initProductDropdown() {
    const productDropdown = document.querySelector('.nav-item.dropdown');
    
    if (productDropdown) {
        productDropdown.addEventListener('mouseenter', function() {
            if (window.innerWidth > 768) {
                const dropdownMenu = this.querySelector('.dropdown-menu');
                dropdownMenu.classList.add('show');
            }
        });
        
        productDropdown.addEventListener('mouseleave', function() {
            if (window.innerWidth > 768) {
                const dropdownMenu = this.querySelector('.dropdown-menu');
                dropdownMenu.classList.remove('show');
            }
        });
    }
    
    // Cerrar dropdowns al hacer click fuera
    document.addEventListener('click', function(e) {
        if (!e.target.closest('.nav-item.dropdown')) {
            document.querySelectorAll('.dropdown-menu').forEach(menu => {
                menu.classList.remove('show');
            });
        }
    });
}

// Inicializar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', function() {
    initProductDropdown();
});