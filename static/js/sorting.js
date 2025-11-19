// === sorting.js - Sistema de Ordenamiento ===

class SortingManager {
    constructor() {
        this.selectors = {
            sortSelect: 'select[onchange*="updateUrlParameter"]',
            sortDropdown: '.sort-dropdown',
            productsGrid: '.products-grid'
        };
        
        this.init();
    }

    init() {
        this.bindSortingEvents();
    }

    /**
     * Vincula eventos de ordenamiento
     */
    bindSortingEvents() {
        // Select de ordenamiento
        const sortSelect = document.querySelector(this.selectors.sortSelect);
        
        if (sortSelect) {
            sortSelect.addEventListener('change', (e) => {
                const sortValue = e.target.value;
                this.applySorting(sortValue);
            });
        }

        // Mostrar loading al cambiar ordenamiento
        this.addLoadingIndicator();
    }

    /**
     * Aplica el ordenamiento seleccionado
     */
    applySorting(sortValue) {
        const currentUrl = new URL(window.location.href);
        
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

    /**
     * Muestra estado de loading
     */
    showLoadingState() {
        const productsGrid = document.querySelector(this.selectors.productsGrid);
        if (productsGrid) {
            productsGrid.style.opacity = '0.7';
            productsGrid.style.transition = 'opacity 0.3s ease';
        }
        
        MasivoTechUtils.showToast('Aplicando ordenamiento...', 'info', 2000);
    }

    /**
     * Agrega indicador de loading al DOM
     */
    addLoadingIndicator() {
        // Puedes agregar un spinner visual si lo necesitas
        const style = document.createElement('style');
        style.textContent = `
            .sorting-loading {
                position: fixed;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                background: rgba(0, 0, 0, 0.8);
                color: white;
                padding: 1rem 2rem;
                border-radius: 8px;
                z-index: 9999;
            }
        `;
        document.head.appendChild(style);
    }
}

// Inicializar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', () => {
    window.sortingManager = new SortingManager();
});