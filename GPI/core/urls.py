from django.contrib import admin
from django.urls import path
from .views import login_view, reemplazos_view, recuperacion_view, base_view, docente_view, reportes_view, CustomLogoutView, asignatura_view, sala_view


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', base_view, name='base'),
    path('login/', login_view, name='login'),
    path('logout/', CustomLogoutView, name='logout'),
    path('reemplazos/', reemplazos_view, name='reemplazos'),
    path('recuperacion/', recuperacion_view, name='recuperacion'),
    path('docente/', docente_view, name='docente'),
    path('reportes/', reportes_view, name='reportes'),
    path('asignaturas/', asignatura_view, name='asignatura_list'),
    path('salas/', sala_view, name='sala_list')
]