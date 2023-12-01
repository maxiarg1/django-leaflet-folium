from django.shortcuts import render
from .models import Location, UbicacionInicial
import folium
from folium.plugins import FastMarkerCluster
from .ping_utils import ping_device

def home(request):
    # Recupero todas las sucursales
    locations = Location.objects.all()

    for location in locations:
        try:
            location.ping_responde = ping_device(location.direccion_ip)
        except requests.RequestException:
            # Manejo de errores si la solicitud de ping falla
            location.ping_responde = False

    ubicacion_inicial = UbicacionInicial.objects.first()

    # Defino el mapa
    #initialMap = folium.Map(location=[-38.939386,-68.112168], zoom_start=11)
    latitud = float(ubicacion_inicial.latitud)
    longitud = float(ubicacion_inicial.longitud)
    initialMap = folium.Map(location=[latitud, longitud], zoom_start=11)

    # Creamos el Clustering de los marcadores
    latitudes = [location.lat for location in locations]
    longitudes = [location.lng for location in locations]
    #popups = [location.name for location in locations]
    popups = [f'Sucursal: {location.name}<br>Dirección: {location.address}' for location in locations]

    print(latitudes)
    print(longitudes)
    print(list(zip(latitudes, longitudes, popups)))

    #FastMarkerCluster(data=list(zip(latitudes, longitudes, popups))).add_to(initialMap)

 # Creamos los marcadores con popups
    for location in locations:
        coordinates = (location.lat, location.lng)
        popup_content = f'Sucursal: {location.name}<br>Dirección: {location.address}'
        marker_color = 'green' if location.ping_responde else 'red'
        folium.Marker(location=coordinates, popup=folium.Popup(html=popup_content, parse_html=True),
                    icon=folium.Icon(color=marker_color)).add_to(initialMap)

    context = {'map':initialMap._repr_html_(), 'locations':locations}
    return render(request, 'map/home.html', context)
