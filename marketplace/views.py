from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q, Sum, Count
from .models import Product, Order, OrderItem
from .forms import OrderForm, ContactForm
from .cart import Cart
from django.http import HttpResponse
from django.utils import timezone
from decimal import Decimal
import mercadopago
from django.conf import settings
import json
from django.views.decorators.csrf import csrf_exempt

#????????????????????????????????????
"""vista para el historial de pedidos. Users"""
#?????????????????????????????????????
from django.contrib.auth.decorators import login_required
from .models import Order
@login_required
def order_history(request):
    """Vista para mostrar el historial de pedidos del usuario"""
    # Filtrar órdenes del usuario actual, ordenadas por fecha descendente
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    
    return render(request, 'users/order_history.html', {
        'orders': orders
    })
#????????????????????????????????????
"""vista para el historial de pedidos. Users"""
#?????????????????????????????????????


def index(request):
    """Página de inicio"""
    products = Product.objects.filter(available=True).order_by('-created_at')[:8]
    categories = Product.CATEGORY_CHOICES
    return render(request, 'marketplace/index.html', {
        'products': products,
        'categories': categories
    })

def product_list(request):
    """Lista de productos con filtros y ordenamiento"""
    category = request.GET.get('category', '')
    search_query = request.GET.get('q', '')
    sort_by = request.GET.get('sort', 'name')
    
    products = Product.objects.filter(available=True)
    
    # Filtro por categoría
    if category:
        products = products.filter(category=category)
    
    # Búsqueda por texto
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) | 
            Q(description__icontains=search_query) |
            Q(category__icontains=search_query)
        )
    
    # Ordenamiento
    sorting_options = {
        'name': 'name',
        'price_low': 'price',
        'price_high': '-price',
        'newest': '-created_at'
    }
    
    order_field = sorting_options.get(sort_by, 'name')
    products = products.order_by(order_field)
    
    categories = Product.CATEGORY_CHOICES
    
    context = {
        'products': products,
        'categories': categories,
        'selected_category': category,
        'search_query': search_query,
        'sort_by': sort_by,
    }
    
    return render(request, 'marketplace/product_list.html', context)

def product_detail(request, product_id):
    """Detalle de un producto específico"""
    product = get_object_or_404(Product, id=product_id, available=True)
    
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        cart = Cart(request)
        cart.add(product, quantity)
        messages.success(request, f'¡{quantity} x {product.name} agregado al carrito!')
        return redirect('product_detail', product_id=product_id)
    
    return render(request, 'marketplace/product_detail.html', {'product': product})

def ofertas(request):
    """Página de ofertas especiales"""
    productos_oferta = Product.objects.filter(available=True).order_by('-created_at')[:8]
    return render(request, 'marketplace/ofertas.html', {
        'productos_oferta': productos_oferta,
        'categories': Product.CATEGORY_CHOICES
    })

def contacto(request):
    """Página de contacto"""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Aquí podrías enviar un email o guardar en la base de datos
            messages.success(request, '¡Mensaje enviado correctamente! Te contactaremos pronto.')
            return redirect('contacto')
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        form = ContactForm()
    
    return render(request, 'marketplace/contacto.html', {'form': form})

def cart_detail(request):
    """Página del carrito de compras con cálculo de envío"""
    cart = Cart(request)
    
    # Verificar si hay productos que exceden el stock
    cart_has_exceeded_stock = False
    for item in cart:
        if item['quantity'] > item['product'].stock:
            cart_has_exceeded_stock = True
            break
    
    # Obtener envío de la sesión
    shipping_price = request.session.get('shipping_price', 0)
    postal_code = request.session.get('postal_code', '')
    total_with_shipping = cart.get_total_price() + Decimal(str(shipping_price))
    
    context = {
        'cart': cart,
        'cart_has_exceeded_stock': cart_has_exceeded_stock,
        'shipping_price': shipping_price,
        'postal_code': postal_code,
        'total_with_shipping': total_with_shipping,
    }
    
    return render(request, 'marketplace/cart.html', context)

def add_to_cart(request, product_id):
    """Agregar producto al carrito (soporta AJAX)"""
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))
    
    # Validar stock disponible
    cart_quantity = cart.cart.get(str(product_id), {}).get('quantity', 0)
    total_quantity = cart_quantity + quantity
    
    if total_quantity > product.stock:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': False,
                'message': f'No hay suficiente stock. Disponible: {product.stock} unidades.'
            })
        messages.error(request, f'No hay suficiente stock. Disponible: {product.stock} unidades.')
        return redirect('product_detail', product_id=product_id)
    
    # Si el producto está agotado
    if product.stock <= 0:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': False,
                'message': 'Este producto está agotado.'
            })
        messages.error(request, 'Este producto está agotado.')
        return redirect('product_detail', product_id=product_id)
    
    # Agregar al carrito si hay stock
    cart.add(product, quantity)
    
    # Si es una petición AJAX, responder con JSON
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'message': f'"{product.name}" agregado al carrito.',
            'cart_total_items': len(cart),
            'cart_total_price': str(cart.get_total_price()),
            'available_stock': product.stock - total_quantity
        })
    
    messages.success(request, f'"{product.name}" agregado al carrito.')
    return redirect('product_detail', product_id=product_id)

def remove_from_cart(request, product_id):
    """Remover producto del carrito"""
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    messages.success(request, f'"{product.name}" removido del carrito.')
    return redirect('cart_detail')

def update_cart(request, product_id):
    """Actualizar cantidad de producto en el carrito - VERSIÓN DEFINITIVA"""
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    
    print(f"🔄 Actualizando carrito - Producto: {product.name}, ID: {product_id}")
    
    # DEBUG: Mostrar todos los datos del request
    print("📋 DATOS DEL REQUEST:")
    print(f"   POST: {dict(request.POST)}")
    print(f"   GET: {dict(request.GET)}")
    print(f"   META: {request.META.get('REQUEST_METHOD')}")
    
    # Obtener la cantidad de MÚLTIPLES FUENTES
    quantity = None
    
    # 1. Intentar desde POST (formulario normal)
    quantity = request.POST.get('quantity')
    print(f"📦 Cantidad desde POST: '{quantity}'")
    
    # 2. Intentar desde GET (fallback)
    if quantity is None or quantity == '':
        quantity = request.GET.get('quantity')
        print(f"📦 Cantidad desde GET: '{quantity}'")
    
    # 3. Si todavía no hay cantidad, mostrar error
    if quantity is None or quantity == '':
        print("❌ CRÍTICO: No se recibió cantidad")
        messages.error(request, 'Error: No se recibió la cantidad. Intenta nuevamente.')
        return redirect('cart_detail')
    
    # CONVERTIR A ENTERO
    try:
        quantity = int(quantity)
        print(f"✅ Cantidad convertida a int: {quantity}")
    except (ValueError, TypeError) as e:
        print(f"❌ Error convirtiendo cantidad '{quantity}': {e}")
        messages.error(request, f'Cantidad no válida: "{quantity}"')
        return redirect('cart_detail')
    
    # VALIDACIONES DE STOCK
    if quantity > product.stock:
        print(f"⚠️  Cantidad excede stock: {quantity} > {product.stock}")
        messages.warning(request, f'No hay suficiente stock. Máximo disponible: {product.stock} unidades.')
        quantity = product.stock
    elif quantity < 1:
        print(f"⚠️  Cantidad menor a 1: {quantity}")
        messages.warning(request, 'La cantidad mínima es 1.')
        quantity = 1
    
    print(f"🛒 Cantidad final para actualizar: {quantity}")
    
    # ACTUALIZAR CARRITO
    cart.add(product, quantity, update_quantity=True)
    
    # MENSAJE DE ÉXITO
    if quantity == 1:
        messages.success(request, f'"{product.name}" actualizado a 1 unidad.')
    else:
        messages.success(request, f'"{product.name}" actualizado a {quantity} unidades.')
    
    print("✅ Carrito actualizado exitosamente")
    return redirect('cart_detail')

def clear_cart(request):
    """Vaciar todo el carrito"""
    cart = Cart(request)
    cart.clear()
    messages.success(request, 'Carrito vaciado correctamente.')
    return redirect('cart_detail')

def checkout(request):
    """Proceso de checkout - TEMPORALMENTE DESHABILITADO"""
    messages.info(request, 'Por favor, usá "Pagar con Mercado Pago" desde el carrito.')
    return redirect('cart_detail')

# Vistas de API para AJAX
def search_autocomplete(request):
    """API para autocompletado de búsqueda"""
    query = request.GET.get('q', '')
    
    if len(query) < 2:
        return JsonResponse({'results': []})
    
    products = Product.objects.filter(
        Q(name__icontains=query) | 
        Q(category__icontains=query),
        available=True
    )[:5]
    
    results = []
    for product in products:
        results.append({
            'name': product.name,
            'category': product.get_category_display(),
            'price': str(product.price),
            'url': f"/producto/{product.id}/",
            'image': product.image.url if product.image else None
        })
    
    return JsonResponse({'results': results})

def calculate_shipping(request):
    """Calcular costo de envío basado en código postal"""
    if request.method == 'POST':
        postal_code = request.POST.get('postal_code')
        print(f"🔍 DEBUG: Código postal recibido: '{postal_code}'")
        
        shipping_price = 0
        
        # Lógica simple de cálculo
        if postal_code:
            if postal_code.startswith(('1', '2')):  # CABA
                shipping_price = 1500
                print("🔍 DEBUG: Zona CABA - $1500")
            elif postal_code.startswith(('16', '17')):  # GBA
                shipping_price = 2000
                print("🔍 DEBUG: Zona GBA - $2000")
            else:  # Resto del país
                shipping_price = 3500
                print("🔍 DEBUG: Zona resto del país - $3500")
        else:
            print("🔍 DEBUG: No se recibió código postal")
        
        print(f"🔍 DEBUG: Precio de envío calculado: ${shipping_price}")
        
        # Guardar en sesión
        request.session['shipping_price'] = float(shipping_price)
        request.session['postal_code'] = postal_code
        
        print(f"🔍 DEBUG: Redirigiendo a cart_detail...")
        return redirect('cart_detail')
    
    return redirect('cart_detail')

def shipping_info(request):
    """Página de información de envíos"""
    return render(request, 'marketplace/shipping_info.html')

def envios_info(request):
    """Página de información de envíos"""
    # Precios de envío para mostrar en la página
    shipping_zones = [
        {'zona': 'CABA', 'precio': '$1.500', 'tiempo': '24-48 horas', 'ejemplos': '1001, 1425, 1876'},
        {'zona': 'GBA', 'precio': '$2.000', 'tiempo': '48-72 horas', 'ejemplos': '1600, 1700, 1754'},
        {'zona': 'Interior del país', 'precio': '$3.500', 'tiempo': '5-7 días', 'ejemplos': '5000, 8000, 9400'},
    ]
    
    context = {
        'shipping_zones': shipping_zones
    }
    
    return render(request, 'marketplace/envios_info.html', context)

# =============================================================================
# MERCADO PAGO - VISTAS NUEVAS
# =============================================================================

def create_mercadopago_payment(request):
    """Crear preferencia de pago con Mercado Pago"""
    if request.method == 'POST':
        try:
            print("🔄 Iniciando creación de pago con Mercado Pago...")
            
            # Configurar Mercado Pago
            sdk = mercadopago.SDK(settings.MERCADOPAGO_ACCESS_TOKEN)
            
            # Obtener carrito y datos de envío
            cart = Cart(request)
            shipping_price = request.session.get('shipping_price', 0)
            postal_code = request.session.get('postal_code', '')
            
            print(f"📦 Carrito: {len(cart)} items")
            print(f"🚚 Envío: ${shipping_price} para {postal_code}")
            
            # Verificar que el carrito no esté vacío
            if not cart:
                print("❌ Carrito vacío")
                return JsonResponse({'error': 'El carrito está vacío'}, status=400)
            
            # Crear items para Mercado Pago
            items = []
            total_cart = 0
            
            # Agregar productos del carrito
            for item in cart:
                product_total = float(item['price']) * item['quantity']
                total_cart += product_total
                
                items.append({
                    "title": item['product'].name[:250],  # Limitar longitud
                    "unit_price": float(item['price']),
                    "quantity": item['quantity'],
                    "currency_id": "ARS"
                })
                print(f"📋 Producto: {item['product'].name} - ${item['price']} x {item['quantity']}")
            
            print(f"💰 Total carrito: ${total_cart}")
            print(f"🚚 Envío: ${shipping_price}")
            print(f"💰 Total final: ${total_cart + float(shipping_price)}")
            
            # Agregar envío como item adicional si existe
            if shipping_price > 0:
                items.append({
                    "title": f"Envío a {postal_code}",
                    "unit_price": float(shipping_price),
                    "quantity": 1,
                    "currency_id": "ARS"
                })
            
            # Crear preferencia de pago
            preference_data = {
    "items": items,
    "back_urls": {
        "success": "http://127.0.0.1:8000/payment/success/",
        "failure": "http://127.0.0.1:8000/payment/failure/", 
        "pending": "http://127.0.0.1:8000/payment/pending/"
    },
    #"auto_return": "all",  # DEJÁ ESTO ACTIVADO
    "external_reference": f"order_{int(timezone.now().timestamp())}",
    "statement_descriptor": "MARKETPLACE"
}
            
            print("📡 Enviando solicitud a Mercado Pago...")
            preference_response = sdk.preference().create(preference_data)
            
            print(f"📨 Respuesta MP: {preference_response}")
            
            if preference_response["status"] in [200, 201]:
                preference = preference_response["response"]
                print(f"✅ Pago creado - ID: {preference['id']}")
                print(f"🔗 Init point: {preference['init_point']}")
                
                return JsonResponse({
                    'id': preference['id'],
                    'init_point': preference['init_point']
                })
            else:
                error_msg = f"Error MP: {preference_response}"
                print(f"❌ {error_msg}")
                return JsonResponse({'error': 'Error al crear el pago'}, status=500)
                
        except Exception as e:
            error_msg = f"Error en create_mercadopago_payment: {str(e)}"
            print(f"💥 {error_msg}")
            import traceback
            traceback.print_exc()
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Método no permitido'}, status=405)

def payment_success(request):
    """Página de éxito de pago"""
    cart = Cart(request)
    
    # Limpiar carrito después de pago exitoso
    cart.clear()
    
    # Limpiar datos de envío de la sesión
    if 'shipping_price' in request.session:
        del request.session['shipping_price']
    if 'postal_code' in request.session:
        del request.session['postal_code']
    
    # Obtener información del pago si está disponible
    payment_id = request.GET.get('payment_id')
    status = request.GET.get('status')
    external_reference = request.GET.get('external_reference')
    
    context = {
        'payment_id': payment_id,
        'status': status,
        'external_reference': external_reference
    }
    
    return render(request, 'marketplace/payment_success.html', context)

def payment_failure(request):
    """Página de fallo de pago"""
    payment_id = request.GET.get('payment_id')
    status = request.GET.get('status')
    
    context = {
        'payment_id': payment_id,
        'status': status
    }
    
    return render(request, 'marketplace/payment_failure.html', context)

def payment_pending(request):
    """Página de pago pendiente"""
    payment_id = request.GET.get('payment_id')
    status = request.GET.get('status')
    
    context = {
        'payment_id': payment_id,
        'status': status
    }
    
    return render(request, 'marketplace/payment_pending.html', context)

@csrf_exempt
def payment_webhook(request):
    """Webhook para recibir notificaciones de Mercado Pago"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print(f"🔔 Webhook recibido: {data}")
            
            if data.get('type') == 'payment':
                payment_id = data['data']['id']
                
                # Configurar Mercado Pago
                sdk = mercadopago.SDK(settings.MERCADOPAGO_ACCESS_TOKEN)
                payment_info = sdk.payment().get(payment_id)
                
                if payment_info["status"] == 200:
                    payment_data = payment_info["response"]
                    
                    # Procesar información del pago
                    status = payment_data.get('status')
                    external_reference = payment_data.get('external_reference')
                    transaction_amount = payment_data.get('transaction_amount')
                    
                    print(f"💰 Pago procesado - ID: {payment_id}, Estado: {status}, Referencia: {external_reference}")
                    
                    # Aquí podrías actualizar tu orden en la base de datos
                    # según el estado del pago
                    
                    if status == 'approved':
                        print("✅ Pago aprobado - Actualizar orden como pagada")
                    elif status == 'rejected':
                        print("❌ Pago rechazado - Actualizar orden como fallida")
                    elif status == 'in_process':
                        print("⏳ Pago pendiente - Actualizar orden como pendiente")
                        
            return JsonResponse({'status': 'ok'})
            
        except Exception as e:
            print(f"❌ Error en webhook: {str(e)}")
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Método no permitido'}, status=405)
