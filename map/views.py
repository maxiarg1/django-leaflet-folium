from django.shortcuts import render
from .models import Location
import folium

def home(request):
    # Recupero todas las sucursales
    locations = Location.objects.all()

    # Defino el mapa
    initialMap = folium.Map(location=[-34.6460675,-58.5268284], zoom_start=11)

    for location in locations:
        coordinates = (location.lat, location.lng)
        folium.Marker(coordinates, popup='Sucursal '+ location.name).add_to(initialMap)

    context = {'map':initialMap._repr_html_(), 'locations':locations}
    return render(request, 'map/home.html', context)
