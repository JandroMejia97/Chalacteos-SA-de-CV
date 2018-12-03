from django.urls import path, re_path

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
        'edicion/departamento/<slug:pk>',
        views.DepartamentoUpdateView.as_view(),
        name='departamento-edicion'
    ),
    path(
        'detalle/departamento/<slug:pk>',
        views.DepartamentoDetailView.as_view(), 
        name='departamento-detalle'
    ),
    re_path(
        r'ajax/departamento/(?P<id_departamento>[0-9]+)/',
        views.departamentos,
        name='ajax-departamento'
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
        'edicion/puesto/<slug:pk>',
        views.PuestoUpdateView.as_view(),
        name='puesto-edicion'
    ),
    path(
        'detalle/puesto/<slug:pk>',
        views.PuestoDetailView.as_view(),
        name='puesto-detalle'
    ),
    re_path(
        r'ajax/puesto/(?P<id_puesto>[0-9]+)/',
        views.puestos,
        name='ajax-puesto'
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
        'edicion/empleado/<slug:pk>',
        views.EmpleadoUpdateView.as_view(),
        name='empleado-edicion'
    ),
    path(
        'detalle/empleado/<slug:pk>',
        views.EmpleadoDetailView.as_view(),
        name='empleado-detalle'
    ),
    re_path(
        r'ajax/empleado/(?P<id>[0-9]+)/',
        views.empleados,
        name='ajax-empleado'
    ),
] 
