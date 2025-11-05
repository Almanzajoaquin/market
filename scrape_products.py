import os
import django
import requests
import json
from django.core.files.base import ContentFile

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'masivo_tech.settings')
django.setup()

from marketplace.models import Product

def get_products_from_api():
    """Obtiene productos reales de APIs de periféricos"""
    
    # API 1: FakeStore API (productos de ejemplo)
    try:
        response = requests.get('https://fakestoreapi.com/products/category/electronics')
        electronics = response.json()
    except:
        electronics = []
    
    # Datos de periféricos predefinidos (como fallback)
    predefined_peripherals = [
        {
            'name': 'Logitech G Pro X Superlight',
            'description': 'Mouse gaming inalámbrico ultraligero, sensor HERO 25K, 63g de peso.',
            'price': 45999,
            'category': 'mouses',
            'image_url': 'https://resource.logitechg.com/w_386,c_limit,f_auto,q_auto,dpr_2.0/d_transparent.gif/content/dam/gaming/en/products/pro-x-superlight/pro-x-superlight-gallery-1.png'
        },
        {
            'name': 'Razer BlackWidow V3',
            'description': 'Teclado mecánico gaming con switches Green Razer, iluminación Chroma RGB.',
            'price': 38999,
            'category': 'teclados',
            'image_url': 'https://assets2.razerzone.com/images/blackwidow-v3/carousel/razer-blackwidow-v3-1.png'
        },
        {
            'name': 'SteelSeries Arctis Pro',
            'description': 'Auriculares gaming High Fidelity con sonido surround DTS Headphone:X v2.0.',
            'price': 67999,
            'category': 'auriculares',
            'image_url': 'https://steelseries.com/cloudfront/images/products/arctis-pro-wireless/main.png'
        },
        {
            'name': 'Samsung Odyssey G7',
            'description': 'Monitor gaming curved 32" 240Hz QLED, 1ms, resolución 2560x1440.',
            'price': 189999,
            'category': 'monitores',
            'image_url': 'https://images.samsung.com/is/image/samsung/p6pim/ar/lc32g75tbslxar/gallery/ar-g7-g75t-lc32g75tbslxar-53223-532203533?$650_519_PNG$'
        },
        {
            'name': 'HyperX Alloy Origins',
            'description': 'Teclado mecánico gaming con switches HyperX Red, aluminum body, RGB.',
            'price': 32999,
            'category': 'teclados',
            'image_url': 'https://www.hyperxgaming.com/content/dam/hyperx/category/keyboards/alloy-origins-core-keyboard/ugc/alloy-origins-core-keyboard-1.png'
        },
        {
            'name': 'Corsair K95 RGB Platinum',
            'description': 'Teclado gaming mecánico con switches Cherry MX, 8MB de almacenamiento, RGB.',
            'price': 54999,
            'category': 'teclados',
            'image_url': 'https://www.corsair.com/medias/sys_master/images/images/h5d/h2d/9117867506718/-CH-9127114-NA-Gallery-K95-RGB-Platinum-01.png'
        },
        {
            'name': 'Razer Viper Ultimate',
            'description': 'Mouse gaming inalámbrico con dock de carga, sensor Focus+ 20K DPI.',
            'price': 51999,
            'category': 'mouses',
            'image_url': 'https://assets2.razerzone.com/images/viper-ultimate/carousel/razer-viper-ultimate-1.png'
        },
        {
            'name': 'HyperX Cloud Flight',
            'description': 'Auriculares inalámbricos gaming, 30h de batería, micrófono desmontable.',
            'price': 42999,
            'category': 'auriculares',
            'image_url': 'https://www.hyperxgaming.com/content/dam/hyperx/category/headsets/cloud-flight-wireless-gaming-headset/ugc/cloud-flight-wireless-gaming-headset-1.png'
        }
    ]
    
    return predefined_peripherals

def download_product_image(image_url, product_name):
    """Descarga la imagen del producto"""
    try:
        response = requests.get(image_url)
        if response.status_code == 200:
            file_name = f"{product_name.replace(' ', '_').lower()}.jpg"
            return ContentFile(response.content, name=file_name)
    except:
        pass
    return None

def create_real_products():
    """Crea productos reales en la base de datos"""
    
    products_data = get_products_from_api()
    created_count = 0
    
    for product_info in products_data:
        # Verificar si el producto ya existe
        if not Product.objects.filter(name=product_info['name']).exists():
            
            # Crear producto
            product = Product(
                name=product_info['name'],
                description=product_info['description'],
                price=product_info['price'],
                category=product_info['category'],
                stock=20,  # Stock por defecto
                available=True
            )
            
            # Descargar y asignar imagen
            image_file = download_product_image(product_info['image_url'], product_info['name'])
            if image_file:
                product.image.save(f"{product_info['name'].replace(' ', '_')}.jpg", image_file)
            else:
                # Imagen por defecto si no se puede descargar
                product.image = 'products/default_product.jpg'
            
            product.save()
            created_count += 1
            print(f"✅ {product_info['name']} - ${product_info['price']}")
    
    print(f"\n🎉 CREADOS {created_count} PRODUCTOS REALES!")
    print("📍 Puedes verlos en: http://127.0.0.1:8000/productos/")

if __name__ == "__main__":
    create_real_products()