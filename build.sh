#!/usr/bin/env bash

echo "=========================================="
echo "BUILD - MASIVO TECH"
echo "=========================================="

# Limpieza de cache (opcional)
echo "=== CLEANING CACHE ==="
find . -name "*.pyc" -delete
find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true

# Instalar dependencias
echo "Instalando dependencias..."
pip install -r requirements.txt

# Verificar Cloudinary
echo "=== CLOUDINARY CHECK ==="
python -c "
import os
print('CLOUDINARY ACTIVE:', bool(os.getenv('CLOUDINARY_CLOUD_NAME')))
"

# Migraciones de base de datos
echo "Aplicando migraciones..."
python manage.py makemigrations
python manage.py migrate --noinput

# Archivos estáticos
echo "Recolectando archivos estáticos..."
python manage.py collectstatic --noinput

# EJECUTAR SCRIPT DE PRODUCTOS (¡ya tiene protección anti-duplicados!)
echo "Cargando productos..."
python scripts/load_products.py

# CREAR ADMIN (¡ya tiene protección anti-duplicados en el command!)
echo "Creando admin..."
python manage.py create_admin

echo "=========================================="
echo "BUILD COMPLETADO EXITOSAMENTE"
echo "=========================================="