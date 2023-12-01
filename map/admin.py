from django.contrib import admin
from .models import Location, UbicacionInicial

admin.site.register(Location)

class UbicacionAdmin(admin.ModelAdmin):
    list_display = ['latitud', 'longitud']

admin.site.register(UbicacionInicial, UbicacionAdmin)