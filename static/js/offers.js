// === offers.js - Gestor de Ofertas ===

class OffersManager {
    constructor() {
        this.selectors = {
            offerCards: '.offer-card',
            offerBadges: '.offer-badge'
        };
        
        this.init();
    }

    init() {
        console.log('🔥 Inicializando OffersManager...');
        this.bindOfferEvents();
        console.log('✅ OffersManager inicializado');
    }

    /**
     * Vincula eventos de ofertas
     */
    bindOfferEvents() {
        const offerCards = document.querySelectorAll(this.selectors.offerCards);
        
        offerCards.forEach(card => {
            // Efecto hover mejorado para ofertas
            card.addEventListener('mouseenter', () => {
                card.style.transform = 'translateY(-8px) scale(1.02)';
                card.style.boxShadow = '0 12px 30px rgba(0, 0, 0, 0.15)';
                card.style.transition = 'all 0.3s ease';
            });
            
            card.addEventListener('mouseleave', () => {
                card.style.transform = 'translateY(0) scale(1)';
                card.style.boxShadow = '0 2px 10px rgba(0, 0, 0, 0.1)';
            });
        });

        console.log(`🔥 Vinculadas ${offerCards.length} tarjetas de oferta`);
    }

    /**
     * Destaca productos en oferta
     */
    highlightOffers() {
        const offerBadges = document.querySelectorAll(this.selectors.offerBadges);
        
        offerBadges.forEach(badge => {
            // Animación pulsante para badges de oferta
            badge.style.animation = 'pulse 2s infinite';
        });
    }
}

// Inicializar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', () => {
    window.offersManager = new OffersManager();
});

// Animación CSS para badges de oferta
const style = document.createElement('style');
style.textContent = `
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
`;
document.head.appendChild(style);