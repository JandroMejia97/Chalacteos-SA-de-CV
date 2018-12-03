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