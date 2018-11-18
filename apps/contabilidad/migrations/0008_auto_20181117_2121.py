# Generated by Django 2.1.2 on 2018-11-18 03:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contabilidad', '0007_cuenta_codigo_cuenta_padre'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cuenta',
            name='nombre_cuenta',
            field=models.CharField(error_messages={'empty': 'Este campo no debe quedar vacío'}, help_text='Ingrese el nombre de la cuenta', max_length=100, null=True, verbose_name='Nombre de la cuenta'),
        ),
    ]
