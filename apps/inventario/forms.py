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
    precio_unitario = forms.DecimalField(
        label='Precio unitario',
        help_text='Ingrese el precio unitario usando coma decimal',
        decimal_places=2
    )
    class Meta:
        model = Detalle
        fields = [
            'id_materia_prima',
            'cantidad_detalle',
            'precio_unitario'
        ]

    def __init__(self, *args, **kwargs):
        super(DetalleCompraForm, self).__init__(*args,**kwargs)
        self.fields['cantidad_detalle'].widget.attrs.update({'min':'0'})
        self.fields['precio_unitario'].widget.attrs.update({'min':'0'})
        self.fields['id_materia_prima'].choices = (('', '---------'),)
        self.fields['id_materia_prima'].widget.attrs.update({'disabled': 'true'})

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
    is_credito = forms.BooleanField(
        label='¿La compra es al crédito?',
        help_text='Indique si está factura será pagada al crédito ya sea total o parcialmente'
    )
    is_contado = forms.BooleanField(
        label='¿La compra es al contado?',
        help_text='Indique si está factura será pagada al contado ya sea total o parcialmente'
    )
    proporcion = forms.DecimalField(
        label='Proporcion',
        help_text='Ingrese la proporcion de la compra que será al credito',
        decimal_places=2
    )
    class Meta:
        model = Proveedor
        fields = [
            'nombre_proveedor',
            'is_credito',
            'is_contado',
            'proporcion'
        ]

    def __init__(self, *args, **kwargs):
        super(ProveedorCompraForm, self).__init__(*args,**kwargs)
        self.fields['nombre_proveedor'] = forms.ModelChoiceField(
            label='Proveedor',
            queryset=Proveedor.objects.all(),
            help_text='Seleccione el proveedor al que se le comprará la materia prima',
            widget=forms.Select(
                attrs={
                    'onchange': 'getMateria("id_nombre_proveedor", "id_id_materia_prima")'
                }
            )
        )
        self.fields['proporcion'].widget.attrs.update({
            'min':'0',
            'step':0.01,
            'hidden':False
        })

class ProveedorForm(forms.ModelForm):
    scope_prefix = 'proveedor_data'
    form_name = 'proveedor_form'

    class Meta:
        model = Proveedor
        fields = [
            'nombre_proveedor'
        ]

    def __init__(self, *args, **kwargs):
        super(ProveedorForm, self).__init__(*args,**kwargs)
        self.fields['nombre_proveedor'] = forms.ModelChoiceField(
            label='Proveedor',
            queryset=Proveedor.objects.all(),
            help_text='Seleccione el proveedor al que se le comprará la materia prima',
        )