from django.conf.urls import include
from django.urls import reverse_lazy, path, re_path
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from . import views

app_name ='contabilidad'

urlpatterns = [
	re_path(
		'sign-in/',
		views.SignInView.as_view(),
		name='sign-in'
	),
	path(
        'sign-out/',
        views.SignOutView.as_view(),
        name='sign-out'
    ),
	path(
		'',
		views.CuentasListView.as_view(),
		name='cuentas'
	),
	path(
		'crear/cuenta/',
		views.CuentaCreateView.as_view(),
		name='cuenta-crear'
	),
	path(
		'edicion/cuenta/<slug:pk>/',
		views.CuentaUpdateView.as_view(),
		name='cuenta-edicion'
	),
	path(
		'detalle/cuenta/<slug:pk>/',
		views.CuentaDetailView.as_view(),
		name='cuenta-detalle'
	),
	re_path(
        r'ajax/cuenta/(?P<id_cuenta>[0-9]+)/',
        views.cuentas,
        name='ajax-cuenta'
    ),
	path(
		'transacciones/',
		views.TransaccionesListView.as_view(),
		name='transacciones'
	),
	path(
		'crear/transaccion/',
		views.TransaccionCreateView.as_view(),
		name='transaccion-crear'
	),
	path(
		'edicion/transaccion/<slug:pk>/',
		views.TransaccionUpdateView.as_view(),
		name='transaccion-edicion'
	),
	path(
		'detalle/transaccion/<slug:pk>/',
		views.CuentaDetailView.as_view(),
		name='transaccion-detalle'
	),
	re_path(
        r'ajax/transaccion/(?P<id_transaccion>[0-9]+)/',
        views.cuentas,
        name='ajax-transaccion'
    ),
	path(
		'movimientos/',
		views.MovimientosListView.as_view(),
		name='movimientos'
	),
	path(
		'crear/movimiento/',
		views.MovimientoCreateView.as_view(),
		name='movimiento-crear'
	),
	path(
		'edicion/movimiento/<slug:pk>/',
		views.MovimientoUpdateView.as_view(),
		name='movimiento-edicion'
	),
	path(
		'detalle/movimiento/<slug:pk>/',
		views.CuentaDetailView.as_view(),
		name='movimiento-detalle'
	),
	re_path(
        r'ajax/movimiento/(?P<id_movimiento>[0-9]+)/',
        views.cuentas,
        name='ajax-movimiento'
    ),
	re_path(
        r'detalle/perfil/(?P<pk>[0-9]+)/$',
        views.PerfilDetailView.as_view(),
        name='perfil-detalle'
    ),
    re_path(
        r'edicion/perfil/(?P<pk>[0-9]+)/$',
        views.PerfilUpdateView.as_view(),
        name='perfil-edicion'
    ),
	path(
		'import/rubro/',
		views.import_data_rubro,
		name='import-rubro'
	),
	path(
		'import/cuenta/',
		views.import_data_cuenta,
		name='import-cuenta'
	)
]
