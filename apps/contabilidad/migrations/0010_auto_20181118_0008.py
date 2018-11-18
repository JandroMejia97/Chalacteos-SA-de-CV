# Generated by Django 2.1.2 on 2018-11-18 06:08

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contabilidad', '0009_auto_20181117_2343'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movimiento',
            name='id_cuenta',
            field=models.ForeignKey(help_text='Seleccione una de las cuentas a afectar', null=True, on_delete=django.db.models.deletion.SET_NULL, to='contabilidad.Cuenta', verbose_name='Cuenta'),
        ),
        migrations.AlterField(
            model_name='movimiento',
            name='monto_abono',
            field=models.DecimalField(decimal_places=2, help_text='Ingrese el monto a abonar (en doláres estadounidenses) a la cuenta seleccionada', max_digits=100, null=True, validators=[django.core.validators.MinValueValidator(0.01, message='La cantidad debe ser positiva')], verbose_name='Monto abono'),
        ),
        migrations.AlterField(
            model_name='movimiento',
            name='monto_cargo',
            field=models.DecimalField(decimal_places=2, help_text='Ingrese el monto a cargar (en doláres estadounidenses) en la cuenta seleccionada', max_digits=100, null=True, validators=[django.core.validators.MinValueValidator(0.01, message='La cantidad debe ser positiva')], verbose_name='Monto cargo'),
        ),
    ]