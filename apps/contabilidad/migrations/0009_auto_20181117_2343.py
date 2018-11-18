# Generated by Django 2.1.2 on 2018-11-18 05:43

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contabilidad', '0008_auto_20181117_2121'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaccion',
            name='monto_transaccion',
            field=models.DecimalField(decimal_places=2, help_text='Ingrese el monto en doláres estadounidenses de la transacción a registrar', max_digits=100, null=True, validators=[django.core.validators.MinValueValidator(0.01, message='La cantidad debe ser positiva')], verbose_name='Monto de la transacción'),
        ),
    ]
