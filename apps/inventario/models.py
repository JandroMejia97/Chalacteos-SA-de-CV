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

    def __str__(self):
        return self.nombre_recurso

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
        blank=False,
        help_text='Seleccion el recurso del que esta compuesto el kardex'
    )

    def __str__(self):
        return str(self.id_recurso)

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
        blank=False,
        help_text='Seleccion el kardex que posee el movimiento'
    )
    fecha_movimiento = models.DateTimeField(
        verbose_name='Fecha',
        auto_now=True,
        blank=False,
        help_text='Ingrese en que se realizo fecha del movimiento'
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
        blank=False,
        help_text='Seleccion el movimiento al que le corresponde el saldo'
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

    def __str__(self):
        return self.id_saldor

    class Meta:
        verbose_name = 'Saldo'
        verbose_name_plural = 'Saldos'
        ordering = ['id_movimiento']
    

class Producto(models.Model):
    id_producto = models.AutoField(
        primary_key=True
    )
    id_recurso = models.OneToOneField(
        Recurso,
        verbose_name='Recurso',
        on_delete=models.CASCADE,
        blank=False,
        help_text='Seleccione el recurso del producto'
    )
    
    def __str__(self):
        return str(self.id_recurso)

    def __str__(self):
        return str(self.id_recurso)

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
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

    def __str__(self):
        return self.nombre_cliente

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

    def __str__(self):
        return self.nombre_proveedor

    class Meta:
        verbose_name = 'Proveedor'
        verbose_name_plural = 'Proveedores'
        ordering = ['nombre_titular_proveedor', 'nombre_proveedor']


class MateriaPrima(models.Model):
    id_materia_prima = models.AutoField(
        primary_key=True
    )
    id_producto = models.ForeignKey(
        Producto,
        verbose_name='Producto',
        on_delete=models.DO_NOTHING,
        blank=False,
        help_text='Seleccion el producto que esta conformado por materia prima'
    )
    id_recurso = models.OneToOneField(
        Recurso,
        verbose_name='Recurso',
        on_delete=models.CASCADE,
        blank=False,
        help_text='Seleccion el recurso para la kardex',
    )
    id_proveedor = models.ForeignKey(
        Proveedor,
        verbose_name='Proveedor',
        on_delete=models.DO_NOTHING,
        blank=False,
        help_text='Seleccion el proveedor al que le pertenece la compra'
    )

    def __str__(self):
        return str(self.id_recurso)

    class Meta:
        verbose_name = 'Materia Prima'
        verbose_name_plural = 'Materias Primas'
        ordering = ['id_producto', 'id_recurso']


class Factura(models.Model):
    id_factura = models.AutoField(
        primary_key=True
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
        help_text="Ingrese el sub total antes de impuestos"
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
        help_text="Ingrese el total (impuestos incluídos)"
    )
    estado_factura = models.CharField(
        verbose_name='Estado de la Factura',
        max_length=20,
        help_text="Estado de la fatura: Despachada, Pendiente de pago, Pendiente de entrada, Entregada"
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

    def __str__(self):
        return '{}'.format(self.id_factura)

    class Meta:
        verbose_name = 'Factura'
        verbose_name_plural = 'Facturas'
        ordering = ['estado_factura','total_factura']


class Venta(models.Model):
    id_venta = models.AutoField(
        primary_key=True
    )
    id_cliente = models.ForeignKey(
        Cliente,
        verbose_name='Cliente',
        on_delete=models.DO_NOTHING,
        blank=False,
        help_text='Seleccion el cliente al que le pertenece la venta'
    )
    id_factura = models.ForeignKey(
        Factura,
        verbose_name='Factura',
        on_delete=models.DO_NOTHING,
        blank=False,
        help_text='Seleccion la factura al que le pertenece la venta'
    )

    def __str__(self):
        return '{}'.format(self.id_venta)

    class Meta:
        verbose_name = 'Venta'
        verbose_name_plural = 'Ventas'
        ordering = ['id_factura','id_cliente']


class Compra(models.Model):
    id_compra = models.AutoField(
        primary_key=True
    )
    id_proveedor = models.ForeignKey(
        Proveedor,
        verbose_name='Proveedor',
        on_delete=models.DO_NOTHING,
        blank=False,
        help_text='Seleccion el proveedor al que le pertenece la compra'
    )
    id_factura = models.ForeignKey(
        Factura,
        verbose_name='Factura',
        on_delete=models.DO_NOTHING,
        blank=False,
        help_text='Seleccion la factura al que le pertenece la venta'
    )

    def __str__(self):
        return self.id_compra

    class Meta:
        verbose_name = 'Compra'
        verbose_name_plural = 'Compras'
        ordering = ['id_factura','id_proveedor']


class Detalle(models.Model):
    id_detalle = models.AutoField(
        primary_key=True
    )
    id_materia_prima =models.ForeignKey(
        MateriaPrima,
        on_delete=models.DO_NOTHING,
        verbose_name='Materia Prima',
        null=True,
        help_text='Seleccion la materia prima que contiene el detalle'
    )
    id_producto = models.ForeignKey(
        Producto,
        on_delete=models.DO_NOTHING,
        verbose_name='Producto',
        null=True,
        help_text='Seleccion el producto que contiene el detalle'
    )
    id_factura = models.ForeignKey(
        Factura,
        on_delete=models.DO_NOTHING,
        verbose_name='Factura',
        null=True,
        help_text="Seleccione la factura que pertenece el detalle"
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
        help_text="Ingrese cantidad del producto o materia prima"
    )


    def __str__(self):
        return self.id_detalle

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

    def __str__(self):
        return self.nombre_impuesto

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
        null=True,
        help_text='Seleccione la factura que se aplicara en la factura con impuesto'
    )
    id_impuesto = models.ForeignKey(
        Impuesto,
        on_delete=models.DO_NOTHING,
        verbose_name='Impuesto',
        null=True,
        help_text='Seleccione el impuesto que se aplicara a la factura con impuesto'
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
