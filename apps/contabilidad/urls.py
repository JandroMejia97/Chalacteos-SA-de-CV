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
		'crear/cuenta',
		views.cuentas,
		name='cuenta-crear'
	),
]
