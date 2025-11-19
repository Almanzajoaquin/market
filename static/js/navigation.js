// === navigation.js - Sistema de Navegación y Paneles Laterales ===

class NavigationManager {
    constructor() {
        this.selectors = {
            mobileMenuToggle: '#mobileMenuToggle',
            mobilePanel: '#mobilePanel',
            mobilePanelClose: '#mobilePanelClose',
            cartToggle: '.cart-toggle',
            cartPanel: '#cartPanel',
            cartPanelClose: '#cartPanelClose',
            panelOverlay: '#panelOverlay',
            mobileDropdownToggle: '.mobile-dropdown-toggle',
            mobileDropdownMenu: '.mobile-dropdown-menu',
            dropdownMenu: '.dropdown-menu',
            navItemDropdown: '.nav-item.dropdown',
            userDropdown: '.user-dropdown',
            userDropdownMenu: '.user-dropdown-menu',
            searchToggle: '.search-toggle'
        };
        
        this.init();
    }

    init() {
        this.bindMobileMenuEvents();
        this.bindCartPanelEvents();
        this.bindMobileDropdownEvents();
        this.bindDesktopDropdownEvents();
        this.bindUserDropdownEvents();
        this.bindSearchEvents();
        this.bindLogoutModal();
        this.bindOverlayEvents();
        this.bindEscapeKey();
    }

    /**
     * Maneja el menú móvil
     */
    bindMobileMenuEvents() {
        const toggle = document.querySelector(this.selectors.mobileMenuToggle);
        const panel = document.querySelector(this.selectors.mobilePanel);
        const closeBtn = document.querySelector(this.selectors.mobilePanelClose);

        if (toggle && panel) {
            toggle.addEventListener('click', () => {
                this.openPanel(panel);
            });
        }

        if (closeBtn && panel) {
            closeBtn.addEventListener('click', () => {
                this.closePanel(panel);
            });
        }
    }

    /**
     * Maneja el panel del carrito
     */
    bindCartPanelEvents() {
        const toggle = document.querySelector(this.selectors.cartToggle);
        const panel = document.querySelector(this.selectors.cartPanel);
        const closeBtn = document.querySelector(this.selectors.cartPanelClose);

        if (toggle && panel) {
            toggle.addEventListener('click', (e) => {
                e.preventDefault();
                this.openPanel(panel);
            });
        }

        if (closeBtn && panel) {
            closeBtn.addEventListener('click', () => {
                this.closePanel(panel);
            });
        }
    }

    /**
     * Maneja los dropdowns en móvil
     */
    bindMobileDropdownEvents() {
        const dropdownToggles = document.querySelectorAll(this.selectors.mobileDropdownToggle);
        
        dropdownToggles.forEach(toggle => {
            toggle.addEventListener('click', (e) => {
                e.preventDefault();
                e.stopPropagation();
                
                const dropdown = toggle.nextElementSibling;
                
                if (dropdown && dropdown.classList.contains('mobile-dropdown-menu')) {
                    // Cerrar otros dropdowns
                    document.querySelectorAll('.mobile-dropdown-menu').forEach(menu => {
                        if (menu !== dropdown) {
                            menu.classList.remove('active');
                            // Resetear íconos
                            const otherIcons = menu.previousElementSibling?.querySelector('i');
                            if (otherIcons) {
                                otherIcons.classList.remove('fa-chevron-up');
                                otherIcons.classList.add('fa-chevron-down');
                            }
                        }
                    });
                    
                    // Toggle este dropdown
                    dropdown.classList.toggle('active');
                    
                    // Rotar ícono
                    const icon = toggle.querySelector('i');
                    if (icon) {
                        icon.classList.toggle('fa-chevron-down');
                        icon.classList.toggle('fa-chevron-up');
                    }
                }
            });
        });
    }

    /**
     * Maneja los dropdowns en desktop
     */
    bindDesktopDropdownEvents() {
        const dropdownItems = document.querySelectorAll(this.selectors.navItemDropdown);
        
        dropdownItems.forEach(item => {
            const dropdownMenu = item.querySelector(this.selectors.dropdownMenu);
            
            if (dropdownMenu) {
                // Hover para abrir
                item.addEventListener('mouseenter', () => {
                    if (window.innerWidth > 991) {
                        dropdownMenu.style.opacity = '1';
                        dropdownMenu.style.visibility = 'visible';
                        dropdownMenu.style.transform = 'translateY(0)';
                    }
                });
                
                // Hover para cerrar
                item.addEventListener('mouseleave', () => {
                    if (window.innerWidth > 991) {
                        dropdownMenu.style.opacity = '0';
                        dropdownMenu.style.visibility = 'hidden';
                        dropdownMenu.style.transform = 'translateY(-10px)';
                    }
                });
            }
        });
    }

    /**
     * Maneja el dropdown del usuario
     */
    bindUserDropdownEvents() {
        const userDropdowns = document.querySelectorAll(this.selectors.userDropdown);
        
        userDropdowns.forEach(dropdown => {
            const toggle = dropdown.querySelector('.user-toggle');
            const menu = dropdown.querySelector(this.selectors.userDropdownMenu);
            
            if (toggle && menu) {
                // Click para abrir/cerrar
                toggle.addEventListener('click', (e) => {
                    e.preventDefault();
                    e.stopPropagation();
                    
                    // Cerrar otros dropdowns de usuario
                    document.querySelectorAll('.user-dropdown-menu').forEach(otherMenu => {
                        if (otherMenu !== menu) {
                            otherMenu.style.opacity = '0';
                            otherMenu.style.visibility = 'hidden';
                        }
                    });
                    
                    // Toggle este dropdown
                    const isVisible = menu.style.opacity === '1';
                    if (isVisible) {
                        menu.style.opacity = '0';
                        menu.style.visibility = 'hidden';
                        menu.style.transform = 'translateY(-10px)';
                    } else {
                        menu.style.opacity = '1';
                        menu.style.visibility = 'visible';
                        menu.style.transform = 'translateY(0)';
                    }
                });
            }
        });

        // Cerrar dropdown al hacer click fuera
        document.addEventListener('click', (e) => {
            if (!e.target.closest('.user-dropdown')) {
                document.querySelectorAll('.user-dropdown-menu').forEach(menu => {
                    menu.style.opacity = '0';
                    menu.style.visibility = 'hidden';
                    menu.style.transform = 'translateY(-10px)';
                });
            }
        });

        // Cerrar dropdown con Escape
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                document.querySelectorAll('.user-dropdown-menu').forEach(menu => {
                    menu.style.opacity = '0';
                    menu.style.visibility = 'hidden';
                    menu.style.transform = 'translateY(-10px)';
                });
            }
        });
    }

    /**
     * Maneja la búsqueda
     */
    bindSearchEvents() {
        const searchToggle = document.querySelector(this.selectors.searchToggle);
        
        if (searchToggle) {
            searchToggle.addEventListener('click', (e) => {
                e.preventDefault();
                this.createSearchModal();
            });
        }
    }

    /**
     * Crea un modal de búsqueda elegante
     */
    createSearchModal() {
        // Crear overlay
        const overlay = document.createElement('div');
        overlay.className = 'search-overlay';
        
        // Crear modal
        const modal = document.createElement('div');
        modal.className = 'search-modal';
        
        modal.innerHTML = `
            <div class="search-modal-header">
                <h3>Buscar Productos</h3>
                <button class="search-close-btn" aria-label="Cerrar búsqueda">
                    <i class="fas fa-times"></i>
                </button>
            </div>
            <form class="search-modal-form" method="GET" action="/productos/">
                <input type="text" 
                       name="q" 
                       placeholder="¿Qué producto estás buscando?"
                       autocomplete="off"
                       autofocus>
                <button type="submit" aria-label="Buscar">
                    <i class="fas fa-search"></i>
                </button>
            </form>
        `;

        overlay.appendChild(modal);
        document.body.appendChild(overlay);

        // Animación de entrada
        setTimeout(() => {
            overlay.style.opacity = '1';
            modal.style.transform = 'translateY(0) scale(1)';
        }, 10);

        // Cerrar modal
        const closeBtn = modal.querySelector('.search-close-btn');
        const closeModal = () => {
            overlay.style.opacity = '0';
            modal.style.transform = 'translateY(-20px) scale(0.95)';
            setTimeout(() => {
                if (overlay.parentNode) {
                    document.body.removeChild(overlay);
                }
            }, 300);
        };

        closeBtn.addEventListener('click', closeModal);

        // Cerrar al hacer click fuera
        overlay.addEventListener('click', (e) => {
            if (e.target === overlay) {
                closeModal();
            }
        });

        // Cerrar con Escape
        const handleEscape = (e) => {
            if (e.key === 'Escape') {
                closeModal();
                document.removeEventListener('keydown', handleEscape);
            }
        };
        document.addEventListener('keydown', handleEscape);

        // Enviar formulario
        const form = modal.querySelector('.search-modal-form');
        const input = form.querySelector('input[name="q"]');
        
        form.addEventListener('submit', (e) => {
            if (!input.value.trim()) {
                e.preventDefault();
                input.focus();
            }
        });

        // Focus en el input
        input.focus();
    }

    /**
     * Maneja el modal de cerrar sesión
     */
    bindLogoutModal() {
        const logoutLinks = document.querySelectorAll('a[data-bs-target="#logoutModal"], .mobile-dropdown-item[data-bs-target="#logoutModal"]');
        
        logoutLinks.forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                e.stopPropagation();
                
                // Cerrar el panel móvil si está abierto
                this.closeAllPanels();
                
                this.showLogoutModal();
            });
        });
        
        // Manejar el modal
        const logoutModal = document.getElementById('logoutModal');
        if (logoutModal) {
            // Botón cerrar
            const closeBtn = logoutModal.querySelector('.btn-close');
            if (closeBtn) {
                closeBtn.addEventListener('click', () => {
                    this.hideLogoutModal();
                });
            }
            
            // Botón cancelar
            const cancelBtn = logoutModal.querySelector('.cancel-btn');
            if (cancelBtn) {
                cancelBtn.addEventListener('click', () => {
                    this.hideLogoutModal();
                });
            }
            
            // Cerrar modal al hacer click fuera
            logoutModal.addEventListener('click', (e) => {
                if (e.target === logoutModal) {
                    this.hideLogoutModal();
                }
            });
        }
        
        // Cerrar con Escape
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                this.hideLogoutModal();
            }
        });
    }

    /**
     * Muestra el modal de cerrar sesión
     */
    showLogoutModal() {
        const modal = document.getElementById('logoutModal');
        const overlay = document.createElement('div');
        overlay.className = 'modal-backdrop fade show';
        overlay.style.cssText = 'z-index: 1040;';
        
        if (modal) {
            modal.style.display = 'block';
            modal.style.opacity = '1';
            modal.classList.add('show');
            document.body.appendChild(overlay);
            document.body.style.overflow = 'hidden';
        }
    }

    /**
     * Oculta el modal de cerrar sesión
     */
    hideLogoutModal() {
        const modal = document.getElementById('logoutModal');
        const backdrop = document.querySelector('.modal-backdrop');
        
        if (modal) {
            modal.style.display = 'none';
            modal.classList.remove('show');
        }
        
        if (backdrop) {
            backdrop.remove();
        }
        
        document.body.style.overflow = '';
    }

    /**
     * Maneja el overlay
     */
    bindOverlayEvents() {
        const overlay = document.querySelector(this.selectors.panelOverlay);
        
        if (overlay) {
            overlay.addEventListener('click', () => {
                this.closeAllPanels();
            });
        }
    }

    /**
     * Maneja la tecla Escape
     */
    bindEscapeKey() {
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                this.closeAllPanels();
                this.hideLogoutModal();
            }
        });
    }

    /**
     * Abre un panel lateral
     */
    openPanel(panel) {
        const overlay = document.querySelector(this.selectors.panelOverlay);
        
        if (panel && overlay) {
            panel.classList.add('active');
            overlay.classList.add('active');
            document.body.style.overflow = 'hidden';
        }
    }

    /**
     * Cierra un panel lateral
     */
    closePanel(panel) {
        const overlay = document.querySelector(this.selectors.panelOverlay);
        
        if (panel && overlay) {
            panel.classList.remove('active');
            overlay.classList.remove('active');
            document.body.style.overflow = '';
        }
    }

    /**
     * Cierra todos los paneles
     */
    closeAllPanels() {
        const panels = document.querySelectorAll('.mobile-panel, .cart-panel');
        const overlay = document.querySelector(this.selectors.panelOverlay);
        
        panels.forEach(panel => {
            panel.classList.remove('active');
        });
        
        if (overlay) {
            overlay.classList.remove('active');
        }
        
        document.body.style.overflow = '';
        
        // Cerrar todos los dropdowns móviles
        document.querySelectorAll('.mobile-dropdown-menu').forEach(menu => {
            menu.classList.remove('active');
            // Resetear íconos
            const icons = menu.previousElementSibling?.querySelector('i');
            if (icons) {
                icons.classList.remove('fa-chevron-up');
                icons.classList.add('fa-chevron-down');
            }
        });
        
        // Cerrar dropdowns de usuario
        document.querySelectorAll('.user-dropdown-menu').forEach(menu => {
            menu.style.opacity = '0';
            menu.style.visibility = 'hidden';
            menu.style.transform = 'translateY(-10px)';
        });
    }

    /**
     * Actualiza el badge del carrito
     */
    updateCartBadge(count) {
        const badge = document.querySelector('.cart-badge');
        if (badge) {
            badge.textContent = count;
            
            // Animación
            badge.style.transform = 'scale(1.3)';
            setTimeout(() => {
                badge.style.transform = 'scale(1)';
            }, 300);
        }
    }
}

// Inicializar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', () => {
    window.navigationManager = new NavigationManager();
});