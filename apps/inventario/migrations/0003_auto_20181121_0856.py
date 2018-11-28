# Generated by Django 2.0 on 2018-11-21 14:56

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0002_auto_20181119_2219'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detalle',
            name='cantidad_detalle',
            field=models.DecimalField(decimal_places=2, help_text='Ingrese cantidad del producto o materia prima', max_digits=1000, validators=[django.core.validators.MinValueValidator(0, message='Este campo debe ser positivo')], verbose_name='Cantidad'),
        ),
    ]