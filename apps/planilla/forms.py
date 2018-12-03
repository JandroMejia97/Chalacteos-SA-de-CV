from django import forms

from .models import *


class EmpleadoForm(forms.ModelForm):
    
    class Meta:
        model = Empleado
        fields = [
            'id_puesto',
            'dui',
            'primer_nombre',
            'segundo_nombre',
            'primer_apellido',
            'segundo_apellido',
            'fecha_nacimiento'
            'codigo',
            'telefono',
            'direccion',
            'activo',
        ]
