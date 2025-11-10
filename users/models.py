from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/',
                                        blank=True,
                                        null=True,
                                        default='profile_pics/default_avatar.png')
    date_of_birth = models.DateField(blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Para login con email en lugar de username
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    def __str__(self):
        return self.email
    def get_display_name(self):
        """Retorna el nombre para mostrar: nombre completo o email"""
        if self.first_name:
            return f"{self.first_name} {self.last_name}".strip()
        return self.email.split('@')[0]  # Parte antes del @

# En settings.py agregar:
# AUTH_USER_MODEL = 'users.CustomUser'