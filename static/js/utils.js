// Utilidades generales para la aplicación
function getCookie(name) {
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

function showToast(message, type = 'info') {
    // Crear elemento toast
    const toast = document.createElement('div');
    toast.className = `custom-toast toast-${type} toast-new`;
    
    // Configuraciones por tipo
    const toastConfig = {
        'success': {
            icon: 'fas fa-check-circle',
            title: '¡Éxito!'
        },
        'error': {
            icon: 'fas fa-times-circle',
            title: 'Error'
        },
        'warning': {
            icon: 'fas fa-exclamation-triangle',
            title: 'Advertencia'
        },
        'info': {
            icon: 'fas fa-info-circle',
            title: 'Información'
        }
    };
    
    const config = toastConfig[type] || toastConfig.info;
    
    toast.innerHTML = `
        <div class="d-flex align-items-start">
            <i class="${config.icon} toast-icon"></i>
            <div class="flex-grow-1">
                <div class="toast-title">${config.title}</div>
                <div class="toast-message">${message}</div>
            </div>
            <button type="button" class="toast-close">
                <i class="fas fa-times"></i>
            </button>
        </div>
    `;
    
    // Agregar funcionalidad de cerrar
    const closeBtn = toast.querySelector('.toast-close');
    closeBtn.addEventListener('click', function() {
        toast.style.animation = 'fadeOut 0.4s ease forwards';
        setTimeout(() => {
            if (toast.parentNode) {
                toast.parentNode.removeChild(toast);
            }
        }, 400);
    });
    
    document.body.appendChild(toast);
    
    // Auto-remover después de 5 segundos
    setTimeout(() => {
        if (toast.parentNode) {
            toast.style.animation = 'fadeOut 0.4s ease forwards';
            setTimeout(() => {
                if (toast.parentNode) {
                    toast.parentNode.removeChild(toast);
                }
            }, 400);
        }
    }, 5000);
    
    // Remover la clase de animación de entrada después de que termine
    setTimeout(() => {
        toast.classList.remove('toast-new');
    }, 1000);
}

function updateCartCounter(count) {
    const cartBadge = document.querySelector('.cart-badge');
    if (cartBadge) {
        cartBadge.textContent = count;
        
        // Efecto de animación
        cartBadge.style.transform = 'scale(1.3)';
        setTimeout(() => {
            cartBadge.style.transform = 'scale(1)';
        }, 300);
    }
}

// Exportar funciones para uso global
window.MasivoTechUtils = {
    getCookie,
    showToast,
    updateCartCounter
};