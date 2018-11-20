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
	),  
]
