from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from .models import Modulo, DiaSemana, Asignatura, Sala, Profesor
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


def docente_view(request):
    if request.method == 'POST':
        if 'eliminar' in request.POST:
            id_profesor = request.POST.get('id_profesor')
            try:
                profesor_a_eliminar = get_object_or_404(Profesor, id_profesor=id_profesor)
                profesor_a_eliminar.delete()
                messages.success(request, "Profesor eliminado exitosamente.")
            except Profesor.DoesNotExist:
                messages.error(request, "El profesor no existe.")
                
        else:
            nombre = request.POST.get('primer_nombre').strip().capitalize()
            segundo_nombre = request.POST.get('segundo_nombre').strip().capitalize() 
            apellido = request.POST.get('primer_apellido').strip().capitalize()
            segundo_apellido = request.POST.get('segundo_apellido').strip().capitalize() 

            if not nombre or not apellido:
                messages.error(request, 'Los nombres y apellidos son obligatorios.')
                return redirect('docente')

            nuevo_profesor = Profesor(
                nombre=nombre,
                segundo_nombre=segundo_nombre,
                apellido=apellido,
                segundo_apellido=segundo_apellido
            )
            nuevo_profesor.save()
            messages.success(request, "Profesor agregado exitosamente.")
        return redirect('docente')
    
    profesores = Profesor.objects.all()
    return render(request, 'templates/docente.html', {'profesores': profesores})


def reemplazos_view(request):
    return render(request, 'templates/gestion_reemplazo.html')

def recuperacion_view(request):
    return render(request, 'templates/gestion_recuperacion.html')


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