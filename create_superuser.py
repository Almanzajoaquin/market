from django.contrib.auth import get_user_model

User = get_user_model()

if not User.objects.filter(email="admin@admin.com").exists():
    User.objects.create_superuser(
        email="admin@admin.com",
        password="admin1234"
    )
    print("Superusuario creado.")
else:
    print("El superusuario ya existe.")
