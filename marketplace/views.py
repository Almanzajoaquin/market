from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib import messages
from .models import Product, Order, OrderItem
from .forms import OrderForm
from .cart import Cart

def index(request):
    products = Product.objects.filter(available=True).order_by('-created_at')[:8]
    categories = Product.CATEGORY_CHOICES
    return render(request, 'marketplace/index.html', {
        'products': products,
        'categories': categories
    })

def product_list(request):
    category = request.GET.get('category', '')
    products = Product.objects.filter(available=True)
    
    if category:
        products = products.filter(category=category)
    
    categories = Product.CATEGORY_CHOICES
    return render(request, 'marketplace/product_list.html', {
        'products': products,
        'categories': categories,
        'selected_category': category
    })

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id, available=True)
    return render(request, 'marketplace/product_detail.html', {'product': product})

def cart_detail(request):
    cart = Cart(request)
    return render(request, 'marketplace/cart.html', {'cart': cart})

def add_to_cart(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))
    
    cart.add(product, quantity)
    messages.success(request, f'"{product.name}" agregado al carrito.')
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'success': True, 'cart_total': len(cart)})
    
    return redirect('cart_detail')

def remove_from_cart(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    messages.success(request, f'"{product.name}" removido del carrito.')
    return redirect('cart_detail')

def update_cart(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))
    
    if quantity > 0:
        cart.add(product, quantity, update_quantity=True)
    else:
        cart.remove(product)
    
    return redirect('cart_detail')

def checkout(request):
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
            
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    quantity=item['quantity'],
                    price=item['price']
                )
            
            cart.clear()
            return render(request, 'marketplace/order_success.html', {'order': order})
    else:
        form = OrderForm()
    
    return render(request, 'marketplace/checkout.html', {
        'form': form,
        'cart': cart
    })