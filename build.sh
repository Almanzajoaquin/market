#!/usr/bin/env bash
# Render build script

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Make Migrations..."
python manage.py makemigrations

echo "Running migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Create Admin"
python manage.py create_admin