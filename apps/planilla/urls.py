from django.urls import path

from . import views

app_name = 'planilla' 

urlpatterns = [
    path(
        'departamentos/',
        views.DepartamentosListView.as_view(),
        name='departamentos'
    ),
    path(
        'crear/departamento',
        views.DepartamentoCreateView.as_view(),
        name='departamento-crear'
    ),
    path(
        'edicion/departamento/<slug:pk>/',
        views.DepartamentoUpdateView.as_view(),
        name='departamento-edicion'
    ),
    path(
        'detalle/departamento/<slug:pk>/',
        views.DepartamentoDetailView.as_view(), 
        name='departamento-detalle'
    ),
    path(
        'puestos/',
        views.PuestosListView.as_view(),
        name='puestos'
    ),
    path(
        'crear/puesto/',
        views.PuestoCreateView.as_view(),
        name='puesto-crear'
    ),
    path(
        'edicion/puesto/<slug:pk>/',
        views.PuestoUpdateView.as_view(),
        name='puesto-edicion'
    ),
    path(
        'detalle/puesto/<slug:pk>/',
        views.PuestoDetailView.as_view(),
        name='puesto-detalle'
    ),
    path(
        'empleados/', 
        views.EmpleadosListView.as_view(),
        name='empleados'
    ),
    path(
        'crear/empleado/',
        views.EmpleadoCreateView.as_view(),
        name='empleado-crear'
    ),
    path(
        'edicion/empleado/<slug:pk>/',
        views.EmpleadoUpdateView.as_view(),
        name='empleado-edicion'
    ),
    path(
        'detalle/empleado/<slug:pk>/',
        views.EmpleadoDetailView.as_view(),
        name='empleado-detalle'
    ),
] 
