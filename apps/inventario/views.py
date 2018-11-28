from django.shortcuts import render

from django.views.generic import CreateView, TemplateView 
from django.views.generic.edit import FormView, UpdateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.shortcuts import render, redirect, get_object_or_404
from django.forms.models import model_to_dict
from django.template import loader
from django.urls import reverse_lazy, reverse
from django.http.response import HttpResponse, HttpResponseRedirect, JsonResponse, Http404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone

from .models import *
from .forms import *

import json

# Create your views here.

class ProveedoresListView(LoginRequiredMixin, ListView):
	model = Proveedor
	template_name = 'inventario/gestionarProveedores.html'
	context_object_name = 'proveedores'

	def get_queryset(self):
		user = self.request.user
		context = Proveedor.objects.all()
		if context:
			return context
		else:
			return render(self.request, template_name='404.html')

	def get_context_data(self, **kwargs):
		context = super(ProveedoresListView, self).get_context_data(**kwargs)
		return context

class ClientesListView(LoginRequiredMixin, ListView):
	model = Cliente
	template_name = 'inventario/gestionarClientes.html'
	context_object_name = 'clientes'

	def get_queryset(self):
		user = self.request.user
		context = Cliente.objects.all()
		if context:
			return context
		else:
			return render(self.request, template_name='404.html')

	def get_context_data(self, **kwargs):
		context = super(ClientesListView, self).get_context_data(**kwargs)
		return context

class VentasListView(LoginRequiredMixin, ListView):
	model = Venta
	template_name = 'inventario/gestionarVentas.html'
	context_object_name = 'ventas'

	def get_queryset(self):
		user = self.request.user
		context = Venta.objects.all()
		if context:
			return context
		else:
			return render(self.request, template_name='404.html')

	def get_context_data(self, **kwargs):
		context = super(VentasListView, self).get_context_data(**kwargs)
		return context

class ComprasListView(LoginRequiredMixin, ListView):
	model = Compra
	template_name = 'inventario/gestionarCompras.html'
	context_object_name = 'compras'

	def get_queryset(self):
		user = self.request.user
		context = Compra.objects.all()
		if context:
			return context
		else:
			return render(self.request, template_name='404.html')

	def get_context_data(self, **kwargs):
		context = super(ComprasListView, self).get_context_data(**kwargs)
		return context

class ImpuestosListView(LoginRequiredMixin, ListView):
	model = Impuesto
	template_name = 'inventario/gestionarImpuestos.html'
	context_object_name = 'impuestos'


class MateriasPrimasListView(LoginRequiredMixin, ListView):
	model = MateriaPrima
	template_name = 'inventario/gestionarMateriaPrima.html'
	context_object_name = 'materiales'

	"""def get_queryset(self):
					 = MateriaPrima.objects.all()
					if context:
						return context
					else:
						return render(self.request, template_name='404.html')
			
				def get_context_data(self, **kwargs):
					context = super(MateriasPrimasListView, self).get_context_data(**kwargs)
					return context"""


class ProveedorCreateView(LoginRequiredMixin, CreateView):
	model = Proveedor
	template_name = 'editForm.html'
	success_url = reverse_lazy('inventario:proveedores')
	fields = [
		'id_proveedor',
		'nombre_proveedor',
		'nombre_titular_proveedor'
	]

class ClienteCreateView(LoginRequiredMixin, CreateView):
	model = Cliente
	template_name = 'editForm.html'
	success_url = reverse_lazy('inventario:clientes')
	fields = [
		'id_cliente',
		'nombre_cliente',
		'nombre_titular_cliente'
	]


class DetalleVentaCreateView(LoginRequiredMixin, CreateView):
	model = Detalle
	template_name = 'inventario/chainedVentaForm.html'
	success_url = reverse_lazy('inventario:detalles')
	fields = [
		'id_producto',
		'cantidad_detalle'
	]

class DetalleCompraCreateView(LoginRequiredMixin, CreateView):
	model = Detalle
	template_name = 'inventario/chainedCompraForm.html'
	success_url = reverse_lazy('inventario:detalles')
	fields = [
		'id_materia_prima',
		'cantidad_detalle'
	]

class VentaCreateView(LoginRequiredMixin, TemplateView):
	template_name = 'inventario/chainedVentaForm.html'
	success_url = reverse_lazy('inventario:ventas')

	def get(self, request, *args, **kwargs):
		context = self.get_context_data(**kwargs)
		context['venta_form'] = VentaForm()
		context['detalle_venta_form'] = DetalleVentaForm()
		return self.render_to_response(context)

class CompraCreateView(LoginRequiredMixin, TemplateView):
	template_name = 'inventario/chainedCompraForm.html'
	success_url = reverse_lazy('inventario:compras')

	def get(self, request, *args, **kwargs):
		context = self.get_context_data(**kwargs)
		context['proveedor_form'] = ProveedorForm()
		context['materia_prima_form'] = MateriaPrima()
		context['compra_form'] = CompraForm()
		context['detalle_compra_form'] = DetalleCompraForm()
		return self.render_to_response(context)

class ImpuestoCreateView(LoginRequiredMixin, CreateView):
	model = Impuesto
	template_name = 'editForm.html'
	success_url = reverse_lazy('inventario:impuestos')
	fields = [
		'id_impuesto',
		'nombre_impuesto',
		'descripcion_impuesto',
		'tasa_impuesto'
	]

class MateriaPrimaCreateView(LoginRequiredMixin, TemplateView):
	template_name = 'inventario/chainedMateriaPrimaForm.html'
	success_url = reverse_lazy('inventario:materia-prima')
	
	def get(self, request, *args, **kwargs):
		context = self.get_context_data(**kwargs)
		context['recurso_form'] = RecursoForm()
		context['proveedor_form'] = ProveedorForm()
		return self.render_to_response(context)

	def post(self, request, *args, **kwargs):
		proveedor = request.POST.get('nombre_proveedor')
		nombre = request.POST['nombre_recurso']
		descripcion = request.POST['descripcion_recurso']

		proveedor = Proveedor.objects.get(id_proveedor=proveedor)
		recurso = Recurso.objects.create(
			nombre_recurso=nombre,
			descripcion_recurso=descripcion
		)
		kardex = Kardex.objects.create(
			id_recurso=recurso
		)
		materia = MateriaPrima.objects.create(
			id_recurso=recurso,
			id_proveedor=proveedor
		)
		message = 'La materia prima ha sido registrada'
		"""request_data = json.loads(request.body)
		recurso_form = RecursoForm(
			request.POST.get('recurso_form', {})
		)
		proveedor_form = ProveedorForm(
			request.POST.get('proveedor_form', {})
		)
		response_data = {}

		if recurso_form.is_valid() and proveedor_form.is_valid():
			response_data.update({
				'success_url': self.success_url
			})
			return JsonResponse(response_data)
		
		response_data.update({
			recurso_form.form_name: recurso_form.errors,
			proveedor_form.form_name: proveedor_form.errors,
		})"""
		return redirect(self.success_url)


class ProveedorUpdateView(LoginRequiredMixin, UpdateView):
	model = Proveedor
	template_name = 'editForm.html'
	success_url = reverse_lazy('inventario:proveedores')
	fields = [
		'id_proveedor',
		'nombre_proveedor',
		'nombre_titular_proveedor'
	]

class ClienteUpdateView(LoginRequiredMixin, UpdateView):
	model = Cliente
	template_name = 'editForm.html'
	success_url = reverse_lazy('inventario:clientes')
	fields = [
		'id_cliente',
		'nombre_cliente',
		'nombre_titular_cliente'
	]

class ImpuestoUpdateView(LoginRequiredMixin, UpdateView):
	model = Impuesto
	template_name = 'editForm.html'
	success_url = reverse_lazy('inventario:impuestos')
	fields = [
		'id_impuesto',
		'nombre_impuesto',
		'descripcion_impuesto',
		'tasa_impuesto'
	]

class MateriaPrimaUpdateView(LoginRequiredMixin, UpdateView):
	model = Impuesto
	template_name = 'editForm.html'
	success_url = reverse_lazy('inventario:materia_prima')
	fields = [
		'id_materia_prima',
		'id_producto',
		'id_recurso',
		'id_proveedor'
	]


class ProveedorDetailView(LoginRequiredMixin, DetailView):
	model = Proveedor
	template_name = 'inventario/viewProveedor.html'
	success_url = reverse_lazy('inventario:proveedores')
	fields = [
		'id_proveedor',
		'nombre_proveedor',
		'nombre_titular_proveedor'
	]
	context_object_name = 'proveedor'

class ClienteDetailView(LoginRequiredMixin, DetailView):
	model = Cliente
	template_name = 'inventario/viewCliente.html'
	success_url = reverse_lazy('inventario:clientes')
	fields = [
		'id_cliente',
		'nombre_cliente',
		'nombre_titular_cliente'
	]
	context_object_name = 'cliente'

class ImpuestoDetailView(LoginRequiredMixin, DetailView):
	model = Impuesto
	template_name = 'inventario/viewImpuesto.html'
	success_url = reverse_lazy('inventario:impuestos')
	fields = [
		'id_impuesto',
		'nombre_impuesto',
		'descripcion_impuesto',
		'tasa_impuesto'
	]
	context_object_name = 'impuesto'

class MateriaPrimaDetailView(LoginRequiredMixin, DetailView):
	model = Impuesto
	template_name = 'inventario/viewMateriaPrima.html'
	success_url = reverse_lazy('inventario:materia_prima')
	fields = [
		'id_materia_prima',
		'id_producto',
		'id_recurso',
		'id_proveedor'
	]
	context_object_name = 'materia_prima'


def proveedores(request, id_proveedor):   
    if request.method == 'DELETE':
        #id_parametro = request.POST['id']
        parametro = Proveedor.objects.get(id_proveedor=id_proveedor)
        parametro.delete()
        message = "El proveedor fue borrado exitosamente"
        return JsonResponse(data={'message': message})

def clientes(request, id_cliente):   
    if request.method == 'DELETE':
        #id_parametro = request.POST['id']
        parametro = Cliente.objects.get(id_cliente=id_cliente)
        parametro.delete()
        message = "El proveedor fue borrado exitosamente"
        return JsonResponse(data={'message': message})

def impuestos(request, id_impuesto):   
    if request.method == 'DELETE':
        #id_parametro = request.POST['id']
        parametro = Impuesto.objects.get(id_impuesto=id_impuesto)
        parametro.delete()
        message = "El proveedor fue borrado exitosamente"
        return JsonResponse(data={'message': message})

		
def load_materia(request):
	if request.method == 'GET':
		id_proveedor = request.GET['id_proveedor']
		materiales = MateriaPrima.objects.all().filter(id_proveedor=id_proveedor).values()
		if materias:
			data = {
				'message': "Datos recuperados",
				'materiales': list(materiales)
			}
		else:
			data = {
				'message': "La materia seleccionada no posee datos"
			}
		return JsonResponse(data=data)
