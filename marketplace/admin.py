from django.contrib import admin
from django.utils.html import format_html
from .models import Product, Order, OrderItem

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