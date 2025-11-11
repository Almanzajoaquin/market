# === settings.py - Configuración Django Optimizada ===

import os
from pathlib import Path
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# =============================================================================
# CONFIGURACIÓN DE SEGURIDAD
# =============================================================================

SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-clave-temporal-para-desarrollo')

# Seguridad: DEBUG debe ser False en producción
DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'

# Hosts permitidos - importante para seguridad
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

# =============================================================================
# CONFIGURACIÓN DE LA APLICACIÓN
# =============================================================================

INSTALLED_APPS = [
    # Apps de Django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    
    # Apps de terceros
    'crispy_forms',
    'crispy_bootstrap5',
    'corsheaders',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'django_extensions',
    
    # Apps locales
    'marketplace',
    'users',
    'chat',
]

MIDDLEWARE = [
    # Middleware de CORS (primero)
    'corsheaders.middleware.CorsMiddleware',
    
    # Middleware de seguridad
    'django.middleware.security.SecurityMiddleware',
    
    # Middleware de sesión
    'django.contrib.sessions.middleware.SessionMiddleware',
    
    # Middleware común
    'django.middleware.common.CommonMiddleware',
    
    # Middleware CSRF
    'django.middleware.csrf.CsrfViewMiddleware',
    
    # Middleware de autenticación
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    
    # Middleware de mensajes
    'django.contrib.messages.middleware.MessageMiddleware',
    
    # Middleware de clickjacking
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
    # Middleware de Allauth
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'masivo_tech.urls'

WSGI_APPLICATION = 'masivo_tech.wsgi.application'

# =============================================================================
# CONFIGURACIÓN DE BASE DE DATOS
# =============================================================================

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# =============================================================================
# CONFIGURACIÓN DE AUTENTICACIÓN
# =============================================================================

# Backends de autenticación
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

# Modelo de usuario personalizado
AUTH_USER_MODEL = 'users.CustomUser'

# Configuración de Allauth
SITE_ID = 1
ACCOUNT_EMAIL_VERIFICATION = 'optional'
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_LOGOUT_ON_GET = True
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
SOCIALACCOUNT_EMAIL_VERIFICATION = 'none'
SOCIALACCOUNT_EMAIL_REQUIRED = False
SOCIALACCOUNT_QUERY_EMAIL = True
SOCIALACCOUNT_AUTO_SIGNUP = True
SOCIALACCOUNT_STORE_TOKENS = True
ACCOUNT_DEFAULT_HTTP_PROTOCOL = 'http'

# Configuración de registro
ACCOUNT_LOGIN_METHODS = {'email'}
ACCOUNT_SIGNUP_FIELDS = ['email*', 'password1*', 'password2*']

# =============================================================================
# CONFIGURACIÓN DE INTERNATIONALIZATION
# =============================================================================

LANGUAGE_CODE = 'es-ar'
TIME_ZONE = 'America/Argentina/Buenos_Aires'
USE_I18N = True
USE_TZ = True

# =============================================================================
# CONFIGURACIÓN DE ARCHIVOS ESTÁTICOS Y MEDIA
# =============================================================================

# Archivos estáticos
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Archivos media
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# =============================================================================
# CONFIGURACIÓN DE TEMPLATES
# =============================================================================

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'marketplace.context_processors.cart_context',
            ],
        },
    },
]

# =============================================================================
# CONFIGURACIÓN DE CRISPY FORMS
# =============================================================================

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# =============================================================================
# CONFIGURACIÓN DE CARRITO
# =============================================================================

CART_SESSION_ID = 'cart'

# =============================================================================
# CONFIGURACIÓN DE APIs EXTERNAS
# =============================================================================

# Google Gemini AI
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
# agregar si se olvida de que es gemini
# if not GEMINI_API_KEY:
#     print("⚠️  GEMINI_API_KEY no configurada - Usando modo básico")

# Mercado Pago - CONFIGURACIÓN BÁSICA
MERCADOPAGO_ACCESS_TOKEN = 'APP_USR-4107629571667346-110823-c8e8df769239a534002daf4df00bd862-2977404630'
MERCADOPAGO_PUBLIC_KEY = 'APP_USR-cc38148a-7263-4d54-b049-512277e179fa'

# Google OAuth
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        },
        'APP': {
            'client_id': os.getenv('GOOGLE_CLIENT_ID',''), 
            'secret': os.getenv('GOOGLE_SECRET', ''),    
            'key': ''
        }
    }
}
SOCIALACCOUNT_ADAPTER = 'users.adapters.CustomSocialAccountAdapter'
# =============================================================================
# CONFIGURACIÓN DE SEGURIDAD ADICIONAL
# =============================================================================

# Validadores de contraseña
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Configuración de CORS
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

# URL base para callbacks
BASE_URL = 'http://127.0.0.1:8000'

# Configuración del admin dashboard
ADMIN_DASHBOARD = True

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
