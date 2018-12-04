from django import forms

from .models import *

class BoletaTrabajoForm(forms.ModelForm):
    scope_prefix = 'boleta_data'
    form_name = 'boleta_form'
    class Meta:
        model = BoletaTrabajo
        fields = [
            'numero_horas',
			'monto_horas'
        ]

    def __init__(self, *args, **kwargs):
        super(DetalleCompraForm, self).__init__(*args,**kwargs)
        self.fields['numero_horas'].widget.attrs.update({'min':'0'})
        self.fields['monto_horas'].widget.attrs.update({'min':'0', 'step':0.01})

class RequisicionForm(forms.ModelForm):
    scope_prefix = 'requisicion_data'
    form_name = 'requisicion_form'
    class Meta:
        model = RequisicionMaterial
        fields = [
            'cantidad_material',
			'costo_total_material'
        ]

    def __init__(self, *args, **kwargs):
        super(DetalleCompraForm, self).__init__(*args,**kwargs)
        self.fields['cantidad_material'].widget.attrs.update({'min':'0'})
        self.fields['costo_total_material'].widget.attrs.update({'min':'0', 'step':0.01})
