# === models.py - Modelos Django Optimizados ===

from django.db import models
from django.core.validators import MinValueValidator
from django.conf import settings
from django.contrib.auth import get_user_model

# Obtener el modelo de usuario de forma compatible
User = get_user_model()


class Product(models.Model):
    """
    Modelo para productos de la tienda gaming
    Gestiona teclados, mouses, auriculares y monitores
    """
    
    # Opciones de categoría
    CATEGORY_CHOICES = [
        ('teclados', 'Teclados Mecánicos'),
        ('mouses', 'Mouses Gaming'),
        ('auriculares', 'Auriculares'),
        ('monitores', 'Monitores Gaming'),
    ]
    
    # Campos principales
    name = models.CharField(
        max_length=200,
        verbose_name="Nombre del Producto",
        help_text="Nombre descriptivo del producto"
    )
    
    description = models.TextField(
        verbose_name="Descripción",
        help_text="Descripción detallada del producto"
    )
    
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name="Precio",
        help_text="Precio en pesos argentinos"
    )
    
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        verbose_name="Categoría",
        help_text="Categoría del producto"
    )
    
    image = models.ImageField(
        upload_to='products/',
        verbose_name="Imagen",
        help_text="Imagen principal del producto",
        blank=True,
        null=True
    )
    
    # Gestión de inventario
    stock = models.PositiveIntegerField(
        default=0,
        verbose_name="Stock Disponible",
        help_text="Cantidad disponible en inventario"
    )
    
    available = models.BooleanField(
        default=True,
        verbose_name="Disponible",
        help_text="¿El producto está disponible para la venta?"
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['category', 'available']),
            models.Index(fields=['created_at']),
            models.Index(fields=['price']),
        ]
    
    def __str__(self):
        """Representación legible del producto"""
        return f"{self.name} - ${self.price}"
    
    def get_price_in_pesos(self):
        """Formatea el precio en formato pesos argentinos"""
        return f"${self.price:,.2f}".replace(',', '.')
    
    def is_in_stock(self):
        """Verifica si el producto está en stock"""
        return self.stock > 0 and self.available
    
    def get_stock_status(self):
        """Devuelve el estado del stock como texto"""
        if self.stock == 0:
            return "agotado"
        elif self.stock < 5:
            return "poco_stock"
        else:
            return "en_stock"


class Order(models.Model):
    """
    Modelo para órdenes de compra
    Gestiona todo el proceso de pedidos
    """
    
    # Estados de la orden
    STATUS_CHOICES = [
        ('pending', 'Pendiente'),
        ('paid', 'Pagado'),
        ('processing', 'Procesando'),
        ('shipped', 'Enviado'),
        ('delivered', 'Entregado'),
        ('cancelled', 'Cancelado'),
    ]
    
    # Relación con usuario (opcional para compras como invitado)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Usuario",
        related_name="orders"
    )
    
    # Información del cliente
    first_name = models.CharField(max_length=100, verbose_name="Nombre")
    last_name = models.CharField(max_length=100, verbose_name="Apellido")
    email = models.EmailField(verbose_name="Email")
    address = models.CharField(max_length=255, verbose_name="Dirección")
    city = models.CharField(max_length=100, verbose_name="Ciudad")
    phone = models.CharField(max_length=20, verbose_name="Teléfono")
    
    # Información de la orden
    total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Total",
        help_text="Total de la orden en pesos"
    )
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name="Estado",
        help_text="Estado actual de la orden"
    )
    
    mercadopago_id = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="ID de MercadoPago",
        help_text="ID de la transacción en MercadoPago"
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Orden"
        verbose_name_plural = "Órdenes"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['created_at']),
            models.Index(fields=['email']),
        ]
    
    def __str__(self):
        """Representación legible de la orden"""
        return f"Orden #{self.id} - {self.first_name} {self.last_name}"
    
    def get_full_name(self):
        """Nombre completo del cliente"""
        return f"{self.first_name} {self.last_name}"
    
    def can_be_cancelled(self):
        """Verifica si la orden puede ser cancelada"""
        return self.status in ['pending', 'paid']


class OrderItem(models.Model):
    """
    Modelo para items individuales dentro de una orden
    Relaciona productos con órdenes
    """
    
    order = models.ForeignKey(
        Order,
        related_name='items',
        on_delete=models.CASCADE,
        verbose_name="Orden"
    )
    
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name="Producto"
    )
    
    quantity = models.PositiveIntegerField(
        verbose_name="Cantidad",
        help_text="Cantidad del producto en la orden"
    )
    
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Precio Unitario",
        help_text="Precio en el momento de la compra"
    )
    
    class Meta:
        verbose_name = "Item de Orden"
        verbose_name_plural = "Items de Orden"
        unique_together = ['order', 'product']
    
    def __str__(self):
        """Representación legible del item"""
        return f"{self.quantity} x {self.product.name}"
    
    def get_total_price(self):
        """Calcula el precio total del item"""
        return self.quantity * self.price


class ShippingOption(models.Model):
    """
    Modelo para opciones de envío
    Configura diferentes métodos de envío disponibles
    """
    
    name = models.CharField(
        max_length=100,
        verbose_name="Nombre del Envío",
        help_text="Nombre descriptivo de la opción de envío"
    )
    
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Precio",
        help_text="Costo del envío en pesos"
    )
    
    estimated_days = models.CharField(
        max_length=50,
        verbose_name="Días Estimados",
        help_text="Tiempo estimado de entrega"
    )
    
    description = models.TextField(
        blank=True,
        verbose_name="Descripción",
        help_text="Descripción detallada del envío"
    )
    
    is_active = models.BooleanField(
        default=True,
        verbose_name="Activo",
        help_text="¿Esta opción de envío está disponible?"
    )
    
    class Meta:
        verbose_name = "Opción de Envío"
        verbose_name_plural = "Opciones de Envío"
        ordering = ['price']
    
    def __str__(self):
        """Representación legible de la opción de envío"""
        return f"{self.name} - ${self.price}"


class ShippingZone(models.Model):
    """
    Modelo para zonas de envío
    Define zonas geográficas y sus opciones de envío
    """
    
    name = models.CharField(
        max_length=100,
        verbose_name="Zona",
        help_text="Nombre de la zona geográfica"
    )
    
    postal_code_start = models.CharField(
        max_length=10,
        verbose_name="Código Postal Inicio",
        help_text="Inicio del rango de códigos postales"
    )
    
    postal_code_end = models.CharField(
        max_length=10,
        verbose_name="Código Postal Fin",
        help_text="Fin del rango de códigos postales"
    )
    
    shipping_option = models.ForeignKey(
        ShippingOption,
        on_delete=models.CASCADE,
        verbose_name="Opción de Envío"
    )
    
    class Meta:
        verbose_name = "Zona de Envío"
        verbose_name_plural = "Zonas de Envío"
        ordering = ['name']
    
    def __str__(self):
        """Representación legible de la zona de envío"""
        return f"{self.name} ({self.postal_code_start}-{self.postal_code_end})"