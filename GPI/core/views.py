from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from .models import Modulo, DiaSemana, Asignatura, Sala, Profesor, Horario, Semestre, Licencia, Reemplazos,Recuperacion
from django.core.exceptions import ObjectDoesNotExist
import json
import logging
import locale
from datetime import timedelta, datetime
from collections import defaultdict

locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')

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
                observaciones=observaciones,
                estado="sin_asignar"
            )
            return JsonResponse({'success': True, 'message': 'Licencia guardada exitosamente.'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': f'Ocurrió un error: {str(e)}'})

    return JsonResponse({'success': False, 'error': 'Método no permitido'})

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



def gestion_recuperacion(request):
    # Recuperaciones existentes para mostrar en el HTML con las relaciones necesarias
    recuperaciones = Recuperacion.objects.select_related(
        'horario__profesor_id_profesor', 
        'horario__asignatura_id_asignatura'
    ).all()  # Aquí usamos select_related para traer tanto al profesor como la asignatura

    mensaje_profesor = None
    if request.method == 'POST':
        # Obtener los datos del formulario
        numero_modulos = request.POST.get('numero_modulos')
        fecha_clase = request.POST.get('fecha_clase')
        fecha_recuperacion = request.POST.get('fecha_recuperacion')
        hora_recuperacion = request.POST.get('hora_recuperacion')
        sala = request.POST.get('sala')
        horario_id = request.POST.get('horario_id_horario')

        # Verificar que el ID del horario sea válido
        try:
            horario = Horario.objects.get(id_horario=horario_id)
        except Horario.DoesNotExist:
            return render(request, 'gestion_recuperacion.html', {
                'recuperaciones': recuperaciones,
                'error': 'El horario no existe. Por favor verifica los datos.',
            })

        # Obtener el profesor relacionado al horario
        profesor = horario.profesor_id_profesor
        mensaje_profesor = f'La recuperación corresponde al profesor {profesor.nombre} {profesor.apellido}'

        # Guardar los datos de recuperación en la base de datos
        nueva_recuperacion = Recuperacion(
            numero_modulos=numero_modulos,
            fecha_clase=fecha_clase,
            fecha_recuperacion=fecha_recuperacion,
            hora_recuperacion=hora_recuperacion,
            sala=sala,
            horario=horario
        )
        nueva_recuperacion.save()

        # Recargar recuperaciones actualizadas
        recuperaciones = Recuperacion.objects.select_related(
            'horario__profesor_id_profesor',
            'horario__asignatura_id_asignatura'
        ).all()

    return render(request, 'templates/gestion_recuperacion.html', {
        'recuperaciones': recuperaciones,
        'mensaje_profesor': mensaje_profesor,
    })
#---------------------------------------------------------------------------

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

#-----------------------------------------

def reemplazos_view(request):
    docentes_con_licencia = Profesor.objects.filter(licencia__isnull=False).distinct()

    reemplazos = Reemplazos.objects.all().select_related(
        'horario__asignatura_id_asignatura',
        'horario__sala_id_sala',
        'horario__modulo_id_modulo',
        'horario__dia_semana_id_dia',
        'horario__profesor_id_profesor'
    )

    grupos_reemplazos = defaultdict(list)
    for reemplazo in reemplazos:
        clave = (
            reemplazo.horario.asignatura_id_asignatura.nombre_asignatura,
            reemplazo.horario.seccion,
            reemplazo.horario.sala_id_sala.numero_sala,
            reemplazo.horario.profesor_id_profesor.nombre,
            reemplazo.horario.profesor_id_profesor.apellido,
        )
        grupos_reemplazos[clave].append(reemplazo)
        
    reemplazos_agrupados = []
    for clave, reemplazos_grupo in grupos_reemplazos.items():
        nombre_asignatura, seccion, numero_sala, nombre_profesor, apellido_profesor = clave


        horarios = sorted([reemplazo.horario.modulo_id_modulo.hora_modulo for reemplazo in reemplazos_grupo])
        hora_inicio = horarios[0] 
        hora_fin = horarios[-1]
        hora_inicio_corta = hora_inicio[:5]
        hora_fin_corta = hora_fin[-5:]
        hora_modulo = hora_inicio_corta + "-" + hora_fin_corta
        nombre_completo_profesor = nombre_profesor
        if reemplazos_grupo[0].horario.profesor_id_profesor.segundo_nombre:
            nombre_completo_profesor += f" {reemplazos_grupo[0].horario.profesor_id_profesor.segundo_nombre}"
        nombre_completo_profesor += f" {apellido_profesor}"
        if reemplazos_grupo[0].horario.profesor_id_profesor.segundo_apellido:
            nombre_completo_profesor += f" {reemplazos_grupo[0].horario.profesor_id_profesor.segundo_apellido}"
        fecha_reemplazo = reemplazos_grupo[0].fecha_reemplazo.strftime('%d de %B de %Y')
        mes = fecha_reemplazo.split(' ')[2]
        fecha_reemplazo = fecha_reemplazo.replace(mes, mes.capitalize())

        reemplazo_agrupado = {
            'nombre_asignatura': nombre_asignatura,
            'seccion': seccion,
            'numero_sala': numero_sala,
            'hora_modulo': hora_modulo,
            'numero_modulos': len(horarios),
            'nombre_profesor': nombre_completo_profesor,
            'fecha_reemplazo': fecha_reemplazo,
            'dia_semana': reemplazos_grupo[0].horario.dia_semana_id_dia.nombre_dia,
            'semana': reemplazos_grupo[0].semana,
        }
        reemplazos_agrupados.append(reemplazo_agrupado)

    return render(request, 'templates/gestion_reemplazo.html', {
        'docentes_con_licencia': docentes_con_licencia,
        'reemplazos': reemplazos_agrupados
    })

def profesores_con_licencia_no_asignada(request):
    profesores = Profesor.objects.filter(
        licencia__estado='sin_asignar'
    ).distinct()
    profesores_data = []
    for profesor in profesores:
        licencia = Licencia.objects.filter(profesor_id_profesor=profesor, estado='sin_asignar').first()
        if licencia:
            profesores_data.append({
                'id_profesor': profesor.id_profesor,
                'nombre': profesor.nombre,
                'segundo_nombre': profesor.segundo_nombre,
                'apellido': profesor.apellido,
                'segundo_apellido': profesor.segundo_apellido,
                'id_licencia': licencia.id_licencia,
                'fecha_inicio': licencia.fecha_inicio.strftime('%Y-%m-%d'),
                'fecha_termino': licencia.fecha_termino.strftime('%Y-%m-%d')
            })

    return JsonResponse({'profesores': profesores_data}, safe=False)

#-----------------------------------------

logger = logging.getLogger(__name__)
def obtener_clases_por_docente(request):
    docente_id = request.GET.get('docente_id')
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_termino = request.GET.get('fecha_termino')

    if not docente_id or not fecha_inicio or not fecha_termino:
        logger.error("Faltan parámetros en la solicitud.")
        return JsonResponse({'error': 'Faltan parámetros'}, status=400)

    try:
        fecha_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d').date()
        fecha_termino = datetime.strptime(fecha_termino, '%Y-%m-%d').date()
        if fecha_termino < fecha_inicio:
            logger.warning("La fecha de término no puede ser antes de la fecha de inicio.")
            return JsonResponse({'error': 'La fecha de término no puede ser antes de la fecha de inicio'}, status=400)
        try:
            profesor = Profesor.objects.get(id_profesor=docente_id)
            logger.debug(f"Profesor encontrado: {profesor.nombre} {profesor.apellido}")
        except Profesor.DoesNotExist:
            logger.error(f"Profesor con id {docente_id} no encontrado.")
            return JsonResponse({'error': 'Profesor no encontrado'}, status=404)
        
        horarios = Horario.objects.filter(
            profesor_id_profesor=profesor
        ).filter(Q(dia_semana_id_dia__gte=1) & Q(dia_semana_id_dia__lte=6))

        logger.debug(f"Horarios obtenidos: {horarios.count()} horarios")

        clases = []
        current_date = fecha_inicio
        while current_date <= fecha_termino:
            dia_semana = current_date.weekday() + 1
            logger.debug(f"Procesando fecha: {current_date} (Día de la semana: {dia_semana})")
            for horario in horarios.filter(dia_semana_id_dia=dia_semana):
                dia = current_date.strftime('%A').capitalize()
                clases.append({
                    'asignatura': horario.asignatura_id_asignatura.nombre_asignatura,
                    'seccion': horario.seccion,
                    'sala': horario.sala_id_sala.numero_sala,
                    'modulo': horario.modulo_id_modulo.hora_modulo,
                    'dia': dia,
                    'fecha_clase': current_date.strftime('%d-%m-%Y'),
                    'modulo_id': horario.modulo_id_modulo.id_modulo,
                    'dia_semana_id': horario.dia_semana_id_dia.id_dia,
                    'id_horario': horario.id_horario
                })
            current_date += timedelta(days=1)

        if not clases:
            logger.info(f"No hay clases para el profesor {profesor.nombre} {profesor.apellido} durante el rango de fechas.")
        
        logger.debug(f"Clases encontradas: {len(clases)}")
        return JsonResponse({'clases': clases})

    except Exception as e:
        logger.error(f"Error inesperado: {str(e)}")
        return JsonResponse({'error': f'Error: {str(e)}'}, status=500)
    
def obtener_profesores_disponibles(request):
    dia_semana = request.GET.get('dia_semana')
    modulo_id = request.GET.get('modulo_id')
    if not dia_semana or not modulo_id:
        return JsonResponse({'error': 'Faltan parámetros'}, status=400)
    try:
        dia_semana = int(dia_semana)
        modulo_id = int(modulo_id)
    except ValueError:
        return JsonResponse({'error': 'Los parámetros deben ser números enteros'}, status=400)
    profesores_disponibles = Profesor.objects.exclude(
        horario__dia_semana_id_dia=dia_semana,
        horario__modulo_id_modulo_id=modulo_id
    ).distinct()
    profesores_data = list(profesores_disponibles.values('id_profesor', 'nombre', 'apellido', 'segundo_nombre', 'segundo_apellido'))
    return JsonResponse({'profesores': profesores_data}, safe=False)

def registrar_reemplazo(request):
    if request.method == 'POST':
        try:
            logger.info('Recibida solicitud POST para registrar reemplazos.')
            data = json.loads(request.body)
            reemplazos = data.get('reemplazos', [])
            id_licencia = data.get('id_licencia')

            if not reemplazos:
                logger.warning('No se proporcionaron reemplazos en la solicitud.')
                return JsonResponse({'error': 'No se proporcionaron reemplazos'}, status=400)

            if not id_licencia:
                logger.warning('No se proporcionó id_licencia en la solicitud.')
                return JsonResponse({'error': 'No se proporcionó id_licencia'}, status=400)

            # Buscar la licencia y cambiar su estado
            licencia = get_object_or_404(Licencia, id_licencia=id_licencia)
            licencia.estado = 'asignado'
            licencia.save()
            logger.info(f'Licencia {id_licencia} actualizada a estado "asignado".')

            logger.info(f'Número de reemplazos recibidos: {len(reemplazos)}')
            for reemplazo in reemplazos:
                semana = reemplazo.get('semana')
                fecha_reemplazo = reemplazo.get('fecha_reemplazo')
                profesor_reemplazo = reemplazo.get('profesor_reemplazo')
                horario_id = reemplazo.get('horario_id')
                logger.info(f'Procesando reemplazo: Semana={semana}, Fecha={fecha_reemplazo}, Profesor={profesor_reemplazo}, Horario ID={horario_id}')
                try:
                    horario = Horario.objects.get(id_horario=horario_id)
                    logger.info(f'Horario encontrado: {horario}')
                except Horario.DoesNotExist:
                    logger.error(f'Horario no encontrado para ID: {horario_id}')
                    return JsonResponse({'error': f'Horario no encontrado para ID {horario_id}'}, status=400)
                
                # Crear el objeto de reemplazo
                reemplazo_obj = Reemplazos.objects.create(
                    semana=semana,
                    fecha_reemplazo=fecha_reemplazo,
                    profesor_reemplazo=profesor_reemplazo,
                    horario=horario,
                )
                logger.info(f'Reemplazo creado: {reemplazo_obj}')

            return JsonResponse({'success': True}, status=200)
        except json.JSONDecodeError:
            logger.error('Error al decodificar el JSON recibido.')
            return JsonResponse({'error': 'Error al procesar la solicitud. JSON mal formado.'}, status=400)
        except Exception as e:
            logger.error(f'Error inesperado: {str(e)}')
            return JsonResponse({'error': f'Error inesperado: {str(e)}'}, status=500)
    
    logger.warning('Método no permitido. Solo se acepta POST.')
    return JsonResponse({'error': 'Método no permitido'}, status=405)