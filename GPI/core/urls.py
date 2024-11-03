"""
URL configuration for GPI project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.shortcuts import redirect
from .views import login_view, reemplazos_view, recuperacion_view,base_view,docente_view, reportes_view, CustomLogoutView, horario_view, asignatura_view, sala_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', base_view, name='base'),
    path('login/', login_view, name='login'),
    path('logout/', CustomLogoutView, name='logout'),  # Cambia 'login/' a 'logout/'
    path('reemplazos/', reemplazos_view, name='reemplazos'),
    path('recuperacion/', recuperacion_view, name='recuperacion'),
    path('docente/', docente_view, name='docente'),
    path('reportes/', reportes_view, name='reportes'),
    path('cargar_horario/', horario_view, name='cargar_horario'),
    path('asignaturas/', asignatura_view, name='asignatura_list'),
    path('salas/', sala_view, name='sala_list')
]