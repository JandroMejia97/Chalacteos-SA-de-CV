from django.shortcuts import render

from django.views.generic import CreateView, TemplateView, View
from django.views.generic.edit import FormView, UpdateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.forms.models import model_to_dict
from django.template import loader
from django.urls import reverse_lazy, reverse
from django.http.response import HttpResponse, HttpResponseRedirect, JsonResponse, Http404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from .models import *
from .forms import *
from apps.contabilidad import views as conta

import json
import csv
import datetime


class DepartamentosListView(ListView):
    model = Departamento
    template_name = 'planilla/gestionarDepartamentos.html'
    context_object_name = 'departamentos'


class PuestosListView(ListView):
    model = Puesto
    template_name = 'planilla/gestionarPuestos.html'
    context_object_name = 'puestos'


class EmpleadosListView(ListView):
    model = Empleado
    template_name = 'planilla/gestionarEmpleados.html'
    context_object_name = 'empleados'


class DepartamentoCreateView(CreateView):
    model = Departamento
    template_name = 'editForm.html'
    success_url = reverse_lazy('planilla:departamentos')
    fields = [
        'nombre',
        'descripcion',
    ]


class PuestoCreateView(CreateView):
    model = Puesto
    template_name = 'editForm.html'
    success_url = reverse_lazy('planilla:puestos')
    fields = [
        'departamento',
        'codigo_puesto',
        'nombre_funcional',
        'descripcion',
        'salario_base'
    ]


class EmpleadoCreateView(View):
    
    def get(self, request):
        user_form = UserCreationForm(instance=request.user)
        empleado_form = EmpleadoForm(instance=request.user.empleado)
        return render(
            request,
            'editEmpleado.html',
            context={
                'user_form': user_form,
                'empleado_form': empleado_form
            }
        )
    
    def post(self, request):
        user_form = UserCreationForm(request.POST, instance=request.user)
        empleado_form = EmpleadoForm(request.POST, instance=request.user.empleado)
        if user_form.is_valid() and empleado_form.is_valid():
            user_form.save()
            empleado_form.save()
            messages.success(request, 'El empleado fue modificado exitosamente')
            return redirect('planilla:empleados')
        messages.error(request, 'Por favor corrija los siguientes errores')


class DepartamentoUpdateView(UpdateView):
    model = Departamento
    template_name = 'editForm.html'
    success_url = reverse_lazy('planilla:departamentos')
    fields = [
        'nombre',
        'descripcion',
    ]


class PuestoUpdateView(UpdateView):
    model = Puesto
    template_name = 'editForm.html'
    success_url = reverse_lazy('planilla:puestos')
    fields = [
        'departamento',
        'codigo_puesto',
        'nombre_funcional',
        'descripcion',
        'salario_base'
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


class DepartamentoDetailView(DetailView):
    model = Departamento
    template_name = 'planilla/viewDepartamento.html'
    success_url = reverse_lazy('planilla:departamentos')
    fields = [
        'nombre',
        'descripcion',
    ]
    context_object_name = 'departamento'


class PuestoDetailView(DetailView):
    model = Puesto
    template_name = 'planilla/viewPuesto.html'
    success_url = reverse_lazy('planilla:puestos')
    fields = [
        'departamento',
        'codigo_puesto',
        'nombre_funcional',
        'descripcion',
        'salario_base'
    ]
    context_object_name = 'puesto'


class EmpleadoDetailView(DetailView):
    model = Empleado
    template_name = 'planilla/viewEmpleado.html'
    success_url = reverse_lazy('planilla:empleados')
    fields = [
        'puesto',
        'dui',
        'user',
        'fecha_nacimiento',
        'telefono',
        'direccion',
        'is_active',
    ]
    context_object_name = 'empleado'
