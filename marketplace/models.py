from django.db import models
""" al final uso user y se armala compatibilidad con try
#cambio esto
#from django.contrib.auth.models import User
# por esto por ahora
#from django.conf import settings
"""
from django.core.validators import MinValueValidator

# FORMA COMPATIBLE - funciona con User normal Y CustomUser
try:
    # Intenta usar AUTH_USER_MODEL si existe
    from django.conf import settings
    from django.contrib.auth import get_user_model
    User = get_user_model()
except (ImportError, AttributeError):
    # Fallback al User original de Django
    from django.contrib.auth.models import User

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('teclados', 'Teclados'),
        ('mouses', 'Mouses'),
        ('auriculares', 'Auriculares'),
        ('monitores', 'Monitores'),
    ]
    
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    image = models.ImageField(upload_to='products/')
    stock = models.PositiveIntegerField(default=0)
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    def get_price_in_pesos(self):
        return f"${self.price:,.2f}".replace(',', '.')

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pendiente'),
        ('paid', 'Pagado'),
        ('shipped', 'Enviado'),
        ('delivered', 'Entregado'),
        ('cancelled', 'Cancelado'),
    ]
    
    # Información del usuario
    # cambio por ahora
    """ se usa el original """
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    #Por esto
    #user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    """ como estamos usando customUser y User da error. solucion elegir uno de los dos"""
    
    # el resto igual
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    
    # Información de la orden
    total = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    mercadopago_id = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Orden #{self.id} - {self.first_name} {self.last_name}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

# Modelos para envíos (opcionales)
class ShippingOption(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nombre del envío")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio")
    estimated_days = models.CharField(max_length=50, verbose_name="Días estimados")
    description = models.TextField(blank=True, verbose_name="Descripción")
    is_active = models.BooleanField(default=True, verbose_name="Activo")
    
    def __str__(self):
        return f"{self.name} - ${self.price}"

class ShippingZone(models.Model):
    name = models.CharField(max_length=100, verbose_name="Zona")
    postal_code_start = models.CharField(max_length=10, verbose_name="Código postal inicio")
    postal_code_end = models.CharField(max_length=10, verbose_name="Código postal fin")
    shipping_option = models.ForeignKey(ShippingOption, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.name} ({self.postal_code_start}-{self.postal_code_end})"