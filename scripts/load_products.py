import os
import sys

# === FIX PARA RENDER ===
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
sys.path.insert(0, project_root)
# === FIN FIX ===

import django
import requests
from django.core.files.base import ContentFile

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'masivo_tech.settings')
django.setup()

from marketplace.models import Product

def get_argentina_products():
    """Productos con precios reales de Argentina - SOLO CATEGORÍAS VÁLIDAS"""
    
    argentina_peripherals = [
        {
            'name': 'Teclado Redragon Kumara K552',
            'description': 'Teclado mecánico gaming retroiluminado, switches Outemu Blue, antighosting.',
            'price': 25999.00,
            'category': 'teclados',
            'image_url': 'https://http2.mlstatic.com/D_NQ_NP_2X_614206-MLA48677918436_122021-F.webp'
        },
        {
            'name': 'Mouse Logitech G203 Lightsync',
            'description': 'Mouse gaming con sensor 8000 DPI, iluminación RGB Lightsync, 6 botones.',
            'price': 18999.00,
            'category': 'mouses', 
            'image_url': 'https://http2.mlstatic.com/D_NQ_NP_2X_836580-MLA43824365525_102020-F.webp'
        },
        {
            'name': 'Auriculares HyperX Cloud Stinger',
            'description': 'Auriculares gaming con sonido stereo, micrófono con cancelación de ruido.',
            'price': 32999.00,
            'category': 'auriculares',
            'image_url': 'https://http2.mlstatic.com/D_NQ_NP_2X_822507-MLA31002772475_062019-F.webp'
        },
        {
            'name': 'Monitor Samsung 24" F390',
            'description': 'Monitor LED 24" Full HD, panel VA, 60Hz, diseño sin bordes.',
            'price': 89999.00,
            'category': 'monitores',
            'image_url': 'https://http2.mlstatic.com/D_NQ_NP_2X_679224-MLA48678692861_122021-F.webp'
        }
    ]
    
    return argentina_peripherals

def create_argentina_products():
    """Crea productos con precios reales de Argentina"""
    
    products_data = get_argentina_products()
    created_count = 0
    skipped_count = 0

    print("🔄 INICIANDO CARGA DE PRODUCTOS")
    for product_info in products_data:
        # Verificar si ya existe (protección contra duplicados)
        if Product.objects.filter(name=product_info['name']).exists():
            print(f"⏭️  Saltando: {product_info['name']} (ya existe)")
            skipped_count += 1
            continue
            
        # Crear producto sin imagen primero
        product = Product(
            name=product_info['name'],
            description=product_info['description'],
            price=product_info['price'],
            category=product_info['category'],
            stock=15,
            available=True
        )
        
        # Descargar y asignar imagen (si el campo existe)
        try:
            # 1. LOG - Solo muestra qué imagen está descargando
            print(f"Descargando imagen para: {product_info['name']}")
            
            # 2. DESCARGAR - Hace una petición HTTP a la URL de la imagen
            response = requests.get(product_info['image_url'], timeout=10)
            
            # 3. VERIFICAR - Revisa si la descarga fue exitosa
            if response.status_code == 200: # 200 = HTTP OK (éxito)
                # 4. CREAR NOMBRE DE ARCHIVO
                file_name = f"{product_info['name'].replace(' ', '_').lower()}.jpg"
                # Ejemplo: "Teclado Redragon Kumara K552" → "teclado_redragon_kumara_k552.jpg"
                
                # 5. CREAR OBJETO ARCHIVO DE DJANGO
                image_file = ContentFile(response.content, name=file_name)
                # ContentFile → Envuelve los bytes de la imagen en un objeto
                # response.content → Los bytes binarios de la imagen descargada
                # name=file_name → El nombre que tendrá el archivo guardado
        
                # 6. ASIGNAR IMAGEN AL PRODUCTO
                product.image.save(file_name, image_file, save=False)
                # product.image → El campo ImageField del modelo Product
                # .save() → Método que guarda la imagen en el storage (Cloudinary/filesystem)
                # save=False → IMPORTANTE: Guarda la imagen PERO NO guarda el producto en BD
        
                print("Imagen descargada exitosamente")
            else:
                print(f"Error HTTP {response.status_code} al descargar imagen")
                # No asignamos imagen por defecto, el campo puede ser obligatorio
        except Exception as e:
            print(f"Error descargando imagen: {str(e)}")
            # Continuamos sin imagen si hay error Captura cualquier error: timeout, conexión, etc.
        
        # Guardar producto
        product.save() # ← Este save() pertenece al MODELO Product
        created_count += 1
        print(f"CREADO: {product_info['name']} - ${product_info['price']}")
    
    print("CARGA DE PRODUCTOS COMPLETADA")
    print(f"PRODUCTOS NUEVOS: {created_count}")
    print(f"PRODUCTOS EXISTENTES: {skipped_count}")
    print(f"TOTAL EN SISTEMA: {Product.objects.count()} productos")
    return created_count, skipped_count

if __name__ == "__main__":
    create_argentina_products()