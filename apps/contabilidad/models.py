from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator, MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User


class Catalogo(models.Model):
	id_catalogo = models.AutoField(
		primary_key=True
	)
	nombre_catalogo = models.CharField(
		max_length = 30,
		verbose_name='Nombre del catalogo',
        blank=False,
        help_text="Nombre del catalogo"
	)
	
	def __str__(self):
		return self.nombre_catalogo


class Empresa(models.Model):
	id_empresa = models.AutoField(
		primary_key = True
	)
	id_usuario = models.OneToOneField(
		User,
		verbose_name='Usuario',
        on_delete=models.CASCADE,
        blank=False
	)
	id_catalogo = models.OneToOneField(
		Catalogo,
		verbose_name='Catálogo',
        on_delete=models.CASCADE,
        blank=False
	)
	nombre_empresa = models.CharField(
		max_length = 30,
		verbose_name='Nombre de la Empresa',
        blank=False,
        help_text="Nombre de la Empresa"
	)

	def __str__(self):
		return self.nombre_empresa
	
	class Meta:
		ordering = ["nombre_empresa"]
		verbose_name = "Empresa"
		verbose_name_plural = 'Empresas'


class Rubro(models.Model):
	id_rubro = models.AutoField(
		primary_key = True
	)
	id_catalogo = models.ForeignKey(
		Catalogo,
		verbose_name='Catálogo',
        on_delete=models.SET_NULL,
        blank=False,
		null=True
	)
	rubro_sup = models.ForeignKey(
		'self',
		verbose_name='Rubro',
        on_delete=models.SET_NULL,
        blank=True,
		null=True
	)
	codigo_rubro = models.CharField(
		verbose_name='Código del rubro', 
        blank=False,
        max_length=2,
        help_text="Ingrese el código del rubro",
        error_messages={
            'value':'El código del rubro no debe ser menor a 1'
        },
        validators=[
            MinLengthValidator(1),
			MaxLengthValidator(2)
        ]
	)	
	nombre_rubro = models.CharField(
		max_length = 50,
		verbose_name ='Nombre del rubro',
        blank=False,
        help_text="Ingrese el nombre del rubro"
	)
	nivel = models.IntegerField(
		verbose_name='Nivel del rubro', 
        blank=False,
        help_text="Ingrese el nivel del rubro. Ejemplo: Activo -> Es Nivel 1, Efectivo -> Es Nivel 2",
        error_messages={
            'value':'El nivel del rubro no debe ser menor a 1, ni mayor a 3'
        },
        validators=[
            MinValueValidator(1),
			MaxValueValidator(31)
        ],
		null=True
	)

	def __str__(self):
		return self.nombre_rubro
	
	class Meta:
		ordering = ["codigo_rubro"]
		verbose_name = "Rubro"
		verbose_name_plural = "Rubros"


class PeriodoContable(models.Model):
	id_perido_contable = models.AutoField(
		primary_key = True
	)
	fecha_inicio_periodo = models.DateTimeField(
		verbose_name='Fecha de inicio',
        auto_now=True,
        help_text='Fecha de inicio de un nuevo período contable',
        error_messages={
            'empty': 'Este campo no debe quedar vacío'
        },
        null=True, 
        blank=False
	)
	fecha_final_periodo = models.DateTimeField(
		verbose_name='Fecha de finalización',
        auto_now=True,
        help_text='Fecha de finalización del período contable',
        error_messages={
            'empty': 'Este campo no debe quedar vacío'
        },
        null=True, 
        blank=False
	)

	class Meta:
		ordering = ["id_perido_contable"]
		verbose_name = "Período Contable"
		verbose_name_plural = "Períodos Contables"


class Cuenta(models.Model):
	id_cuenta = models.AutoField(
		primary_key = True
	)
	id_rubro = models.ForeignKey(
		Rubro,
		verbose_name='Rubro',
        on_delete=models.SET_NULL,
		help_text='Seleccion el rubro al que pertenece la cuenta',
        blank=False,
        null=True
	)
	codigo_cuenta = models.IntegerField(
		verbose_name='Código de la cuenta', 
        blank=False,
        null=True,
        help_text="Debe ingresar el código de la cuenta dependiendo de su ubicación en el catálogo",
        error_messages={
            'value':'Debe ser un código mayor a 1'
        },
        validators=[
            MinValueValidator(1)
        ]
	)
	codigo_cuenta_padre=models.ForeignKey(
		'self',
		verbose_name='Cuenta Padre',
		on_delete=models.SET_NULL,
		blank=True,
		null=True,
		help_text='Seleccione la cuenta a la que pertenece esta subcuenta'
	)
	nombre_cuenta = models.CharField(
		max_length = 100,
		verbose_name='Nombre de cuenta',
        blank=False,
        null=True,
        help_text="Ingrese el nombre de la cuenta",
        error_messages={
            'empty': 'Este campo no debe quedar vacío'
        }
	)
	is_cuenta_acreedora = models.BooleanField(
		verbose_name='¿Es cuenta de naturaleza acreedora?',
        blank=False,
        default=False,
        help_text="Defina si la cuenta es de naturaleza acreedora o deudora"
	)
	is_alta = models.BooleanField(
		verbose_name='¿Está de alta?',
        blank=False,
        default=True,
        help_text="Defina si la cuenta está en uso"
	)

	def __str__(self):
		return self.nombre_cuenta
	
	class Meta:
		ordering = ["id_rubro","codigo_cuenta"]
		verbose_name = "Cuenta"
		verbose_name_plural = "Cuentas"


class EstadoFinanciero(models.Model):
	id_estado_financiero = models.AutoField(
		primary_key = True,
	)
	id_usuario = models.ForeignKey(
		User,
		verbose_name='Usuario',
        on_delete=models.SET_NULL,
        blank=False,
        null=True
	)
	id_empresa = models.ForeignKey(
		Empresa,
		verbose_name='Empresa',
        on_delete=models.SET_NULL,
        blank=False,
        null=True
	)
	id_perido_contable = models.ForeignKey(
        PeriodoContable,
        verbose_name='Período Contable',
        on_delete=models.SET_NULL,
        blank=False,
        null=True
	)
	id_cuenta = models.ManyToManyField(
		Cuenta,
		help_text='Cuenta que sera saldada',
        error_messages={
            'select': 'Debe seleccionar uno de la lista'
        }, 
        blank=True
	)
	nombre_estado_financiero = models.CharField(
		max_length = 45,
		verbose_name='Estado Financiero',
        blank=False,
        help_text="Nombre del Estado Financiero",
        error_messages={
            'empty': 'Este campo no debe quedar vacío'
        }
	)
	def __str__(self):
		return self.nombre_estado_financiero
	
	class Meta:
		ordering = ["id_perido_contable", "nombre_estado_financiero"]
		verbose_name = "Estado Financiero"
		verbose_name_plural = "Estados Financieros"


class Mayorizacion(models.Model):
	id_mayorizacion = models.AutoField(
		primary_key = True
	)
	id_perido_contable = models.ForeignKey(
		PeriodoContable,
		verbose_name='Períodos contables',
        on_delete=models.SET_NULL,
        blank=False,
        null =True
	)
	id_cuenta = models.ManyToManyField(
		Cuenta,
		help_text='Cuenta que sera saldada',
        error_messages={
            'select': 'Debe seleccionar uno de la lista'
        }, 
        blank=True
	)
	monto_saldo = models.DecimalField(
        verbose_name='Saldo',
        max_digits=100,
        decimal_places=2,
        blank=False,
        validators=[
            MinValueValidator(
                0, 
                message="La cantidad debe ser positiva"
            )
        ], 
	)
	is_saldo_acreedor =models.BooleanField(
		verbose_name='¿Es un saldo acreedor?',
        blank=False,
        default=False,
        help_text="Defina si el saldo de la cuenta es acreedor o deudor"
	)
	
	class Meta:
		ordering = ["id_mayorizacion","id_perido_contable"]
		verbose_name = "Mayorizacion"
		verbose_name_plural = "Mayorizaciones"


class Transaccion(models.Model):
	id_transaccion = models.AutoField(
		primary_key = True
	)
	id_perido_contable = models.ForeignKey(
		PeriodoContable,
		verbose_name='Período Contable',
        on_delete=models.SET_NULL,
        blank=False,
        null = True
	)
	numero_transaccion = models.IntegerField(
		verbose_name='Número de transacción', 
        blank=True,
        null=True,
        help_text="Debe ingresar el número de transacción a realizar",
        error_messages={
            'value':'Debe ser un código mayor a 1'
        },
        validators=[
            MinValueValidator(1)
        ]
	)	
	fecha_transaccion = models.DateTimeField(
		verbose_name='Fecha de transacción',
        auto_now=True,
        help_text='Fecha en que se realiza la transacción',
        error_messages={
            'empty': 'Este campo no debe quedar vacío'
        },
        null=True, 
        blank=False
	)
	descripcion_transaccion = models.CharField(
		max_length = 100,
		verbose_name='Descripción de la transacción',
        blank=False,
        null=True,
        help_text="Ingrese la descripción de la transacción realizada",
        error_messages={
            'empty': 'Este campo no debe quedar vacío'
        }
	)
	monto_transaccion = models.DecimalField(
        verbose_name='Monto de la transacción',
        max_digits=100,
        decimal_places=2,
        blank=False,
        null= True,
        validators=[
            MinValueValidator(
                0, 
                message="La cantidad debe ser positiva"
            )
        ],
	)	
	
	def __str__(self):
		return self.numero_transaccion

	class Meta:
		ordering = ["fecha_transaccion", "numero_transaccion"]
		verbose_name = "Transacción"
		verbose_name_plural = "Transacciones"

class Movimiento(models.Model):
	id_movimiento = models.AutoField(
		primary_key = True
	)
	id_transaccion = models.ForeignKey(
		Transaccion,
		verbose_name='Transaccion',
        on_delete=models.SET_NULL,
        blank=False,
        null=True
	)
	id_cuenta = models.ForeignKey(
		Cuenta,
		verbose_name='Cuenta',
        on_delete=models.SET_NULL,
        blank=False,
        null=True
	)
	id_mayorizacion = models.ForeignKey(
		Mayorizacion,
		verbose_name='Mayorizacion',
		on_delete=models.SET_NULL,
		blank=False,
		null=True
	)
	monto_cargo = models.DecimalField(
        verbose_name='Monto cargo',
        max_digits=100,
        decimal_places=2,
        blank=False,
        null=True,
        validators=[
            MinValueValidator(
                0, 
                message="La cantidad debe ser positiva"
            )
        ],
	)
	monto_abono = models.DecimalField(
		verbose_name='Monto abono',
        max_digits=100,
        decimal_places=2,
        blank=False,
        null=True,
        validators=[
            MinValueValidator(
                0, 
                message="La cantidad debe ser positiva"
            )
        ],
	)
	
	class Meta:
		ordering = ["id_transaccion", "id_movimiento"]
		verbose_name = "Movimiento"
		verbose_name_plural = "Movimientos"
												