from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q, Sum, Count
from .models import Product, Order, OrderItem
from .forms import OrderForm, ContactForm
from .cart import Cart

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
    """Página del carrito de compras"""
    cart = Cart(request)
    
    # Verificar si hay productos que exceden el stock
    cart_has_exceeded_stock = False
    for item in cart:
        if item['quantity'] > item['product'].stock:
            cart_has_exceeded_stock = True
            break
    
    return render(request, 'marketplace/cart.html', {
        'cart': cart,
        'cart_has_exceeded_stock': cart_has_exceeded_stock
    })

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
    """Actualizar cantidad de producto en el carrito"""
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    
    print(f"🔄 Actualizando carrito - Producto: {product.name}, ID: {product_id}")
    
    # Obtener la cantidad del formulario
    quantity = request.POST.get('quantity')
    print(f"📦 Cantidad recibida: {quantity}")
    
    # Validar que quantity no sea None y sea un número válido
    if quantity is None:
        print("❌ Cantidad es None")
        messages.error(request, 'Cantidad no válida.')
        return redirect('cart_detail')
    
    try:
        quantity = int(quantity)
        print(f"✅ Cantidad convertida a int: {quantity}")
    except (ValueError, TypeError) as e:
        print(f"❌ Error convirtiendo cantidad: {e}")
        messages.error(request, 'Cantidad no válida.')
        return redirect('cart_detail')
    
    # Validar que no exceda el stock
    if quantity > product.stock:
        print(f"⚠️  Cantidad excede stock: {quantity} > {product.stock}")
        messages.error(request, f'No puedes agregar más de {product.stock} unidades de "{product.name}".')
        quantity = product.stock
    elif quantity < 1:
        print(f"⚠️  Cantidad menor a 1: {quantity}")
        messages.error(request, 'La cantidad debe ser al menos 1.')
        quantity = 1
    else:
        print(f"✅ Cantidad válida: {quantity}")
    
    # Actualizar o remover del carrito
    if quantity > 0:
        print(f"🛒 Actualizando cantidad a: {quantity}")
        cart.add(product, quantity, update_quantity=True)
        messages.success(request, f'Cantidad de "{product.name}" actualizada a {quantity}.')
    else:
        print("🗑️  Removiendo producto del carrito")
        cart.remove(product)
        messages.success(request, f'"{product.name}" removido del carrito.')
    
    print("✅ Carrito actualizado correctamente")
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