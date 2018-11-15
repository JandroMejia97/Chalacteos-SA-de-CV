from django.contrib import admin

from .models import *

admin.site.register(Rubro)
admin.site.register(Cuenta)
admin.site.register(Catalogo)
admin.register(Empresa)
admin.site.register(EstadoFinanciero)
admin.site.register(Mayorizacion)
admin.site.register(Movimiento)
admin.site.register(PeriodoContable)
admin.site.register(Transaccion)
