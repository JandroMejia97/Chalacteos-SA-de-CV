from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Empresa(models.Model):
    id_empresa = models.AutoField(
        primary_key=True
    )
    nic = models.CharField(
        max_length=20,
        verbose_name='NIC',
    )
    nombre = models.CharField(
        verbose_name='Nombre de la empresa',
        max_length=50, 
        null=False, 
        blank=False
    )
    ncr = models.CharField(
        verbose_name='NCR',
        max_length=50, 
        null=False, 
        blank=False
    )

    class Meta:
        verbose_name = 'Empresa'
        verbose_name_plural = 'Empresas'
        unique_together = ("nic", "nombre")
        ordering= ["id_empresa"]

    def __str__(self):
        return '%s' % (self.nombre)


class Departamento(models.Model):
    id_departamento = models.AutoField(
        primary_key=True
    )
    empresa = models.ForeignKey(
        Empresa,
        verbose_name='Empresa',
        on_delete=models.DO_NOTHING,
        blank=False,
        default=0,
        null=False
    )
    nombre = models.CharField(
        verbose_name='Nombre del Departamento',
        max_length=40,
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
        verbose_name = 'Departamento'
        verbose_name_plural = 'Departamentos'
        unique_together = ("id_departamento", "nombre")
        ordering= ["id_departamento"]

    def __str__(self):
        return '%s' % (self.nombre)

class Puesto(models.Model):
    id_puesto = models.AutoField(
        primary_key=True
    )
    departamento = models.ForeignKey(
        Departamento,
        verbose_name='Departamento',
        on_delete=models.DO_NOTHING,
        blank=False,
        default=0,
        null=False,
        help_text='Seleccione el departamento'
    )
    codigo_puesto = models.CharField(
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
        validators=[
            MinValueValidator(
                0, 
                message='Este campo debe ser positivo'
            )
        ],
        help_text='Ingrese el salario para este puesto'
    )

    class Meta:
        verbose_name = 'Puesto'
        verbose_name_plural = 'Puestos'
        unique_together = ("codigo_puesto", "nombre_funcional")
        ordering= ["id_puesto"]
 

    def __str__(self):
        return ' %s' % (self.nombre_funcional)


class Empleado(models.Model):
    empleado = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )
    puesto = models.ForeignKey(
        Puesto,
        verbose_name='Puesto',
        on_delete=models.DO_NOTHING,
        blank=False,
        null=True
    )
    dui = models.CharField(
        verbose_name='DUI',
        max_length=10, 
        null=True, 
        blank=False,
        help_text='Ingrese el Documento Único de Identidad del empleado' 
    )
    fecha_nacimiento = models.DateField(
        verbose_name='Fecha de nacimiento',
        null=True, 
        blank=False,
        help_text='Ingrese el segundo apellido de la persona' 
    )
    telefono = models.IntegerField(
        verbose_name='Numero de telefono',
        null=True, 
        blank=False,
        help_text='Ingrese el telefono'
    )
    direccion = models.CharField(
        verbose_name='Direccion',
        max_length=50,
        help_text='Ingrese la direccion',
        null=True
    )
    is_active = models.BooleanField(
        verbose_name='¿El empleado está de alta?',
        default=True,
        help_text='Active esta casilla para mantener de alta al empleado'
    )

    class Meta:
        verbose_name = 'Empleado'
        verbose_name_plural = 'Empleados'
        ordering= ["puesto", 'dui']

    def __str__(self):
        return '%s %s' % (self.empleado.first_name, self.empleado.last_name)

    """@receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Empleado.objects.create(empleado=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.empleado.save()"""
