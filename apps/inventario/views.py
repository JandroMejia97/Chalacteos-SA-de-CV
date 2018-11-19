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

class FacturasListView(LoginRequiredMixin, ListView):
	model = Factura
	template_name = 'inventario/gestionarFacturaVentas.html'
	context_object_name = 'facturas'

	def get_queryset(self):
		user = self.request.user
		context = Factura.objects.all()
		if context:
			return context
		else:
			return render(self.request, template_name='404.html')

	def get_context_data(self, **kwargs):
		context = super(FacturasListView, self).get_context_data(**kwargs)
		return context

class DetallesListView(LoginRequiredMixin, ListView):
	model = Detalle
	template_name = 'inventario/gestionarDetalleVentas.html'
	context_object_name = 'detalles'

	def get_queryset(self):
		user = self.request.user
		context = Detalle.objects.all()
		if context:
			return context
		else:
			return render(self.request, template_name='404.html')

	def get_context_data(self, **kwargs):
		context = super(DetallesListView, self).get_context_data(**kwargs)
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

class FacturaCreateView(LoginRequiredMixin, CreateView):
	model = Factura
	template_name = 'editForm.html'
	success_url = reverse_lazy('inventario:facturas')
	fields = [
		'id_factura',
		'id_venta',
		'sub_total_factura',
		'total_factura',
		'estado_factura'
	]

class DetalleCreateView(LoginRequiredMixin, CreateView):
	model = Detalle
	template_name = 'editForm.html'
	success_url = reverse_lazy('inventario:detalles')
	fields = [
		'id_detalle',
		'id_materia_prima',
		'id_producto',
		'id_factura',
		'cantidad_detalle'
	]

class VentaCreateView(LoginRequiredMixin, CreateView):
	model = Venta
	template_name = 'editForm.html'
	success_url = reverse_lazy('inventario:ventas')
	fields = [
		'id_venta',
		'id_cliente'
	]


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

class FacturaUpdateView(LoginRequiredMixin, UpdateView):
	model = Factura
	template_name = 'editForm.html'
	success_url = reverse_lazy('inventario:facturas')
	fields = [
		'id_factura',
		'id_venta',
		'sub_total_factura',
		'total_factura',
		'estado_factura'
	]

class DetalleUpdateView(LoginRequiredMixin, UpdateView):
	model = Detalle
	template_name = 'editForm.html'
	success_url = reverse_lazy('inventario:detalles')
	fields = [
		'id_detalle',
		'id_materia_prima',
		'id_producto',
		'id_factura',
		'cantidad_detalle'
	]

class VentaUpdateView(LoginRequiredMixin, UpdateView):
	model = Venta
	template_name = 'editForm.html'
	success_url = reverse_lazy('inventario:ventas')
	fields = [
		'id_venta',
		'id_cliente'
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

class FacturaDetailView(LoginRequiredMixin, DetailView):
	model = Factura
	template_name = 'inventario/viewFacturaVenta.html'
	success_url = reverse_lazy('inventario:facturas')
	fields = [
		'id_factura',
		'id_venta',
		'sub_total_factura',
		'total_factura',
		'estado_factura'
	]
	context_object_name = 'factura'

class DetalleDetailView(LoginRequiredMixin, DetailView):
	model = Detalle
	template_name = 'inventario/viewDetalleVenta.html'
	success_url = reverse_lazy('inventario:detalles')
	fields = [
		'id_detalle',
		'id_materia_prima',
		'id_producto',
		'id_factura',
		'cantidad_detalle'
	]
	context_object_name = 'detalle'

class VentaDetailView(LoginRequiredMixin, DetailView):
	model = Venta
	template_name = 'inventario/viewVenta.html'
	success_url = reverse_lazy('inventario:ventas')
	fields = [
		'id_venta',
		'id_cliente'
	]
	context_object_name = 'venta'


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

def facturas(request, id_factura):   
    if request.method == 'DELETE':
        #id_parametro = request.POST['id']
        parametro = Factura.objects.get(id_factura=id_factura)
        parametro.delete()
        message = "El proveedor fue borrado exitosamente"
        return JsonResponse(data={'message': message})

def detalles(request, id_detalle):   
    if request.method == 'DELETE':
        #id_parametro = request.POST['id']
        parametro = Detalle.objects.get(id_detalle=id_detalle)
        parametro.delete()
        message = "El proveedor fue borrado exitosamente"
        return JsonResponse(data={'message': message})

def ventas(request, id_venta):   
    if request.method == 'DELETE':
        #id_parametro = request.POST['id']
        parametro = Venta.objects.get(id_venta=id_venta)
        parametro.delete()
        message = "El proveedor fue borrado exitosamente"
        return JsonResponse(data={'message': message})