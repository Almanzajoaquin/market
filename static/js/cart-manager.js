// CartManager unificado - Maneja todo relacionado al carrito
class CartManager {
    constructor() {
        this.init();
    }
    
    init() {
        this.bindAddToCartButtons();
        this.bindCartUpdateEvents();
    }
    
    // Para páginas de productos (product_list, ofertas, index)
    bindAddToCartButtons() {
        const addToCartButtons = document.querySelectorAll('.add-to-cart-btn');
        
        addToCartButtons.forEach(button => {
            button.addEventListener('click', (e) => {
                this.handleAddToCart(e, button);
            });
        });
    }
    
    // Solo para la página del carrito (cart.html)
    bindCartUpdateEvents() {
        // Si no estamos en la página del carrito, salir
        if (!document.querySelector('.quantity-form')) return;
        
        console.log('🛒 Inicializando eventos de actualización del carrito...');
        
        const quantityInputs = document.querySelectorAll('.quantity-input');
        const quantityForms = document.querySelectorAll('.quantity-form');
        
        quantityInputs.forEach((input, index) => {
            // Guardar el valor original para debugging
            const originalValue = input.value;
            console.log(`📦 Input ${index}: valor inicial = ${originalValue}`);
            
            input.addEventListener('change', function() {
                const newValue = this.value;
                console.log(`🔄 Cambio detectado: ${originalValue} -> ${newValue}`);
                
                if (newValue === originalValue) {
                    console.log('⏭️  Mismo valor, no hacer submit');
                    return;
                }
                
                // Mostrar loading state
                this.disabled = true;
                this.style.opacity = '0.7';
                
                console.log(`📤 Enviando formulario con cantidad: ${newValue}`);
                
                // Enviar formulario automáticamente
                quantityForms[index].submit();
            });
        });
        
        // Botones de incremento/decremento
        const quantityButtons = document.querySelectorAll('.quantity-btn');
        quantityButtons.forEach(button => {
            button.addEventListener('click', function(e) {
                e.preventDefault();
                
                const action = this.dataset.action;
                const input = this.closest('.input-group').querySelector('.quantity-input');
                const form = this.closest('.quantity-form');
                
                let currentValue = parseInt(input.value);
                const max = parseInt(input.max);
                const min = parseInt(input.min);
                
                console.log(`🔘 Botón ${action}: valor actual = ${currentValue}, min = ${min}, max = ${max}`);
                
                if (action === 'increase' && currentValue < max) {
                    input.value = currentValue + 1;
                    console.log(`➕ Nuevo valor: ${input.value}`);
                } else if (action === 'decrease' && currentValue > min) {
                    input.value = currentValue - 1;
                    console.log(`➖ Nuevo valor: ${input.value}`);
                } else {
                    console.log('⏹️  Límite alcanzado, no cambiar');
                    return;
                }
                
                // Disparar evento change para auto-submit
                console.log(`🎯 Disparando evento change con valor: ${input.value}`);
                const event = new Event('change', { bubbles: true });
                input.dispatchEvent(event);
            });
        });
        
        // Prevenir envío de formulario con Enter
        quantityForms.forEach(form => {
            form.addEventListener('keypress', function(e) {
                if (e.key === 'Enter') {
                    e.preventDefault();
                    console.log('⏹️  Enter prevenido');
                }
            });
        });
        
        console.log(`✅ Eventos de carrito inicializados: ${quantityInputs.length} inputs, ${quantityButtons.length} botones`);
    }
    
    handleAddToCart(e, button) {
        e.preventDefault();
        e.stopPropagation();
        
        const productId = button.dataset.productId;
        console.log(`🛒 Intentando agregar producto ID: ${productId}`);
        
        if (!productId) {
            console.error('❌ Error: product-id no encontrado en el botón');
            this.showErrorState(button, button.innerHTML, 'Error: ID de producto no válido');
            return;
        }
        
        this.addProductToCart(productId, 1, button);
    }
    
    addProductToCart(productId, quantity, button) {
        const originalText = button.innerHTML;
        
        // Mostrar estado de loading
        this.showLoadingState(button);
        
        console.log(`📤 Enviando petición AJAX para producto ${productId}`);
        
        // Hacer petición AJAX
        fetch(`/carrito/agregar/${productId}/`, {
            method: 'POST',
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': this.getCookie('csrftoken'),
            },
            body: new URLSearchParams({
                'quantity': quantity.toString(),
                'csrfmiddlewaretoken': this.getCookie('csrftoken')
            })
        })
        .then(response => {
            console.log(`📥 Respuesta recibida: ${response.status}`);
            if (!response.ok) {
                throw new Error(`Error HTTP: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log('📊 Datos recibidos:', data);
            if (data.success) {
                this.showSuccessState(button, originalText, data);
            } else {
                console.error('❌ Error del servidor:', data.message);
                this.showErrorState(button, originalText, data.message);
            }
        })
        .catch(error => {
            console.error('❌ Error en la petición:', error);
            this.showErrorState(button, originalText, 'Error de conexión. Intenta nuevamente.');
        });
    }
    
    showLoadingState(button) {
        button.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Agregando...';
        button.disabled = true;
        button.classList.add('btn-loading');
    }
    
    showSuccessState(button, originalText, data) {
        console.log('✅ Producto agregado exitosamente');
        this.showToast(data.message, 'success');
        this.updateCartCounter(data.cart_total_items);
        
        button.innerHTML = '<i class="fas fa-check me-2"></i>¡Agregado!';
        button.classList.remove('btn-loading');
        button.classList.add('btn-success');
        
        // Restaurar después de 2 segundos
        setTimeout(() => {
            button.innerHTML = originalText;
            button.disabled = false;
            button.classList.remove('btn-success');
        }, 2000);
    }
    
    showErrorState(button, originalText, message = 'Error al agregar al carrito') {
        console.error('❌ Mostrando error:', message);
        button.innerHTML = originalText;
        button.disabled = false;
        button.classList.remove('btn-loading');
        this.showToast(message, 'error');
    }
    
    // Utilidades
    getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    
    showToast(message, type = 'info') {
        // Usar la función de utils.js si existe, sino crear una básica
        if (window.MasivoTechUtils && typeof window.MasivoTechUtils.showToast === 'function') {
            window.MasivoTechUtils.showToast(message, type);
        } else {
            // Toast básico de emergencia
            const toast = document.createElement('div');
            toast.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
            toast.style.cssText = 'top: 20px; right: 20px; z-index: 9999;';
            toast.innerHTML = `${message}<button type="button" class="btn-close" data-bs-dismiss="alert"></button>`;
            document.body.appendChild(toast);
            setTimeout(() => toast.remove(), 4000);
        }
    }
    
    updateCartCounter(count) {
        if (window.MasivoTechUtils && typeof window.MasivoTechUtils.updateCartCounter === 'function') {
            window.MasivoTechUtils.updateCartCounter(count);
        } else {
            const cartBadge = document.querySelector('.cart-badge');
            if (cartBadge) {
                cartBadge.textContent = count;
            }
        }
    }
}

// Inicializar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 Inicializando CartManager...');
    window.cartManager = new CartManager();
});