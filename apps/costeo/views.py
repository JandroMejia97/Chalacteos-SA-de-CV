from django.shortcuts import render

from django.views.generic import CreateView, TemplateView 
from django.views.generic.list import ListView
from django.shortcuts import render, redirect, get_object_or_404
from django.forms.models import model_to_dict
from django.template import loader
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import *
from .forms import *
from apps.planilla import views as planilla
from apps.contabilidad import views as conta

class OrdenCreateView(LoginRequiredMixin, TemplateView):
	template_name = 'costeo/chainedOrdenForm.html'
	success_url = reverse_lazy('costeo:orden')
	
	def get(self, request, *args, **kwargs):
		context = self.get_context_data(**kwargs)
		empresa = conta.Empresa.objects.get(id_empresa=1)
		departamento = planilla.departamento.objects.get(id_departamento=empresa.id_departamento)
		
		

class BoletaCreateView(LoginRequiredMixin, TemplateView):
	template_name = 'costeo/chainedBoletaTrabajoForm.html'
	success_url = reverse_lazy('costeo:boleta')

	def get_context_data(self, **kwargs):
		context = super(BoletaCreateView,self).get_context_data(**kwargs)
		empresa = conta.Empresa.objects.get(id_empresa=1)
		if 'empresa_form' not in context:
			context['empresa_form'] = planilla.EmpresaForm(instance=empresa)
		context['id_empresa'] = empresa
		return context

	def get(self, request, *args, **kwargs):
		context = self.get_context_data(**kwargs)
		context['boleta_form'] = BoletaTrabajoForm()
		context['departamento_form'] = planilla.DepartamentoForm()
		return self.render_to_response(context)

	def post():
		pass


class RequisicionCreateView(LoginRequiredMixin, TemplateView):
	template_name = 'costeo/chainedRequisionMPForm.html'
	success_url = reverse_lazy('costeo:orden')

	def get_context_data(self, **kwargs):
		context = super(BoletaCreateView,self).get_context_data(**kwargs)
		empresa = conta.Empresa.objects.get(id_empresa=1)
		if 'empresa_form' not in context:
			context['empresa_form'] = planilla.EmpresaForm(instance=empresa)
		context['id_empresa'] = empresa
		return context

	def get(self, request, *args, **kwargs):
		context = self.get_context_data(**kwargs)
		context['requisicion_form'] = RequisicionForm()
		context['departamento_form'] = planilla.DepartamentoForm()
		return self.render_to_response(context)
