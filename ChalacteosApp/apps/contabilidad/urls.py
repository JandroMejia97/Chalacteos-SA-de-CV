from django.conf.urls import url,include
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from . import views

app_name ='contabilidad'

urlpatterns = [
	url(r'^crearcuenta/$', auth_views.LoginView.as_view(
            template_name= 'contabilidad/crearcuenta.html'),
            name='crearcuenta' ),
]
