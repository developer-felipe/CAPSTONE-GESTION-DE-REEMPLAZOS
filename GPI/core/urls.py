from django.contrib import admin
from django.urls import path
from .views import (    login_view, reemplazos_view,guardar_licencia ,recuperacion_view , gestionar_recuperacion,base_view, docente_view, reportes_view, CustomLogoutView,asignatura_view, sala_view, crear_docente_view, crear_profesor_y_horarios,
profesores_reemplazantes, secciones_por_asignatura, asignaturas_por_docente, docentes_con_licencia, modulos,salas )


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', base_view, name='base'),
    path('login/', login_view, name='login'),
    path('logout/', CustomLogoutView, name='logout'),
    path('reemplazos/', reemplazos_view, name='reemplazos'),
    path('recuperacion/', recuperacion_view, name='recuperacion'),
    path('gestionar_recuperacion/', gestionar_recuperacion, name='gestionar_recuperacion'),
    path('docente/', docente_view, name='docente'),
    path('reportes/', reportes_view, name='reportes'),
    path('asignaturas/', asignatura_view, name='asignatura_list'),
    path('salas/', sala_view, name='sala_list'),
    path('guardar_licencia/', guardar_licencia, name='guardar_licencia'),
    path('profesor/<int:profesor_id>/guardar_licencia/', guardar_licencia, name='guardar_licencia'),
    path('crear_docente/', crear_docente_view, name='crear_docente'),
    path('crear_profesor_y_horarios/',crear_profesor_y_horarios, name='crear_docente_horario'),
    
    path('api/docentes_con_licencia/', docentes_con_licencia, name='docentes_con_licencia'),
    path('api/asignaturas_por_docente/<int:docente_id>/', asignaturas_por_docente, name='asignaturas_por_docente'),
    path('api/secciones_por_asignatura/<int:asignatura_id>/', secciones_por_asignatura, name='secciones_por_asignatura'),
    path('api/modulos/', modulos, name='modulos'),
    path('api/salas/', salas, name='salas'),
    path('api/profesores_reemplazantes/', profesores_reemplazantes, name='profesores_reemplazantes'),
]