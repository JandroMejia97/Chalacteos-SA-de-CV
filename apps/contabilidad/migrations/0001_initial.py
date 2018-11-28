from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Catalogo',
            fields=[
                ('id_catalogo', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_catalogo', models.CharField(help_text='Ingrese el nombre del catalogo', max_length=30, verbose_name='Nombre del catalogo')),
            ],
        ),
        migrations.CreateModel(
            name='Cuenta',
            fields=[
                ('id_cuenta', models.AutoField(primary_key=True, serialize=False)),
                ('codigo_cuenta', models.IntegerField(error_messages={'value': 'Debe ser un código mayor o igual a 1'}, help_text='Debe ingresar el código de la cuenta dependiendo de su ubicación en el catálogo', null=True, validators=[django.core.validators.MinValueValidator(1)], verbose_name='Código de la cuenta')),
                ('nombre_cuenta', models.CharField(error_messages={'empty': 'Este campo no debe quedar vacío'}, help_text='Ingrese el nombre de la cuenta', max_length=100, null=True, verbose_name='Nombre de la cuenta')),
                ('is_cuenta_acreedora', models.BooleanField(default=False, help_text='Marque este campo sí y solo sí la cuenta es de naturaleza acreedora', verbose_name='¿Es cuenta de naturaleza acreedora?')),
                ('is_alta', models.BooleanField(default=True, help_text='Marque esta casilla sí y solo sí la cuenta está en uso', verbose_name='¿Está de alta?')),
                ('codigo_cuenta_padre', models.ForeignKey(blank=True, help_text='Seleccione la cuenta a la que pertenece esta subcuenta', null=True, on_delete=django.db.models.deletion.SET_NULL, to='contabilidad.Cuenta', verbose_name='Cuenta Padre')),
            ],
            options={
                'verbose_name': 'Cuenta',
                'verbose_name_plural': 'Cuentas',
                'ordering': ['id_rubro', 'codigo_cuenta'],
            },
        ),
        migrations.CreateModel(
            name='Empresa',
            fields=[
                ('id_empresa', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_empresa', models.CharField(help_text='Ingrese el nombre de la empresa', max_length=30, verbose_name='Nombre de la Empresa')),
                ('id_catalogo', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='contabilidad.Catalogo', verbose_name='Catálogo')),
                ('id_usuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Usuario')),
            ],
            options={
                'verbose_name': 'Empresa',
                'verbose_name_plural': 'Empresas',
                'ordering': ['nombre_empresa'],
            },
        ),
        migrations.CreateModel(
            name='EstadoFinanciero',
            fields=[
                ('id_estado_financiero', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_estado_financiero', models.CharField(error_messages={'empty': 'Este campo no debe quedar vacío'}, help_text='Nombre del Estado Financiero', max_length=45, verbose_name='Estado Financiero')),
                ('id_cuenta', models.ManyToManyField(blank=True, error_messages={'select': 'Debe seleccionar uno de la lista'}, help_text='Cuenta que sera saldada', to='contabilidad.Cuenta')),
                ('id_empresa', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='contabilidad.Empresa', verbose_name='Empresa')),
            ],
            options={
                'verbose_name': 'Estado Financiero',
                'verbose_name_plural': 'Estados Financieros',
                'ordering': ['id_perido_contable', 'nombre_estado_financiero'],
            },
        ),
        migrations.CreateModel(
            name='Mayorizacion',
            fields=[
                ('id_mayorizacion', models.AutoField(primary_key=True, serialize=False)),
                ('monto_saldo', models.DecimalField(decimal_places=2, max_digits=100, validators=[django.core.validators.MinValueValidator(0, message='La cantidad debe ser positiva')], verbose_name='Saldo')),
                ('is_saldo_acreedor', models.BooleanField(default=False, help_text='Defina si el saldo de la cuenta es acreedor o deudor', verbose_name='¿Es un saldo acreedor?')),
                ('id_cuenta', models.ManyToManyField(blank=True, error_messages={'select': 'Debe seleccionar uno de la lista'}, help_text='Cuenta que sera saldada', to='contabilidad.Cuenta')),
            ],
            options={
                'verbose_name': 'Mayorizacion',
                'verbose_name_plural': 'Mayorizaciones',
                'ordering': ['id_mayorizacion', 'id_perido_contable'],
            },
        ),
        migrations.CreateModel(
            name='Movimiento',
            fields=[
                ('id_movimiento', models.AutoField(primary_key=True, serialize=False)),
                ('monto_cargo', models.DecimalField(decimal_places=2, help_text='Ingrese el monto a cargar (en doláres estadounidenses) en la cuenta seleccionada.<strong><br>NOTA: El monto de cumplir partida doble y ser congruente con la transacción registrada</strong>', max_digits=100, null=True, validators=[django.core.validators.MinValueValidator(0.01, message='La cantidad debe ser positiva')], verbose_name='Monto cargo')),
                ('monto_abono', models.DecimalField(decimal_places=2, help_text='Ingrese el monto a abonar (en doláres estadounidenses) a la cuenta seleccionada. <strong><br>NOTA: El monto de cumplir partida doble y ser congruente con la transacción registrada</strong>', max_digits=100, null=True, validators=[django.core.validators.MinValueValidator(0.01, message='La cantidad debe ser positiva')], verbose_name='Monto abono')),
                ('id_cuenta', models.ForeignKey(help_text='Seleccione una de las cuentas a afectar', null=True, on_delete=django.db.models.deletion.SET_NULL, to='contabilidad.Cuenta', verbose_name='Cuenta')),
                ('id_mayorizacion', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='contabilidad.Mayorizacion', verbose_name='Mayorizacion')),
            ],
            options={
                'verbose_name': 'Movimiento',
                'verbose_name_plural': 'Movimientos',
                'ordering': ['id_transaccion', 'id_movimiento'],
            },
        ),
        migrations.CreateModel(
            name='PeriodoContable',
            fields=[
                ('id_periodo_contable', models.AutoField(primary_key=True, serialize=False)),
                ('fecha_inicio_periodo', models.DateTimeField(error_messages={'empty': 'Este campo no debe quedar vacío'}, help_text='Fecha de inicio del nuevo período contable', null=True, verbose_name='Fecha de inicio')),
                ('fecha_final_periodo', models.DateTimeField(error_messages={'empty': 'Este campo no debe quedar vacío'}, help_text='Fecha de finalización del período contable', null=True, verbose_name='Fecha de finalización')),
            ],
            options={
                'verbose_name': 'Período Contable',
                'verbose_name_plural': 'Períodos Contables',
                'ordering': ['id_periodo_contable'],
            },
        ),
        migrations.CreateModel(
            name='Rubro',
            fields=[
                ('id_rubro', models.AutoField(primary_key=True, serialize=False)),
                ('codigo_rubro', models.CharField(error_messages={'value': 'El código del rubro no debe ser menor a 1'}, help_text='Ingrese el código del rubro', max_length=8, validators=[django.core.validators.MinLengthValidator(1), django.core.validators.MaxLengthValidator(8)], verbose_name='Código del rubro')),
                ('nombre_rubro', models.CharField(help_text='Ingrese el nombre del rubro', max_length=100, verbose_name='Nombre del rubro')),
                ('nivel', models.IntegerField(error_messages={'value': 'El nivel del rubro no debe ser menor a 1, ni mayor a 3'}, help_text='Ingrese el nivel del rubro. Ejemplo: Activo -> Es Nivel 1, Efectivo -> Es Nivel 2', null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(31)], verbose_name='Nivel del rubro')),
                ('id_catalogo', models.ForeignKey(help_text='Seleccione el catalogo al que pertenece este rubro', null=True, on_delete=django.db.models.deletion.SET_NULL, to='contabilidad.Catalogo', verbose_name='Catálogo')),
                ('rubro_sup', models.ForeignKey(blank=True, help_text='Seleccione el rubro al que pertenece este subrubro', null=True, on_delete=django.db.models.deletion.SET_NULL, to='contabilidad.Rubro', verbose_name='Rubro')),
            ],
            options={
                'verbose_name': 'Rubro',
                'verbose_name_plural': 'Rubros',
                'ordering': ['codigo_rubro'],
            },
        ),
        migrations.CreateModel(
            name='TipoTransaccion',
            fields=[
                ('id_tipo', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_tipo', models.CharField(error_messages={'empty': 'Este campo no debe quedar vacío'}, help_text='Ingrese el nombre del tipo de transacción a realizar', max_length=100, null=True, verbose_name='Nombre del tipo de transacción')),
                ('descripcion_tipo', models.CharField(error_messages={'empty': 'Este campo no debe quedar vacío'}, help_text='Ingrese la descripción del tipo de transacción a realizar', max_length=100, null=True, verbose_name='Descripción del tipo transacción')),
            ],
            options={
                'verbose_name': 'Tipo de Transacción',
                'verbose_name_plural': 'Tipos de transacciones',
                'ordering': ['id_tipo', 'nombre_tipo'],
            },
        ),
        migrations.CreateModel(
            name='Transaccion',
            fields=[
                ('id_transaccion', models.AutoField(primary_key=True, serialize=False)),
                ('numero_transaccion', models.IntegerField(blank=True, error_messages={'value': 'Debe ser un código mayor a 1'}, help_text='Debe ingresar el número de transacción a realizar', null=True, validators=[django.core.validators.MinValueValidator(1)], verbose_name='Número de transacción')),
                ('fecha_transaccion', models.DateTimeField(auto_now=True, error_messages={'empty': 'Este campo no debe quedar vacío'}, help_text='Fecha en que se realiza la transacción', null=True, verbose_name='Fecha de transacción')),
                ('descripcion_transaccion', models.CharField(error_messages={'empty': 'Este campo no debe quedar vacío'}, help_text='Ingrese la descripción de la transacción realizada', max_length=100, null=True, verbose_name='Descripción de la transacción')),
                ('monto_transaccion', models.DecimalField(decimal_places=2, help_text='Ingrese el monto en doláres estadounidenses de la transacción a registrar', max_digits=100, null=True, validators=[django.core.validators.MinValueValidator(0.01, message='La cantidad debe ser positiva')], verbose_name='Monto de la transacción')),
                ('id_perido_contable', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='contabilidad.PeriodoContable', verbose_name='Período Contable')),
                ('id_tipo', models.ForeignKey(help_text='Seleccione el tipo de transacción a registrar', null=True, on_delete=django.db.models.deletion.SET_NULL, to='contabilidad.TipoTransaccion', verbose_name='Tipo de Transacción')),
            ],
            options={
                'verbose_name': 'Transacción',
                'verbose_name_plural': 'Transacciones',
                'ordering': ['fecha_transaccion', 'numero_transaccion'],
            },
        ),
        migrations.AddField(
            model_name='movimiento',
            name='id_transaccion',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='contabilidad.Transaccion', verbose_name='Transaccion'),
        ),
        migrations.AddField(
            model_name='mayorizacion',
            name='id_perido_contable',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='contabilidad.PeriodoContable', verbose_name='Períodos contables'),
        ),
        migrations.AddField(
            model_name='estadofinanciero',
            name='id_perido_contable',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='contabilidad.PeriodoContable', verbose_name='Período Contable'),
        ),
        migrations.AddField(
            model_name='estadofinanciero',
            name='id_usuario',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Usuario'),
        ),
        migrations.AddField(
            model_name='cuenta',
            name='id_rubro',
            field=models.ForeignKey(help_text='Seleccion el rubro al que pertenece la cuenta', null=True, on_delete=django.db.models.deletion.SET_NULL, to='contabilidad.Rubro', verbose_name='Rubro'),
        ),
    ]
