from django.conf.urls import include
from django.urls import reverse_lazy, path
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from . import views

app_name ='contabilidad'

urlpatterns = [
	path('cuentas/', views.cuentas, name='cuentas'),
]
