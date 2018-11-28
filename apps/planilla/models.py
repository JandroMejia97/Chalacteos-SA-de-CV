from django.db import models

# Create your models here.


class Empresa(models.Model):
	id = models.AutoField(primary_key=True)
	nic = models.CharField(max_length=20)
	nombre = models.CharField(max_length=50, null=False, blank=False)
	ncr = models.CharField(max_length=50, null=False, blank=False)
	calendar = models.IntegerField(null=False, blank=False)

	class Meta:
		unique_together = ("nic", "nombre")
		ordering= ["id"]

	
	def __str__(self):
		return '%s' % (self.ncr)

class Empleado(models.Model):

    id = models.AutoField(primary_key=True)
    dui = models.CharField(max_length=10, null=False, blank=False )
    primer_nombre = models.CharField(max_length=30, null=False, blank=False)
    segundo_nombre = models.CharField(max_length=30, null=False, blank=False)
    primer_apellido = models.CharField(max_length=20,null=False, blank=False)
    segundo_apellido = models.CharField(max_length=20, null = True, blank=True )
    fecha_nacimiento = models.DateField(null=False, blank=False)
    
    codigo = models.CharField(max_length=10)
    telefono = models.IntegerField(null=False, blank=False)
    direccion = models.CharField(max_length=50)
    activo = models.BooleanField()

    class Meta:
    	unique_together = ("dui", "codigo")
    	ordering= ["id"]

    def __str__(self):
    	return ' %s %s %s %s' % ( self.primer_nombre, self.segundo_nombre, self.primer_apellido, self.segundo_apellido)

class Departamento(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=20,null=False, blank=False)
    descripcion = models.TextField(max_length=250,null=True, blank=True)

    class Meta:
        unique_together = ("id", "nombre")
        ordering= ["id"]

    def __str__(self):
        return '%s ' % (self.nombre)



class Puesto(models.Model):
    id = models.AutoField(primary_key=True)
    codigo = models.CharField(max_length=50,null=False, blank=False)
    nombre_funcional = models.CharField(max_length=50, null=False, blank=False)
    descripcion = models.TextField()
    salario_base = models.DecimalField(max_digits=6, decimal_places=2, null=False, blank=False)

    class Meta:
        unique_together = ("codigo", "nombre_funcional")
        ordering= ["id"]
 

    def __str__(self):
        return ' %s ' % (self.nombre_funcional)


class EmpleadoEmpresa(models.Model):
    id = models.AutoField(primary_key=True)
    empleado = models.ForeignKey(Empleado,on_delete=models.CASCADE)
    empresa = models.ForeignKey(Empresa,on_delete=models.CASCADE)

    def __str__(self):
        return '%s %s %s' % (self.empleado.primer_nombre, self.empleado.primer_apellido, self.empresa.ncr)

    class Meta:
        unique_together = ("empleado", "empresa")



class PuestoEmpresa(models.Model):
    id = models.AutoField(primary_key=True)
    puesto = models.ForeignKey(Puesto,on_delete=models.CASCADE)
    empresa = models.ForeignKey(Empresa,on_delete=models.CASCADE)

    def __str__(self):
        return '%s %s' % (self.puesto.nombre_funcional, self.empresa.ncr)

    class Meta:
        unique_together = ("puesto", "empresa")


class DepartamentoEmpresa(models.Model):
    id = models.AutoField(primary_key=True)
    departamento = models.ForeignKey(Departamento,on_delete=models.CASCADE)
    empresa = models.ForeignKey(Empresa,on_delete=models.CASCADE)

    def __str__(self):
        return '%s %s' % (self.departamento.nombre, self.empresa.ncr)

    class Meta:
        unique_together = ("departamento", "empresa")

class Asignacion(models.Model):
    id = models.AutoField(primary_key=True)
    empleado_empresa = models.ForeignKey(EmpleadoEmpresa,on_delete=models.CASCADE) 
    puesto_empresa = models.ForeignKey(PuestoEmpresa,on_delete=models.CASCADE)
    departamento_empresa = models.ForeignKey(DepartamentoEmpresa,on_delete=models.CASCADE)
    salario_asignado = models.DecimalField(max_digits=6, decimal_places=2, null=False, blank=False)
    fecha_asignacion = models.DateField(null=False, blank=False)
    calendario = models.IntegerField(null=False, blank=False)

    def __str__(self):
        return '%s %s %s ' % (self.empleado_empresa.empleado.primer_nombre, self.empleado_empresa.empleado.primer_apellido, self.puesto_empresa.puesto.nombre_funcional)

    class Meta:
        unique_together = ("empleado_empresa", "puesto_empresa")

class DetallePlanilla(models.Model):

    id = models.AutoField(primary_key=True)
    fecha = models.DateField(null=False, blank=False)
    asignacion = models.ForeignKey(Asignacion,on_delete=models.CASCADE)
    empresa = models.ForeignKey(Empresa,on_delete=models.CASCADE)
    dias_trabajados = models.IntegerField()
    descuentos = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    ingresos = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)

    isss_empleado = models.DecimalField(max_digits=6, decimal_places=2,null=False, blank=False)
    isss_patronal = models.DecimalField(max_digits=6, decimal_places=2,null=False, blank=False)
    afp_empleado = models.DecimalField(max_digits=6, decimal_places=2,null=False, blank=False)
    afp_patronal = models.DecimalField(max_digits=6, decimal_places=2,null=False, blank=False)
    renta = models.DecimalField(max_digits=6, decimal_places=2, null=False, blank=False)
    
    aguinaldo = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    vacaciones = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)

    salario_neto = models.DecimalField(max_digits=6, decimal_places=2,null=False, blank=False)
    pago_real = models.DecimalField(max_digits=6, decimal_places=2,null=False, blank=False)

    def __str__(self):
        return '%s %s %s %s %s %s %s' % (self.fecha, self.asignacion, self.dias_trabajados, self.isss_empleado, self.afp_empleado, self.renta, self.salario_neto)

    class Meta:
        unique_together = ("asignacion", "fecha")
        ordering = ["id"]

class Renta(models.Model):
    id = models.AutoField(primary_key=True)
    tipo = models.CharField(max_length=50,null=False, blank=False)
    v1 = models.DecimalField(max_digits=8, decimal_places=2,null=False, blank=False)
    v2 = models.DecimalField(max_digits=8, decimal_places=2,null=False, blank=False)
    porc = models.DecimalField(max_digits=6, decimal_places=2,null=True, blank=True)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return '%s %s ' % (self.id, self.tipo)


