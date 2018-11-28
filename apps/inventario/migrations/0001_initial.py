import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id_cliente', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_cliente', models.CharField(help_text='Nombre del cliente', max_length=50, verbose_name='Cliente')),
                ('nombre_titular_cliente', models.CharField(help_text='Nombre del titular del cliente', max_length=50, verbose_name='Titular')),
            ],
            options={
                'verbose_name': 'Cliente',
                'verbose_name_plural': 'Clientes',
                'ordering': ['nombre_titular_cliente', 'nombre_cliente'],
            },
        ),
        migrations.CreateModel(
            name='Compra',
            fields=[
                ('id_compra', models.AutoField(primary_key=True, serialize=False)),
            ],
            options={
                'verbose_name': 'Compra',
                'verbose_name_plural': 'Compras',
                'ordering': ['id_factura', 'id_proveedor'],
            },
        ),
        migrations.CreateModel(
            name='Detalle',
            fields=[
                ('id_detalle', models.AutoField(primary_key=True, serialize=False)),
                ('cantidad_detalle', models.DecimalField(decimal_places=2, help_text='Ingrese cantidad del producto o materia prima', max_digits=1000, validators=[django.core.validators.MinValueValidator(0, message='Este campo debe ser positivo')], verbose_name='Cantidad')),
            ],
            options={
                'verbose_name': 'Detalle de Factura',
                'verbose_name_plural': 'Detalles de Facturas',
                'ordering': ['id_materia_prima', 'id_producto', 'cantidad_detalle'],
            },
        ),
        migrations.CreateModel(
            name='Factura',
            fields=[
                ('id_factura', models.AutoField(primary_key=True, serialize=False)),
                ('sub_total_factura', models.DecimalField(decimal_places=2, help_text='Ingrese el sub total antes de impuestos', max_digits=1000, validators=[django.core.validators.MinValueValidator(0, message='Este campo debe ser positivo')], verbose_name='Sub Total')),
                ('total_factura', models.DecimalField(decimal_places=2, help_text='Ingrese el total (impuestos incluídos)', max_digits=1000, validators=[django.core.validators.MinValueValidator(0, message='Este campo debe ser positivo')], verbose_name='Total')),
                ('estado_factura', models.CharField(help_text='Estado de la fatura: Despachada, Pendiente de pago, Pendiente de entrada, Entregada', max_length=20, verbose_name='Estado de la Factura')),
                ('monto_aplicacion', models.DecimalField(decimal_places=2, help_text='Ingrese el recargo por el impuesto a la compra o venta', max_digits=1000, validators=[django.core.validators.MinValueValidator(0, message='Este campo debe ser positivo')], verbose_name='Monto Aplicado')),
            ],
            options={
                'verbose_name': 'Factura',
                'verbose_name_plural': 'Facturas',
                'ordering': ['estado_factura', 'total_factura'],
            },
        ),
        migrations.CreateModel(
            name='FacturaImpuesto',
            fields=[
                ('id_aplicacion', models.AutoField(primary_key=True, serialize=False)),
                ('monto_aplicacion', models.DecimalField(decimal_places=2, help_text='Ingrese el recargo por el impuesto a la compra o venta', max_digits=1000, validators=[django.core.validators.MinValueValidator(0, message='Este campo debe ser positivo')], verbose_name='Monto Aplicado')),
                ('id_factura', models.ForeignKey(help_text='Seleccione la factura que se aplicara en la factura con impuesto', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='inventario.Factura', verbose_name='Factura')),
            ],
            options={
                'verbose_name': 'Factura - Impuesto',
                'verbose_name_plural': 'Facturas - Impuestos',
                'ordering': ['id_factura', 'id_impuesto'],
            },
        ),
        migrations.CreateModel(
            name='Impuesto',
            fields=[
                ('id_impuesto', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_impuesto', models.CharField(help_text='Ingrese el nombre del impuesto', max_length=75, verbose_name='Nombre del Impuesto')),
                ('descripcion_impuesto', models.CharField(help_text='Breve descripcion del impuesto', max_length=250, verbose_name='Descripción')),
                ('tasa_impuesto', models.DecimalField(decimal_places=6, help_text='Ingrese la tasa que se le aplica al total de la transacción', max_digits=1000, validators=[django.core.validators.MinValueValidator(0, message='Este campo debe ser positivo'), django.core.validators.MaxValueValidator(2.0, message='La tasa a lo sumo debe ser menor a 1.0')], verbose_name='Tasa de impuesto')),
            ],
            options={
                'verbose_name': 'Impuesto',
                'verbose_name_plural': 'Impuestos',
                'ordering': ['nombre_impuesto', 'tasa_impuesto'],
            },
        ),
        migrations.CreateModel(
            name='Kardex',
            fields=[
                ('id_kardex', models.AutoField(primary_key=True, serialize=False)),
            ],
            options={
                'verbose_name': 'Kardex',
                'verbose_name_plural': 'Kardexs',
                'ordering': ['id_recurso'],
            },
        ),
        migrations.CreateModel(
            name='MateriaPrima',
            fields=[
                ('id_materia_prima', models.AutoField(primary_key=True, serialize=False)),
            ],
            options={
                'verbose_name': 'Materia Prima',
                'verbose_name_plural': 'Materias Primas',
                'ordering': ['id_proveedor', 'id_recurso'],
            },
        ),
        migrations.CreateModel(
            name='Movimiento',
            fields=[
                ('id_movimiento', models.AutoField(primary_key=True, serialize=False)),
                ('fecha_movimiento', models.DateTimeField(auto_now=True, help_text='Ingrese en que se realizo fecha del movimiento', verbose_name='Fecha')),
                ('cantidad_movimiento', models.DecimalField(decimal_places=2, help_text='Ingrese la cantidad actual del producto o materia prima', max_digits=1000, validators=[django.core.validators.MinValueValidator(0, message='Este campo debe ser positivo')], verbose_name='Cantidad')),
                ('costo_unitario_movimiento', models.DecimalField(decimal_places=2, help_text='Ingrese el costo unitario del producto o materia prima', max_digits=1000, validators=[django.core.validators.MinValueValidator(0, message='Este campo debe ser positivo')], verbose_name='Costo Unitario')),
                ('monto_movimiento', models.DecimalField(decimal_places=2, help_text='Este campo es auto generado', max_digits=1000, validators=[django.core.validators.MinValueValidator(0, message='Este campo debe ser positivo')], verbose_name='Monto')),
                ('is_Input', models.BooleanField(default=True, help_text='Defina si esta transacción es una entrada o salida de materia prima o producto', verbose_name='¿Es una entrada?')),
                ('id_kardex', models.ForeignKey(help_text='Seleccion el kardex que posee el movimiento', on_delete=django.db.models.deletion.DO_NOTHING, to='inventario.Kardex', verbose_name='Kardex')),
            ],
            options={
                'verbose_name': 'Movimiento',
                'verbose_name_plural': 'Movimientos',
                'ordering': ['-fecha_movimiento'],
                'get_latest_by': 'fecha_movimiento',
            },
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id_producto', models.AutoField(primary_key=True, serialize=False)),
            ],
            options={
                'verbose_name': 'Producto',
                'verbose_name_plural': 'Productos',
                'ordering': ['id_producto', 'id_recurso'],
            },
        ),
        migrations.CreateModel(
            name='Proveedor',
            fields=[
                ('id_proveedor', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_proveedor', models.CharField(help_text='Nombre del proveedor', max_length=50, verbose_name='Proveedor')),
                ('nombre_titular_proveedor', models.CharField(help_text='Nombre del titular del proveedor', max_length=50, verbose_name='Titular')),
            ],
            options={
                'verbose_name': 'Proveedor',
                'verbose_name_plural': 'Proveedores',
                'ordering': ['nombre_titular_proveedor', 'nombre_proveedor'],
            },
        ),
        migrations.CreateModel(
            name='Recurso',
            fields=[
                ('id_recurso', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_recurso', models.CharField(help_text='Nombre del recurso, sea este materia prima o producto', max_length=50, verbose_name='Nombre del recurso')),
                ('descripcion_recurso', models.CharField(help_text='Una breve descripción del recurso', max_length=250, verbose_name='Descripción del recurso')),
            ],
            options={
                'verbose_name': 'Recurso',
                'verbose_name_plural': 'Recursos',
                'ordering': ['nombre_recurso'],
            },
        ),
        migrations.CreateModel(
            name='Saldo',
            fields=[
                ('id_saldor', models.AutoField(primary_key=True, serialize=False)),
                ('cantidad_saldo', models.DecimalField(decimal_places=2, help_text='Ingrese la cantidad actual del producto o materia prima', max_digits=1000, validators=[django.core.validators.MinValueValidator(0, message='Este campo debe ser positivo')], verbose_name='Cantidad')),
                ('costo_unitario_saldo', models.DecimalField(decimal_places=2, help_text='Ingrese el costo unitario del producto o materia prima', max_digits=1000, validators=[django.core.validators.MinValueValidator(0, message='Este campo debe ser positivo')], verbose_name='Costo Unitario')),
                ('monto_saldo', models.DecimalField(decimal_places=2, help_text='Este campo es auto generado', max_digits=1000, validators=[django.core.validators.MinValueValidator(0, message='Este campo debe ser positivo')], verbose_name='Monto')),
                ('id_movimiento', models.OneToOneField(help_text='Seleccion el movimiento al que le corresponde el saldo', on_delete=django.db.models.deletion.DO_NOTHING, to='inventario.Movimiento')),
            ],
            options={
                'verbose_name': 'Saldo',
                'verbose_name_plural': 'Saldos',
                'ordering': ['id_movimiento'],
            },
        ),
        migrations.CreateModel(
            name='Venta',
            fields=[
                ('id_venta', models.AutoField(primary_key=True, serialize=False)),
                ('id_cliente', models.ForeignKey(help_text='Seleccion el cliente al que le pertenece la venta', on_delete=django.db.models.deletion.DO_NOTHING, to='inventario.Cliente', verbose_name='Cliente')),
                ('id_factura', models.ForeignKey(help_text='Seleccion la factura al que le pertenece la venta', on_delete=django.db.models.deletion.DO_NOTHING, to='inventario.Factura', verbose_name='Factura')),
            ],
            options={
                'verbose_name': 'Venta',
                'verbose_name_plural': 'Ventas',
                'ordering': ['id_factura', 'id_cliente'],
            },
        ),
        migrations.AddField(
            model_name='producto',
            name='id_recurso',
            field=models.OneToOneField(help_text='Seleccione el recurso del producto', on_delete=django.db.models.deletion.CASCADE, to='inventario.Recurso', verbose_name='Recurso'),
        ),
        migrations.AddField(
            model_name='materiaprima',
            name='id_proveedor',
            field=models.ForeignKey(help_text='Seleccion el proveedor al que le pertenece la compra', on_delete=django.db.models.deletion.DO_NOTHING, to='inventario.Proveedor', verbose_name='Proveedor'),
        ),
        migrations.AddField(
            model_name='materiaprima',
            name='id_proveedor',
            field=models.ForeignKey(help_text='Seleccion el proveedor al que le pertenece la compra', on_delete=django.db.models.deletion.DO_NOTHING, to='inventario.Proveedor', verbose_name='Proveedor'),
        ),
        migrations.AddField(
            model_name='materiaprima',
            name='id_recurso',
            field=models.OneToOneField(help_text='Seleccion el recurso para la kardex', on_delete=django.db.models.deletion.CASCADE, to='inventario.Recurso', verbose_name='Recurso'),
        ),
        migrations.AddField(
            model_name='kardex',
            name='id_recurso',
            field=models.OneToOneField(help_text='Seleccion el recurso del que esta compuesto el kardex', on_delete=django.db.models.deletion.DO_NOTHING, to='inventario.Recurso', verbose_name='Recurso'),
        ),
        migrations.AddField(
            model_name='facturaimpuesto',
            name='id_impuesto',
            field=models.ForeignKey(help_text='Seleccione el impuesto que se aplicara a la factura con impuesto', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='inventario.Impuesto', verbose_name='Impuesto'),
        ),
        migrations.AddField(
            model_name='detalle',
            name='id_factura',
            field=models.ForeignKey(help_text='Seleccione la factura que pertenece el detalle', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='inventario.Factura', verbose_name='Factura'),
        ),
        migrations.AddField(
            model_name='detalle',
            name='id_materia_prima',
            field=models.ForeignKey(help_text='Seleccion la materia prima que contiene el detalle', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='inventario.MateriaPrima', verbose_name='Materia Prima'),
        ),
        migrations.AddField(
            model_name='detalle',
            name='id_producto',
            field=models.ForeignKey(help_text='Seleccion el producto que contiene el detalle', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='inventario.Producto', verbose_name='Producto'),
        ),
        migrations.AddField(
            model_name='compra',
            name='id_factura',
            field=models.ForeignKey(help_text='Seleccion la factura al que le pertenece la venta', on_delete=django.db.models.deletion.DO_NOTHING, to='inventario.Factura', verbose_name='Factura'),
        ),
        migrations.AddField(
            model_name='compra',
            name='id_proveedor',
            field=models.ForeignKey(help_text='Seleccion el proveedor al que le pertenece la compra', on_delete=django.db.models.deletion.DO_NOTHING, to='inventario.Proveedor', verbose_name='Proveedor'),
        ),
    ]
