from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

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
        ('processing', 'Procesando'),
        ('shipped', 'Enviado'),
        ('delivered', 'Entregado'),
        ('cancelled', 'Cancelado'),
    ]
    
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Orden #{self.id} - {self.first_name} {self.last_name}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.quantity} x {self.product.name}"


# Al final del archivo, puedes agregar esto para crear un producto de ejemplo
def create_sample_products():
    """Crear productos de ejemplo si no existen"""
    if not Product.objects.filter(name="Logitech G203 Lightsync").exists():
        Product.objects.create(
            name="Logitech G203 Lightsync",
            description="""El mouse gaming Logitech G203 Lightsync ofrece colores LIGHTSYNC RGB brillantes, 
            un sensor gaming y un diseño clásico con 6 botones. Experimenta un rendimiento gaming confiable 
            y una gran precisión con hasta 8,000 DPI.\n\n
            • Sensor gaming para seguimiento preciso\n
            • Iluminación LIGHTSYNC RGB personalizable\n  
            • 6 botones programables\n
            • Hasta 8,000 DPI\n
            • Diseño clásico y cómodo""",
            price=18999,
            category="mouses",
            stock=25,
            available=True,
            image="products/g203.jpg"  # Necesitarás subir esta imagen
        )