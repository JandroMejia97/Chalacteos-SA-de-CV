from django import forms
from django.contrib.auth.models import User
from .models import *


class UserForm(forms.ModelForm):
    
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email'
        ]

class EmpleadoForm(forms.ModelForm):
    
    class Meta:
        model = Empleado
        fields = [
            'puesto',
            'dui',
            'fecha_nacimiento',
            'telefono',
            'direccion',
            'is_active',
        ]

class DepartamentoForm(forms.ModelForm):
    scope_prefix = 'departamento_data'
    form_name = 'departamento_form'
    class Meta:
        model = Departamento
        fields = [
            'nombre'
        ]
    def __init__(self, *args, **kwargs):
        super(DetalleCompraForm, self).__init__(*args,**kwargs)
        self.fields['nombre'].choices = (('', '---------'),)
        self.fields['nombre'].widget.attrs.update({'disabled': 'true'})

class EmpleadoBoletaForm(forms.ModelForm):
    scope_prefix = 'empleado_data'
    form_name = 'empleado_form'
    class Meta:
        model = Empleado
        fields = [
            'puesto',
            'dui',
            'fecha_nacimiento',
            'telefono',
            'direccion',
            'is_active',
        ]

class EmpresaForm(forms.ModelForm):
    scope_prefix = 'empresa_data'
    form_name = 'empresa_form'
    class Meta:
        model = Empresa
        fields = [
            'nombre'
        ]

