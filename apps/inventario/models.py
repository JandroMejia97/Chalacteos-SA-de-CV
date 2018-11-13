from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator


class Recurso(models.Model):
    id_recurso = models.AutoField(
        primary_key=True
    )
    nombre_recurso = models.CharField(
        verbose_name='Nombre del recurso',
        blank=False,
        max_length=50,
        help_text="Nombre del recurso, sea este materia prima o producto"
    )
    descripcion_recurso = models.CharField(
        verbose_name='Descripción del recurso',
        blank=False,
        max_length=250,
        help_text="Una breve descripción del recurso"
    )

    class Meta:
        verbose_name = 'Recurso'
        verbose_name_plural = 'Recursos'
        ordering = ['nombre_recurso']


class Kardex(models.Model):
    id_kardex = models.AutoField(
        primary_key=True
    )
    id_recurso = models.OneToOneField(
        Recurso,
        verbose_name='Recurso',
        on_delete=models.DO_NOTHING,
        blank=False
    )

    class Meta:
        verbose_name = 'Kardex'
        verbose_name_plural = 'Kardexs'
        ordering = ['id_recurso']


class Movimiento(models.Model):
    id_movimiento = models.AutoField(
        primary_key=True
    )
    id_kardex = models.ForeignKey(
        Kardex,
        verbose_name='Kardex',
        on_delete=models.DO_NOTHING,
        blank=False
    )
    fecha_movimiento = models.DateTimeField(
        verbose_name='Fecha',
        auto_now=True,
        blank=False
    )
    cantidad_movimiento = models.DecimalField(
        verbose_name='Cantidad',
        max_digits=1000,
        decimal_places=2,
        blank=False,
        validators=[
            MinValueValidator(
                0, 
                message="Este campo debe ser positivo"
            )
        ],
        help_text="Ingrese la cantidad actual del producto o materia prima"
    )
    costo_unitario_movimiento = models.DecimalField(
        verbose_name='Costo Unitario',
        max_digits=1000,
        decimal_places=2,
        blank=False,
        validators=[
            MinValueValidator(
                0, 
                message="Este campo debe ser positivo"
            )
        ],
        help_text="Ingrese el costo unitario del producto o materia prima"
    )
    monto_movimiento = models.DecimalField(
        verbose_name='Monto',
        max_digits=1000,
        decimal_places=2,
        blank=False,
        validators=[
            MinValueValidator(
                0, 
                message="Este campo debe ser positivo"
            )
        ],
        help_text="Este campo es auto generado"
    )
    is_Input = models.BooleanField(
        verbose_name='¿Es una entrada?',
        blank=False,
        default=True,
        help_text="Defina si esta transacción es una entrada o salida de materia prima o producto"
    )

    def transaction_date(self):
        self.fecha_movimiento = timezone.now()
        self.save()

    def __str__(self):
        return self.fecha_movimiento

    class Meta:
        verbose_name = 'Movimiento'
        verbose_name_plural = 'Movimientos'
        get_latest_by = 'fecha_movimiento'
        ordering = ['-fecha_movimiento']

class Saldo(models.Model):
    id_saldor = models.AutoField(
        primary_key=True
    )
    id_movimiento =models.OneToOneField(
        Movimiento,
        on_delete=models.DO_NOTHING,
        blank=False
    )
    cantidad_saldo = models.DecimalField(
        verbose_name='Cantidad',
        max_digits=1000,
        decimal_places=2,
        blank=False,
        validators=[
            MinValueValidator(
                0, 
                message="Este campo debe ser positivo"
            )
        ],
        help_text="Ingrese la cantidad actual del producto o materia prima"
    )
    costo_unitario_saldo = models.DecimalField(
        verbose_name='Costo Unitario',
        max_digits=1000,
        decimal_places=2,
        blank=False,
        validators=[
            MinValueValidator(
                0, 
                message="Este campo debe ser positivo"
            )
        ],
        help_text="Ingrese el costo unitario del producto o materia prima"
    )
    monto_saldo = models.DecimalField(
        verbose_name='Monto',
        max_digits=1000,
        decimal_places=2,
        blank=False,
        validators=[
            MinValueValidator(
                0, 
                message="Este campo debe ser positivo"
            )
        ],
        help_text="Este campo es auto generado"
    )

    class Meta:
        verbose_name = 'Saldo'
        verbose_name_plural = 'Saldos'
        ordering = ['id_movimiento']
    

class Producto(models.Model):
    id_producto = models.AutoField(
        primary_key='True'
    )
    id_recurso = models.OneToOneField(
        Recurso,
        verbose_name='Recurso',
        on_delete=models.CASCADE,
        blank=False
    )

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['id_producto', 'id_recurso']


class MateriaPrima(models.Model):
    id_materia_prima = models.AutoField(
        primary_key=True
    )
    id_producto = models.ForeignKey(
        Producto,
        verbose_name='Producto',
        on_delete=models.DO_NOTHING,
        blank=False
    )
    id_recurso = models.OneToOneField(
        Recurso,
        verbose_name='Recurso',
        on_delete=models.CASCADE,
        blank=False
    )

    class Meta:
        verbose_name = 'Materia Prima'
        verbose_name_plural = 'Materias Primas'
        ordering = ['id_producto', 'id_recurso']


class Cliente(models.Model):
    id_cliente = models.AutoField(
        primary_key=True
    )
    nombre_cliente = models.CharField(
        verbose_name='Cliente',
        blank=False,
        max_length=50,
        help_text="Nombre del cliente",
    )
    nombre_titular_cliente = models.CharField(
        verbose_name='Titular',
        blank=False,
        max_length=50,
        help_text='Nombre del titular del cliente'
    )

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['nombre_titular_cliente', 'nombre_cliente']


class Proveedor(models.Model):
    id_proveedor = models.AutoField(
        primary_key=True
    )
    nombre_proveedor = models.CharField(
        verbose_name='Proveedor',
        blank=False,
        max_length=50,
        help_text="Nombre del proveedor",
    )
    nombre_titular_proveedor = models.CharField(
        verbose_name='Titular',
        blank=False,
        max_length=50,
        help_text='Nombre del titular del proveedor'
    )

    class Meta:
        verbose_name = 'Proveedor'
        verbose_name_plural = 'Proveedores'
        ordering = ['nombre_titular_proveedor', 'nombre_proveedor']


class Venta(models.Model):
    id_venta = models.AutoField(
        primary_key=True
    )
    id_cliente = models.ForeignKey(
        Cliente,
        verbose_name='Cliente',
        on_delete=models.DO_NOTHING,
        blank=False
    )

    class Meta:
        verbose_name = 'Venta'
        verbose_name_plural = 'Ventas'
        ordering = ['id_cliente']


class Compra(models.Model):
    id_compra = models.AutoField(
        primary_key=True
    )
    id_proveedor = models.ForeignKey(
        Proveedor,
        verbose_name='Proveedor',
        on_delete=models.DO_NOTHING,
        blank=False
    )

    class Meta:
        verbose_name = 'Compra'
        verbose_name_plural = 'Compras'
        ordering = ['id_proveedor']


class Factura(models.Model):
    id_factura = models.AutoField(
        primary_key=True
    )
    id_venta = models.OneToOneField(
        Venta,
        verbose_name='Venta',
        on_delete=models.DO_NOTHING,
        null=True
    )
    id_compra = models.OneToOneField(
        Compra,
        verbose_name='Compra',
        on_delete=models.DO_NOTHING,
        null=True
    )
    sub_total_factura = models.DecimalField(
        verbose_name='Sub Total',
        max_digits=1000,
        decimal_places=2,
        blank=False,
        validators=[
            MinValueValidator(
                0, 
                message="Este campo debe ser positivo"
            )
        ],
        help_text="Ingrese el sub total antes de impuestos de la compra o venta"
    )
    total_factura = models.DecimalField(
        verbose_name='Total',
        max_digits=1000,
        decimal_places=2,
        blank=False,
        validators=[
            MinValueValidator(
                0, 
                message="Este campo debe ser positivo"
            )
        ],
        help_text="Ingrese el total de la compra o venta (impuestos incluídos)"
    )
    estado_factura = models.CharField(
        verbose_name='Estado de la Factura',
        max_length=20,
        help_text="Estado de la fatura: Despachada, Pendiente de pago, Pendiente de entrada, Entregada"
    )

    class Meta:
        verbose_name = 'Factura'
        verbose_name_plural = 'Facturas'
        ordering = ['id_venta', 'id_compra', 'estado_factura','total_factura']


class Detalle(models.Model):
    id_detalle = models.AutoField(
        primary_key=True
    )
    id_materia_prima =models.ForeignKey(
        MateriaPrima,
        on_delete=models.DO_NOTHING,
        verbose_name='Materia Prima',
        null=True
    )
    id_producto = models.ForeignKey(
        Producto,
        on_delete=models.DO_NOTHING,
        verbose_name='Producto',
        null=True
    )
    id_factura = models.ForeignKey(
        Factura,
        on_delete=models.DO_NOTHING,
        verbose_name='Factura',
        null=True
    )
    cantidad_detalle = models.DecimalField(
        verbose_name='Cantidad',
        max_digits=1000,
        decimal_places=2,
        blank=False,
        validators=[
            MinValueValidator(
                0, 
                message="Este campo debe ser positivo"
            )
        ],
        help_text="Ingrese el total de la compra o venta (impuestos incluídos)"
    )

    class Meta:
        verbose_name = 'Detalle de Factura'
        verbose_name_plural = 'Detalles de Facturas'
        ordering = ['id_materia_prima', 'id_producto', 'cantidad_detalle']


class Impuesto(models.Model):
    id_impuesto = models.AutoField(
        primary_key=True
    )
    nombre_impuesto = models.CharField(
        verbose_name='Nombre del Impuesto',
        blank=False,
        max_length=75,
        help_text="Ingrese el nombre del impuesto"
    )
    descripcion_impuesto = models.CharField(
        verbose_name='Descripción',
        blank=False,
        max_length=250,
        help_text="Breve descripcion del impuesto"
    )
    tasa_impuesto = models.DecimalField(
        verbose_name='Tasa de impuesto',
        max_digits=1000,
        blank=False,
        decimal_places=6,
        validators=[
            MinValueValidator(
                0, 
                message="Este campo debe ser positivo"
            ),
            MaxValueValidator(
                2.0,
                message="La tasa a lo sumo debe ser menor a 1.0"
            )
        ],
        help_text="Ingrese la tasa que se le aplica al total de la transacción"
    )

    class Meta:
        verbose_name = "Impuesto"
        verbose_name_plural = "Impuestos"
        ordering = ['nombre_impuesto', 'tasa_impuesto']

class FacturaImpuesto(models.Model):
    id_aplicacion = models.AutoField(
        primary_key=True
    )
    id_factura = models.ForeignKey(
        Factura,
        on_delete=models.DO_NOTHING,
        verbose_name='Factura',
        null=True
    )
    id_impuesto = models.ForeignKey(
        Impuesto,
        on_delete=models.DO_NOTHING,
        verbose_name='Impuesto',
        null=True
    )
    monto_aplicacion = models.DecimalField(
        verbose_name='Monto Aplicado',
        max_digits=1000,
        decimal_places=2,
        blank=False,
        validators=[
            MinValueValidator(
                0, 
                message="Este campo debe ser positivo"
            )
        ],
        help_text="Ingrese el recargo por el impuesto a la compra o venta"
    )

    class Meta:
        verbose_name = 'Factura - Impuesto'
        verbose_name_plural = 'Facturas - Impuestos'
        ordering = ['id_factura', 'id_impuesto']
