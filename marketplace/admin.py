from django.contrib import admin
from django.utils.html import format_html
from .models import Product, Order, OrderItem, ShippingOption, ShippingZone
from django.urls import path
from django.shortcuts import redirect
from django.utils import timezone
from datetime import timedelta

class ProductAdmin(admin.ModelAdmin):
    list_display = ['image_preview', 'name', 'category_display', 'price', 'stock', 'available', 'created_at']
    list_editable = ['price', 'stock', 'available']
    list_filter = ['category', 'available', 'created_at']
    search_fields = ['name', 'description']
    list_per_page = 20
    
    fieldsets = [
        ('Información Básica', {'fields': ['name', 'description', 'category', 'price']}),
        ('Inventario e Imagen', {'fields': ['stock', 'available', 'image']}),
    ]
    
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']
    
    def image_preview(self, obj):
        if obj.image and obj.image.url:
            return format_html('<img src="{}" style="width: 50px; height: 50px; object-fit: cover;" />', obj.image.url)
        return "📷 Sin imagen"
    image_preview.short_description = 'Imagen'
    
    def category_display(self, obj):
        return dict(Product.CATEGORY_CHOICES).get(obj.category, obj.category)
    category_display.short_description = 'Categoría'
    
    def get_queryset(self, request):
        return super().get_queryset(request).order_by('-created_at')
    
    def stock_status(self, obj):
        if obj.stock == 0:
            return format_html('<span style="color: red; font-weight: bold;">🔴 AGOTADO</span>')
        elif obj.stock < 10:
            return format_html('<span style="color: orange; font-weight: bold;">🟡 POCO STOCK ({})</span>', obj.stock)
        else:
            return format_html('<span style="color: green;">🟢 EN STOCK ({})</span>', obj.stock)
    stock_status.short_description = 'Estado Stock'

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    readonly_fields = ['product', 'quantity', 'price']
    extra = 0
    can_delete = False

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email', 'total_display', 'status', 'created_at', 'order_actions']
    list_filter = ['status', 'created_at']
    search_fields = ['first_name', 'last_name', 'email', 'mercadopago_id']
    readonly_fields = ['created_at', 'updated_at', 'mercadopago_id']
    inlines = [OrderItemInline]
    
    fieldsets = [
        ('Información del Cliente', {
            'fields': [
                'first_name', 'last_name', 'email', 'phone', 
                'address', 'city'
            ]
        }),
        ('Información de la Orden', {
            'fields': [
                'total', 'status', 'mercadopago_id', 'user'
            ]
        }),
        ('Fechas', {
            'fields': ['created_at', 'updated_at'],
            'classes': ['collapse']
        }),
    ]
    
    def total_display(self, obj):
        return f"${obj.total}"
    total_display.short_description = 'Total'
    
    def order_actions(self, obj):
        return format_html('''
            <div class="order-actions">
                <a href="/admin/marketplace/order/{}/change/" class="button">📝 Editar</a>
            </div>
        ''', obj.id)
    order_actions.short_description = 'Acciones'

@admin.register(ShippingOption)
class ShippingOptionAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'estimated_days', 'is_active']
    list_filter = ['is_active']
    list_editable = ['price', 'estimated_days', 'is_active']

@admin.register(ShippingZone)
class ShippingZoneAdmin(admin.ModelAdmin):
    list_display = ['name', 'postal_code_start', 'postal_code_end', 'shipping_option']
    list_filter = ['shipping_option']

# Registrar modelos
admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
# OrderItem no necesita registro porque se muestra inline en Order