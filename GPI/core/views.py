from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from .models import Modulo, DiaSemana, Asignatura, Sala
import json


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

def horario_view(request):
    modulos = Modulo.objects.all()
    dias = DiaSemana.objects.all()
    
    context = {
        'modulos' : modulos,
        'dias' : dias
    }
    return render(request, 'templates/horario.html',context)

def asignatura_view(request):
    if request.method == 'GET':
        asignaturas = Asignatura.objects.all().values('id_asignatura', 'nombre_asignatura')
        asignaturas_list = list(asignaturas)
        return JsonResponse(asignaturas_list, safe=False)

    elif request.method == 'POST':
        data = json.loads(request.body)
        nombre_asignatura = data.get('nombre')
        
        if nombre_asignatura:
            nueva_asignatura = Asignatura(nombre_asignatura=nombre_asignatura)
            nueva_asignatura.save()
            return JsonResponse({'message': 'Asignatura agregada'}, status=201)
        else:
            return JsonResponse({'error': 'Nombre de asignatura no proporcionado'}, status=400)

    return JsonResponse({'error': 'Método no permitido'}, status=405)

def sala_view(request):
    if request.method == 'GET':
        salas = Sala.objects.all().values('id_sala', 'numero_sala')
        salas_list = list(salas)
        return JsonResponse(salas_list, safe=False)
    
    elif request.method == 'POST':
        data = json.loads(request.body)
        numero_sala = data.get('numero_sala')
        
        if numero_sala:
            nueva_sala = Sala(numero_sala=numero_sala)
            nueva_sala.save()
            return JsonResponse({'message' : 'Sala agregada'}, status=201)
        else:
            return JsonResponse({'message' : 'Número de la sala no proporcionado'})
        
    return JsonResponse({'error': 'Método no permitido'}, status=405)