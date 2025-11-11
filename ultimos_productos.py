import os
import django
import requests
from django.core.files.base import ContentFile

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'masivo_tech.settings')
django.setup()

from marketplace.models import Product

def get_gaming_products():
    """30 productos gaming reales - teclados, monitores, auriculares y mouse"""
    
    gaming_products = [
        # TECLADOS (8 productos)
        {
            'name': 'Logitech G Pro X Mechanical',
            'description': 'Teclado mecánico gaming, switches GX Blue, RGB LIGHTSYNC, diseño tenkeyless.',
            'price': 38999,
            'category': 'teclados',
            'image_url': 'https://resource.logitechg.com/w_386,c_limit,f_auto,q_auto,dpr_2.0/d_transparent.gif/content/dam/gaming/en/products/pro-x-keyboard/g-pro-x-keyboard-gallery-1.png'
        },
        {
            'name': 'Razer BlackWidow V3 Pro',
            'description': 'Teclado mecánico wireless, switches Green Razer, Chroma RGB, durabilidad 80M clicks.',
            'price': 65999,
            'category': 'teclados',
            'image_url': 'https://assets2.razerzone.com/images/blackwidow-v3/carousel/razer-blackwidow-v3-1.png'
        },
        {
            'name': 'Corsair K95 RGB Platinum',
            'description': 'Teclado gaming mecánico con switches Cherry MX Speed, 8MB almacenamiento, RGB.',
            'price': 54999,
            'category': 'teclados',
            'image_url': 'https://www.corsair.com/medias/sys_master/images/images/h5d/h2d/9117867506718/-CH-9127114-NA-Gallery-K95-RGB-Platinum-01.png'
        },
        {
            'name': 'SteelSeries Apex Pro',
            'description': 'Teclado mecánico gaming con switches ajustables OmniPoint, OLED display inteligente.',
            'price': 78999,
            'category': 'teclados',
            'image_url': 'https://steelseries.com/cloudfront/images/products/apex-pro-tkl-2023/main.png'
        },
        {
            'name': 'HyperX Alloy Origins Core',
            'description': 'Teclado mecánico 60% gaming, switches HyperX Red, aluminum body, RGB dinámico.',
            'price': 32999,
            'category': 'teclados',
            'image_url': 'https://www.hyperxgaming.com/content/dam/hyperx/category/keyboards/alloy-origins-core-keyboard/ugc/alloy-origins-core-keyboard-1.png'
        },
        {
            'name': 'Redragon Kumara K552',
            'description': 'Teclado mecánico gaming retroiluminado, switches Outemu Blue, antighosting.',
            'price': 25999,
            'category': 'teclados',
            'image_url': 'https://http2.mlstatic.com/D_NQ_NP_2X_614206-MLA48677918436_122021-F.webp'
        },
        {
            'name': 'ASUS ROG Strix Scope',
            'description': 'Teclado mecánico gaming switches Cherry MX Red, diseño ergonómico, RGB Aura Sync.',
            'price': 44999,
            'category': 'teclados',
            'image_url': 'https://dlcdnwebimgs.asus.com/gain/8C4C3D8F-1D1E-4B9A-9F7C-0F9C5A5D5A36/w717/h525'
        },
        {
            'name': 'Razer Huntsman Mini',
            'description': 'Teclado 60% gaming, switches optical Red, actuación rápida, Chroma RGB.',
            'price': 41999,
            'category': 'teclados',
            'image_url': 'https://assets2.razerzone.com/images/huntsman-mini/carousel/razer-huntsman-mini-1.png'
        },

        # MOUSES (8 productos)
        {
            'name': 'Logitech G Pro X Superlight',
            'description': 'Mouse gaming inalámbrico ultraligero 63g, sensor HERO 25K, 70h batería.',
            'price': 45999,
            'category': 'mouses',
            'image_url': 'https://resource.logitechg.com/w_386,c_limit,f_auto,q_auto,dpr_2.0/d_transparent.gif/content/dam/gaming/en/products/pro-x-superlight/pro-x-superlight-gallery-1.png'
        },
        {
            'name': 'Razer Viper Ultimate',
            'description': 'Mouse gaming inalámbrico con dock de carga, sensor Focus+ 20K DPI, 74h batería.',
            'price': 51999,
            'category': 'mouses',
            'image_url': 'https://assets2.razerzone.com/images/viper-ultimate/carousel/razer-viper-ultimate-1.png'
        },
        {
            'name': 'SteelSeries Aerox 3 Wireless',
            'description': 'Mouse gaming honeycomb 66g, sensor TrueMove Air, 200h batería, IP54 waterproof.',
            'price': 42999,
            'category': 'mouses',
            'image_url': 'https://steelseries.com/cloudfront/images/products/aerox-3-wireless/main.png'
        },
        {
            'name': 'Corsair Dark Core RGB Pro',
            'description': 'Mouse gaming inalámbrico, 18.000 DPI, 50h batería, iluminación RGB SLIPSTREAM.',
            'price': 42999,
            'category': 'mouses',
            'image_url': 'https://www.corsair.com/medias/sys_master/images/images/hb3/h0f/9117871325214/-CH-9318111-NA-Gallery-Dark-Core-RGB-Pro-SE-01.png'
        },
        {
            'name': 'Logitech G203 Lightsync',
            'description': 'Mouse gaming con sensor 8000 DPI, iluminación RGB Lightsync, 6 botones programables.',
            'price': 18999,
            'category': 'mouses',
            'image_url': 'https://http2.mlstatic.com/D_NQ_NP_2X_836580-MLA43824365525_102020-F.webp'
        },
        {
            'name': 'Razer DeathAdder V2',
            'description': 'Mouse gaming ergonómico, sensor Focus+ 20K DPI, switches optical 70M clicks.',
            'price': 34999,
            'category': 'mouses',
            'image_url': 'https://assets2.razerzone.com/images/deathadder-v2/carousel/razer-deathadder-v2-1.png'
        },
        {
            'name': 'HyperX Pulsefire Haste',
            'description': 'Mouse gaming honeycomb 59g, cable paracord, PTFE feet, sensor Pixart 3335.',
            'price': 27999,
            'category': 'mouses',
            'image_url': 'https://www.hyperxgaming.com/content/dam/hyperx/category/gaming-mice/pulsefire-haste-gaming-mouse/ugc/pulsefire-haste-gaming-mouse-1.png'
        },
        {
            'name': 'Glorious Model O Wireless',
            'description': 'Mouse gaming honeycomb 69g, sensor BAMF, 71h batería, RGB espectacular.',
            'price': 34999,
            'category': 'mouses',
            'image_url': 'https://cdn.shopify.com/s/files/1/0274/3905/6810/products/model-o-wireless-matte-white_1.png'
        },

        # AURICULARES (7 productos)
        {
            'name': 'SteelSeries Arctis Pro',
            'description': 'Auriculares gaming High Fidelity con sonido surround DTS Headphone:X v2.0, dual drivers.',
            'price': 67999,
            'category': 'auriculares',
            'image_url': 'https://steelseries.com/cloudfront/images/products/arctis-pro-wireless/main.png'
        },
        {
            'name': 'HyperX Cloud Flight',
            'description': 'Auriculares inalámbricos gaming, 30h de batería, micrófono desmontable, cómodos.',
            'price': 42999,
            'category': 'auriculares',
            'image_url': 'https://www.hyperxgaming.com/content/dam/hyperx/category/headsets/cloud-flight-wireless-gaming-headset/ugc/cloud-flight-wireless-gaming-headset-1.png'
        },
        {
            'name': 'Logitech G Pro X Wireless',
            'description': 'Auriculares gaming inalámbricos, sonido surround, batería 20h, micrófono Blue VOICE.',
            'price': 59999,
            'category': 'auriculares',
            'image_url': 'https://resource.logitechg.com/w_386,c_limit,f_auto,q_auto,dpr_2.0/d_transparent.gif/content/dam/gaming/en/products/pro-x-wireless-gaming-headset/gallery/pro-x-wireless-gaming-headset-gallery-1.png'
        },
        {
            'name': 'Razer BlackShark V2 Pro',
            'description': 'Auriculares wireless, micrófono HyperClear, THX Spatial Audio, 24h batería.',
            'price': 52999,
            'category': 'auriculares',
            'image_url': 'https://assets2.razerzone.com/images/blackshark-v2-pro/carousel/razer-blackshark-v2-pro-1.png'
        },
        {
            'name': 'HyperX Cloud Stinger',
            'description': 'Auriculares gaming con sonido stereo, micrófono con cancelación de ruido, lightweight.',
            'price': 32999,
            'category': 'auriculares',
            'image_url': 'https://http2.mlstatic.com/D_NQ_NP_2X_822507-MLA31002772475_062019-F.webp'
        },
        {
            'name': 'Corsair Virtuoso RGB Wireless',
            'description': 'Auriculares premium, sonido Hi-Res, micrófono broadcast, 20h batería.',
            'price': 67999,
            'category': 'auriculares',
            'image_url': 'https://www.corsair.com/medias/sys_master/images/images/hd5/h4b/9117871341598/-CH-9127414-NA-Gallery-K100-RGB-01.png'
        },
        {
            'name': 'ASUS ROG Delta S',
            'description': 'Auriculares gaming, drivers ESS Quad-DAC, USB-C, AI Noise-Canceling mic.',
            'price': 48999,
            'category': 'auriculares',
            'image_url': 'https://dlcdnwebimgs.asus.com/gain/4EFC3D0B-2216-4FDF-9A7A-1B3F8C5D5A36/w717/h525'
        },

        # MONITORES (7 productos)
        {
            'name': 'Samsung Odyssey G7',
            'description': 'Monitor gaming curved 32" 240Hz QLED, 1ms, resolución 2560x1440, HDR600.',
            'price': 189999,
            'category': 'monitores',
            'image_url': 'https://images.samsung.com/is/image/samsung/p6pim/ar/lc32g75tbslxar/gallery/ar-g7-g75t-lc32g75tbslxar-53223-532203533?$650_519_PNG$'
        },
        {
            'name': 'ASUS ROG Swift PG279QM',
            'description': 'Monitor gaming 27" 240Hz IPS, resolución 2560x1440, G-SYNC, HDR400.',
            'price': 459999,
            'category': 'monitores',
            'image_url': 'https://dlcdnwebimgs.asus.com/gain/4EFC3D0B-2216-4FDF-9A7A-1B3F8C5D5A36/w717/h525'
        },
        {
            'name': 'LG UltraGear 27GN800-B',
            'description': 'Monitor 27" 144Hz IPS, 1ms, HDR10, FreeSync, 95% DCI-P3.',
            'price': 189999,
            'category': 'monitores',
            'image_url': 'https://www.lg.com/us/images/monitors/md07518621/gallery/27GN800-B-DZ-01.jpg'
        },
        {
            'name': 'AOC 24G2SE',
            'description': 'Monitor gaming 24" 144Hz VA, 1ms, FreeSync, diseño sin bordes.',
            'price': 89999,
            'category': 'monitores',
            'image_url': 'https://www.aoc.com/wp-content/uploads/2020/09/24G2SE_front.png'
        },
        {
            'name': 'MSI Optix MAG274QRF',
            'description': 'Monitor 27" 165Hz IPS, 2K, 1ms, RGB lighting, adjustable stand.',
            'price': 219999,
            'category': 'monitores',
            'image_url': 'https://www.msi.com/newsroom/wp-content/uploads/2020/12/MAG274QRF-1.png'
        },
        {
            'name': 'Dell Alienware AW2521H',
            'description': 'Monitor gaming 25" 360Hz IPS, 1ms, G-SYNC, diseño Alienware.',
            'price': 389999,
            'category': 'monitores',
            'image_url': 'https://i.dell.com/is/image/DellContent/content/dam/ss2/products/electronics-and-accessories/dell/alienware/aw2521h-monitor/media-gallery/monitor-alienware-25-aw2521h-gallery-1.psd'
        },
        {
            'name': 'BenQ EX2780Q',
            'description': 'Monitor 27" 144Hz IPS, 2K, HDRi, altavoces 2.1, USB-C.',
            'price': 169999,
            'category': 'monitores',
            'image_url': 'https://www.benq.com/content/dam/b2c/es-es/monitor/home-entertainment/ex2780q/gallery/EX2780Q-Gallery-01-1200x1200.png'
        }
    ]
    
    return gaming_products

def create_gaming_products():
    """Crea 30 productos gaming reales en la base de datos"""
    
    products_data = get_gaming_products()
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
            
            # Descargar imagen del producto real
            try:
                response = requests.get(product_info['image_url'], timeout=15)
                if response.status_code == 200:
                    file_name = f"{product_info['name'].replace(' ', '_').lower()}.jpg"
                    image_file = ContentFile(response.content, name=file_name)
                    product.image.save(file_name, image_file)
                    print(f"✅ Imagen descargada: {product_info['name']}")
                else:
                    print(f"⚠️ Error HTTP {response.status_code} en: {product_info['name']}")
                    product.image = 'products/default_product.jpg'
            except Exception as e:
                print(f"⚠️ Error descargando imagen {product_info['name']}: {str(e)}")
                product.image = 'products/default_product.jpg'
            
            product.save()
            created_count += 1
            print(f"🎮 CREADO: {product_info['name']} - ${product_info['price']}")
        else:
            print(f"⏭️ Saltado: {product_info['name']} (ya existe)")
    
    print(f"\n🎉 CREADOS {created_count} PRODUCTOS GAMING REALES!")
    print("📍 Distribución:")
    print(f"   🎹 Teclados: 8 productos")
    print(f"   🖱️  Mouses: 8 productos") 
    print(f"   🎧 Auriculares: 7 productos")
    print(f"   🖥️  Monitores: 7 productos")
    print(f"   💰 Total: 30 productos")
    
    return created_count

if __name__ == "__main__":
    create_gaming_products()