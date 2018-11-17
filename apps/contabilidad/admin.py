from django.contrib import admin

from .models import *

admin.site.register(Cuenta)
admin.site.register(Catalogo)
admin.site.register(Empresa)
admin.site.register(EstadoFinanciero)
admin.site.register(Mayorizacion)
admin.site.register(Movimiento)
admin.site.register(Transaccion)

@admin.register(PeriodoContable)
class PeriodoContableAdmin(admin.ModelAdmin):
    list_display = (
        'id_periodo_contable',
        'fecha_inicio_periodo',
        'fecha_final_periodo'
    )
    fields = [
        (
            'fecha_inicio_periodo',
            'fecha_final_periodo'
        )
    ]

@admin.register(Rubro)
class RubroAdmin(admin.ModelAdmin):
    list_display = (
        'id_rubro',
        'rubro_sup',
        'codigo_rubro',
        'nombre_rubro',
        'nivel'
    )