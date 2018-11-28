from django import forms

from .models import *

class EmpresaForm(forms.ModelForm):
	
	class Meta:
		model = Empresa
		exclude = ()
		field = [
			'nic',
			'ncr',
			'nombre',
			'calendar',
		]
		widgets = {
			'nic': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Escriba el NIC','autofocus':'True', 'requerid':'True', 'maxlength':'20'}),
			'ncr': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Escriba el Nombre Comercial','autofocus':'True', 'requerid':'True', 'maxlength':'50'}),
			'nombre': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Escriba el Nombre Registrado','autofocus':'True', 'requerid':'True', 'maxlength':'50'}),
			'calendar': forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Escriba el Calendario Base','autofocus':'True', 'requerid':'True', 'maxlength':'2'}),
		}

class EmpleadoForm(forms.ModelForm):
	
	class Meta:
		model = Empleado
		exclude = ()
		field = [
			'dui',
			'primer_nombre',
			'segundo_nombre',
			'primer_apellido',
			'segundo_apellido',
			'fecha_nacimiento',
			'codigo',
			'telefono',
			'direccion',
			'activo',
		]
		widgets = {
			'dui': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Escriba el DUI','autofocus':'True', 'requerid':'True', 'maxlength':'10'}),
			'primer_nombre': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Escriba el Primer Nombre','autofocus':'True', 'requerid':'True', 'maxlength':'20'}),
			'segundo_nombre': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Escriba el Segundo Nombre','autofocus':'True', 'requerid':'True', 'maxlength':'20'}),
			'primer_apellido': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Escriba el Primer Apellido','autofocus':'True', 'requerid':'True', 'maxlength':'20'}),
			'segundo_apellido': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Escriba el Segundo Apellido','autofocus':'True', 'requerid':'True', 'maxlength':'20'}),
			'fecha_nacimiento': forms.TextInput(attrs={'class':'form-control','autofocus':'True', 'requerid':'True', 'type':'date'}),
			'codigo': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Escriba el codigo del empleado','autofocus':'True', 'requerid':'True', 'maxlength':'8'}),
			'telefono': forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Escriba el telefono','autofocus':'True', 'requerid':'True'}),
			'direccion': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Escriba la direccion','autofocus':'True', 'requerid':'True', 'maxlength':'60'}),
			'activo': forms.CheckboxInput(attrs={'class':'form-control'}),

		}


class DepartamentoForm(forms.ModelForm):
	
	class Meta:
		model = Departamento
		exclude = ()
		field = [
			'nombre',
			'descripcion',
		]
		widgets = {
			'nombre': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Escriba el Nombre','autofocus':'True', 'requerid':'True', 'maxlength':'20'}),
			'descripcion': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Escriba la descripcion','autofocus':'True', 'requerid':'True', 'maxlength':'250', 'type':'textarea'}),
		}


class PuestoForm(forms.ModelForm):
	
	class Meta:
		model = Puesto
		exclude = ()
		field = [
			'codigo',
			'nombre_funcional',
			'descripcion',
			'salario_base',
		]
		widgets = {
			'codigo': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Digite el codigo del puesto','autofocus':'True', 'requerid':'True', 'maxlength':'8'}),
			'descripcion': forms.TextInput(attrs={'class':'form-control', 'placeholder':'descripcion del puesto','autofocus':'True', 'requerid':'True', 'maxlength':'200'}),
			'nombre_funcional': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Digite nombre funcional del puesto','autofocus':'True', 'requerid':'True', 'maxlength':'50'}),
			'salario_base': forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Digite el salario base del puesto','autofocus':'True', 'requerid':'True'}),
		}

class AsignacionForm(forms.ModelForm):
	
	class Meta:
		model = Asignacion
		exclude = ()
		field = [
			'empleado_empresa',
			'puesto_empresa',
			'departamento_empresa',
			'salario_asignado',
			'fecha_asignacion',
			'calendario',
		]
		widgets = {
			'empleado_empresa': forms.TextInput(attrs={'class':'form-control','autofocus':'True', 'requerid':'True'}),
			'puesto_empresa': forms.TextInput(attrs={'class':'form-control','autofocus':'True', 'requerid':'True'}),
			'departamento_empresa': forms.TextInput(attrs={'class':'form-control','autofocus':'True', 'requerid':'True'}),
			'salario_asignado': forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Digite el salario asignado','autofocus':'True', 'requerid':'True'}),
			'fecha_asignacion': forms.TextInput(attrs={'class':'form-control', 'type':'date','autofocus':'True', 'requerid':'True'}),
			'calendario': forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Digite el calendario Base','autofocus':'True', 'requerid':'True'}),
		}
