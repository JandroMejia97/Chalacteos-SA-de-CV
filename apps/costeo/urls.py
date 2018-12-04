from django.conf.urls import url,include

from . import views

app_name = 'costeo'
urlpatterns = [
    path(
		'crear/boleta/',
		views.BoletaCreateView.as_view(),
		name='boleta-crear'
	),
]
