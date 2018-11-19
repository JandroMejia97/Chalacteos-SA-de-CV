from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.contabilidad.urls', namespace='contabilidad'), name='contabilidad'),
    path('', include('apps.inventario.urls', namespace='inventario'), name='inventario'),
    path('planilla/',include('apps.planilla.urls', namespace='planilla'), name='planilla'),
    path('costeo/',include('apps.costeo.urls', namespace='costeo'), name='costeo')
]
