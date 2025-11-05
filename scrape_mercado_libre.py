import os
import django
import requests
from django.core.files.base import ContentFile

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'masivo_tech.settings')
django.setup()

from marketplace.models import Product

def get_argentina_products():
    """Productos con precios reales de Argentina"""
    
    argentina_peripherals = [
        {
            'name': 'Teclado Redragon Kumara K552',
            'description': 'Teclado mecánico gaming retroiluminado, switches Outemu Blue, antighosting.',
            'price': 25999,
            'category': 'teclados',
            'image_url': 'https://http2.mlstatic.com/D_NQ_NP_2X_614206-MLA48677918436_122021-F.webp'
        },
        {
            'name': 'Mouse Logitech G203 Lightsync',
            'description': 'Mouse gaming con sensor 8000 DPI, iluminación RGB Lightsync, 6 botones.',
            'price': 18999,
            'category': 'mouses', 
            'image_url': 'https://http2.mlstatic.com/D_NQ_NP_2X_836580-MLA43824365525_102020-F.webp'
        },
        {
            'name': 'Auriculares HyperX Cloud Stinger',
            'description': 'Auriculares gaming con sonido stereo, micrófono con cancelación de ruido.',
            'price': 32999,
            'category': 'auriculares',
            'image_url': 'https://http2.mlstatic.com/D_NQ_NP_2X_822507-MLA31002772475_062019-F.webp'
        },
        {
            'name': 'Monitor Samsung 24" F390',
            'description': 'Monitor LED 24" Full HD, panel VA, 60Hz, diseño sin bordes.',
            'price': 89999,
            'category': 'monitores',
            'image_url': 'https://http2.mlstatic.com/D_NQ_NP_2X_679224-MLA48678692861_122021-F.webp'
        },
        {
            'name': 'Silla Gamer X-Vision',
            'description': 'Silla gaming ergonómica, soporte lumbar, reclinable, base metálica.',
            'price': 78999,
            'category': 'sillas',
            'image_url': 'https://http2.mlstatic.com/D_NQ_NP_2X_850011-MLA49879623517_052022-F.webp'
        },
        {
            'name': 'Mousepad Redragon Flick',
            'description': 'Mousepad gaming tamaño XXL, base antideslizante, superficie optimizada.',
            'price': 8999,
            'category': 'otros',
            'image_url': 'https://http2.mlstatic.com/D_NQ_NP_2X_750380-MLA48678027336_122021-F.webp'
        }
    ]
    
    return argentina_peripherals

def create_argentina_products():
    """Crea productos con precios reales de Argentina"""
    
    products_data = get_argentina_products()
    created_count = 0
    
    for product_info in products_data:
        if not Product.objects.filter(name=product_info['name']).exists():
            
            product = Product(
                name=product_info['name'],
                description=product_info['description'],
                price=product_info['price'],
                category=product_info['category'],
                stock=15,
                available=True
            )
            
            # Descargar imagen
            try:
                response = requests.get(product_info['image_url'])
                if response.status_code == 200:
                    file_name = f"{product_info['name'].replace(' ', '_').lower()}.jpg"
                    image_file = ContentFile(response.content, name=file_name)
                    product.image.save(file_name, image_file)
            except:
                product.image = 'products/default_product.jpg'
            
            product.save()
            created_count += 1
            print(f"✅ {product_info['name']} - ${product_info['price']}")
    
    print(f"\n🇦🇷 CREADOS {created_count} PRODUCTOS CON PRECIOS ARGENTINOS!")

if __name__ == "__main__":
    create_argentina_products()