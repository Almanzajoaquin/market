from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from .forms import UserUpdateForm, ProfileUpdateForm
from .models import CustomUser
from marketplace.models import Order  # ← AGREGAR ESTA IMPORTACIÓN

@login_required
def profile(request):
    """Vista del perfil del usuario"""
    return render(request, 'users/profile.html')

@login_required
def update_profile(request):
    """Vista para actualizar perfil"""
    if request.method == 'POST':
        # esto cambia
        #user_form = UserUpdateForm(request.POST, instance=request.user)
        #profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        # por esto
        form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
        
        """ y esto cambia
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Tu perfil ha sido actualizado!')
            return redirect('profile')
        """
        """Por esto"""
        if form.is_valid():
            form.save()
            messages.success(request, 'Tu perfil ha sido actualizado exitosamente!')
            return redirect('profile')
    else:
        # esto cambia
        #user_form = UserUpdateForm(instance=request.user)
        #profile_form = ProfileUpdateForm(instance=request.user)
    
        #Por esto
        form = UserUpdateForm(instance=request.user)
    """ no se necesita entonces por ahora
    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'users/update_profile.html', context)
    """
    return render(request, 'users/update_profile.html', {'form': form})

@login_required
def change_password(request):
    """Vista para cambiar contraseña"""
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Tu contraseña ha sido cambiada exitosamente!')
            return redirect('profile')
        else:
            messages.error(request, 'Por favor corrige los errores below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'users/change_password.html', {'form': form})

@login_required
def delete_account(request):
    """Vista para eliminar cuenta"""
    if request.method == 'POST':
        user = request.user
        user.delete()
        messages.success(request, 'Tu cuenta ha sido eliminada exitosamente.')
        return redirect('index')
    return render(request, 'users/delete_account.html')

# -------------------------Vista para historial de pedidos (si tienes app de órdenes)
def order_history(request):
    """Vista del historial de pedidos del usuario"""
     # Obtener órdenes del usuario actual
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    
    return render(request, 'users/order_history.html', {
        'orders': orders
    })