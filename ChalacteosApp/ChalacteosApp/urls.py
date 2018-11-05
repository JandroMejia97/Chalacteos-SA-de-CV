from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('contabilidad/',include('apps.contabilidad.urls', namespace='contabilidad'), name='contabilidad'),
    path('inventario/',include('apps.inventario.urls', namespace='inventario'), name='inventario')
]
