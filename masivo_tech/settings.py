import os
from pathlib import Path
#---------------------------------------------
# Cargar variables d entorno

from dotenv import load_dotenv
load_dotenv()
#---------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

#------------------------------------------------------------------------------------
# para funcionalidad de registro con google
SECRET_KEY = os.getenv('SECRET_KEY','django-insecure-clave-temporal-para-desarrollo')
DEBUG = os.getenv('DEBUF','True').lower()=='true'
ALLOWED_HOSTS = os.getenv('ALLOWED_HOST','localhost,127.0.0.1').split(',')
#------------------------------------------------------------------------------------

#------------------------------------------------------------------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    'marketplace',
    'users',
    
    'crispy_forms',
    'crispy_bootstrap5',
    'chat',
    'corsheaders',
    
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    # ver urls
    'django_extensions',
        
]
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # tomi middle    
    'allauth.account.middleware.AccountMiddleware',
]

# tomi auth
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]
AUTH_USER_MODEL = 'users.CustomUser'
#tomi Allauth Configuration
SITE_ID = 1
ACCOUNT_EMAIL_VERIFICATION = 'optional'
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_LOGOUT_ON_GET = True
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
# Allauth Configuration ACTUALIZADA:
ACCOUNT_LOGIN_METHODS = {'email'}
ACCOUNT_SIGNUP_FIELDS = ['email*', 'password1*', 'password2*']

# Crispy Forms
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# Email Configuration (para recuperación de contraseña)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'  # Para desarrollo
# Para producción:
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# Google OAuth (usa variables de entorno en producción)
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
            'secret': os.getenv('GOOGLE_CLIENT_SECRET', ''),    
            'key': ''
        }
    }
}


#----------------------------------------------------------------------------

ROOT_URLCONF = 'masivo_tech.urls'

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

WSGI_APPLICATION = 'masivo_tech.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

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
LANGUAGE_CODE = 'es-ar'
TIME_ZONE = 'America/Argentina/Buenos_Aires'
USE_I18N = True
USE_TZ = True

# ARCHIVOS ESTÁTICOS - CONFIGURACIÓN CORRECTA
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Crispy Forms
CRISPY_ALLOWED_TEMPLATE_PACKS = 'bootstrap5'
CRISPY_TEMPLATE_PACK = 'bootstrap5'

# Carrito
CART_SESSION_ID = 'cart'

# Agregar al final de settings.py
ADMIN_DASHBOARD = True

# Configuración de templates del admin
if ADMIN_DASHBOARD:
    import os
    TEMPLATES[0]['DIRS'] = [os.path.join(BASE_DIR, 'templates')]

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

#q onda jaja aca va lo de mercado pago 

CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

BASE_URL = 'http://127.0.0.1:8000'