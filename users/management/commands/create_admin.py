from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = "Crea un superusuario si no existe"

    def handle(self, *args, **kwargs):
        email = "admin@admin.com"
        username = "admin"
        password = "admin1234"

        if not User.objects.filter(email=email).exists():
            self.stdout.write("Creando superusuario...")
            User.objects.create_superuser(
                email=email,
                username=username,  # requerido porque REQUIRED_FIELDS incluye 'username'
                password=password
            )
        else:
            self.stdout.write("El superusuario ya existe.")
