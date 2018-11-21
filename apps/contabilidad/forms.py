from django import forms

from .models import *

class TransaccionForm(forms.ModelForm):
    scope_prefix = 'transaccion_data'
    form_name = 'transaccion_form'

    class Meta:
        model = Transaccion
        fields = [
            'id_tipo',
            'descripcion_transaccion',
            'monto_transaccion',
        ]

class MovimientoForm(forms.ModelForm):
    scope_prefix = 'movimiento_data'
    form_name = 'movimiento_form'

    class Meta:
        model = Movimiento
        fields = [
            'monto_cargo',
            'monto_abono'
        ]
