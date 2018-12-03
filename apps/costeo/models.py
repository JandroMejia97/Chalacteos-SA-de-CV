from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator

class RequisionMaterial(models.Model):
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

class MateriaPrima(models.Model):


class OrdenFabricacion(models.Model)
