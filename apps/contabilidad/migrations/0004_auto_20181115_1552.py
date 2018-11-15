# Generated by Django 2.1.2 on 2018-11-15 21:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contabilidad', '0003_auto_20181114_0011'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='empresa',
            options={'ordering': ['nombre_empresa'], 'verbose_name': 'Empresa', 'verbose_name_plural': 'Empresas'},
        ),
        migrations.AlterModelOptions(
            name='rubro',
            options={'ordering': ['codigo_rubro'], 'verbose_name': 'Rubro', 'verbose_name_plural': 'Rubros'},
        ),
        migrations.AddField(
            model_name='catalogo',
            name='nombre_catalogo',
            field=models.CharField(default='Catalogo', help_text='Nombre del catalogo', max_length=30, verbose_name='Nombre del catalogo'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='rubro',
            name='rubro_sup',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='contabilidad.Rubro', verbose_name='Rubro'),
        ),
    ]
