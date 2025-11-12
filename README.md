#  MasivoTech - Tienda de Computadoras

<div align="center">

![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![MercadoPago](https://img.shields.io/badge/MercadoPago-00B1EA?style=for-the-badge)

**Tienda especializada en productos de computación con IA integrada**

[Características](#características) • [Instalación](#instalación) • [Tecnologías](#tecnologías)

</div>

## Descripción

MasivoTech es una aplicación web desarrollada en Django que funciona como una tienda online especializada en productos de computación. Los usuarios pueden explorar, buscar y comprar productos tecnológicos con un sistema de pago integrado con Mercado Pago.

## Características

<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 15px; margin: 20px 0;">

<div style="background: #f8f9fa; padding: 15px; border-radius: 8px; border-left: 4px solid #3498db;">
<h4> Carrito de Compras</h4>
<p>Sistema completo de carrito de compras con integración de Mercado Pago para procesar pagos de forma segura.</p>
</div>

<div style="background: #f8f9fa; padding: 15px; border-radius: 8px; border-left: 4px solid #3498db;">
<h4> Chat con IA</h4>
<p>Asistente virtual integrado con Gemini AI para ayudar a los usuarios con consultas sobre productos.</p>
</div>

<div style="background: #f8f9fa; padding: 15px; border-radius: 8px; border-left: 4px solid #3498db;">
<h4> Búsqueda Avanzada</h4>
<p>Sistema de búsqueda y filtrado para encontrar productos específicos fácilmente.</p>
</div>

<div style="background: #f8f9fa; padding: 15px; border-radius: 8px; border-left: 4px solid #3498db;">
<h4> Autenticación</h4>
<p>Sistema de registro y login con opción de autenticación mediante Google o correo electrónico tradicional.</p>
</div>

</div>

## Instalación

Sigue estos pasos para configurar el proyecto en tu entorno local:

### Prerrequisitos
- Python 3.8 o superior
- Pip (gestor de paquetes de Python)
- Virtualenv (recomendado)

### 1. Clonar el repositorio
```
-------------------------------------------------bash
git clone https://github.com/tuusuario/market.git
cd market

###

2. Configurar entorno virtual
      python -m venv venv
    # En Windows:
      venv\Scripts\activate

    # En macOS/Linux:
      source venv/bin/activate

3. Instalar dependencias
      pip install -r requirements.txt
4. Configurar variables de entorno
      Crea un archivo .env en la raíz del proyecto:

SECRET_KEY=tu_clave_secreta_aqui
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

GOOGLE_CLIENT_ID=
GOOGLE_SECRET=
GEMINI_API_KEY=tu_api_key_de_gemini

MERCADOPAGO_PUBLIC_KEY= =tu_public_key
MERCADOPAGO_ACCESS_TOKEN=tu_access_token

5. Configurar la base de datos
    python manage.py migrate
6. Crear superusuario
    python manage.py createsuperuser
7. Ejecutar el servidor
    python manage.py runserver
-------------------------------------------------bash
```
La aplicación estará disponible en: http://127.0.0.1:8000

 Tecnologías
<div align="center">
Backend: Django · Python · SQLite
Frontend: HTML · CSS · JavaScript · Bootstrap
APIs: Mercado Pago · Gemini AI · OAuth 2.0
Herramientas: Git · Virtualenv · Pip
</div>

##  Estructura del Proyecto

**MARKET/**
- `marketplace/` - Aplicación principal
- `users/` - Gestión de usuarios  
- `templates/` - Plantillas HTML
- `static/` - Archivos estáticos
- `venv/` - Entorno virtual
- `manage.py` - Utilidad de Django
- `requirements.txt` - Dependencias
- `.env` - Variables de entorno

Funcionalidades Adicionales
Scraping de productos de Mercado Libre

Sistema de ofertas y promociones

Sección de contacto con representantes

Envío de correos electrónicos de confirmación

Gestión de perfil de usuario

Historial de pedidos

<div align="center">
MASIVOTECH - Proyecto Django © 2025
</div>
