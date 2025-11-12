from django.urls import path
from . import views
from .views import cart_panel_api

urlpatterns = [
    # Páginas principales
    path('', views.index, name='index'),
    path('productos/', views.product_list, name='product_list'),
    path('producto/<int:product_id>/', views.product_detail, name='product_detail'),
    path('ofertas/', views.ofertas, name='ofertas'),
    path('contacto/', views.contacto, name='contacto'),
    path('envios/', views.envios_info, name='envios_info'),
    
    # Carrito
    path('carrito/', views.cart_detail, name='cart_detail'),
    path('carrito/agregar/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('carrito/remover/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('carrito/actualizar/<int:product_id>/', views.update_cart, name='update_cart'),
    path('carrito/vaciar/', views.clear_cart, name='clear_cart'),
    path('carrito/calcular-envio/', views.calculate_shipping, name='calculate_shipping'),
    path('carrito/api/panel/', cart_panel_api, name='cart_panel_api'),

    # Mercado Pago
    path('payment/create/', views.create_mercadopago_payment, name='create_payment'),
    path('payment/success/', views.payment_success, name='payment_success'),
    path('payment/failure/', views.payment_failure, name='payment_failure'),
    path('payment/pending/', views.payment_pending, name='payment_pending'),
    path('payment/webhook/', views.payment_webhook, name='payment_webhook'),
    
    # API y Utilidades
    path('buscar/autocomplete/', views.search_autocomplete, name='search_autocomplete'),
    path('mis-pedidos/', views.order_history, name='order_history'),
]