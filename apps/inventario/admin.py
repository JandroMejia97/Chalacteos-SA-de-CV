from django.contrib import admin

from .models import *

admin.site.register(Recurso)
admin.site.register(Kardex)
admin.site.register(Movimiento)
admin.site.register(Producto)
admin.site.register(MateriaPrima)
admin.site.register(Cliente)
admin.site.register(Proveedor)
admin.site.register(Venta)
admin.site.register(Compra)
admin.site.register(Factura)
admin.site.register(Detalle)
admin.site.register(Impuesto)