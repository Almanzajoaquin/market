// === utils.js - Utilidades Generales Optimizadas ===

/**
 * Utilidades generales para MasivoTech
 * Funciones reutilizables y helpers
 */
class MasivoTechUtils {
    /**
     * Obtiene el valor de una cookie por nombre
     */
    static getCookie(name) {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        if (parts.length === 2) return parts.pop().split(';').shift();
        return null;
    }

    /**
     * Muestra una notificación toast
     */
    static showToast(message, type = 'info', duration = 5000) {
        // Crear contenedor de toasts si no existe
        let toastContainer = document.getElementById('toast-container');
        if (!toastContainer) {
            toastContainer = document.createElement('div');
            toastContainer.id = 'toast-container';
            toastContainer.className = 'toast-container';
            document.body.appendChild(toastContainer);
        }

        const toast = this.createToastElement(message, type);
        toastContainer.appendChild(toast);

        // Auto-remover después de la duración
        setTimeout(() => {
            this.removeToast(toast);
        }, duration);

        return toast;
    }

    /**
     * Crea elemento toast
     */
    static createToastElement(message, type) {
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        
        const icons = {
            success: 'check-circle',
            error: 'exclamation-triangle',
            warning: 'exclamation-circle',
            info: 'info-circle'
        };

        toast.innerHTML = `
            <div class="toast-content">
                <i class="fas fa-${icons[type] || 'info-circle'} toast-icon"></i>
                <div class="toast-message">${message}</div>
                <button class="toast-close" aria-label="Cerrar">
                    <i class="fas fa-times"></i>
                </button>
            </div>
        `;

        // Agregar funcionalidad de cerrar
        const closeBtn = toast.querySelector('.toast-close');
        closeBtn.addEventListener('click', () => this.removeToast(toast));

        // Animar entrada
        requestAnimationFrame(() => {
            toast.classList.add('toast-show');
        });

        return toast;
    }

    /**
     * Remueve toast con animación
     */
    static removeToast(toast) {
        toast.classList.remove('toast-show');
        toast.classList.add('toast-hide');
        
        setTimeout(() => {
            if (toast.parentNode) {
                toast.parentNode.removeChild(toast);
            }
        }, 300);
    }

    /**
     * Formatea precio en formato argentino
     */
    static formatPrice(price) {
        return new Intl.NumberFormat('es-AR', {
            style: 'currency',
            currency: 'ARS'
        }).format(price);
    }

    /**
     * Valida formato de email
     */
    static isValidEmail(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }

    /**
     * Valida formato de teléfono argentino
     */
    static isValidPhone(phone) {
        const phoneRegex = /^(\+54|54|0)?(9|11|15)?[2-9]\d{7}$/;
        return phoneRegex.test(phone.replace(/\s/g, ''));
    }

    /**
     * Debounce function para optimizar eventos
     */
    static debounce(func, wait, immediate = false) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                timeout = null;
                if (!immediate) func(...args);
            };
            const callNow = immediate && !timeout;
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
            if (callNow) func(...args);
        };
    }

    /**
     * Throttle function para limitar ejecuciones
     */
    static throttle(func, limit) {
        let inThrottle;
        return function(...args) {
            if (!inThrottle) {
                func.apply(this, args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        };
    }

    /**
     * Maneja errores de API de forma consistente
     */
    static handleApiError(error, context = '') {
        let userMessage = 'Ocurrió un error inesperado. Por favor, intenta nuevamente.';
        
        if (error.message.includes('NetworkError')) {
            userMessage = 'Error de conexión. Verifica tu conexión a internet.';
        } else if (error.message.includes('Failed to fetch')) {
            userMessage = 'No se pudo conectar con el servidor. Intenta más tarde.';
        }
        
        this.showToast(userMessage, 'error');
        return userMessage;
    }

    /**
     * Realiza peticiones fetch con manejo de errores
     */
    static async fetchWithErrorHandling(url, options = {}) {
        try {
            const response = await fetch(url, {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': this.getCookie('csrftoken'),
                    ...options.headers
                },
                ...options
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            throw this.handleApiError(error, 'fetch');
        }
    }

    /**
     * Scroll suave a un elemento
     */
    static smoothScrollTo(element, offset = 0) {
        const elementPosition = element.getBoundingClientRect().top;
        const offsetPosition = elementPosition + window.pageYOffset - offset;

        window.scrollTo({
            top: offsetPosition,
            behavior: 'smooth'
        });
    }

    /**
     * Detecta si el dispositivo es móvil
     */
    static isMobileDevice() {
        return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
    }

    /**
     * Detecta si el usuario prefiere motion reducido
     */
    static prefersReducedMotion() {
        return window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    }
}

// Hacer utilidades disponibles globalmente
window.MasivoTechUtils = MasivoTechUtils;