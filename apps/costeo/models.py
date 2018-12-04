from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator

class Requision(models.Model):
	id_requision = models.AutoField(
		primary_key=True
	)
	cantidad_material = models.DecimalField(
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
		help_text="Ingrese la cantidad actual materia prima"
	)
	costo_total_material = models.DecimalField(
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
		help_text="Ingrese la cantidad actual del producto o materia prima"
	)

	def __str__(self):
		return self.id_requision

	class Meta:
		verbose_name = 'RequisionMaterial'
		verbose_name_plural = 'RequisionMateriales'
		ordering = ['id_requision']

class Departamento(models.Model):
	id_departamento = models.AutoField(
		primary_key=True
	)
	nombre_departamento = models.CharField(
		verbose_name='Nombre Departamento',
		blank=False,
		max_length=75,
		help_text="Ingrese el departamento"
	)

	def __str__(self):
		return self.id_departamento

	class Meta:
		verbose_name = 'Departamento'
		verbose_name_plural = 'Departamento'
		ordering = ['id_departamento']


class Producto(models.Model):
	id_producto = models.AutoField(
		primary_key=True
	)
	nombre_producto = models.CharField(
		verbose_name='Nombre del Producto',
		blank=False,
		max_length=75,
		help_text="Ingrese el nombre del producto"
	)
	precio_unitario = models.DecimalField(
		verbose_name='Precio Unitario',
		max_digits=1000,
		decimal_places=2,
		blank=False,
		validators=[
			MinValueValidator(
				0, 
				message="Este campo debe ser positivo"
			)
		],
		help_text="Ingrese el precio unitario del producto"
	)

	def __str__(self):
		return self.id_requision

	class Meta:
		verbose_name = 'Producto'
		verbose_name_plural = 'Productos'
		ordering = ['id_producto']

class ManoObraDirecta(models.Model):
	id_mano_obra_directa = models.AutoField(
		primary_key=True
	)
	monto_mod = models.DecimalField(
		verbose_name='Monto de la mano de obra directa',
		max_digits=1000,
		decimal_places=2,
		blank=False,
		validators=[
			MinValueValidator(
				0, 
				message="Este campo debe ser positivo"
			)
		],
		help_text="Ingrese el salario del empleado"
	)

	def __str__(self):
		return self.id_mano_obra_directa

	class Meta:
		verbose_name = 'ManoObraDirecta'
		verbose_name_plural = 'ManoObraDirecta'
		ordering = ['id_mano_obra_directa']

class CostoIndirectoFabricacion(models.Model):
	id_costo_indirecto = models.AutoField(
		primary_key=True
	)
	tasa = models.DecimalField(
		verbose_name='Tasa del costo indirecta de fabricacion',
		max_digits=1000,
		decimal_places=2,
		blank=False,
		validators=[
			MinValueValidator(
				0, 
				message="Este campo debe ser positivo"
			)
		],
		help_text="Ingrese la tasa del costo indirecta de fabricacion"
	)
	importe = models.DecimalField(
		verbose_name='Importe del costo indirecta de fabricacion',
		max_digits=1000,
		decimal_places=2,
		blank=False,
		validators=[
			MinValueValidator(
				0, 
				message="Este campo debe ser positivo"
			)
		],
		help_text="Ingrese el importe del costo indirecta de fabricacion"
	)

	def __str__(self):
		return self.id_costo_indirecto

	class Meta:
		verbose_name = 'CostoIndirectoFabricacion'
		verbose_name_plural = 'CostoIndirectoFabricacion'
		ordering = ['id_costo_indirecto']


class OrdenFabricacion(models.Model):
	id_orden = models.AutoField(
		primary_key=True
	)
	id_mano_obra_directa = models.OneToOneField(
		ManoObraDirecta,
		verbose_name='ManoObraDirecta',
		on_delete=models.CASCADE,
		blank=False,
		help_text='Seleccione la orden de fabricacion del producto'
	)
	id_costo_indirecto = models.ForeignKey(	
		CostoIndirectoFabricacion,
		verbose_name='CostoIndirectoFabricacion',
		on_delete=models.DO_NOTHING,
		blank=False,
		help_text='Seleccion la orden de fabricacion a la cual se le aplicara el cif'
	)
	id_producto = models.ManyToManyField(
		Producto,
		verbose_name='Producto',
		blank=False,
		help_text='Seleccione el producto ',
		unique=False
	)
	id_departamento = models.ManyToManyField(
		Departamento,
		verbose_name='Departamento',
		blank=False,
		help_text='Seleccione el Ddepartamento ',
		unique=False
	)
	cantidad_orden = models.DecimalField(
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
		help_text="Ingrese la cantidad de ordenes de fabricacion"
	)
	costo_total_orden = models.DecimalField(
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
		help_text="Ingrese la costo total de la orden de fabricacion"
	)

	def __str__(self):
		return self.id_orden

	class Meta:
		verbose_name = 'OrdenFabricacion'
		verbose_name_plural = 'OrdenFabricacion'
		ordering = ['id_orden']


class Empleado(models.Model):
	id_empleado = models.AutoField(
		primary_key=True
	)
	nombre_empledado = models.CharField(
		verbose_name='Nombre Empleado',
		blank=False,
		max_length=75,
		help_text="Ingrese el nombre del empleado"
	)
	salario = models.DecimalField(
		verbose_name='Salario',
		max_digits=1000,
		decimal_places=2,
		blank=False,
		validators=[
			MinValueValidator(
				0, 
				message="Este campo debe ser positivo"
			)
		],
		help_text="Ingrese el salario del empleado"
	)

class BaseAsignacion(models.Model):
	id_base = models.AutoField(
		primary_key=True
	)
	nombre_base = models.CharField(
		verbose_name='Nombre de la Base Asignación',
		blank=False,
		max_length=75,
		help_text="Ingrese el nombre de la base asignación"
	)
	def __str__(self):
		return self.nombre_base

	class Meta:
		verbose_name = 'BaseAsignacion'
		verbose_name_plural = 'BaseAsignaciones'
		ordering = ['nombre_base']

class Gasto(models.Model):
	id_gasto = models.AutoField(
		primary_key=True
	)
	id_base = models.OneToOneField(
		BaseAsignacion,
		verbose_name='BaseAsignacion',
		on_delete=models.CASCADE,
		blank=False,
		help_text='Seleccione la base asignación del gasto'
	)
	def __str__(self):
		return self.id_gasto

	class Meta:
		verbose_name = 'Gasto'
		verbose_name_plural = 'Gastos'
		ordering = ['id_gasto']

class BoletaTrabajo(models.Model):
	id_boleta = models.AutoField(
		primary_key=True
	)
	numero_horas = models.DecimalField(
		verbose_name='Numero de Horas',
		max_digits=1000,
		decimal_places=2,
		blank=False,
		validators=[
			MinValueValidator(
				0, 
				message="Este campo debe ser positivo"
			)
		],
		help_text="Ingrese el numero de horas trabajadas"
	)
	total_horas = models.DecimalField(
		verbose_name='Total de Horas',
		max_digits=1000,
		decimal_places=2,
		blank=False,
		validators=[
			MinValueValidator(
				0, 
				message="Este campo debe ser positivo"
			)
		],
		help_text="Ingrese el total de horas trabjadas"
	)
	def __str__(self):
		return self.id_boleta

	class Meta:
		verbose_name = 'BoletaTrabajo'
		verbose_name_plural = 'BoletaTrabajo'
		ordering = ['id_boleta']

class MateriaPrima(models.Model):
	id_materia_prima = models.AutoField(
		primary_key=True
	)
	id_requision = models.ForeignKey(
		RequisionMaterial,
		verbose_name='RequisionMaterial',
		on_delete=models.DO_NOTHING,
		blank=False,
		help_text='Seleccion la requision a la que pertenece la materia prima'
	)
	id_orden = models.ManyToManyField(
		OrdenFabricacion,
		verbose_name='OrdenFabricacion',
		blank=False,
		help_text='Seleccione la orden',
		unique=False
	)
	id_producto = models.ManyToManyField(
		Producto,
		verbose_name='Producto',
		blank=False,
		help_text='Seleccione el producto ',
		unique=False
	)
	precio_unitario = models.DecimalField(
		verbose_name='Precio Unitario',
		max_digits=1000,
		decimal_places=2,
		blank=False,
		validators=[
			MinValueValidator(
				0, 
				message="Este campo debe ser positivo"
			)
		],
		help_text="Ingrese el precio unitario de la materia prima "
	)
	def __str__(self):
		return self.id_materia_prima

	class Meta:
		verbose_name = 'MateriaPrima'
		verbose_name_plural = 'MateriaPrima'
		ordering = ['id_materia_prima']

