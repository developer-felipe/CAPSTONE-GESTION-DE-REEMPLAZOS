from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.http import JsonResponse
from .models import Modulo, DiaSemana, Asignatura, Sala, Profesor, Horario, Semestre, Licencia
import json
import logging


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
    modulos = Modulo.objects.all()
    dias = DiaSemana.objects.all()
    profesores = Profesor.objects.all()

    context = {
        'modulos': modulos,
        'dias': dias,
        'profesores': profesores,
    }

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

    return render(request, 'templates/docente.html', context)




def guardar_licencia(request):
    if request.method == 'POST':
        # Obtener los datos del formulario
        profesor_id = request.POST.get('profesor_id_profesor')  # ID del profesor
        fecha_inicio = request.POST.get('fecha_inicio')
        fecha_termino = request.POST.get('fecha_fin')
        motivo = request.POST.get('motivo')
        observaciones = request.POST.get('observaciones')
        
        # Verificar que se haya recibido el ID del profesor
        if not profesor_id:
            return JsonResponse({'success': False, 'error': 'Falta el ID del profesor'})

        # Obtener el profesor o devolver error si no existe
        profesor = get_object_or_404(Profesor, id_profesor=profesor_id)

        # Crear la licencia
        try:
            nueva_licencia = Licencia.objects.create(
                profesor_id_profesor=profesor,
                fecha_inicio=fecha_inicio,
                fecha_termino=fecha_termino,
                motivo=motivo,
                observaciones=observaciones
            )
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    # Si no es un POST, devuelve un error
    return JsonResponse({'success': False, 'error': 'Método no permitido'})

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

logger = logging.getLogger(__name__)
def crear_profesor_y_horarios(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            profesor_data = data.get('profesor')
            ultimo_profesor = Profesor.objects.last()
            if ultimo_profesor:
                nuevo_id_profesor = ultimo_profesor.id_profesor + 1
            else:
                nuevo_id_profesor = 1
            profesor = Profesor.objects.create(
                id_profesor=nuevo_id_profesor,
                nombre=profesor_data['nombre'],
                apellido=profesor_data['apellido'],
                segundo_nombre=profesor_data.get('segundo_nombre', ''),
                segundo_apellido=profesor_data.get('segundo_apellido', '')
            )
            logger.info(f"Profesor creado con ID: {profesor.id_profesor}")
            for horario_data in data['horarios_asignados']:
                try:
                    asignatura = Asignatura.objects.get(id_asignatura=horario_data['asignaturaID'])
                    sala = Sala.objects.get(id_sala=horario_data['salaID'])
                    modulo = Modulo.objects.get(id_modulo=horario_data['moduloID'])
                    dia = DiaSemana.objects.get(id_dia=horario_data['diaID'])
                    semestre = Semestre.objects.get(id_semestre=horario_data['semestreID'])
                except Exception as e:
                    logger.error(f"Error al obtener los objetos relacionados: {e}")
                    return JsonResponse({"error": f"Error al obtener los objetos relacionados: {str(e)}"}, status=500)
                Horario.objects.create(
                    profesor_id_profesor=profesor,
                    asignatura_id_asignatura=asignatura,
                    sala_id_sala=sala,
                    dia_semana_id_dia=dia,
                    modulo_id_modulo=modulo,
                    semestre_id_semestre=semestre,
                    seccion=horario_data['seccion'],
                    jornada=horario_data['jornada']
                )
                logger.info(f"Horario creado para el profesor ID {profesor.id_profesor}.")

            return JsonResponse({"message": "Profesor y horarios creados exitosamente!"}, status=201)
        except Exception as e:
            logger.error(f"Error inesperado: {e}")
            return JsonResponse({"error": str(e)}, status=500)

    
def crear_docente_view(request):
    modulos = Modulo.objects.all()
    dias = DiaSemana.objects.all()
    profesores = Profesor.objects.all()
    ultimo_profesor = profesores.last()
    ultimo_id = ultimo_profesor.id_profesor if ultimo_profesor else 0
    context = {
        'modulos': modulos,
        'dias': dias,
        'profesores': profesores,
        'ultimo_id': ultimo_id
    }
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
    return render(request, 'templates/crear_docente.html',context)