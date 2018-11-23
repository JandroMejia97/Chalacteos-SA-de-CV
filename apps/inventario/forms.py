from django import forms

from .models import *

class VentaForm(forms.ModelForm):
    scope_prefix = 'venta_data'
    form_name = 'venta_form'
    class Meta:
        model = Venta
        fields = [
            'id_cliente'
        ]

class DetalleVentaForm(forms.ModelForm):
    scope_prefix = 'detalle_venta_data'
    form_name = 'detalle_venta_form'
    class Meta:
        model = Detalle
        fields = [
            'id_producto',
            'cantidad_detalle'
        ]

class CompraForm(forms.ModelForm):
    scope_prefix = 'compra_data'
    form_name = 'compra_form'
    class Meta:
        model = Compra
        fields = [
            'id_proveedor'
        ]

class DetalleCompraForm(forms.ModelForm):
    scope_prefix = 'detalle_compra_data'
    form_name = 'detalle_compra_form'
    class Meta:
        model = Detalle
        fields = [
            'id_materia_prima',
            'cantidad_detalle'
        ]

class RecursoForm(forms.ModelForm):
    scope_prefix = 'recurso_data'
    form_name = 'recurso_form'

    class Meta:
        model = Recurso
        fields = [
            'nombre_recurso',
            'descripcion_recurso'
        ]


class MateriaPrimaForm(forms.ModelForm):
    scope_prefix = 'materia_prima_data'
    form_name = 'materia_prima_form'
    class Meta:
        model = MateriaPrima
        fields = [
            'id_materia_prima'
        ]

class ProveedorCompraForm(forms.ModelForm):
    scope_prefix = 'proveedor_data'
    form_name = 'proveedor_form'
    class Meta:
        model = Proveedor
        fields = [
            'nombre_proveedor',
        ]

    def __init__(self, *args, **kwargs):
        super(ProveedorForm, self).__init__(*args,**kwargs)
        self.fields['nombre_proveedor'] = forms.ModelChoiceField(
            label='Proveedor',
            queryset=Proveedor.objects.all(),
            help_text='Seleccione el proveedor al que se le comprará la materia prima',
            widget=forms.Select(
                attrs={
                    'onchange': 'getMateria()'
                }
            )
        )

class ProveedorForm(forms.ModelForm):
    scope_prefix = 'proveedor_data'
    form_name = 'proveedor_form'
    class Meta:
        model = Proveedor
        fields = [
            'nombre_proveedor',
        ]

    def __init__(self, *args, **kwargs):
        super(ProveedorForm, self).__init__(*args,**kwargs)
        self.fields['nombre_proveedor'] = forms.ModelChoiceField(
            label='Proveedor',
            queryset=Proveedor.objects.all(),
            help_text='Seleccione el proveedor al que se le comprará la materia prima',
        )