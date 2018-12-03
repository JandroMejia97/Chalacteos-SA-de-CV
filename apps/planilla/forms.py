from django import forms

from .models import *


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