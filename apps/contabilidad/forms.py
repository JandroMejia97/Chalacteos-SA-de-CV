from django import forms

from .models import *

class TransaccionForm(forms.ModelForm):

    class Meta:
        model = Transaccion
        fields = [
            'id_tipo',
            'descripcion_transaccion',
            'monto_transaccion',
        ]

class MovimientoForm(forms.ModelForm):

    class Meta:
        model = Movimiento
        fields = [
            'monto_cargo',
            'monto_abono'
        ]
