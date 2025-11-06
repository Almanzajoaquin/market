from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'address', 'city', 'phone']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tu nombre'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tu apellido'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email@ejemplo.com'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Dirección completa'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ciudad'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Teléfono'}),
        }

class ContactForm(forms.Form):
    nombre = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Tu nombre completo'
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control', 'placeholder': 'tu@email.com'
    }))
    asunto = forms.CharField(max_length=200, required=False, widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Asunto del mensaje'
    }))
    mensaje = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control', 'placeholder': 'Tu mensaje...', 'rows': 5
    }))