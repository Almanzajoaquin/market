from django.contrib import admin
from django.urls import path
from django.shortcuts import render
from django.db.models import Sum, Count, Avg
from django.utils import timezone
from datetime import timedelta
import json
from .models import Order, OrderItem, Product

def admin_dashboard(request):
    """Dashboard personalizado para el admin"""
    
    # Estadísticas principales
    total_orders = Order.objects.count()
    total_revenue = Order.objects.aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    total_products = Product.objects.count()
    low_stock_products = Product.objects.filter(stock__lt=10, stock__gt=0).count()
    out_of_stock_products = Product.objects.filter(stock=0).count()
    
    # Ventas últimos 30 días
    thirty_days_ago = timezone.now() - timedelta(days=30)
    recent_orders = Order.objects.filter(created_at__gte=thirty_days_ago)
    recent_revenue = recent_orders.aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    
    # Órdenes por estado
    orders_by_status = Order.objects.values('status').annotate(
        count=Count('id'),
        revenue=Sum('total_amount')
    )
    
    # Productos más vendidos
    top_products = OrderItem.objects.values(
        'product__name', 
        'product__category'
    ).annotate(
        total_sold=Sum('quantity'),
        revenue=Sum('price')
    ).order_by('-total_sold')[:10]
    
    # Ventas por día (últimos 7 días)
    sales_data = []
    for i in range(7):
        day = timezone.now() - timedelta(days=i)
        day_start = day.replace(hour=0, minute=0, second=0, microsecond=0)
        day_end = day.replace(hour=23, minute=59, second=59, microsecond=999999)
        
        day_sales = Order.objects.filter(
            created_at__range=(day_start, day_end)
        ).aggregate(
            total=Sum('total_amount'),
            count=Count('id')
        )
        
        sales_data.append({
            'date': day.strftime('%Y-%m-%d'),
            'day_name': day.strftime('%a'),
            'total': day_sales['total'] or 0,
            'count': day_sales['count'] or 0
        })
    
    sales_data.reverse()
    
    context = {
        'title': 'Dashboard MasivoTech',
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'total_products': total_products,
        'low_stock_products': low_stock_products,
        'out_of_stock_products': out_of_stock_products,
        'recent_revenue': recent_revenue,
        'orders_by_status': list(orders_by_status),
        'top_products': list(top_products),
        'sales_data': sales_data,
        'sales_json': json.dumps(sales_data),
    }
    
    return render(request, 'admin/marketplace/dashboard.html', context)