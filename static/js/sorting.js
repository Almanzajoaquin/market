// Sistema de ordenamiento mejorado
class SortingManager {
    constructor() {
        this.init();
    }
    
    init() {
        this.bindSortingEvents();
        this.updateActiveSort();
    }
    
    bindSortingEvents() {
        // Dropdown de ordenamiento
        const sortDropdown = document.querySelector('.sort-dropdown');
        const sortToggle = document.querySelector('.sort-dropdown-toggle');
        const sortMenu = document.querySelector('.sort-dropdown-menu');
        const sortOptions = document.querySelectorAll('.sort-option');
        
        if (sortToggle && sortMenu) {
            // Toggle del dropdown
            sortToggle.addEventListener('click', (e) => {
                e.stopPropagation();
                sortMenu.classList.toggle('show');
                sortToggle.classList.toggle('active');
            });
            
            // Cerrar dropdown al hacer click fuera
            document.addEventListener('click', () => {
                sortMenu.classList.remove('show');
                sortToggle.classList.remove('active');
            });
            
            // Prevenir que el dropdown se cierre al hacer click dentro
            sortMenu.addEventListener('click', (e) => {
                e.stopPropagation();
            });
        }
        
        // Opciones de ordenamiento
        sortOptions.forEach(option => {
            option.addEventListener('click', () => {
                const sortValue = option.dataset.sort;
                this.applySorting(sortValue);
            });
        });
        
        // Remover ordenamiento específico
        const removeButtons = document.querySelectorAll('[data-sort-remove]');
        removeButtons.forEach(button => {
            button.addEventListener('click', (e) => {
                e.preventDefault();
                e.stopPropagation();
                this.removeSorting();
            });
        });
    }
    
    applySorting(sortValue) {
        const currentUrl = new URL(window.location.href);
        
        // Actualizar parámetro de ordenamiento
        if (sortValue) {
            currentUrl.searchParams.set('sort', sortValue);
        } else {
            currentUrl.searchParams.delete('sort');
        }
        
        // Mostrar estado de loading
        this.showLoadingState();
        
        // Navegar a la nueva URL
        window.location.href = currentUrl.toString();
    }
    
    removeSorting() {
        const currentUrl = new URL(window.location.href);
        currentUrl.searchParams.delete('sort');
        
        this.showLoadingState();
        window.location.href = currentUrl.toString();
    }
    
    showLoadingState() {
        const productsGrid = document.querySelector('.products-grid') || document.querySelector('.row');
        if (productsGrid) {
            productsGrid.classList.add('loading');
        }
        
        // Mostrar toast de carga
        MasivoTechUtils.showToast('Aplicando ordenamiento...', 'info');
    }
    
    updateActiveSort() {
        const currentSort = new URLSearchParams(window.location.search).get('sort');
        const sortOptions = document.querySelectorAll('.sort-option');
        const sortBadges = document.querySelectorAll('.sort-badge');
        
        // Remover estado activo de todos
        sortOptions.forEach(option => option.classList.remove('active'));
        sortBadges.forEach(badge => badge.classList.remove('active'));
        
        // Activar el actual
        if (currentSort) {
            const activeOption = document.querySelector(`.sort-option[data-sort="${currentSort}"]`);
            const activeBadge = document.querySelector(`.sort-badge:has(button[data-sort-remove="${currentSort}"])`);
            
            if (activeOption) activeOption.classList.add('active');
            if (activeBadge) activeBadge.classList.add('active');
            
            // Actualizar texto del dropdown toggle
            const toggle = document.querySelector('.sort-dropdown-toggle span');
            if (toggle) {
                const optionText = activeOption ? activeOption.textContent.trim() : 'Ordenar por...';
                toggle.textContent = optionText;
            }
        }
    }
}

// Inicializar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', function() {
    window.sortingManager = new SortingManager();
});