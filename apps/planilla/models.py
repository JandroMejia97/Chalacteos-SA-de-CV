from django.db import models

# Create your models here.



class Departamento(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(
        verbose_name='Nombre del Departamento',
        max_length=20,
        null=False, 
        blank=False,
        help_text='Ingrese el nombre del departamento'
    )
    descripcion = models.TextField(
        verbose_name='Descripcion del Departamento',
        max_length=250,
        null=True, 
        blank=True,
        help_text='Ingrese una descripcion del departamento'
    )

    class Meta:
        unique_together = ("id", "nombre")
        ordering= ["id"]

    def __str__(self):
        return '%s ' % (self.nombre)

class Puesto(models.Model):
    id = models.AutoField(primary_key=True)
    id_departamento = models.ForeignKey(
        Departamento,
        verbose_name='Departamento',
        on_delete=models.CASCADE,
        blank=False,
        default=0,
        null=False,
        help_text='Seleccione el departamento'
    )
    codigo = models.CharField(
        verbose_name='Codigo del puesto',
        max_length=50,
        null=False,
        help_text='Ingrese el codigo del puesto',
        blank=False
    )
    nombre_funcional = models.CharField(
        verbose_name='Nombre del Puesto',
        max_length=50, 
        null=False, 
        blank=False,
        help_text='Ingrese el nombre del puesto'
    )
    descripcion = models.TextField(
        verbose_name='Descripcion del Puesto',
        max_length=50, 
        help_text='Ingrese una descripcion del puesto'
    )
    salario_base = models.DecimalField(
        verbose_name='Salario de un Puesto',
        max_digits=6, 
        decimal_places=2, 
        null=False, 
        blank=False,
        help_text='Ingrese el salario para este puesto'
    )

    class Meta:
        unique_together = ("codigo", "nombre_funcional")
        ordering= ["id"]
 

    def __str__(self):
        return ' %s ' % (self.nombre_funcional)

class Empresa(models.Model):
    id = models.AutoField(primary_key=True)
    id_departamento = models.ForeignKey(
        Departamento,
        verbose_name='Departamento',
        on_delete=models.CASCADE,
        blank=False,
        default=0,
        null=False
    )
    nic = models.CharField(max_length=20)
    nombre = models.CharField(
        max_length=50, 
        null=False, 
        blank=False
    )
    ncr = models.CharField(
        max_length=50, 
        null=False, 
        blank=False
    )
    calendar = models.IntegerField(
        null=False, 
        blank=False
    )

    class Meta:
        unique_together = ("nic", "nombre")
        ordering= ["id"]

    def __str__(self):
        return '%s' % (self.ncr)



class Empleado(models.Model):
    id = models.AutoField(primary_key=True)
    id_puesto = models.OneToOneField(
        Puesto,
        verbose_name='Puesto',
        on_delete=models.CASCADE,
        blank=False,
        default=0,
        null=False,
        help_text='Seleccione el puesto de la persona' 
    )
    dui = models.CharField(
        verbose_name='Dui de la persona',
        max_length=10, 
        null=False, 
        blank=False,
        help_text='Ingrese el Dui de la persona' 
    )
    primer_nombre = models.CharField(
        verbose_name='Primer nombre',
        max_length=30, 
        null=False, 
        blank=False,
        help_text='Ingrese el primer nombre de la persona'
    )
    segundo_nombre = models.CharField(
        verbose_name='Segundo nombre',
        max_length=30, 
        null=False, 
        blank=False,
        help_text='Ingrese el segundo nombre de la persona'
    )
    primer_apellido = models.CharField(
        verbose_name='Primer apellido',
        max_length=20,
        null=False, 
        blank=False,
        help_text='Ingrese el primer apellido de la persona'
    )
    segundo_apellido = models.CharField(
        verbose_name='Segundo apellido',
        max_length=20, 
        null = True, 
        blank=True,
        help_text='Ingrese el segundo apellido de la persona' 
    )
    fecha_nacimiento = models.DateField(
        verbose_name='Fecha de nacimiento',
        null=False, 
        blank=False,
        help_text='Ingrese su fecha de nacimiento' 
    )
    codigo = models.CharField(
        verbose_name='Codigo del empleado',
        null=False, 
        blank=False,
        max_length=10,
        help_text='Ingrese su codigo' 
    )
    telefono = models.IntegerField(
        verbose_name='Numero de telefono',
        null=False, 
        blank=False,
        help_text='Ingrese el telefono'
    )
    direccion = models.CharField(
        verbose_name='Direccion',
        max_length=50,
        help_text='Ingrese la direccion'
    )
    activo = models.BooleanField()

    class Meta:
        unique_together = ("dui", "codigo")
        ordering= ["id"]

    def __str__(self):
        return ' %s %s %s %s' % ( self.primer_nombre, self.segundo_nombre, self.primer_apellido, self.segundo_apellido)

