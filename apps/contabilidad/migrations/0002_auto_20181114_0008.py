# Generated by Django 2.1.2 on 2018-11-14 06:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contabilidad', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='rubro',
            options={'ordering': ['rubro_sup', 'codigo_rubro'], 'verbose_name': 'Rubro', 'verbose_name_plural': 'Rubros'},
        ),
        migrations.RenameField(
            model_name='rubro',
            old_name='rub_id_rubro',
            new_name='rubro_sup',
        ),
    ]
