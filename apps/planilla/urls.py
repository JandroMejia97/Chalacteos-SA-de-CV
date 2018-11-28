from django.conf.urls import url
from django.conf.urls import url, include
#from .views import *
from django.urls import path
from django.contrib.auth.decorators import login_required

from .views import *

app_name = 'appsic' 

urlpatterns = [

    path('', index, name='index'),

    path('lista_empresa', EmpresaList.as_view(), name='list'),
    path('detail_empresa/(?P<pk>\d+)$', EmpresaDetail.as_view(), name='detail'),
    path('nuevo', EmpresaCreation.as_view(), name='new'),
    path('editar/(?P<pk>\d+)', EmpresaUpdate.as_view(), name='edit'),
    path('borrar/(?P<pk>\d+)', EmpresaDelete.as_view(), name='delete'),



    path('lista_empleado', EmpleadoList.as_view(), name='list_empleado'),
    path('detail_empleado/(?P<pk>\d+)', EmpleadoDetail.as_view(), name='detail_empleado'),
    path('^nuevo_empleado', EmpleadoCreation.as_view(), name='new_empleado'),
    path('^editar_empleado/(?P<pk>\d+)', EmpleadoUpdate.as_view(), name='edit_empleado'),
    path('^borrar_empleado/(?P<pk>\d+)', EmpleadoDelete.as_view(), name='delete_empleado'),


    path('lista_departamento', DepartamentoList.as_view(), name='list_departamento'),
    path('detail_departamento/(?P<pk>\d+)', DepartamentoDetail.as_view(), name='detail_departamento'),
    path('nuevo_departamento', DepartamentoCreation.as_view(), name='new_departamento'),
    path('editar_departamento/(?P<pk>\d+)', DepartamentoUpdate.as_view(), name='edit_departamento'),
    path('borrar_departamento/(?P<pk>\d+)', DepartamentoDelete.as_view(), name='delete_departamento'),


    path('lista_puesto', PuestoList.as_view(), name='list_puesto'),
    path('detail_puesto/(?P<pk>\d+)', PuestoDetail.as_view(), name='detail_puesto'),
    path('nuevo_puesto', PuestoCreation.as_view(), name='new_puesto'),
    path('editar_puesto/(?P<pk>\d+)', PuestoUpdate.as_view(), name='edit_puesto'),
    path('borrar_puesto/(?P<pk>\d+)', login_required(PuestoDelete.as_view()), name='delete_puesto'),


    path('lista_empleadoempresa', EmpleadoEmpresaList.as_view(), name='list_empleadoempresa'),
    path('detail_empleadoempresa/(?P<pk>\d+)', EmpleadoEmpresaDetail.as_view(), name='detail_empleadoempresa'),
    path('nuevo_empleadoempresa', EmpleadoEmpresaCreation.as_view(), name='new_empleadoempresa'),
    path('editar_empleadoempresa/(?P<pk>\d+)', EmpleadoEmpresaUpdate.as_view(), name='edit_empleadoempresa'),
    path('borrar_empleadoempresa/(?P<pk>\d+)', EmpleadoEmpresaDelete.as_view(), name='delete_empleadoempresa'),




    path('lista_puestoempresa', PuestoEmpresaList.as_view(), name='list_puestoempresa'),
    path('detail_puestoempresa/(?P<pk>\d+)', PuestoEmpresaDetail.as_view(), name='detail_puestoempresa'),
    path('nuevo_puestoempresa', PuestoEmpresaCreation.as_view(), name='new_puestoempresa'),
    path('editar_puestoempresa/(?P<pk>\d+)', PuestoEmpresaUpdate.as_view(), name='edit_puestoempresa'),
    path('borrar_puestoempresa/(?P<pk>\d+)', PuestoEmpresaDelete.as_view(), name='delete_puestoempresa'),




    path('lista_departamentoempresa', DepartamentoEmpresaList.as_view(), name='list_departamentoempresa'),
    path('detail_departamentoempresa/(?P<pk>\d+)', DepartamentoEmpresaDetail.as_view(), name='detail_departamentoempresa'),
    path('nuevo_departamentoempresa', DepartamentoEmpresaCreation.as_view(), name='new_departamentoempresa'),
    path('editar_departamentoempresa/(?P<pk>\d+)', DepartamentoEmpresaUpdate.as_view(), name='edit_departamentoempresa'),
    path('borrar_departamentoempresa/(?P<pk>\d+)', DepartamentoEmpresaDelete.as_view(), name='delete_departamentoempresa'),


    path('lista/empresas', Empresa_AsignacionList.as_view(), name='empresa_asignacion'),
    path('asignacion/(?P<pk>\d+)/', asignacion, name='asignacion'),
    path('asignacion/editar/(?P<pk>\d+)/', asignacion_editar, name='asignacion_editar'),
    path('asignacion/lista', AsignacionList.as_view(), name='list_asignacion'),
    path('asignaciones/(?P<pk>\d+)/', Asignaciones, name='asignacion_listar'),
    path('asignacion/borrar/(?P<pk>\d+)', AsignacionDelete.as_view(), name='asignacion_eliminar'),
    path('asfilter',AsfilterList.as_view(), name='asfilter'),


    

    path('lista_renta', RentaList.as_view(), name='list_renta'),
    path('nuevo_renta', RentaCreation.as_view(), name='new_renta'),
    path('editar_renta/(?P<pk>\d+)', RentaUpdate.as_view(), name='edit_renta'),

    path('borrar_planilla/(?P<pk>\d+)', PlanillaDelete.as_view(), name='delete_planilla'),




    path('consultar_planillas/', consultar_planillas, name='lista_planilla'),
    path('consultar/', consultar_empresa, name='lista_empresas'),
    path('buscar/', buscar, name='buscar'),
    path('newPlanilla/', newPlanilla, name='newPlanilla'),
    path('impresion/(?P<pk>\d+)', pasajeros_problematicos_csv, name='impresion'),

    #Busquedas

    path('filtro/', filtro, name='filtro'),
] 
