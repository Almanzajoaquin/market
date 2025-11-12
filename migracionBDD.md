# ----------------------------------------Migrar de SQLite a PostgreSQL
# 1. Crear PostgreSQL en Render
En Render:

"New" → "PostgreSQL"
Name: tu-app-db
Database: tu_app_db
User: automático
Plan: Free

# 2. Añadir a requirements.txt
    psycopg2-binary==2.9.7
    dj-database-url==2.0.0
    python-dotenv==1.0.0

# Configurar tu Django para PostgreSQL
settings.py - MODIFICAR:

python
import os
import dj_database_url
from pathlib import Path

if 'DATABASE_URL' in os.environ:
    # Producción - PostgreSQL de Render
    DATABASES = {
        'default': dj_database_url.config(
            default=os.environ.get('DATABASE_URL'),
            conn_max_age=600,
            ssl_require=True
        )
    }
else:
    # Desarrollo - SQLite
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# 3. Migrar tus datos !!!!!!!!!!!!!!!!!!!!(OPCIONAL)
Si quieres llevar tus datos de SQLite a PostgreSQL:


# A). Exportar datos de SQLite       
    python manage.py dumpdata > datos.json

# B). Configurar PostgreSQL localmente para prueba
    Instalar PostgreSQL local o usar Render directo

# C). En Render, cambiar settings para usar PostgreSQL

# D). Aplicar migraciones
    python manage.py migrate

# E). Importar datos (en producción)
    python manage.py loaddata datos.json


📁 Manejo de archivos estáticos y media
Archivos estáticos (CSS, JS, imágenes de la app)

- Se sirven con WhiteNoise (gratis)
- Se suben en build time

📁 Archivos media (uploads de usuarios)
NO se guardan en el filesystem (se pierden en cada deploy)

Soluciones:
Opción 1: AWS S3 (recomendado)
{
# requirements.txt
    django-storages==1.13.2
    boto3==1.28.62
# settings.py
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
}

Opción 2: Cloudinary (más fácil)
{
# requirements.txt
    django-cloudinary-storage==0.3.0

# settings.py 
    INSTALLED_APPS = ['cloudinary_storage', 'django.contrib.staticfiles', 'cloudinary']
    DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
}

# Variables de entorno en Render
En tu Web Service → Environment Variables:
{
    DEBUG=False
    SECRET_KEY=tu-clave-super-secreta
    DATABASE_URL=postgresql://user:pass@host:port/db  # AUTOMÁTICO de Render
    ALLOWED_HOSTS=tu-app.onrender.com

# Si usas AWS S3 o Cloudinary:
    AWS_ACCESS_KEY_ID=xxx
    AWS_SECRET_ACCESS_KEY=xxx
    AWS_STORAGE_BUCKET_NAME=xxx
}