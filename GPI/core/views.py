from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib import messages


def login_view(request):
    if request.method == 'POST':
        username = request.POST['usuario']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('reemplazos')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
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

def CustomLogoutView(request):
    return render(request, 'templates/login.html')