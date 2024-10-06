from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .forms import LoginForm

def login_view(request):
    form = LoginForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('reemplazos')  # Redirige a la vista de reemplazos
            else:
                form.add_error(None, 'Usuario o contraseña incorrectos')
    
    return render(request, 'templates/login.html', {'form': form})

def reemplazos_view(request):
    return render(request, 'templates/gestion_reemplazo.html')

def recuperacion_view(request):
    return render(request, 'templates/gestion_recuperacion.html')

def docente_view(request):
    return render(request, 'templates/docente.html')

def base_view(request):
    return render(request, 'templates/base.html')