from django import forms

from .models import *

class TransaccionForm(forms.ModelForm):
    scope_prefix = 'transaccion_data'
    form_name = 'transaccion_form'

    descripcion_transaccion =  forms.CharField(
        label='Descripción de la transacción',
        help_text='Ingrese la descripción de la transacción realizada',
        widget=forms.Textarea(
            attrs={'rows':2}
        )
    )

    class Meta:
        model = Transaccion
        fields = [
            'id_tipo',
            'monto_transaccion',
        ]

class MovimientoForm(forms.ModelForm):
    scope_prefix = 'movimiento_data'
    form_name = 'movimiento_form'

    sub_cuenta = forms.ChoiceField(
        label='Sub Cuenta',
        help_text='Seleccione la subcuenta a afectar',
    )

    class Meta:
        model = Movimiento
        fields = [
            'id_cuenta',
            'monto_cargo',
            'monto_abono'
        ]

    def __init__(self, *args, **kwargs):
        super(MovimientoForm, self).__init__(*args, **kwargs)
        self.fields['id_cuenta'] = forms.ModelChoiceField(
            label='Cuenta',
            queryset=Cuenta.objects.filter(codigo_cuenta_padre=None),
            help_text='Seleccione la cuenta mayor a afectar',
            widget=forms.Select(
                attrs={'onclick': 'getCuenta()'}
            )
        )
        """self.fields['sub_cuenta'] = forms.ModelChoiceField(
            label='Sub Cuenta',
            queryset=Cuenta.objects.exclude(codigo_cuenta_padre=None),
            help_text='Seleccione la subcuenta a afectar',
        )"""