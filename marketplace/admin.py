from django.contrib import admin
from django.utils.html import format_html
from .models import Product, Order, OrderItem
from django.urls import path
from django.shortcuts import redirect
from .admin_dashboard import admin_dashboard
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

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    readonly_fields = ['product', 'quantity', 'price']
    extra = 0
    can_delete = False

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email', 'total_amount', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['first_name', 'last_name', 'email']
    readonly_fields = ['created_at', 'total_amount']
    inlines = [OrderItemInline]

admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)

class MasivoTechAdminSite(admin.AdminSite):
    site_header = "🎮 MasivoTech Admin"
    site_title = "MasivoTech Administration"
    index_title = "Dashboard Principal"
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('dashboard/', self.admin_view(admin_dashboard), name='admin_dashboard'),
        ]
        return custom_urls + urls
    
    def index(self, request, extra_context=None):
        # Redirigir al dashboard personalizado por defecto
        return redirect('admin:admin_dashboard')

# Reemplazar el admin site por defecto
admin_site = MasivoTechAdminSite()

# Re-registrar los modelos con el admin site personalizado
admin_site.register(Product, ProductAdmin)
admin_site.register(Order, OrderAdmin)

# Reemplazar el admin por defecto
admin.site = admin_site
site = admin.site

class ProductAdmin(admin.ModelAdmin):
    # ... código existente ...
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Ordenar por stock bajo primero
        return qs.extra(select={
            'stock_status': '''
                CASE 
                    WHEN stock = 0 THEN 2
                    WHEN stock < 10 THEN 1  
                    ELSE 0
                END
            '''
        }).order_by('stock_status', '-created_at')
    
    def stock_status(self, obj):
        if obj.stock == 0:
            return format_html('<span style="color: red; font-weight: bold;">🔴 AGOTADO</span>')
        elif obj.stock < 10:
            return format_html('<span style="color: orange; font-weight: bold;">🟡 POCO STOCK ({})</span>', obj.stock)
        else:
            return format_html('<span style="color: green;">🟢 EN STOCK ({})</span>', obj.stock)
    stock_status.short_description = 'Estado Stock'

class OrderAdmin(admin.ModelAdmin):
    # ... código existente ...
    
    def order_actions(self, obj):
        return format_html('''
            <div class="order-actions">
                <a href="/admin/marketplace/order/{}/change/" class="btn btn-sm btn-info">📝 Editar</a>
                <a href="/admin/marketplace/order/{}/delete/" class="btn btn-sm btn-danger">🗑️ Eliminar</a>
            </div>
        ''', obj.id, obj.id)
    order_actions.short_description = 'Acciones'