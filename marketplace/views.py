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
    """Proceso de checkout"""
    cart = Cart(request)
    
    if not cart:
        messages.warning(request, 'Tu carrito está vacío.')
        return redirect('product_list')
    
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.total_amount = cart.get_total_price()
            order.save()
            
            # Crear items de la orden
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    quantity=item['quantity'],
                    price=item['price']
                )
            
            # Limpiar carrito
            cart.clear()
            
            # Mostrar página de éxito
            return render(request, 'marketplace/order_success.html', {'order': order})
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        # Pre-llenar formulario si el usuario está autenticado
        initial_data = {}
        if request.user.is_authenticated:
            initial_data = {
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
                'email': request.user.email,
            }
        form = OrderForm(initial=initial_data)
    
    return render(request, 'marketplace/checkout.html', {
        'form': form,
        'cart': cart
    })

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