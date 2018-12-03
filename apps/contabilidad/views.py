import csv
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
from .forms import *

import datetime
import csv
import json


class IndexView(LoginRequiredMixin, TemplateView):
	template_name = 'index.html'

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
		context = Cuenta.objects.all().filter(is_alta=True)
		if context:
			return context
		else:
			return render(self.request, template_name='404.html')

	def get_context_data(self, **kwargs):
		context = super(CuentasListView, self).get_context_data(**kwargs)
		return context


class TransaccionesListView(LoginRequiredMixin, ListView):
	model = Transaccion
	template_name = 'contabilidad/gestionarTransacciones.html'
	context_object_name = 'transacciones'

	def get_context_data(self, *args, **kwargs):
		context = super(TransaccionesListView, self).get_context_data(*args, **kwargs)
		return context


class MovimientosListView(LoginRequiredMixin, ListView):
	model = Movimiento
	template_name = 'contabilidad/gestionarMovimientos.html'
	context_object_name = 'movimientos'

	def get_queryset(self):
		transaccion = Transaccion.objects.get(id_transaccion=self.request.GET['pk'])
		context = Movimiento.objects.filter(id_transaccion=transaccion)
		return context

	def get_context_data(self, *args, **kwargs):
		context = super(MovimientosListView, self).get_context_data(*args, **kwargs)
		return context


class EstadoFinancieroListView(LoginRequiredMixin, ListView):
	model = EstadoFinanciero
	template_name = 'contabilidad/gestionarEstadosFinancieros.html'
	context_object_name = 'estados_financieros'

	def get_queryset(self):
		user = self.request.user
		context = EstadoFinanciero.objects.all()
		if context:
			return context
		else:
			return render(self.request, template_name='404.html')

	def get_context_data(self, **kwargs):
		context = super(EstadoFinancieroListView, self).get_context_data(**kwargs)
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


class EstadoFinancieroCreateView(LoginRequiredMixin, CreateView):
	model = EstadoFinanciero
	template_name = 'editForm.html'
	success_url = reverse_lazy('contabilidad:estados_financieros')
	fields = [
		'id_estado_financiero',
		'id_periodo_contable',
		'nombre_estado_financiero'
	]


class TransaccionCreateView(LoginRequiredMixin, TemplateView):
	template_name = 'contabilidad/chainedForm.html'
	success_url = 'contabilidad:transacciones'

	def get(self, request, *args, **kwargs):
		context = self.get_context_data(**kwargs)
		context['transaccion_form'] = TransaccionForm()
		context['movimiento_form'] = MovimientoForm()
		context['fecha'] = PeriodoContable.objects.all().order_by('fecha_inicio_periodo')[:1]
		return self.render_to_response(context)

	def post(self, request, *args, **kwargs):
		periodo = PeriodoContable.objects.all().last()
		ultima_transaccion = Transaccion.objects.filter(id_periodo_contable=periodo).count()

		abonos_str = request.POST['abonos']
		cargos_str = request.POST['cargos']
		codigos_cuentas_str = request.POST['codigo_cuentas']
		fecha = request.POST['fecha']
		
		abonos_data = abonos_str.split(',')
		cargos_data = cargos_str.split(',')
		codigos_cuentas_data = codigos_cuentas_str.split(',')

		tipo = TipoTransaccion.objects.get(id_tipo=request.POST['codigoTipo'])

		monto_transaccion=float(request.POST['monto'])

		correcto = False
		message = None
		
		total_abonos = 0
		total_cargos = 0

		for i in range(0, len(codigos_cuentas_data)-1):
			if abonos_data[i] == 'None':
				cargos_data[i] = float(cargos_data[i]) 
				total_cargos += cargos_data[i]
			if cargos_data[i] == 'None':
				abonos_data[i] = float(abonos_data[i])
				total_abonos += abonos_data[i]
		
		if total_abonos == total_cargos:
			if total_abonos == monto_transaccion:

				transaccion = Transaccion.objects.create(
					id_periodo_contable=periodo,
					id_tipo=tipo,
					numero_transaccion=ultima_transaccion+1,
					descripcion_transaccion=request.POST['descripcion'],
					monto_transaccion=monto_transaccion,
					fecha_transaccion=fecha
				)

				for i in range(0, len(codigos_cuentas_data)-1):
					codigo = int(codigos_cuentas_data[i])	
					cuenta = Cuenta.objects.get(id_cuenta=codigo)
					
					if abonos_data[i] == 'None':
						Movimiento.objects.create(
							id_transaccion=transaccion,
							id_cuenta=cuenta,
							monto_cargo=cargos_data[i],
							monto_abono=None
						)
					if cargos_data[i] == 'None':
						Movimiento.objects.create(
							id_transaccion=transaccion,
							id_cuenta=cuenta,
							monto_cargo=None,
							monto_abono=abonos_data[i]
						)
				message = 'Registro exitoso, será redireccionado'
				correcto = True
			else:
				message = 'El monto de la partida doble no concuerda con el monto de la transaccion'
		else:
			message = 'Los movimientos registrados para esta transacción no cumplen partida doble'
		
		if correcto:
			return JsonResponse(data={'message':message, 'success_url': '/transacciones/'})
		else:
			return JsonResponse(data={'message':message})

class MovimientoCreateView(LoginRequiredMixin, CreateView):
	model = Movimiento
	template_name = 'contabilidad/chainedForm.html'
	success_url = reverse_lazy('contabilidad:transacciones')
	fields = [
		'id_cuenta',
		'monto_cargo',
        'monto_abono'
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


class EstadoFinancieroUpdateView(LoginRequiredMixin, UpdateView):
	model = EstadoFinanciero
	template_name = 'editForm.html'
	success_url = reverse_lazy('contabilidad:estados_financieros')
	fields = [
		'id_estado_financiero',
		'id_periodo_contable',
		'nombre_estado_financiero'
	]


class TransaccionUpdateView(LoginRequiredMixin, UpdateView):
	model = Transaccion
	template_name = 'editForm.html'
	success_url = reverse_lazy('contabilidad:transacciones')
	fields = [
		'id_rubro',
		'codigo_cuenta',
		'nombre_cuenta',
		'is_cuenta_acreedora'
	]


class MovimientoUpdateView(LoginRequiredMixin, UpdateView):
	model = Movimiento
	template_name = 'editForm.html'
	success_url = reverse_lazy('contabilidad:transacciones')
	fields = [
		'monto_cargo',
        'monto_abono'
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


class EstadoFinancieroDetailView(LoginRequiredMixin, DetailView):
	model = EstadoFinanciero
	template_name = 'contabilidad/viewEstadosFinancieros.html'
	success_url = reverse_lazy('contabilidad:estados_financieros')
	fields = [
		'id_estado_financiero',
		'id_periodo_contable',
		'nombre_estado_financiero'
	]
	context_object_name = 'estados_financieros'


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


class BalanceGeneralDetailView(LoginRequiredMixin, DetailView):
	model = EstadoFinanciero
	template_name = 'contabilidad/estados/balanceGeneral.html'
	fields = [
		'id_empresa',
		'nombre_estado_financiero'
		'id_periodo_contable',
	]
	context_object_name = 'balance_general'


class EstadoResultadosDetailView(LoginRequiredMixin, DetailView):
	model = EstadoFinanciero
	template_name = 'contabilidad/estados/estadoResultados.html'
	fields = [
		'id_empresa',
		'nombre_estado_financiero'
		'id_periodo_contable',
	]
	context_object_name = 'estado_resultados'


class BalanceComprobacionDetailView(LoginRequiredMixin, DetailView):
	model = EstadoFinanciero
	template_name = 'contabilidad/estados/balanceComprobacion.html'
	fields = [
		'id_empresa',
		'nombre_estado_financiero'
		'id_periodo_contable',
	]
	context_object_name = 'balance_comprobacion'


class EstadoCapitalDetailView(LoginRequiredMixin, DetailView):
	model = EstadoFinanciero
	template_name = 'contabilidad/estados/estadoCapital.html'
	fields = [
		'id_empresa',
		'nombre_estado_financiero'
		'id_periodo_contable',
	]
	context_object_name = 'estado_capital'

def get_movimientos(request, id_transaccion):
	context = {}
	context['transaccion'] = Transaccion.objects.get(id_transaccion=id_transaccion)
	if context['transaccion']:
		context['movimientos'] = Movimiento.objects.filter(id_transaccion=context['transaccion'])
		return render(request, template_name='contabilidad/viewTransaccion.html', context=context)
	else:
		return render(request, template_name='404.html')

def registrar_transaccion(data):
	periodos = PeriodoContable.objects.all().order_by('fecha_inicio_periodo')[:1]
	periodo_instance = None
	for periodo in periodos:
		periodo_instance = periodo
	ultima_transaccion = Transaccion.objects.filter(id_periodo_contable=periodo_instance).count()
	tipo = None
	transaccion = Transaccion.objects.create(
		id_periodo_contable=periodo_instance,
		id_tipo=tipo,
		numero_transaccion=ultima_transaccion,
		fecha_transaccion=datetime.datetime.now(),
		descripcion_transaccion='Compra de materia prima',
		monto_transaccion=data['total']
	)
	cuentas = {}
	if data['tipo'] == 'COMPRA':
		cuentas['inv_mp'] = Cuenta.objects.get(codigo_cuenta=111101)
		cuentas['iva'] = Cuenta.objects.get(codigo_cuenta=2110)
		if data['compra'] == 'CREDITO':
			tipo = TipoTransaccion.objects.get(nombre_tipo='COMPRA AL CREDITO')
			cuentas['cp'] = Cuenta.objects.get(codigo_cuenta=2102)
			movimiento_abono = Movimiento.objects.create(
				id_transaccion=transaccion,
				id_cuenta=cuentas['cp'],
				monto_cargo=None,
				monto_abono=data['total']
			)
		elif data['compra'] == 'CONTADO':
			tipo = TipoTransaccion.objects.get(nombre_tipo='COMPRA AL CONTADO')
			cuentas['cg'] = Cuenta.objects.get(codigo_cuenta=110101)
			movimiento_abono = Movimiento.objects.create(
				id_transaccion=transaccion,
				id_cuenta=cuentas['cg'],
				monto_cargo=None,
				monto_abono=data['total']
			)
		elif data['compra'] == 'PROPORCION':
			tipo = TipoTransaccion.objects.get(nombre_tipo='COMPRA PARCIALMENTE AL CREDITO')
			cuentas['cp'] = Cuenta.objects.get(codigo_cuenta=2102)
			cuentas['cg'] = Cuenta.objects.get(codigo_cuenta=110101)
			movimiento_abono1 = Movimiento.objects.create(
				id_transaccion=transaccion,
				id_cuenta=cuentas['cg'],
				monto_cargo=None,
				monto_abono=data['total']*(1-data['proporcion'])
			)
			movimiento_abono2 = Movimiento.objects.create(
				id_transaccion=transaccion,
				id_cuenta=cuentas['cp'],
				monto_cargo=None,
				monto_abono=data['total']*data['proporcion']
			)
		transaccion.id_tipo = tipo
		transaccion.save()
		inventario_cargo = Movimiento.objects.create(
			id_transaccion=transaccion,
			id_cuenta=cuentas['inv_mp'],
			monto_cargo=data['sub_total'],
			monto_abono=None
		)
		iva_cargo = Movimiento.objects.create(
			id_transaccion=transaccion,
			id_cuenta=cuentas['iva'],
			monto_cargo=data['iva'],
			monto_abono=None
		)
	elif data['tipo'] == 'VENTA':
		cuentas['inv_pt'] = Cuenta.objects.get(codigo_cuenta=111104)
		cuentas['iva'] = Cuenta.objects.get(codigo_cuenta=2111)
		if data['venta'] == 'CREDITO':
			tipo = TipoTransaccion.objects.get(nombre_tipo='VENTA AL CREDITO')
			cuentas['cc'] = Cuenta.objects.get(codigo_cuenta=1104)
			movimiento_cargo = Movimiento.objects.create(
				id_transaccion=transaccion,
				id_cuenta=cuentas['cc'],
				monto_cargo=data['total'],
				monto_abono=None
			)
		elif data['venta'] == 'CONTADO':
			tipo = TipoTransaccion.objects.get(nombre_tipo='VENTA AL CONTADO')
			cuentas['cg'] = Cuenta.objects.get(codigo_cuenta=110101)
			movimiento_cargo = Movimiento.objects.create(
				id_transaccion=transaccion,
				id_cuenta=cuentas['cg'],
				monto_cargo=data['total'],
				monto_abono=None
			)
		elif data['venta'] == 'PROPORCION':
			tipo = TipoTransaccion.objects.get(nombre_tipo='VENTA PARCIALMENTE AL CREDITO')
			cuentas['cc'] = Cuenta.objects.get(codigo_cuenta=1104)
			cuentas['cg'] = Cuenta.objects.get(codigo_cuenta=110101)
			movimiento_cargo1 = Movimiento.objects.create(
				id_transaccion=transaccion,
				id_cuenta=cuentas['cg'],
				monto_cargo=data['total']*(1-data['proporcion']),
				monto_abono=None
			)
			movimiento_cargo2 = Movimiento.objects.create(
				id_transaccion=transaccion,
				id_cuenta=cuentas['cc'],
				monto_cargo=data['total']*data['proporcion'],
				monto_abono=None
			)
		transaccion.id_tipo = tipo
		transaccion.save()
		inventario_cargo = Movimiento.objects.create(
			id_transaccion=transaccion,
			id_cuenta=cuentas['inv_pt'],
			monto_cargo=None,
			monto_abono=data['sub_total']
		)
		iva_cargo = Movimiento.objects.create(
			id_transaccion=transaccion,
			id_cuenta=cuentas['iva'],
			monto_cargo=None,
			monto_abono=data['iva']
		)
	return transaccion
			
@login_required(login_url='/sign-in/')
def cuentas(request, id_cuenta):   
    if request.method == 'DELETE':
        parametro = Cuenta.objects.get(id_cuenta=id_cuenta)
        parametro.is_alta = False
        parametro.save()
        message = "La cuenta fue borrada exitosamente"
        return JsonResponse(data={'message': message})

@login_required
def estados_financieros(request, id_estado_financiero):   
    if request.method == 'DELETE':
        parametro = EstadoFinanciero.objects.get(id_estado_financiero=id_estado_financiero)
        parametro.delete()
        message = "El estado financiero fue borrado exitosamente"
        return JsonResponse(data={'message': message})

@login_required(login_url='/sign-in/')
def load_sub_cuenta(request):
	if request.method == 'GET':
		id_cuenta = request.GET['id_cuenta']
		cuenta = Cuenta.objects.get(id_cuenta=id_cuenta)
		cuentas = Cuenta.objects.all().filter(codigo_cuenta_padre=cuenta).values()
		if cuentas:
			data = {
				'message': "Datos recuperados",
				'cuentas': list(cuentas)
			}
		else:
			data = {
				'message': "La cuenta seleccionda no posee subcuentas"
			}
		return JsonResponse(data=data)

def import_data_rubro(request):
	catalogo = Catalogo.objects.create(nombre_catalogo="Catalogo")
	f = 'C:\\rubros.csv'
	with open(f) as file:
		reader = csv.reader(file)
		for new in reader:
			type(new[0])
			row = new[0].split(";")
			if row[0] != "id_rubro":
				codigo_rubro=int(row[1])
				nombre_rubro=str(row[2]).upper()

				id_catalogo=Catalogo.objects.get(id_catalogo=int(row[3]))
				if row[4] == '':
					rubro_sup=None
				else:
					rubro_sup=Rubro.objects.get(id_rubro=row[4])
				nivel=int(row[5])
				created = Rubro.objects.update_or_create(
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
			row=new[0].split(";")
			if row[0] != "id_cuenta":

				codigo_cuenta=int(row[1])
				nombre_cuenta=row[2]
				if row[3] == '1':
					is_cuenta_acreedora=True
				else:
					is_cuenta_acreedora=False
				is_alta = bool(row[4])
				if row[5] == '' or row[5] == None:
					id_rubro = None
				else:
					id_rubro = Rubro.objects.get(id_rubro=int(row[5]))
				if row[6] == '' or row[6] == None:
					codigo_cuenta_padre = None
				else:
					codigo_cuenta_padre = Cuenta.objects.get(id_cuenta=int(row[6]))
				objeto, created = Cuenta.objects.update_or_create(
					codigo_cuenta=codigo_cuenta,
					nombre_cuenta=nombre_cuenta,
					is_cuenta_acreedora=is_cuenta_acreedora,
					is_alta=is_alta,
					id_rubro=id_rubro,
					codigo_cuenta_padre=codigo_cuenta_padre
				)
	return HttpResponse('Hecho')

def import_data_transaccion(self):
	f = 'C:\\tipo_transaccion.csv'
	with open(f) as file:
		reader = csv.reader(file)
		for new in reader:
			row=new[0].split(";")
			if row[0] != "id_tipo":
				nombre_tipo = new[1]
				descripcion_tipo = new[2]
				objecto, created = TipoTransaccion.objects.update_or_create(
					nombre_tipo=nombre_tipo,
					descripcion_tipo=descripcion_tipo
				)
	return HttpResponse('Hecho')