from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        #fields = ('email', 'username', 'phone_number')
        fields = ('email', 'username', 'first_name', 'last_name', 'phone_number')


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        #fields = ('email', 'username', 'phone_number', 'profile_picture', 'date_of_birth', 'bio')
        fields = ('email', 'username', 'first_name', 'last_name', 'phone_number', 'profile_picture')

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        #fields = ['username', 'email', 'phone_number']
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'profile_picture']
        widgets = {
            'profile_picture': forms.FileInput(attrs={'class': 'form-control'}),
        }

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['profile_picture', 'date_of_birth', 'bio']