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
		context = Cuenta.objects.all()
		if context:
			return context
		else:
			return render(self.request, template_name='404.html')

	def get_context_data(self, **kwargs):
		context = super(CuentasListView, self).get_context_data(**kwargs)
		return context

def cuentas(request):
	cuentas = Cuenta.objects.all()
	return render(request, 'contabilidad/gestionarCuentas.html',{})


class CuentaCreateView(LoginRequiredMixin, CreateView):
	model = Cuenta
	template_name = 'editForm.html'
	success_url = '/cuentas/'
	fields = [
		'id_rubro',
		'nombre_cuenta'
	]
