// static/js/tomi-dropdown.js
(function() {
    'use strict';
    
    function initTomiDropdown() {
        const dropdownToggle = document.querySelector('.tomi-dropdown-toggle');
        const dropdownMenu = document.querySelector('.tomi-dropdown-menu');
        
        if (!dropdownToggle || !dropdownMenu) return;
        
        console.log('Inicializando dropdown de Tomi...');
        
        dropdownToggle.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            
            // Toggle del dropdown
            const isShowing = dropdownMenu.style.display === 'block';
            dropdownMenu.style.display = isShowing ? 'none' : 'block';
        });
        
        // Cerrar al hacer click fuera
        document.addEventListener('click', function(e) {
            if (!dropdownToggle.contains(e.target) && !dropdownMenu.contains(e.target)) {
                dropdownMenu.style.display = 'none';
            }
        });
        
        // Cerrar al hacer scroll
        window.addEventListener('scroll', function() {
            dropdownMenu.style.display = 'none';
        });
    }
    
    document.addEventListener('DOMContentLoaded', initTomiDropdown);
})();