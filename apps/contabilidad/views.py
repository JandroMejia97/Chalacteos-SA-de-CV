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
