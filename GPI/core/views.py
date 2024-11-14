from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from .models import Modulo, DiaSemana, Asignatura, Sala, Profesor, Horario, Semestre, Licencia, Reemplazos,Recuperacion
from django.core.exceptions import ObjectDoesNotExist
import json
from datetime import timedelta, date

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
    profesores = Profesor.objects.all()
    context = {
        'profesores': profesores,
    }

    if request.method == 'POST':
        if 'eliminar' in request.POST:
            id_profesor = request.POST.get('id_profesor')
            try:
                profesor_a_eliminar = get_object_or_404(Profesor, id_profesor=id_profesor)

                Licencia.objects.filter(profesor_id_profesor=profesor_a_eliminar).delete()

                Horario.objects.filter(profesor_id_profesor=profesor_a_eliminar).delete()

                profesor_a_eliminar.delete()

                messages.success(request, "Profesor y sus licencias eliminadas exitosamente.")
                return redirect('docente')
            except Profesor.DoesNotExist:
                messages.error(request, "El profesor no existe.")
                return redirect('docente')
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
        profesor_id = request.POST.get('profesor_id_profesor')  
        fecha_inicio = request.POST.get('fecha_inicio')
        fecha_termino = request.POST.get('fecha_fin')
        motivo = request.POST.get('motivo')
        observaciones = request.POST.get('observaciones')

        if not profesor_id:
            return JsonResponse({'success': False, 'error': 'Falta el ID del profesor'})
        
        profesor = get_object_or_404(Profesor, id_profesor=profesor_id)

        try:
            nueva_licencia = Licencia.objects.create(
                profesor_id_profesor=profesor,
                fecha_inicio=fecha_inicio,
                fecha_termino=fecha_termino,
                motivo=motivo,
                observaciones=observaciones
            )
            # Responder con éxito
            return JsonResponse({'success': True, 'message': 'Licencia guardada exitosamente.'})
        except Exception as e:
            # Manejar error en el proceso
            return JsonResponse({'success': False, 'error': f'Ocurrió un error: {str(e)}'})

    return JsonResponse({'success': False, 'error': 'Método no permitido'})


def reemplazos_view(request):

    return render(request, 'templates/gestion_reemplazo.html')


def recuperacion_view(request):
    return render(request, 'templates/gestion_recuperacion.html')



def gestionar_recuperacion(request):
    # Obtener todos los horarios y recuperaciones
    horarios = Horario.objects.all()
    recuperaciones = Recuperacion.objects.all()

    if request.method == 'POST':
        # Obtener los datos del formulario
        numero_modulos = request.POST.get('numero_modulos')
        fecha_clase = request.POST.get('fecha_clase')
        fecha_recuperacion = request.POST.get('fecha_recuperacion')
        hora_recuperacion = request.POST.get('hora_recuperacion')
        sala = request.POST.get('sala')
        horario_id = request.POST.get('horario_id_horario')
        
        print(f"horario_id recibido: {horario_id}")  # Esto imprimirá el valor recibido de `horario_id_horario`

        # Validar que el ID del horario sea correcto
        try:
            # Intenta convertir el ID a entero y buscar el horario
            horario_id = int(horario_id)
            horario = Horario.objects.get(id_horario=horario_id)
        except (ValueError, ObjectDoesNotExist):
            # Si no se encuentra el horario o el ID no es válido, muestra un mensaje de error
            return render(request, 'gestion_recuperacion.html', {
                'horarios': horarios,
                'recuperaciones': recuperaciones,
                'error': 'El ID del horario no es válido o no existe.'
            })

        # Crear la nueva recuperación
        nueva_recuperacion = Recuperacion(
            numero_modulos=numero_modulos,
            fecha_clase=fecha_clase,
            fecha_recuperacion=fecha_recuperacion,
            hora_recuperacion=hora_recuperacion,
            sala=sala,
            horario=horario
        )
        nueva_recuperacion.save()

        # Volver a cargar la página con la lista actualizada de horarios y recuperaciones
        return render(request, 'gestion_recuperacion.html', {
            'horarios': horarios,
            'recuperaciones': Recuperacion.objects.all(),  # Aseguramos que las recuperaciones se recarguen
            'success': 'Recuperación agregada exitosamente'
        })

    # Si no es POST, simplemente mostrar los horarios y recuperaciones
    return render(request, 'gestion_recuperacion.html', {
        'horarios': horarios,
        'recuperaciones': recuperaciones
    })



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
            for horario_data in data['horarios_asignados']:
                try:
                    asignatura = Asignatura.objects.get(id_asignatura=horario_data['asignaturaID'])
                    sala = Sala.objects.get(id_sala=horario_data['salaID'])
                    modulo = Modulo.objects.get(id_modulo=horario_data['moduloID'])
                    dia = DiaSemana.objects.get(id_dia=horario_data['diaID'])
                    semestre = Semestre.objects.get(id_semestre=horario_data['semestreID'])
                except Exception as e:
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
            return JsonResponse({"message": "Profesor y horarios creados exitosamente!"}, status=201)
        except Exception as e:
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

def docentes_con_licencia(request):
    # Obtener la fecha actual
    today = date.today()

    # Filtrar los docentes que tienen una licencia activa
    docentes = Profesor.objects.filter(
        licencia__fecha_inicio__lte=today,
        licencia__fecha_termino__gte=today
    ).distinct()

    # Devolver los docentes con licencia activa
    docentes_list = [
        {"id": docente.id_profesor, "nombre": f"{docente.nombre} {docente.apellido}"}
        for docente in docentes
    ]
    
    return JsonResponse(docentes_list, safe=False)

def asignaturas_por_docente(request, docente_id):
    asignaturas = Horario.objects.filter(profesor_id_profesor=docente_id).values('asignatura_id_asignatura__id_asignatura', 'asignatura_id_asignatura__nombre_asignatura')
    asignaturas_list = [{"id": asignatura["asignatura_id_asignatura__id_asignatura"], "nombre": asignatura["asignatura_id_asignatura__nombre_asignatura"]} for asignatura in asignaturas]

    return JsonResponse(asignaturas_list, safe=False)

def secciones_por_asignatura(request, asignatura_id):
    #aquí pasa un problema
    secciones = Horario.objects.filter(asignatura_id_asignatura_id=asignatura_id).values('seccion')
    secciones_list = [{"id": seccion["seccion"], "numero_seccion": seccion["seccion"]} for seccion in secciones.distinct()]
    
    return JsonResponse(secciones_list, safe=False)

def modulos(request, asignatura_id):
    modulos = Modulo.objects.all().values('id_modulo', 'hora_modulo')
    
    """
    aquí pasa un problema ya que el filtro debe tener más parametros, o va a devolver modulos correspondiente de TODAS las asignaturas donde el ID de la asignatura sea igual al que recibe
    el filtro debe contener:  
    
    
    la wea de arriba no tiene nada que ver
    solución: el html no debería ser un formulario, debe ser una tabla precargada con todas las asignaturas donde no podrá asistir
    si tiene licencia de lunes a miercoles, debe extraer el día lunes, martes y miercoles con todas las clases que tiene que realizar
    los datos ya están precargados según la asignatura, sección, hora, y módulo. solo deberá elegirse al profesor reemplazante.
    problematica: qué pasa con las licencias indefinidas? solución: deberá cargarse la semana completa pero tiene otro problema, si lleva más de dos semanas hay que agregar
    una nueva instancia para que se registre un nuevo registro de esa semana y no sé como hacerlo de momento.
    problematica, cómo se genera una nueva instancia de reemplazo? que tire todas las licencias con fecha de inicio y fin para poder identificar con qué licencia se está trabajando
    se deberá establecer un nuevo atributo en licencias que tenga un estado para: licencia sin asignacion de reemplazo - licencia en progreso - licencia y reemplazo finalizado.
    """
    modulo = Horario.objects.filter(asignatura_id_asignatura_id=asignatura_id).values('modulo_id_modulo')
    modulos_list = [{"id": modulo["id_modulo"], "hora_modulo": modulo["hora_modulo"]} for modulo in modulos]
    
    return JsonResponse(modulos_list, safe=False)

def salas(request):
    salas = Sala.objects.all().values('id_sala', 'numero_sala')
    salas_list = [{"id": sala["id_sala"], "numero_sala": sala["numero_sala"]} for sala in salas]
    
    return JsonResponse(salas_list, safe=False)

def profesores_reemplazantes(request):
    profesores = Profesor.objects.all().values('id_profesor', 'nombre', 'apellido')
    profesores_list = [{"id": profesor["id_profesor"], "nombre": profesor["nombre"], "apellido": profesor["apellido"]} for profesor in profesores]
    return JsonResponse(profesores_list, safe=False)