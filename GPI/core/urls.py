from django.contrib import admin
from django.urls import path
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .views import (login_view, reemplazos_view,guardar_licencia ,recuperacion_view,base_view, docente_view, reportes_view, CustomLogoutView,asignatura_view, sala_view, crear_docente_view, crear_profesor_y_horarios,
profesores_con_licencia_no_asignada,obtener_clases_por_docente,obtener_profesores_disponibles,registrar_reemplazo, modificar_docente_view, modificar_profesor_y_horarios, registrar_recuperacion,
 eliminar_recuperacion , gestionar_licencias,editar_licencia ,eliminar_licencia ,todas_salas,todas_asignaturas,docente_recuperación, docente_asignatura, profesor_por_nombre, modulo_por_id,
 actualizar_reemplazo,obtenerHorario)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('base/', base_view, name='base'),
    path('', login_view, name='login'),
    path('logout/', CustomLogoutView, name='logout'),
    path('reemplazos/', reemplazos_view, name='reemplazos'),
    path('recuperacion/', recuperacion_view, name='recuperacion'),
    path('docente/', docente_view, name='docente'),
    path('reportes/', reportes_view, name='reportes'),
    path('asignaturas/', asignatura_view, name='asignatura_list'),
    path('salas/', sala_view, name='sala_list'),
    path('guardar_licencia/', guardar_licencia, name='guardar_licencia'),
    path('profesor/<int:profesor_id>/guardar_licencia/', guardar_licencia, name='guardar_licencia'),
    path('crear_docente/', crear_docente_view, name='crear_docente'),
    path('crear_profesor_y_horarios/',crear_profesor_y_horarios, name='crear_docente_horario'),
    path('profesores_con_licencia_no_asignada/', profesores_con_licencia_no_asignada, name='profesores_con_licencia_no_asignada'),
    path('obtener_clases_por_docente/', obtener_clases_por_docente, name='obtener_clases_por_docente'),
    path('obtener_profesores_disponibles/', obtener_profesores_disponibles, name='obtener_profesores_disponibles'),
    path('registrar_reemplazo/', registrar_reemplazo, name='registrar_reemplazo'),
    path('registrar_recuperacion/', registrar_recuperacion, name='registrar_recuperacion'),
    
    path('modificar_docente/<int:id>/', modificar_docente_view, name='modificar_docente'),
    path('modificar_profesor_y_horarios/', modificar_profesor_y_horarios, name='modificar_profesor_y_horarios'),
    
    path('eliminar-recuperacion/<int:id_recuperacion>/', eliminar_recuperacion, name='eliminar_recuperacion'),
    path('todas_asignaturas/', todas_asignaturas, name='todas_asignaturas'),
    path('todas_salas/', todas_salas, name='todas_salas'),
    path('docente_recuperación/', docente_recuperación, name='docente_recuperación'),
    path('docente_asignatura/<int:profesorId>/', docente_asignatura, name='docente_asignatura'),
    
    path('profesor_licencias/<int:profesor_id>/', gestionar_licencias, name='gestionar_licencias'),
    path('licencias/<int:id_licencia>/', editar_licencia, name='editar_licencia'),
    path('licencias/eliminar/<int:id_licencia>/', eliminar_licencia, name='eliminar_licencia'),
    
    path('reemplazos/profesor_por_nombre/<str:nombre>/', profesor_por_nombre, name='profesor_por_nombre'),
    path('modulo_por_id/<int:modulo>/', modulo_por_id, name='modulo_por_id'),
    path('reemplazos/actualizar_reemplazo/',actualizar_reemplazo, name='actualizar_reemplazo'),
    path('obtener_horarios/<int:id_profesor>/', obtenerHorario, name='obtener_horarios'),

]