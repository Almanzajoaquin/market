// === cart-panel-simple.js - Carrito Lateral Simple ===

class CartPanelSimple {
    constructor() {
        this.initialized = false;
        this.init();
    }

    init() {
        if (this.initialized) return;
        
        console.log('🛒 Inicializando CartPanelSimple...');
        this.bindEvents();
        this.loadInitialCart();
        this.initialized = true;
    }

    async loadInitialCart() {
        console.log('📥 CartPanelSimple: Cargando carrito inicial...');
        await this.reloadCartPanel();
    }

    bindEvents() {
        // Delegación de eventos para los botones del carrito lateral
        document.addEventListener('click', (e) => {
            const cartPanel = document.getElementById('cartPanel');
            if (!cartPanel || !cartPanel.classList.contains('active')) return;

            // Botón +
            if (e.target.closest('.cart-plus')) {
                e.preventDefault();
                e.stopPropagation();
                this.handleQuantityChange(e.target.closest('.cart-plus'), 1);
            }
            // Botón -
            if (e.target.closest('.cart-minus')) {
                e.preventDefault();
                e.stopPropagation();
                this.handleQuantityChange(e.target.closest('.cart-minus'), -1);
            }
            // Botón eliminar
            if (e.target.closest('.cart-remove')) {
                e.preventDefault();
                e.stopPropagation();
                this.handleRemoveItem(e.target.closest('.cart-remove'));
            }
        });

        // Escuchar cuando se agregan productos al carrito
        document.addEventListener('masivotech:cartPanelUpdate', () => {
            console.log('🔄 CartPanelSimple: Recibió actualización del cart manager');
            this.reloadCartPanel();
        });

        // También escuchar el evento general de cart update
        document.addEventListener('masivotech:cartUpdate', (e) => {
            console.log('🔄 CartPanelSimple: Cart update recibido', e.detail);
            this.reloadCartPanel();
        });

        // Recargar cuando se abre el panel
        document.addEventListener('click', (e) => {
            if (e.target.closest('.cart-toggle')) {
                setTimeout(() => {
                    this.reloadCartPanel();
                }, 300);
            }
        });
    }

    async handleQuantityChange(button, change) {
        const productId = button.dataset.productId;
        const quantityElement = document.getElementById(`quantity${productId}`);
        
        if (!quantityElement) {
            console.error('❌ No se encontró elemento de cantidad para producto:', productId);
            return;
        }

        let currentQuantity = parseInt(quantityElement.textContent) || 1;
        let newQuantity = currentQuantity + change;

        // Validar límites
        if (newQuantity < 1) newQuantity = 1;

        console.log(`🔄 Actualizando cantidad: ${currentQuantity} → ${newQuantity} para producto ${productId}`);
        
        // Actualizar visualmente inmediatamente
        quantityElement.textContent = newQuantity;
        
        // Habilitar/deshabilitar botón -
        const minusBtn = document.querySelector(`.cart-minus[data-product-id="${productId}"]`);
        if (minusBtn) {
            minusBtn.disabled = newQuantity <= 1;
        }

        // Actualizar total del item (estimado)
        this.updateItemTotal(productId, newQuantity);

        // Enviar actualización al servidor
        await this.updateCartItem(productId, newQuantity);
    }

    updateItemTotal(productId, quantity) {
        const totalElement = document.getElementById(`total${productId}`);
        if (!totalElement) return;

        // Buscar el precio unitario
        const priceText = totalElement.closest('.cart-panel-item')?.querySelector('.cart-item-price')?.textContent;
        if (priceText) {
            const unitPrice = parseFloat(priceText.replace('$', '').replace(' c/u', ''));
            if (!isNaN(unitPrice)) {
                const total = unitPrice * quantity;
                totalElement.textContent = `$${total.toFixed(2)}`;
            }
        }
    }

    async handleRemoveItem(button) {
        const productId = button.dataset.productId;
        
        if (!confirm('¿Estás seguro de que quieres eliminar este producto del carrito?')) {
            return;
        }

        await this.removeCartItem(productId);
    }

        async updateCartItem(productId, quantity) {
        try {
            console.log(`📤 Enviando actualización: Producto ${productId}, Cantidad ${quantity}`);
            
            const formData = new URLSearchParams();
            formData.append('quantity', quantity);
            formData.append('csrfmiddlewaretoken', this.getCSRFToken());

            const response = await fetch(`/carrito/actualizar/${productId}/`, {
                method: 'POST',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': this.getCSRFToken(),
                },
                body: formData
            });

            if (response.ok) {
                const data = await response.json();
                console.log('✅ Respuesta del servidor:', data);
                
                if (data.success) {
                    this.updateCartDisplay(data);
                    MasivoTechUtils.showToast(data.message || 'Carrito actualizado', 'success');
                    
                    // Si el carrito quedó vacío después de actualizar, recargar panel
                    if (data.cart_total_items === 0) {
                        setTimeout(() => {
                            this.reloadCartPanel();
                        }, 1000);
                    }
                } else {
                    throw new Error(data.message || 'Error del servidor');
                }
            } else {
                throw new Error(`Error HTTP: ${response.status}`);
            }
        } catch (error) {
            console.error('❌ Error actualizando item:', error);
            MasivoTechUtils.showToast(error.message || 'Error al actualizar el carrito', 'error');
            this.reloadCartPanel(); // Recargar todo el panel en caso de error
        }
    }

    async removeCartItem(productId) {
        try {
            console.log(`📤 Enviando eliminación: Producto ${productId}`);
            
            const formData = new URLSearchParams();
            formData.append('csrfmiddlewaretoken', this.getCSRFToken());

            const response = await fetch(`/carrito/remover/${productId}/`, {
                method: 'POST',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': this.getCSRFToken(),
                },
                body: formData
            });

            if (response.ok) {
                const data = await response.json();
                console.log('✅ Respuesta del servidor:', data);
                
                if (data.success) {
                    this.updateCartDisplay(data);
                    MasivoTechUtils.showToast(data.message || 'Producto eliminado del carrito', 'success');
                    
                    // Recargar panel completo después de eliminar
                    setTimeout(() => {
                        this.reloadCartPanel();
                    }, 500);
                } else {
                    throw new Error(data.message || 'Error del servidor');
                }
            } else {
                throw new Error(`Error HTTP: ${response.status}`);
            }
        } catch (error) {
            console.error('❌ Error eliminando item:', error);
            MasivoTechUtils.showToast(error.message || 'Error al eliminar el producto', 'error');
            this.reloadCartPanel(); // Recargar todo el panel en caso de error
        }
    }

        updateCartDisplay(data) {
        console.log('📊 Actualizando display del carrito:', data);
        
        // Actualizar badge del carrito en el header
        const badge = document.querySelector('.cart-badge');
        const panelCount = document.getElementById('cartPanelCount');
        
        if (badge && data.cart_total_items !== undefined) {
            badge.textContent = data.cart_total_items;
            // Animación
            badge.style.transform = 'scale(1.3)';
            setTimeout(() => {
                badge.style.transform = 'scale(1)';
            }, 300);
        }
        if (panelCount && data.cart_total_items !== undefined) {
            panelCount.textContent = data.cart_total_items;
        }

        // Actualizar total del panel si está disponible
        if (data.cart_total_price) {
            const panelTotal = document.getElementById('cartPanelTotal');
            if (panelTotal) {
                panelTotal.textContent = `$${data.cart_total_price}`;
            }
        }

        // Actualizar NavigationManager si existe
        if (window.navigationManager && window.navigationManager.updateCartBadge) {
            window.navigationManager.updateCartBadge(data.cart_total_items);
        }

        // Notificar al CartManager principal
        if (window.cartManager && window.cartManager.updateGlobalCartBadge) {
            window.cartManager.updateGlobalCartBadge(data.cart_total_items);
        }
    }

    async reloadCartPanel() {
        const contentElement = document.getElementById('cartPanelContent');
        const cartPanel = document.getElementById('cartPanel');
        
        if (!contentElement) {
            console.log('❌ CartPanelSimple: No se encontró cartPanelContent');
            return;
        }

        try {
            console.log('🔄 CartPanelSimple: Recargando panel del carrito...');
            
            const response = await fetch('/carrito/api/panel/');
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const html = await response.text();
            contentElement.innerHTML = html;
            
            console.log('✅ CartPanelSimple: Panel recargado correctamente');
            
        } catch (error) {
            console.error('❌ CartPanelSimple: Error recargando panel:', error);
            
            // Mostrar error elegante
            contentElement.innerHTML = `
                <div class="cart-panel-error text-center py-4">
                    <i class="fas fa-exclamation-triangle fa-2x text-warning mb-2"></i>
                    <p class="text-muted">Error al cargar el carrito</p>
                    <button onclick="window.cartPanelSimple.reloadCartPanel()" class="btn btn-sm btn-outline-primary">
                        Reintentar
                    </button>
                </div>
            `;
        }
    }

    getCSRFToken() {
        let token = document.querySelector('[name=csrfmiddlewaretoken]')?.value;
        if (!token && typeof MasivoTechUtils !== 'undefined') {
            token = MasivoTechUtils.getCookie('csrftoken');
        }
        console.log('🔐 CSRF Token:', token ? 'Encontrado' : 'No encontrado');
        return token;
    }

    // Método para abrir el panel manualmente
    openPanel() {
        const cartPanel = document.getElementById('cartPanel');
        const overlay = document.querySelector('.panel-overlay');
        
        if (cartPanel && overlay) {
            cartPanel.classList.add('active');
            overlay.classList.add('active');
            document.body.style.overflow = 'hidden';
            
            // Cargar contenido cuando se abre
            this.reloadCartPanel();
        }
    }

    // Método para cerrar el panel manualmente
    closePanel() {
        const cartPanel = document.getElementById('cartPanel');
        const overlay = document.querySelector('.panel-overlay');
        
        if (cartPanel) {
            cartPanel.classList.remove('active');
        }
        if (overlay) {
            overlay.classList.remove('active');
        }
        
        document.body.style.overflow = '';
    }
}

// Inicializar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', () => {
    window.cartPanelSimple = new CartPanelSimple();
});

// Hacer disponible globalmente
window.CartPanelSimple = CartPanelSimple;