#!/usr/bin/env bash
echo "=== CLEANING CACHE ==="
find . -name "*.pyc" -delete
find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true

echo "Installing dependencies..."
pip install -r requirements.txt

echo "=== CLOUDINARY FORCE RESET ==="
python -c "
import os
print('CLOUDINARY ACTIVE:', bool(os.getenv('CLOUDINARY_CLOUD_NAME')))
"

echo "Make Migrations..."
python manage.py makemigrations

echo "Running migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Create Admin"
python manage.py create_admin