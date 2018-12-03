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
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from .models import *
from .forms import *
from apps.contabilidad import views as conta

import json
import csv

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

	def get_context_data(self, **kwargs):
		context = super(VentaCreateView,self).get_context_data(**kwargs)
		producto= Producto.objects.get(id_producto=1)
		recurso = Recurso.objects.get(nombre_recurso=producto.id_recurso)
		kardex = Kardex.objects.get(id_recurso=recurso.id_recurso)
		movimiento = Movimiento.objects.get(id_kardex=kardex.id_kardex)

		if 'producto_form' not in context:
			context['producto_form'] = RecursoProductoForm(instance=recurso)
		if 'movimiento_form' not in context:
			context['movimiento_form'] = MovimientoForm(instance=movimiento)
		context['id_producto'] = producto
		return context

	def get(self, request, *args, **kwargs):
		context = self.get_context_data(**kwargs)
		context['venta_form'] = ClienteVentaForm()
		context['detalle_venta_form'] = DetalleVentaForm()
		context['impuesto'] = Impuesto.objects.get(nombre_impuesto='IVA')
		return self.render_to_response(context)

	def post(self, request, *args, **kwargs):
		sub_total_venta = float(request.POST['totalVenta'])
		total_data =  request.POST['totalFila']
		cliente_data = request.POST['cliente']
		producto_data = request.POST['producto']
		cantidad_data = request.POST['cantidad']

		impuesto = Impuesto.objects.get(nombre_impuesto='IVA')
		iva_v = sub_total_venta*float(impuesto.tasa_impuesto)
		total = iva_v + sub_total_venta

		data = {}
		data['tipo'] = 'VENTA'
		data['total'] = total

		if(request.POST.get('isCredito')):
			is_credito = request.POST['isCredito']
			if is_credito:
				data['venta'] = 'CREDITO'
				transaccion = conta.registrar_transaccion(data)
				factura = Factura.objects.create(
					sub_total_factura=sub_total_venta,
					total_factura=total,
					monto_aplicacion=iva_v,
					is_credito=True,
					is_contado=False
				)
			else:
				data['venta'] = 'CONTADO'
				transaccion = conta.registrar_transaccion(data)
				factura = Factura.objects.create(
					sub_total_factura=sub_total_venta,
					total_factura=total,
					monto_aplicacion=iva_v,
					is_credito=False,
					is_contado=True
				)
		else:
			data['proporcion'] = float(request.POST['proporcion'])
			data['venta'] = 'PROPORCION'
			transaccion = conta.registrar_transaccion(data)
			factura = Factura.objects.create(
				sub_total_factura=sub_total_venta,
				total_factura=total,
				monto_aplicacion=iva_v,
				is_credito=True,
				is_contado=True,
				proporcion=data['proporcion'],
				transaccion=transaccion
			)
		cliente = Cliente.objects.get(nombre_cliente=cliente_data)
		venta = Venta.objects.create(
			id_cliente=cliente,
			id_factura=factura
		)

		producto = Producto.objects.get(id_producto=1)
		recurso = Recurso.objects.get(id_recurso=producto.id_recurso.id_recurso)
		kardex = Kardex.objects.get(id_recurso=recurso.id_recurso)
		total_data=float(total_data)
		cantidad_data=int(cantidad_data)
		movimiento = Movimiento.objects.create(
			id_kardex=kardex,
			cantidad_movimiento=cantidad_data,
			costo_unitario_movimiento=total_data/cantidad_data,
			monto_movimiento=total_data,
			is_Input=False,
		)
		movimiento.save()
		
		message = 'La venta ha sido registrada'
		return JsonResponse(data={'message': message, 'success_url': self.success_url})

class CompraCreateView(LoginRequiredMixin, TemplateView):
	template_name = 'inventario/chainedCompraForm.html'
	success_url = reverse_lazy('inventario:compras')

	def get(self, request, *args, **kwargs):
		context = self.get_context_data(**kwargs)
		context['compra_form'] = ProveedorCompraForm()
		context['detalle_compra_form'] = DetalleCompraForm()
		context['impuesto'] = Impuesto.objects.get(nombre_impuesto='IVA')
		return self.render_to_response(context)

	def post(self, request, *args, **kwargs):
		sub_total_compra = float(request.POST['totalCompra'])
		totales_data =  request.POST['totales'].split(',')
		proveedores_data = request.POST['proveedores'].split(',')
		materiales_data = request.POST['materiales'].split(',')
		cantidades_data = request.POST['cantidades'].split(',')

		impuesto = Impuesto.objects.get(nombre_impuesto='IVA')
		iva = sub_total_compra*float(impuesto.tasa_impuesto)
		total = iva + sub_total_compra

		data = {}
		data['tipo'] = 'COMPRA'
		data['total'] = total
		
		if(request.POST.get('isCredito')):
			is_credito = request.POST['isCredito']
			if is_credito:
				data['compra'] = 'CREDITO'
				transaccion = conta.registrar_transaccion(data)
				factura = Factura.objects.create(
					sub_total_factura=sub_total_compra,
					total_factura=total,
					monto_aplicacion=iva,
					is_credito=True,
					is_contado=False,
					transaccion=transaccion
				)
			else:
				data['compra'] = 'CONTADO'
				transaccion = conta.registrar_transaccion(data)
				factura = Factura.objects.create(
					sub_total_factura=sub_total_compra,
					total_factura=total,
					monto_aplicacion=iva,
					is_credito=False,
					is_contado=True,
					transaccion=transaccion
				)
		else:
			data['proporcion'] = float(request.POST['proporcion'])
			data['compra'] = 'PROPORCION'
			transaccion = conta.registrar_transaccion(data)

			factura = Factura.objects.create(
				sub_total_factura=sub_total_compra,
				total_factura=total,
				monto_aplicacion=iva,
				is_credito=True,
				is_contado=True,
				proporcion=data['proporcion'],
				transaccion=transaccion
			)

		compra = Compra.objects.create(
			id_factura=factura
		)

		for i in range(0, len(proveedores_data)-1):
			materia_prima = MateriaPrima.objects.get(id_materia_prima=materiales_data[i])
			recurso = Recurso.objects.get(id_recurso=materia_prima.id_recurso.id_recurso)
			kardex = Kardex.objects.get(id_recurso=recurso.id_recurso)
			totales_data[i]=float(totales_data[i])
			cantidades_data[i]=int(cantidades_data[i])
			movimiento = Movimiento.objects.create(
				id_kardex=kardex,
				cantidad_movimiento=cantidades_data[i],
				costo_unitario_movimiento=totales_data[i]/cantidades_data[i],
				monto_movimiento=totales_data[i],
				is_Input=True,
			)
			movimiento.save()
			movimiento.cantidad_saldo = get_existencias(kardex)
			movimiento.monto_saldo = get_monto(kardex)
			movimiento.costo_unitario_saldo = get_costo(kardex)
			movimiento.save()

			if not compra.id_proveedor.filter(id_proveedor=proveedores_data[i]):
				compra.id_proveedor.add(proveedores_data[i])
		message = 'La compra ha sido registrada'
		return JsonResponse(data={'message': message, 'success_url': self.success_url})
		
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

class MateriaPrimaUpdateView(LoginRequiredMixin, TemplateView):
	template_name = 'inventario/chainedMateriaPrimaForm.html'
	success_url = reverse_lazy('inventario:materia-prima')
	
	def get_context_data(self, **kwargs):
		context = super(MateriaPrimaUpdateView,self).get_context_data(**kwargs)
		pk = self.kwargs.get('pk', 0)
		materia_prima = MateriaPrima.objects.get(id_materia_prima=pk)
		proveedor = Proveedor.objects.get(nombre_proveedor=materia_prima.id_proveedor)
		recurso = Recurso.objects.get(id_recurso=materia_prima.id_recurso.id_recurso)
		if 'proveedor_form' not in context:
			context['proveedor_form'] = ProveedorForm(instance=proveedor)
		if 'recurso_form' not in context:
			context['recurso_form'] = RecursoForm(instance=recurso)
		context['id_materia_prima'] = pk
		return context

	def post(self, request, *args, **kwargs):
		id_materia_prima = kwargs['pk']
		materia_prima = MateriaPrima.objects.get(id_materia_prima=id_materia_prima)
		proveedor = Proveedor.objects.get(nombre_proveedor=materia_prima.id_proveedor)
		recurso = Recurso.objects.get(nombre_recurso=materia_prima.id_recurso)
		proveedor_form = ProveedorForm(request.POST, instance=proveedor)
		recurso_form = RecursoForm(request.POST, instance=recurso)

		if proveedor_form.is_valid() and recurso_form.is_valid():
			proveedor_form.save()
			recurso_form.save()
			return redirect(self.success_url)
		else:
			return redirect(self.success_url)


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
	model = MateriaPrima
	template_name = 'inventario/viewMateriaPrima.html'
	success_url = reverse_lazy('inventario:materia_prima')
	fields = [
		'nombre_proveedor',
		'nombre_recurso',
		'descripcion_recurso',
		'unidad_medida'
	]
	context_object_name = 'materia_prima'

class RecursoDetailView(LoginRequiredMixin, DetailView):
	model = Kardex
	template_name = 'inventario/viewKardex.html'
	success_url = reverse_lazy('inventario:kardex')
	fields = [
		'nombre_proveedor',
		'nombre_recurso',
		'descripcion_recurso',
		'unidad_medida'
	]

@login_required(login_url='/sign-in/')
def proveedores(request, id_proveedor):   
    if request.method == 'DELETE':
        parametro = Proveedor.objects.get(id_proveedor=id_proveedor)
        parametro.delete()
        message = "El proveedor fue borrado exitosamente"
        return JsonResponse(data={'message': message})

@login_required(login_url='/sign-in/')
def clientes(request, id_cliente):   
    if request.method == 'DELETE':
        parametro = Cliente.objects.get(id_cliente=id_cliente)
        parametro.delete()
        message = "El cliente fue borrado exitosamente"
        return JsonResponse(data={'message': message})

@login_required(login_url='/sign-in/')
def impuestos(request, id_impuesto):   
    if request.method == 'DELETE':
        parametro = Impuesto.objects.get(id_impuesto=id_impuesto)
        parametro.delete()
        message = "El proveedor fue borrado exitosamente"
        return JsonResponse(data={'message': message})

@login_required(login_url='/sign-in/')
def materiales(request, id_materia_prima):   
    if request.method == 'DELETE':
        parametro = MateriaPrima.objects.get(id_materia_prima=id_materia_prima)
        parametro.delete()
        message = "La materia prima fue borrada exitosamente"
        return JsonResponse(data={'message': message})

@login_required(login_url='/sign-in/')		
def load_materia(request):
	if request.method == 'GET':
		id_proveedor = request.GET['id_proveedor']
		materiales = MateriaPrima.objects.filter(id_proveedor=id_proveedor)
		recursos = ""
		ident = ""
		for material in materiales:
			result = Recurso.objects.get(id_recurso=material.id_recurso.id_recurso)
			ident += str(result.id_recurso)+"-"
			recursos += str(result.nombre_recurso)+"-"

		materiales = materiales.values()

		if recursos:
			data = {
				'message': 'Datos recuperados',
				'identificador': ident,
				'nombres': recursos
			}
		else:
			data = {
				'message': "No se le han registrado materias primas al proveedor seleccionado"
			}
		return JsonResponse(data=data)

@login_required(login_url='/sign-in/')
def get_movimientos(request, id_kardex):
	movimientos = Movimiento.objects.filter(id_kardex=id_kardex).order_by('fecha_movimiento')
	if movimientos:
		kardex = Kardex.objects.get(id_kardex=id_kardex)
		return render(request, template_name='inventario/viewKardex.html', context={'movimientos': movimientos, 'kardex': kardex})
	else:
		return render(request, template_name='404.html')

def get_existencias(id_kardex):
    entradas = Movimiento.objects.filter(id_kardex=id_kardex).filter(is_Input=True).aggregate(total_entradas=models.Sum('cantidad_movimiento'))
    if entradas['total_entradas'] == None:
        entradas['total_entradas'] = 0
    salidas = Movimiento.objects.filter(id_kardex=id_kardex).filter(is_Input=False).aggregate(total_salidas=models.Sum('cantidad_movimiento'))
    if salidas['total_salidas'] == None:
        salidas['total_salidas'] = 0
    return float(entradas['total_entradas'])-float(salidas['total_salidas'])

def get_monto(id_kardex):
    monto_entradas = Movimiento.objects.filter(id_kardex=id_kardex).filter(is_Input=True).aggregate(total_monto=models.Sum('monto_movimiento'))
    if monto_entradas['total_monto'] == None:
        monto_entradas['total_monto'] = 0
    monto_salidas = Movimiento.objects.filter(id_kardex=id_kardex).filter(is_Input=False).aggregate(total_monto=models.Sum('monto_movimiento'))
    if monto_salidas['total_monto'] == None:
        monto_salidas['total_monto'] = 0
    return float(monto_entradas['total_monto'])-float(monto_salidas['total_monto'])

def get_costo(id_kardex):
	if get_monto(id_kardex) == 0 or get_existencias(id_kardex) == 0:
		costo = 0
	else:
		costo = get_monto(id_kardex)/get_existencias(id_kardex)
    
	return float(costo)

def get_costo_unitario_venta(request, id):
	producto= Producto.objects.filter(id_producto=id)
	recurso = Recurso.objects.get(nombre_recurso=producto.id_recurso)
	kardex = Kardex.objects.get(id_recurso=recurso.id_recurso)
	movimiento = Movimiento.objects.get(id_kardex=kardex.id_kardex)

	if 'producto_form' not in context:
		context['producto_form'] = RecursoProductoForm(instance=recurso)
	if 'movimiento_form' not in context:
		context['movimiento_form'] = MovimientoForm(instance=movimiento)
	context['id_producto'] = producto
	return context

def import_data_proveedor(request):
	f = 'C:\\proveedores.csv'
	with open(f) as file:
		reader = csv.reader(file)
		for new in reader:
			row=new[0].split(";")
			if row[0] != "id_proveedor":
				nombre_proveedor=new[1]
				nombre_titular_proveedor=new[2]
				objeto, created = Proveedor.objects.update_or_create(
					nombre_proveedor=nombre_proveedor,
					nombre_titular_proveedor=nombre_titular_proveedor
				)
	return HttpResponse('Hecho')

def import_data_recursos(request):
	f = 'C:\\recursos.csv'
	with open(f) as file:
		reader = csv.reader(file)
		for new in reader:
			row=new[0].split(";")
			if row[0] != "id_recurso":
				nombre_recurso = new[1]
				descripcion_recurso = new[2]
				unidad_medida = new[3]
				objecto, created = Recurso.objects.update_or_create(
					nombre_recurso=nombre_recurso,
					descripcion_recurso=descripcion_recurso,
					unidad_medida=unidad_medida
				)
	return HttpResponse('Hecho')

def import_data_cliente(request):
	f = 'C:\\clientes.csv'
	with open(f) as file:
		reader = csv.reader(file)
		for new in reader:
			row=new[0].split(";")
			if row[0] != "id_cliente":
				nombre_cliente=new[1]
				nombre_titular_cliente=new[2]
				objeto, created = Cliente.objects.update_or_create(
					nombre_cliente=nombre_cliente,
					nombre_titular_cliente=nombre_titular_cliente
				)
	return HttpResponse('Hecho')

def import_data_materia(request):
	f = 'C:\\materia_prima.csv'
	with open(f) as file:
		reader = csv.reader(file)
		for new in reader:
			row=new[0].split(";")
			if row[0] != "id_materia_prima":
				id_proveedor = new[1]
				id_recurso = new[2]
				proveedor = Proveedor.objects.get(id_proveedor=id_proveedor)
				recurso = Recurso.objects.get(id_recurso=id_recurso)
				objecto, created = MateriaPrima.objects.update_or_create(
					id_proveedor=proveedor,
					id_recurso=recurso
				)
	return HttpResponse('Hecho')

def import_data_impuesto(request):
	f = 'C:\\impuestos.csv'
	with open(f) as file:
		reader = csv.reader(file)
		for new in reader:
			row=new[0].split(";")
			if row[0] != "ID_IMPUESTO":
				nombre_impuesto = new[1]
				descripcion_impuesto = new[2]
				tasa_impuesto = float(new[3])
				objeto, created = Impuesto.objects.update_or_create(
					nombre_impuesto=nombre_impuesto,
					descripcion_impuesto=descripcion_impuesto,
					tasa_impuesto=tasa_impuesto
				)
	return HttpResponse('Hecho')