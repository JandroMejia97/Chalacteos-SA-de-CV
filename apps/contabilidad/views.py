from django.views.generic import CreateView, TemplateView 
from django.views.generic.edit import FormView, UpdateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.shortcuts import render, redirect, get_object_or_404
from django.forms.models import model_to_dict
from django.template import loader
from django.urls import reverse_lazy, reverse
from django.http.response import HttpResponse, HttpResponseRedirect, JsonResponse, Http404
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.utils import timezone

from .models import *

import csv

class SignInView(LoginView):
    template_name = 'iniciarSesion.html'


class SignOutView(LoginRequiredMixin, LogoutView):
    template_name = 'iniciarSesion.html'


class CuentasListView(LoginRequiredMixin, ListView):
	model = Cuenta
	template_name = 'contabilidad/gestionarCuentas.html'
	context_object_name = 'cuentas'

	def get_queryset(self):
		user = self.request.user
		context = Cuenta.objects.all().filter(is_alta=True)
		if context:
			return context
		else:
			return render(self.request, template_name='404.html')

	def get_context_data(self, **kwargs):
		context = super(CuentasListView, self).get_context_data(**kwargs)
		return context


class CuentaCreateView(LoginRequiredMixin, CreateView):
	model = Cuenta
	template_name = 'editForm.html'
	success_url = reverse_lazy('contabilidad:cuentas')
	fields = [
		'id_rubro',
		'codigo_cuenta',
		'nombre_cuenta',
		'is_cuenta_acreedora'
	]


class CuentaUpdateView(LoginRequiredMixin, UpdateView):
	model = Cuenta
	template_name = 'editForm.html'
	success_url = reverse_lazy('contabilidad:cuentas')
	fields = [
		'id_rubro',
		'codigo_cuenta',
		'nombre_cuenta',
		'is_cuenta_acreedora'
	]


class PerfilUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'editForm.html'
    success_url = '/'
    fields = [
        'username',
        'first_name',
        'last_name',
        'email',
        'date_joined'
    ]


class CuentaDetailView(LoginRequiredMixin, DetailView):
	model = Cuenta
	template_name = 'contabilidad/viewCuenta.html'
	success_url = reverse_lazy('contabilidad:cuentas')
	fields = [
		'id_rubro',
		'codigo_cuenta',
		'nombre_cuenta',
		'is_cuenta_acreedora'
	]
	context_object_name = 'cuenta'


class PerfilDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'viewPerfil.html'
    fields = [
        'username',
        'first_name',
        'last_name',
        'email',
        'date_joined',
        'last_login'
    ]
    context_object_name = 'user'

@login_required(login_url='/sign-in/')
def cuentas(request, id_cuenta):   
    if request.method == 'DELETE':
        parametro = Cuenta.objects.get(id_cuenta=id_cuenta)
        parametro.is_alta = False
        parametro.save()
        message = "La cuenta fue borrada exitosamente"
        return JsonResponse(data={'message': message})

@login_required()
def registrar_transaccion(request):
	if request.method == 'GET':
		clean = None

def import_data_rubro(request):
	f = 'C:\\rubros.csv'
	with open(f) as file:
		reader = csv.reader(file)
		for new in reader:
			type(new[0])
			row = new[0].split(";")
			if row[0] != "id_rubro":
				codigo_rubro=int(row[1])
				nombre_rubro=row[2]
				id_catalogo=Catalogo.objects.get(id_catalogo=int(row[3]))
				if row[4] == '':
					rubro_sup=None
				else:
					rubro_sup=Rubro.objects.get(id_rubro=row[4])
				nivel=int(row[5])
				created = Rubro.objects.create(
					codigo_rubro=codigo_rubro,
					nombre_rubro=nombre_rubro,
					id_catalogo=id_catalogo,
					rubro_sup=rubro_sup,
					nivel=nivel
				)
	return HttpResponse('Hecho')

def import_data_cuenta(request):
	f = 'C:\\cuentas.csv'
	with open(f) as file:
		reader = csv.reader(file)
		for new in reader:
			type(new[0])
			row = new[0].split(";")
			if row[0] != "id_cuenta":
				codigo_cuenta=int(row[1])
				nombre_cuenta=row[2]
				is_cuenta_acreedora=bool(row[3])
				is_alta=bool(row[4])
				if row[5] == '' or row[5] == None:
					id_rubro = None
				else:
					id_rubro = Rubro.objects.get(id_rubro=int(row[5]))
				if row[6] == '' or row[6] == None:
					codigo_cuenta_padre = None
				else:
					codigo_cuenta_padre = Cuenta.objects.get(id_cuenta=int(row[6]))
				created = Cuenta.objects.create(
					codigo_cuenta=codigo_cuenta,
					nombre_cuenta=nombre_cuenta,
					is_cuenta_acreedora=is_cuenta_acreedora,
					is_alta=is_alta,
					id_rubro=id_rubro,
					codigo_cuenta_padre=codigo_cuenta_padre
				)
	return HttpResponse('Hecho')