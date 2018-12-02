from django.shortcuts import render, render_to_response, redirect, get_object_or_404
from .models import *
from django.http import HttpResponse 
import csv

from django.views.generic.list import ListView

from django.urls import reverse_lazy

from django.views.generic.detail import DetailView

from django.contrib.auth.decorators import login_required

from .forms import *

from django.template import  RequestContext

from django.views.generic.edit import (
    CreateView,
    UpdateView,
    DeleteView

)


def index(request):
    return render(request,"planilla/inicio/index.html")
#Departamento

class DepartamentosListView(ListView):
    model = Departamento
    template_name = 'planilla/gestionarDepartamentos.html'
    context_object_name = 'departamentos'

    def get_queryset(self):
        user = self.request.user
        context = Departamento.objects.all()
        if context:
            return context
        else:
            return render(self.request, template_name='404.html')

    def get_context_data(self, **kwargs):
        context = super(DepartamentosListView, self).get_context_data(**kwargs)
        return context

class DepartamentoCreateView(CreateView):
    model = Departamento
    template_name = 'editForm.html'
    success_url = reverse_lazy('planilla:departamentos')
    fields = [
        'nombre',
        'descripcion',
    ]

class DepartamentoUpdateView(UpdateView):
    model = Departamento
    template_name = 'editForm.html'
    success_url = reverse_lazy('planilla:departamentos')
    fields = [
        'nombre',
        'descripcion',
    ]

class DepartamentoDetailView(DetailView):
    model = Departamento
    template_name = 'planilla/viewDepartamento.html'
    success_url = reverse_lazy('planilla:departamentos')
    fields = [
        'nombre',
        'descripcion',
    ]
    context_object_name = 'departamento'


#Puesto

class PuestosListView(ListView):
    model = Puesto
    template_name = 'planilla/gestionarPuestos.html'
    context_object_name = 'puestos'

    def get_queryset(self): 
        context = Puesto.objects.all()
        if context:
            return context
        else:
            return render(self.request, template_name='404.html')

    def get_context_data(self, **kwargs):
        context = super(PuestosListView, self).get_context_data(**kwargs)
        return context

class PuestoCreateView(CreateView):
    model = Puesto
    template_name = 'editForm.html'
    success_url = reverse_lazy('planilla:puestos')
    fields = [
        'codigo',
        'id_puesto',
        'nombre_funcional',
        'descripcion',
        'salario_base'
    ]

class PuestoUpdateView(UpdateView):
    model = Puesto
    template_name = 'editForm.html'
    success_url = reverse_lazy('planilla:puestos')
    fields = [
        'codigo',
        'id_puesto',
        'nombre_funcional',
        'descripcion',
        'salario_base'
    ]

class PuestoDetailView(DetailView):
    model = Puesto
    template_name = 'planilla/viewPuesto.html'
    success_url = reverse_lazy('planilla:puestos')
    fields = [
        'codigo',
        'id_puesto',
        'nombre_funcional',
        'descripcion',
        'salario_base'
    ]
    context_object_name = 'puesto'


#Empleado

class EmpleadosListView(ListView):
    model = Empleado
    template_name = 'planilla/gestionarEmpleados.html'
    context_object_name = 'empleados'

    def get_queryset(self):
        user = self.request.user
        context = Empleado.objects.all()
        if context:
            return context
        else:
            return render(self.request, template_name='404.html')

    def get_context_data(self, **kwargs):
        context = super(EmpleadosListView, self).get_context_data(**kwargs)
        return context

class EmpleadoCreateView(CreateView):
    model = Empleado
    template_name = 'editForm.html'
    success_url = reverse_lazy('planilla:empleados')
    fields = [
        'id_puesto',
        'dui',
        'primer_nombre',
        'segundo_nombre',
        'primer_apellido',
        'segundo_apellido',
        'fecha_nacimiento',
        'codigo',
        'telefono',
        'direccion',
        'activo',
    ]
 
class EmpleadoUpdateView(UpdateView):
    model = Empleado
    template_name = 'editForm.html'
    success_url = reverse_lazy('planilla:empleados')
    fields = [
        'id_puesto',
        'dui',
        'primer_nombre',
        'segundo_nombre',
        'primer_apellido',
        'segundo_apellido',
        'fecha_nacimiento'
        'codigo',
        'telefono',
        'direccion',
        'activo',
    ]

class EmpleadoDetailView(DetailView):
    model = Empleado
    template_name = 'planilla/viewEmpleado.html'
    success_url = reverse_lazy('planilla:empleados')
    fields = [
        'id_puesto',
        'dui',
        'primer_nombre',
        'segundo_nombre',
        'primer_apellido',
        'segundo_apellido',
        'fecha_nacimiento'
        'codigo',
        'telefono',
        'direccion',
        'activo',
    ]
    context_object_name = 'empleado'
