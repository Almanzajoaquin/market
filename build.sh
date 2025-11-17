#!/usr/bin/env bash
echo "Installing dependencies..."
pip install -r requirements.txt

# DEBUG CLOUDINARY
echo "=== CLOUDINARY DEBUG ==="
python -c "
import os
print('CLOUD_NAME:', os.getenv('CLOUDINARY_CLOUD_NAME'))
print('API_KEY:', os.getenv('CLOUDINARY_API_KEY')[:10] + '...' if os.getenv('CLOUDINARY_API_KEY') else 'None')
print('API_SECRET:', os.getenv('CLOUDINARY_API_SECRET')[:10] + '...' if os.getenv('CLOUDINARY_API_SECRET') else 'None')
"

echo "Make Migrations..."
python manage.py makemigrations

echo "Running migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Create Admin"
python manage.py create_admin