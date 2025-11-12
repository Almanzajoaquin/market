# === marketplace/views.py - VERSIÓN CORREGIDA Y OPTIMIZADA ===

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from decimal import Decimal
import mercadopago
import json
from django.conf import settings

from .models import Product, Order, OrderItem
from .forms import OrderForm, ContactForm
from .cart import Cart

# =============================================================================
# VISTAS PRINCIPALES
# =============================================================================

def index(request):
    """Vista principal de la página de inicio"""
    featured_products = Product.objects.filter(available=True).order_by('-created_at')[:8]
    
    context = {
        'products': featured_products,
        'categories': Product.CATEGORY_CHOICES,
        'page_title': 'Masivo Tech - Periféricos Gaming 🎮'
    }
    
    return render(request, 'marketplace/index.html', context)

def product_list(request):
    """Vista para listar productos con filtros"""
    category = request.GET.get('category', '')
    search_query = request.GET.get('q', '')
    sort_by = request.GET.get('sort', 'name')
    
    products = Product.objects.filter(available=True)
    
    # Filtros
    if category:
        products = products.filter(category=category)
    
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) | 
            Q(description__icontains=search_query)
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
    
    context = {
        'products': products,
        'categories': Product.CATEGORY_CHOICES,
        'selected_category': category,
        'search_query': search_query,
        'sort_by': sort_by,
        'page_title': 'Productos - Masivo Tech'
    }
    
    return render(request, 'marketplace/product_list.html', context)

def product_detail(request, product_id):
    """Vista para detalle de producto"""
    product = get_object_or_404(Product, id=product_id, available=True)
    
    if request.method == 'POST':
        return handle_add_to_cart(request, product)
    
    context = {
        'product': product,
        'page_title': f'{product.name} - Masivo Tech'
    }
    
    return render(request, 'marketplace/product_detail.html', context)

def handle_add_to_cart(request, product):
    """Maneja la lógica de agregar al carrito"""
    try:
        quantity = int(request.POST.get('quantity', 1))
        cart = Cart(request)
        
        # Validar stock
        cart_quantity = cart.cart.get(str(product.id), {}).get('quantity', 0)
        total_quantity = cart_quantity + quantity
        
        if total_quantity > product.stock:
            messages.error(request, f'No hay suficiente stock. Disponible: {product.stock} unidades.')
            return redirect('product_detail', product_id=product.id)
        
        cart.add(product, quantity)
        messages.success(request, f'¡{quantity} x {product.name} agregado al carrito! 🎮')
        
    except ValueError:
        messages.error(request, 'Cantidad no válida')
    except Exception as e:
        messages.error(request, 'Error al agregar al carrito')
    
    return redirect('product_detail', product_id=product.id)

def ofertas(request):
    """Vista para ofertas especiales"""
    productos_oferta = Product.objects.filter(available=True).order_by('-created_at')[:8]
    
    context = {
        'productos_oferta': productos_oferta,
        'page_title': 'Ofertas Especiales - Masivo Tech'
    }
    
    return render(request, 'marketplace/ofertas.html', context)

def contacto(request):
    """Vista para página de contacto"""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            messages.success(request, '¡Mensaje enviado correctamente! Te contactaremos pronto. 📧')
            return redirect('contacto')
    else:
        form = ContactForm()
    
    context = {
        'form': form,
        'page_title': 'Contacto - Masivo Tech'
    }
    
    return render(request, 'marketplace/contacto.html', context)

def envios_info(request):
    """Vista para información de envíos"""
    shipping_zones = [
        {'zona': 'CABA', 'precio': '$1.500', 'tiempo': '24-48 horas'},
        {'zona': 'GBA', 'precio': '$2.000', 'tiempo': '48-72 horas'},
        {'zona': 'Interior', 'precio': '$3.500', 'tiempo': '5-7 días'},
    ]
    
    context = {
        'shipping_zones': shipping_zones,
        'page_title': 'Información de Envíos - Masivo Tech'
    }
    
    return render(request, 'marketplace/envios_info.html', context)

# =============================================================================
# VISTAS DEL CARRITO (CORREGIDAS)
# =============================================================================

def cart_detail(request):
    """Vista principal del carrito"""
    cart = Cart(request)
    
    # Verificar stock
    cart_has_exceeded_stock = False
    for item in cart:
        if item['quantity'] > item['product'].stock:
            cart_has_exceeded_stock = True
            break
    
    shipping_price = request.session.get('shipping_price', 0)
    postal_code = request.session.get('postal_code', '')
    total_with_shipping = cart.get_total_price() + Decimal(str(shipping_price))
    
    context = {
        'cart': cart,
        'cart_has_exceeded_stock': cart_has_exceeded_stock,
        'shipping_price': shipping_price,
        'postal_code': postal_code,
        'total_with_shipping': total_with_shipping,
        'page_title': 'Carrito de Compras - Masivo Tech'
    }
    
    return render(request, 'marketplace/cart.html', context)

def cart_panel_api(request):
    """API para panel lateral del carrito"""
    cart = Cart(request)
    
    context = {
        'cart': cart,
        'cart_total_items': len(cart),
        'cart_total_price': cart.get_total_price(),
    }
    
    return render(request, 'marketplace/cart_panel_content.html', context)

def add_to_cart(request, product_id):
    """Agregar producto al carrito"""
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    
    try:
        quantity = int(request.POST.get('quantity', 1))
        
        # Validar stock
        cart_quantity = cart.cart.get(str(product_id), {}).get('quantity', 0)
        total_quantity = cart_quantity + quantity
        
        if total_quantity > product.stock:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'message': f'Stock insuficiente. Disponible: {product.stock}'
                })
            messages.error(request, f'Stock insuficiente. Disponible: {product.stock}')
            return redirect('product_detail', product_id=product_id)
        
        cart.add(product, quantity)
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'message': f'"{product.name}" agregado al carrito.',
                'cart_total_items': len(cart),
                'cart_total_price': str(cart.get_total_price())
            })
        
        messages.success(request, f'"{product.name}" agregado al carrito.')
        
    except ValueError:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'message': 'Cantidad no válida'})
        messages.error(request, 'Cantidad no válida')
    
    return redirect('product_detail', product_id=product_id)

def remove_from_cart(request, product_id):
    """Remover producto del carrito"""
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    
    cart.remove(product)
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'cart_total_items': len(cart),
            'cart_total_price': str(cart.get_total_price()),
            'message': 'Producto eliminado del carrito'
        })
    
    messages.success(request, f'"{product.name}" removido del carrito.')
    return redirect('cart_detail')

def update_cart(request, product_id):
    """Actualizar cantidad en carrito"""
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    
    try:
        quantity = int(request.POST.get('quantity', 1))
        
        # Validar stock
        if quantity > product.stock:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'message': f'Stock máximo: {product.stock} unidades'
                })
            messages.error(request, f'Stock máximo: {product.stock} unidades')
            return redirect('cart_detail')
        
        cart.add(product, quantity, update_quantity=True)
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'cart_total_items': len(cart),
                'cart_total_price': str(cart.get_total_price()),
                'message': 'Carrito actualizado'
            })
        
        messages.success(request, f'"{product.name}" actualizado a {quantity} unidades.')
        
    except ValueError:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'message': 'Cantidad no válida'})
        messages.error(request, 'Cantidad no válida')
    
    return redirect('cart_detail')

def clear_cart(request):
    """Vaciar carrito completo"""
    cart = Cart(request)
    cart.clear()
    messages.success(request, 'Carrito vaciado correctamente.')
    return redirect('cart_detail')

def calculate_shipping(request):
    """Calcular costo de envío"""
    if request.method == 'POST':
        postal_code = request.POST.get('postal_code', '')
        
        shipping_price = 0
        if postal_code:
            if postal_code.startswith(('1', '2')):  # CABA
                shipping_price = 1500
            elif postal_code.startswith(('16', '17')):  # GBA
                shipping_price = 2000
            else:  # Interior
                shipping_price = 3500
        
        request.session['shipping_price'] = float(shipping_price)
        request.session['postal_code'] = postal_code
    
    return redirect('cart_detail')

# =============================================================================
# MERCADO PAGO
# =============================================================================
@require_http_methods(["POST"])
@csrf_exempt
def create_mercadopago_payment(request):
    """Crear preferencia de pago en MercadoPago - VERSIÓN CON DEBUG COMPLETO"""
    try:
        print("=" * 50)
        print("🔄 INICIANDO CREACIÓN DE PAGO MERCADOPAGO")
        print("=" * 50)
        
        # 1. Verificar SDK
        try:
            import mercadopago
            print("✅ Paquete mercadopago disponible")
        except ImportError as e:
            error_msg = f"❌ mercadopago no instalado: {e}"
            print(error_msg)
            return JsonResponse({'error': error_msg}, status=500)
        
        # 2. Verificar credenciales
        if not hasattr(settings, 'MERCADOPAGO_ACCESS_TOKEN'):
            error_msg = "❌ MERCADOPAGO_ACCESS_TOKEN no existe en settings"
            print(error_msg)
            return JsonResponse({'error': error_msg}, status=500)
        
        if not settings.MERCADOPAGO_ACCESS_TOKEN:
            error_msg = "❌ MERCADOPAGO_ACCESS_TOKEN está vacío"
            print(error_msg)
            return JsonResponse({'error': error_msg}, status=500)
        
        print(f"✅ Credenciales configuradas: {settings.MERCADOPAGO_ACCESS_TOKEN[:20]}...")
        
        # 3. Inicializar SDK
        try:
            sdk = mercadopago.SDK(settings.MERCADOPAGO_ACCESS_TOKEN)
            print("✅ SDK de MercadoPago inicializado")
        except Exception as e:
            error_msg = f"❌ Error inicializando SDK: {e}"
            print(error_msg)
            return JsonResponse({'error': error_msg}, status=500)
        
        # 4. Verificar carrito
        cart = Cart(request)
        print(f"🛒 Carrito tiene {len(cart)} items")
        
        if len(cart) == 0:
            error_msg = "❌ El carrito está vacío"
            print(error_msg)
            return JsonResponse({'error': error_msg}, status=400)
        
        # 5. Construir items con validación
        items = []
        total_carrito = 0
        
        print("📦 Construyendo items del carrito:")
        for i, item in enumerate(cart, 1):
            try:
                product_name = item['product'].name[:250]  # Limitar longitud
                unit_price = float(item['price'])
                quantity = item['quantity']
                item_total = unit_price * quantity
                total_carrito += item_total
                
                item_data = {
                    "title": product_name,
                    "unit_price": unit_price,
                    "quantity": quantity,
                    "currency_id": "ARS"
                }
                items.append(item_data)
                
                print(f"   {i}. {product_name} - ${unit_price} x {quantity} = ${item_total}")
                
            except Exception as e:
                error_msg = f"❌ Error procesando item {i}: {e}"
                print(error_msg)
                return JsonResponse({'error': error_msg}, status=500)
        
        print(f"💰 Total carrito: ${total_carrito}")
        
        # 6. Agregar envío si existe
        shipping_price = request.session.get('shipping_price', 0)
        postal_code = request.session.get('postal_code', '')
        
        if shipping_price > 0:
            try:
                shipping_item = {
                    "title": f"Envío a {postal_code}"[:250],
                    "unit_price": float(shipping_price),
                    "quantity": 1,
                    "currency_id": "ARS"
                }
                items.append(shipping_item)
                print(f"🚚 Envío agregado: ${shipping_price} para {postal_code}")
            except Exception as e:
                error_msg = f"❌ Error agregando envío: {e}"
                print(error_msg)
                return JsonResponse({'error': error_msg}, status=500)
        
        # 7. Crear preferencia de pago
        preference_data = {
            "items": items,
            "back_urls": {
                "success": "http://127.0.0.1:8000/payment/success/",
                "failure": "http://127.0.0.1:8000/payment/failure/", 
                "pending": "http://127.0.0.1:8000/payment/pending/"
            },
            # "auto_return": "approved",  # ← REMOVER ESTA LÍNEA
            "external_reference": f"masivotech_{int(timezone.now().timestamp())}",
        }
        
        print("📤 Enviando datos a MercadoPago...")
        print(f"📊 Datos enviados: {preference_data}")
        
        try:
            preference_response = sdk.preference().create(preference_data)
            print(f"📥 Respuesta de MP recibida: {preference_response}")
        except Exception as e:
            error_msg = f"❌ Error en la petición a MercadoPago: {e}"
            print(error_msg)
            return JsonResponse({'error': error_msg}, status=500)
        
        # 8. Procesar respuesta
        if preference_response["status"] in [200, 201]:
            preference = preference_response["response"]
            init_point = preference.get('init_point') or preference.get('sandbox_init_point')
            
            if not init_point:
                error_msg = "❌ MercadoPago no devolvió URL de pago válida"
                print(error_msg)
                print(f"📋 Respuesta completa: {preference}")
                return JsonResponse({'error': error_msg}, status=500)
            
            print(f"✅ Pago creado exitosamente - ID: {preference['id']}")
            print(f"🔗 URL de pago: {init_point}")
            
            return JsonResponse({
                'id': preference['id'],
                'init_point': init_point,
                'message': 'Pago creado exitosamente'
            })
        else:
            error_msg = f"❌ Error de MercadoPago - Status: {preference_response['status']}"
            print(error_msg)
            print(f"📋 Respuesta completa: {preference_response}")
            return JsonResponse({'error': error_msg}, status=500)
            
    except Exception as e:
        error_msg = f"💥 ERROR NO MANEJADO: {str(e)}"
        print(error_msg)
        import traceback
        print(f"📝 Traceback completo: {traceback.format_exc()}")
        return JsonResponse({'error': error_msg}, status=500)


def payment_success(request):
    """Pago exitoso"""
    cart = Cart(request)
    cart.clear()
    clear_shipping_session(request)
    
    context = {
        'payment_id': request.GET.get('payment_id'),
        'status': request.GET.get('status'),
        'page_title': 'Pago Exitoso - Masivo Tech'
    }
    
    return render(request, 'marketplace/payment_success.html', context)

def payment_failure(request):
    """Pago fallido"""
    context = {
        'payment_id': request.GET.get('payment_id'),
        'status': request.GET.get('status'),
        'page_title': 'Pago Fallido - Masivo Tech'
    }
    
    messages.error(request, 'El pago no pudo ser procesado.')
    return render(request, 'marketplace/payment_failure.html', context)

def payment_pending(request):
    """Pago pendiente"""
    context = {
        'payment_id': request.GET.get('payment_id'),
        'status': request.GET.get('status'),
        'page_title': 'Pago Pendiente - Masivo Tech'
    }
    
    messages.info(request, 'Tu pago está siendo procesado.')
    return render(request, 'marketplace/payment_pending.html', context)

@csrf_exempt
def payment_webhook(request):
    """Webhook para notificaciones de MercadoPago"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print(f"📦 Webhook recibido: {data}")
            return JsonResponse({'status': 'ok'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Método no permitido'}, status=405)

# =============================================================================
# UTILIDADES
# =============================================================================

def get_base_url(request):
    """Obtener URL base"""
    if hasattr(settings, 'BASE_URL'):
        return settings.BASE_URL.rstrip('/')
    return 'http://127.0.0.1:8000'

def clear_shipping_session(request):
    """Limpiar datos de envío de la sesión"""
    for key in ['shipping_price', 'postal_code']:
        if key in request.session:
            del request.session[key]

def search_autocomplete(request):
    """Autocompletado de búsqueda"""
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

@login_required
def order_history(request):
    """Historial de pedidos del usuario"""
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    
    context = {
        'orders': orders,
        'page_title': 'Mis Pedidos - Masivo Tech'
    }
    
    return render(request, 'users/order_history.html', context)