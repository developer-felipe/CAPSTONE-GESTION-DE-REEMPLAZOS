from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Usuario

def login_view(request):
    if request.method == 'POST':
        usuario = request.POST['usuario']
        password = request.POST['password']
        try:
            user = Usuario.objects.get(usuario=usuario)
            if password == user.password:
                request.session['user_id'] = user.id_usuario
                return redirect('reemplazos')
            else:
                messages.error(request, 'Contraseña incorrecta.')
        except Usuario.DoesNotExist:
            messages.error(request, 'Usuario no encontrado.')
    return render(request, 'templates/login.html')

def reemplazos_view(request):
    return render(request, 'templates/gestion_reemplazo.html')

def recuperacion_view(request):
    return render(request, 'templates/gestion_recuperacion.html')

def docente_view(request):
    return render(request, 'templates/docente.html')

def reportes_view(request):
    return render(request, 'templates/reportes.html')

def base_view(request):
    return render(request, 'templates/base.html')