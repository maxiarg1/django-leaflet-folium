from django.db import models

class Location(models.Model):
    name = models.CharField(max_length=250, verbose_name='Nombre Sucursal')
    address = models.CharField(max_length=250, verbose_name='Dirección')
    lat = models.FloatField(verbose_name='Latitud')
    lng = models.FloatField(verbose_name='Longitud')
    direccion_ip = models.GenericIPAddressField(default='0.0.0.0', protocol='IPv4')
    ping_responde = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Sucursal'
        verbose_name_plural = 'Sucursales'
        ordering = ['name']

    def __str__(self):
        return self.name


class UbicacionInicial(models.Model):
    latitud = models.DecimalField(max_digits=9, decimal_places=6)
    longitud = models.DecimalField(max_digits=9, decimal_places=6)

    def __str__(self):
        return f'Latitud: {self.latitud}, Longitud: {self.longitud}'
    
class GeoJSONFile(models.Model):
    file = models.FileField(upload_to='geojson_files/', verbose_name='Archivo GeoJSON')
    color = models.CharField(max_length=30, default='black', verbose_name='Color de líneas')
    weight = models.IntegerField(default=2, verbose_name='Grosor de líneas')
    opacity = models.FloatField(default=0.4, verbose_name='Opacidad de líneas')
    fillColor = models.CharField(max_length=30, default='red', verbose_name='Color de relleno')
    fillOpacity = models.FloatField(default=0.1, verbose_name='Opacidad de relleno')

    class Meta:
        verbose_name = 'Archivo GeoJSON'
        verbose_name_plural = 'Archivos GeoJSON'

    def __str__(self):
        return f'Archivo GeoJSON: {self.file.name}'