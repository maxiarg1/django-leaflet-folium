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