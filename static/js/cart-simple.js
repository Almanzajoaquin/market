// JavaScript simplificado para el carrito - SOLO actualización de cantidades
document.addEventListener('DOMContentLoaded', function() {
    console.log('🛒 Inicializando carrito...');
    
    // Botones de + y -
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
            
            console.log(`🔘 Botón ${action}: ${currentValue} -> `);
            
            if (action === 'increase' && currentValue < max) {
                input.value = currentValue + 1;
                console.log(`➕ Nuevo valor: ${input.value}`);
            } else if (action === 'decrease' && currentValue > min) {
                input.value = currentValue - 1;
                console.log(`➖ Nuevo valor: ${input.value}`);
            } else {
                console.log('⏹️  Límite alcanzado');
                return;
            }
            
            // Enviar formulario inmediatamente
            console.log('📤 Enviando formulario...');
            form.submit();
        });
    });
    
    // Input directo - enviar al cambiar
    const quantityInputs = document.querySelectorAll('.quantity-input');
    quantityInputs.forEach(input => {
        input.addEventListener('change', function() {
            console.log('📝 Cambio manual:', this.value);
            this.closest('.quantity-form').submit();
        });
    });
    
    console.log(`✅ Carrito inicializado: ${quantityButtons.length} botones, ${quantityInputs.length} inputs`);
});