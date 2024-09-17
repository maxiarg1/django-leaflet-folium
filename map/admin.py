from django.contrib import admin
from django import forms
from django.forms.widgets import CheckboxInput
from .models import Location, UbicacionInicial, GeoJSONFile

class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = '__all__'  # Incluye todos los campos del modelo
        widgets = {
            'ping_responde': CheckboxInput(),
        }

class LocationAdmin(admin.ModelAdmin):
    form = LocationForm
    list_display = ['name', 'address', 'lat', 'lng', 'direccion_ip', 'ping_responde']
    # ... otros ajustes si es necesario

admin.site.register(Location, LocationAdmin)
admin.site.register(UbicacionInicial)

class GeoJSONFileAdmin(admin.ModelAdmin):
    list_display = ['file', 'color', 'weight', 'opacity', 'fillColor', 'fillOpacity']
    search_fields = ['file__name']

admin.site.register(GeoJSONFile, GeoJSONFileAdmin)