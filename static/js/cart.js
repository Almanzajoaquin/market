// === cart.js - Con animación de confirmación ===

class CartManager {
    constructor() {
        this.selectors = {
            addButtons: '.add-to-cart-btn',
            detailButtons: '.add-to-cart-btn-detail',
            cartBadge: '.cart-badge'
        };
        
        this.initialized = false;
    }

    init() {
        if (this.initialized) return;

        this.cleanupExistingListeners();
        this.bindAddToCartEvents();
        this.initialized = true;
    }

    cleanupExistingListeners() {
        // Limpiar event listeners anteriores
        document.querySelectorAll(this.selectors.addButtons).forEach(button => {
            const newButton = button.cloneNode(true);
            button.parentNode.replaceChild(newButton, button);
        });

        document.querySelectorAll(this.selectors.detailButtons).forEach(button => {
            const newButton = button.cloneNode(true);
            button.parentNode.replaceChild(newButton, button);
        });
    }

    bindAddToCartEvents() {
        document.querySelectorAll(this.selectors.addButtons).forEach(button => {
            button.addEventListener('click', (e) => {
                e.preventDefault();
                e.stopPropagation();
                e.stopImmediatePropagation();
                this.handleAddToCart(button);
            }, true);
        });

        document.querySelectorAll(this.selectors.detailButtons).forEach(button => {
            button.addEventListener('click', (e) => {
                e.preventDefault();
                e.stopPropagation();
                e.stopImmediatePropagation();
                this.handleAddToCartDetail(button);
            }, true);
        });
    }

    handleAddToCart(button) {
        const productId = button.dataset.productId;
        if (!productId) return;
        this.addProductToCart(productId, 1, button);
    }

    handleAddToCartDetail(button) {
        const productId = button.dataset.productId;
        const quantityInput = document.getElementById('quantity');
        const quantity = quantityInput ? parseInt(quantityInput.value) : 1;
        if (!productId || quantity < 1) return;
        this.addProductToCart(productId, quantity, button);
    }

    async addProductToCart(productId, quantity, button) {
        // Guardar estado original
        const originalHTML = button.innerHTML;
        const originalDisabled = button.disabled;
        const originalClasses = button.className;
        
        // 🔄 1. ESTADO DE CARGA
        button.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Agregando...';
        button.disabled = true;
        button.className = originalClasses + ' btn-loading';
        
        try {
            const response = await fetch(`/carrito/agregar/${productId}/`, {
                method: 'POST',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': this.getCSRFToken(),
                },
                body: new URLSearchParams({
                    'quantity': quantity.toString(),
                    'csrfmiddlewaretoken': this.getCSRFToken()
                })
            });

            const data = await response.json();
            
            if (data.success) {
                // ✅ 2. ESTADO DE ÉXITO (animación)
                button.innerHTML = '<i class="fas fa-check me-2"></i>¡Agregado!';
                button.className = originalClasses + ' btn-success';
                button.style.transform = 'scale(1.05)';
                button.style.transition = 'all 0.3s ease';
                
                MasivoTechUtils.showToast(data.message, 'success');
                this.updateGlobalCartBadge(data.cart_total_items);
                this.notifyCartPanel();
                
                // 🔄 3. RESTAURAR DESPUÉS DE 1.5 SEGUNDOS
                setTimeout(() => {
                    button.innerHTML = originalHTML;
                    button.disabled = originalDisabled;
                    button.className = originalClasses;
                    button.style.transform = 'scale(1)';
                }, 1500);
                
            } else {
                // ❌ ERROR - Restaurar inmediatamente
                button.innerHTML = originalHTML;
                button.disabled = originalDisabled;
                button.className = originalClasses;
                MasivoTechUtils.showToast(data.message, 'error');
            }
            
        } catch (error) {
            // ❌ ERROR - Restaurar inmediatamente
            button.innerHTML = originalHTML;
            button.disabled = originalDisabled;
            button.className = originalClasses;
            MasivoTechUtils.showToast('Error de conexión', 'error');
        }
    }

    getCSRFToken() {
        return document.querySelector('[name=csrfmiddlewaretoken]')?.value || 
               (typeof MasivoTechUtils !== 'undefined' ? MasivoTechUtils.getCookie('csrftoken') : '');
    }

    notifyCartPanel() {
        if (window.cartPanelSimple && window.cartPanelSimple.reloadCartPanel) {
            window.cartPanelSimple.reloadCartPanel();
        }
    }

    updateGlobalCartBadge(count) {
        const badges = document.querySelectorAll('.cart-badge, #cartPanelCount');
        badges.forEach(badge => {
            if (badge) {
                badge.textContent = count;
                badge.style.transform = 'scale(1.3)';
                setTimeout(() => badge.style.transform = 'scale(1)', 300);
            }
        });
        
        if (window.navigationManager && window.navigationManager.updateCartBadge) {
            window.navigationManager.updateCartBadge(count);
        }
    }
}

// Inicialización
if (!window.cartManager) {
    document.addEventListener('DOMContentLoaded', () => {
        window.cartManager = new CartManager();
        window.cartManager.init();
    });
}