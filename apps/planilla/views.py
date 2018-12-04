from django.shortcuts import render

from django.views.generic import CreateView, TemplateView, View
from django.views.generic.edit import FormView, UpdateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.shortcuts import render, redirect, get_object_or_404
from django.forms.models import model_to_dict
from django.template import loader
from django.urls import reverse_lazy, reverse
from django.http.response import HttpResponse, HttpResponseRedirect, JsonResponse, Http404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from .models import *
from .forms import *
from apps.contabilidad import views as conta

import json
import csv
import datetime


class DepartamentosListView(ListView, LoginRequiredMixin):
	model = Departamento
	template_name = 'planilla/gestionarDepartamentos.html'
	context_object_name = 'departamentos'


class PuestosListView(ListView, LoginRequiredMixin):
	model = Puesto
	template_name = 'planilla/gestionarPuestos.html'
	context_object_name = 'puestos'


class EmpleadosListView(ListView, LoginRequiredMixin):
	model = Empleado
	template_name = 'planilla/gestionarEmpleados.html'
	context_object_name = 'empleados'

	def get_queryset(self):
		context = Empleado.objects.all().filter(is_active = True)
		if context:
			return context
		else:
			return render(self.request, template_name = '404.html')


class DepartamentoCreateView(CreateView, LoginRequiredMixin):
	model = Departamento
	template_name = 'editForm.html'
	success_url = reverse_lazy('planilla:departamentos')
	fields = [
		'nombre',
		'descripcion',
	]


class PuestoCreateView(CreateView, LoginRequiredMixin):
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


class EmpleadoCreateView(View, LoginRequiredMixin):
	
	def get(self, request):
		user_form = UserForm(instance = request.user)
		empleado_form = EmpleadoForm(instance = request.user.empleado)
		return render(
			request,
			'planilla/editEmpleado.html',
			context = {
				'user_form': user_form,
				'empleado_form': empleado_form
			}
		)
	
	def post(self, request):
		user_form = UserForm(request.POST, instance = request.user)
		empleado_form = EmpleadoForm(request.POST, instance = request.user.empleado)
		if user_form.is_valid() and empleado_form.is_valid():
			user_form.save()
			empleado_form.save()
			messages.success(request, 'El empleado fue modificado exitosamente')
			return redirect('planilla:empleados')
		messages.error(request, 'Por favor corrija los siguientes errores')


class DepartamentoUpdateView(UpdateView, LoginRequiredMixin):
	model = Departamento
	template_name = 'editForm.html'
	success_url = reverse_lazy('planilla:departamentos')
	fields = [
		'nombre',
		'descripcion',
	]


class PuestoUpdateView(UpdateView, LoginRequiredMixin):
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


class EmpleadoUpdateView(UpdateView, LoginRequiredMixin):
	model = Empleado
	template_name = 'editForm.html'
	success_url = reverse_lazy('planilla:empleados')
	fields = [
		'puesto',
		'dui',
		'fecha_nacimiento',
		'telefono',
		'direccion',
		'is_active',
	]


class DepartamentoDetailView(DetailView, LoginRequiredMixin):
	model = Departamento
	template_name = 'planilla/viewDepartamento.html'
	success_url = reverse_lazy('planilla:departamentos')
	fields = [
		'nombre',
		'descripcion',
	]
	context_object_name = 'departamento'


class PuestoDetailView(DetailView, LoginRequiredMixin):
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


class EmpleadoDetailView(DetailView, LoginRequiredMixin):
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

@login_required(login_url = '/sign-in/')
def departamentos(request, id_departamento):   
	if request.method == 'DELETE':
		parametro = Departamento.objects.get(id_departamento = id_departamento)
		parametro.delete()
		message = "El departamento fue borrado exitosamente"
		return JsonResponse(data = {'message': message})

@login_required(login_url = '/sign-in/')
def puestos(request, id_puesto):   
	if request.method == 'DELETE':
		parametro = Puesto.objects.get(id_puesto = id_puesto)
		parametro.delete()
		message = "El puesto fue borrado exitosamente"
		return JsonResponse(data = {'message': message})

@login_required(login_url = '/sign-in/')
def empleados(request, id):   
	if request.method == 'DELETE':
		parametro = Empleado.objects.get(id = id)
		parametro.is_active = False
		message = "El empleado fue borrado exitosamente"
		return JsonResponse(data = {'message': message})

@login_required(login_url = '/sign-in/')
def import_data_departamento(request):
	f = 'C:\\departamentos.csv'
	with open(f) as file:
		reader = csv.reader(file)
		for new in reader:
			row = new[0].split(";")
			empresa = Empresa.objects.get(id_empresa=new[1])
			nombre = new[2]
			descripcion = new[3]
			objeto, created = Departamento.objects.update_or_create(
				empresa = empresa,
				nombre = nombre,
				descripcion = descripcion
			)
	return HttpResponse('Hecho')

@login_required(login_url = '/sign-in/')
def import_data_puesto(request):
	f = 'C:\\puestos.csv'
	with open(f) as file:
		reader = csv.reader(file)
		for new in reader:
			row = new[0].split(";")
			departamento = Departamento.objects.get(id_departamento=new[1])
			codigo_puesto = new[2]
			nombre_funcional = new[3]
			descripcion = new[4]
			salario_base = float(new[8])
			objeto, created = Puesto.objects.update_or_create(
				departamento = departamento,
				codigo_puesto = codigo_puesto,
				nombre_funcional = nombre_funcional,
				descripcion = descripcion,
				salario_base = salario_base,
			)
	return HttpResponse('Hecho')
 
@login_required(login_url = '/sign-in/')
def import_data_empleado(request):
	f = 'C:\\empleados.csv'
	with open(f) as file:
		count = 3
		reader = csv.reader(file)
		for new in reader:
			row = new[0].split(";")
			empleado = User.objects.get(id=count)
			puesto = Puesto.objetcs.get(id_puesto=new[1])
			dui = new[2]
			fecha_nacimiento = new[3]
			telefono = new[4]
			direccion = new[5]
			is_active = new[6]
			objeto, created = Empleado.objects.update_or_create(
				empleado=empleado,
				puesto=puesto,
				dui=dui,
				fecha_nacimiento = fecha_nacimiento,
				telefono = telefono,
				direccion = direccion,
				is_active = is_active,
			)
			count+=1
	return HttpResponse('Hecho') 

@login_required(login_url = '/sign-in/')
def import_data_usuario(request):
	f = 'C:\\usuarios.csv'
	with open(f) as file:
		reader = csv.reader(file)
		for new in reader:
			row = new[0].split(";")
			nombres = new[0]
			apellidos = new[1]
			correo = new[2]
			objeto, created = User.objects.update_or_create(
				username=new[0].split(";")[0],
				first_name = nombres,
				last_name = apellidos,
				email = correo
			)
	return HttpResponse('Hecho') 
