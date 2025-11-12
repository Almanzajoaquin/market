// === main.js - JavaScript Principal Optimizado ===

/**
 * Clase principal que maneja la inicialización de toda la aplicación
 */
class MasivoTechApp {
    constructor() {
        this.modules = new Map();
        this.initialized = false;
    }

    /**
     * Inicializa la aplicación y todos los módulos necesarios
     */
    init() {
        if (this.initialized) return;

        console.log('🚀 Iniciando MasivoTech App...');
        
        // Inicializar módulos core que se necesitan en todas las páginas
        this.initCoreModules();
        
        // Inicializar módulos específicos según la página actual
        this.initPageSpecificModules();
        
        this.initialized = true;
        console.log('✅ MasivoTech App inicializada correctamente');
    }

    /**
     * Inicializa módulos core que se necesitan en todas las páginas
     */
    initCoreModules() {
        // Tooltips de Bootstrap
        this.initTooltips();
        
        // Navegación principal
        this.initNavigation();
        
        // Sistema de notificaciones
        this.initNotifications();
    }

    /**
     * Inicializa módulos específicos según la página actual
     */
    initPageSpecificModules() {
        const path = window.location.pathname;
        
        // Mapeo de rutas a módulos (ACTUALIZADO)
        const pageModules = {
            '/carrito/': ['cart'],
            '/productos/': ['cart', 'sorting'],
            '/soporte/': ['chat'],
            '/ofertas/': ['cart', 'offers'],
            '/': ['cart']
        };

        // Encontrar módulos para la página actual
        const modulesToLoad = Object.entries(pageModules)
            .filter(([route]) => path.includes(route))
            .flatMap(([, modules]) => modules);

        // ✅ AGREGAR ESTA PARTE NUEVA para detalle de producto
        if (path.includes('/producto/')) {
            modulesToLoad.push('cart');
            modulesToLoad.push('cartPanel');
        }

        // Cargar módulos únicos
        [...new Set(modulesToLoad)].forEach(module => {
            this.tryLoadModule(module);
        });
    }

    /**
     * Intenta cargar un módulo de forma segura
     */
    tryLoadModule(moduleName) {
        try {
            let module;
            
            switch (moduleName) {
                case 'cart':
                    if (typeof CartManager !== 'undefined') {
                        module = new CartManager();
                    }
                    break;
                case 'cartPanel':
                    if (typeof CartPanelManager !== 'undefined') {
                        module = new CartPanelManager();
                    }
                    break;
                case 'sorting':
                    if (typeof SortingManager !== 'undefined') {
                        module = new SortingManager();
                    }
                    break;
                case 'offers':
                    if (typeof OffersManager !== 'undefined') {
                        module = new OffersManager();
                    }
                    break;
                case 'chat':
                    if (typeof ChatManager !== 'undefined') {
                        module = new ChatManager();
                    }
                    break;
            }
            
            if (module && typeof module.init === 'function') {
                this.modules.set(moduleName, module);
                module.init();
                console.log(`✅ Módulo ${moduleName} cargado`);
            } else {
                console.warn(`⚠️ Módulo ${moduleName} no disponible`);
            }
            
        } catch (error) {
            console.error(`❌ Error cargando módulo ${moduleName}:`, error);
        }
    }

    /**
     * Inicializa tooltips de Bootstrap
     */
    initTooltips() {
        const tooltipElements = document.querySelectorAll('[data-bs-toggle="tooltip"]');
        if (tooltipElements.length > 0 && typeof bootstrap !== 'undefined') {
            tooltipElements.forEach(el => {
                new bootstrap.Tooltip(el, {
                    trigger: 'hover focus'
                });
            });
        }
    }

    /**
     * Inicializa la navegación principal
     */
    initNavigation() {
        // La navegación ahora está manejada por navigation.js
        console.log('🧭 Navegación manejada por NavigationManager');
    }

    /**
     * Inicializa el sistema de notificaciones
     */
    initNotifications() {
        // Escuchar eventos personalizados de notificaciones
        document.addEventListener('masivotech:notification', (e) => {
            const { message, type = 'info', duration = 5000 } = e.detail;
            if (typeof MasivoTechUtils !== 'undefined') {
                MasivoTechUtils.showToast(message, type, duration);
            }
        });

        // Escuchar actualizaciones del carrito para notificar
        document.addEventListener('masivotech:cartUpdate', (e) => {
            console.log('🛒 Carrito actualizado desde main.js:', e.detail);
            
            // Notificar a todos los módulos del carrito
            if (this.modules.has('cartPanel')) {
                console.log('🔄 Notificando a CartPanelManager');
            }
            if (this.modules.has('cart')) {
                console.log('🔄 Notificando a CartManager');
            }
        });
    }

    /**
     * Obtiene un módulo específico
     */
    getModule(moduleName) {
        return this.modules.get(moduleName);
    }

    /**
     * Verifica si un módulo está cargado
     */
    hasModule(moduleName) {
        return this.modules.has(moduleName);
    }

    /**
     * Actualiza todos los módulos del carrito
     */
    updateCartModules(data) {
        // Notificar a CartManager si está cargado
        if (this.modules.has('cart')) {
            const cartManager = this.modules.get('cart');
            if (cartManager.updateCartCounter) {
                cartManager.updateCartCounter(data.cart_total_items);
            }
        }

        // Notificar a CartPanelManager si está cargado
        if (this.modules.has('cartPanel')) {
            const cartPanelManager = this.modules.get('cartPanel');
            if (cartPanelManager.updateCartBadge) {
                cartPanelManager.updateCartBadge(data.cart_total_items);
            }
            if (cartPanelManager.loadCartContent) {
                cartPanelManager.loadCartContent();
            }
        }

        // Notificar a NavigationManager si está disponible
        if (window.navigationManager && window.navigationManager.updateCartBadge) {
            window.navigationManager.updateCartBadge(data.cart_total_items);
        }
    }
}

// Inicializar la aplicación cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', () => {
    window.masivoTechApp = new MasivoTechApp();
    window.masivoTechApp.init();
});

// Función global para actualizar el carrito desde cualquier parte
window.updateMasivoTechCart = function(data) {
    if (window.masivoTechApp) {
        window.masivoTechApp.updateCartModules(data);
    }
};

// Disparar evento de actualización del carrito
window.dispatchCartUpdate = function(data) {
    const event = new CustomEvent('masivotech:cartUpdate', {
        detail: data
    });
    document.dispatchEvent(event);
    
    // También actualizar mediante la función global
    window.updateMasivoTechCart(data);
};

// Exportar para uso global
window.MasivoTechApp = MasivoTechApp;

// Auto-inicialización de módulos críticos como fallback
document.addEventListener('DOMContentLoaded', function() {
    // Inicializar CartManager como fallback si no se cargó por main.js
    setTimeout(() => {
        if (typeof CartManager !== 'undefined' && !window.masivoTechApp?.getModule('cart')) {
            console.log('🛒 Inicializando CartManager como fallback...');
            window.cartManager = new CartManager();
            window.cartManager.init();
        }

        // Inicializar CartPanelManager como fallback si no se cargó por main.js
        if (typeof CartPanelManager !== 'undefined' && !window.masivoTechApp?.getModule('cartPanel')) {
            console.log('🛒 Inicializando CartPanelManager como fallback...');
            window.cartPanelManager = new CartPanelManager();
            window.cartPanelManager.init();
        }
    }, 1000);
});
// Nuevas interacciones para las mejoras
class EnhancedInteractions {
    constructor() {
        this.init();
    }

    init() {
        this.initProductHover();
        this.initQuickView();
        this.initFormEnhancements();
        this.initScrollAnimations();
    }

    initProductHover() {
        // Efectos hover mejorados para productos
        document.addEventListener('DOMContentLoaded', () => {
            const productCards = document.querySelectorAll('.enhanced-card');
            
            productCards.forEach(card => {
                card.addEventListener('mouseenter', () => {
                    card.style.transform = 'translateY(-8px)';
                });
                
                card.addEventListener('mouseleave', () => {
                    card.style.transform = 'translateY(0)';
                });
            });
        });
    }

    initQuickView() {
        // Quick view para productos (para futura implementación)
        document.addEventListener('click', (e) => {
            if (e.target.closest('.btn-quick-view')) {
                const productId = e.target.closest('.btn-quick-view').dataset.productId;
                MasivoTechUtils.showToast('Vista rápida próximamente', 'info');
            }
        });
    }

    initFormEnhancements() {
        // Mejoras visuales para formularios
        const formInputs = document.querySelectorAll('.enhanced-form .form-control');
        
        formInputs.forEach(input => {
            input.addEventListener('focus', function() {
                this.parentElement.classList.add('focused');
            });
            
            input.addEventListener('blur', function() {
                if (!this.value) {
                    this.parentElement.classList.remove('focused');
                }
            });
        });
    }

    initScrollAnimations() {
        // Animaciones al hacer scroll
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animate-in');
                }
            });
        }, observerOptions);

        // Observar elementos para animar
        document.querySelectorAll('.enhanced-card, .stat-item, .contact-info-item').forEach(el => {
            observer.observe(el);
        });
    }
}

// Inicializar mejoras
document.addEventListener('DOMContentLoaded', () => {
    window.enhancedInteractions = new EnhancedInteractions();
});
// Mejoras para las nuevas tarjetas de productos
class EnhancedProductCards {
    constructor() {
        this.init();
    }

    init() {
        this.initQuickView();
        this.initProductHover();
        this.initLoadingStates();
    }

    initQuickView() {
        // Quick view para productos
        document.addEventListener('click', (e) => {
            if (e.target.closest('.btn-quick-view')) {
                const productId = e.target.closest('.btn-quick-view').dataset.productId;
                this.showQuickView(productId);
            }
        });
    }

    showQuickView(productId) {
        // Para futura implementación - modal de vista rápida
        MasivoTechUtils.showToast('Vista rápida próximamente', 'info');
        
        // Por ahora, redirigir a la página de detalle
        // window.location.href = `/producto/${productId}/`;
    }

    initProductHover() {
        // Efectos hover mejorados
        const productCards = document.querySelectorAll('.product-card');
        
        productCards.forEach(card => {
            card.addEventListener('mouseenter', () => {
                card.style.transform = 'translateY(-8px)';
            });
            
            card.addEventListener('mouseleave', () => {
                card.style.transform = 'translateY(0)';
            });
        });
    }

    initLoadingStates() {
        // Estados de carga para los botones
        document.addEventListener('click', (e) => {
            if (e.target.closest('.add-to-cart-btn')) {
                const btn = e.target.closest('.add-to-cart-btn');
                const card = btn.closest('.product-card');
                
                // Agregar estado de carga temporal
                card.classList.add('loading');
                setTimeout(() => {
                    card.classList.remove('loading');
                }, 1500);
            }
        });
    }
}

// Inicializar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', () => {
    window.enhancedProductCards = new EnhancedProductCards();
});