from django.shortcuts import render
from .models import Location, UbicacionInicial, GeoJSONFile
import folium
from folium.plugins import FastMarkerCluster
import os
from django.conf import settings
from django.http import JsonResponse
from django.http import HttpResponse
from folium import Map, Marker, Popup, Icon, Tooltip, FeatureGroup
import pandas as pd


def home(request):
    # Recupero todas las sucursales
    locations = Location.objects.all()

    ubicacion_inicial = UbicacionInicial.objects.first()

    # Defino el mapa
    latitud = float(ubicacion_inicial.latitud)
    longitud = float(ubicacion_inicial.longitud)
    initialMap = folium.Map(location=[latitud, longitud], zoom_start=11)

    #creamos los boundaries del mapa para no poder ir mas allá de la provincia.
    min_lon, max_lon = -65.997803, -73.941581
    min_lat, max_lat = -34.967792, -43.205659

    initialMap = folium.Map(
        max_bounds=True,
        location=[-20, -40],
        zoom_start=6,
        min_lat=min_lat,
        max_lat=max_lat,
        min_lon=min_lon,
        max_lon=max_lon,
    )

    # Crear un objeto FeatureGroup para almacenar todos los marcadores
    marker_layer = FeatureGroup(name='Todos los Marcadores')
    # Crear un objeto FeatureGroup para almacenar todos los GeoJSON
    GeoJSON_layer = FeatureGroup(name='Todos los GeoJSON')

    # Creamos los marcadores con popups
    for location in locations:
        coordinates = (location.lat, location.lng)
        marker_color = 'green' if location.ping_responde else 'red'
        tooltip_content = location.name
        #Se crea un DataFrame df con dos columnas y una fila
        df = pd.DataFrame(data=[[location.name, location.direccion_ip]],columns=["Lugar", "IP"])
        #Se utiliza el método to_html del DataFrame para convertir los datos en una tabla HTML. 
        #La opción classes se utiliza para agregar clases CSS a la tabla, haciendo que tenga un estilo específico 
        #en este caso, se aplican algunas clases de Bootstrap para tablas).
        html = df.to_html(classes="table table-striped table-hover table-condensed table-responsive")
        popup = folium.Popup(html)
        
        marker = folium.Marker(
        location=coordinates,
        popup=popup,
        icon=folium.Icon(color=marker_color)
    )
        

        marker.add_child(folium.Tooltip(tooltip_content))  # Agregar tooltip utilizando add_child
        marker.add_to(marker_layer)

    # Agregar la capa de marcadores al mapa
    marker_layer.add_to(initialMap)



    # Cargar GeoJSON desde la base de datos
    for geojson_file in GeoJSONFile.objects.all():
        ruta = os.path.join(settings.MEDIA_ROOT, str(geojson_file.file))

        style_function = lambda feature: {
            'color': GeoJSONFile.color,
            'weight': GeoJSONFile.weight,
            'opacity': GeoJSONFile.opacity,
            'fillColor' : GeoJSONFile.fillColor,
            'fillOpacity': GeoJSONFile.fillOpacity,
        }
        cargar_geojson(ruta, GeoJSON_layer, style_function)
    
    folium.TileLayer("OpenStreetMap").add_to(initialMap)
    folium.TileLayer(show=False).add_to(initialMap)    
    # Agregar control de capas al mapa
    folium.LayerControl().add_to(initialMap)

    context = {'map': initialMap._repr_html_(), 'locations': locations}
    return render(request, 'map/home.html', context)

def cargar_geojson(ruta, geojson_layer, estilo):
    if os.path.exists(ruta):
        geojson = folium.GeoJson(
            ruta,
            name="Mi GeoJSON Overlay",
            style_function=estilo,
        )
        geojson.add_to(geojson_layer)
    else:
        print(f"El archivo GeoJSON '{ruta}' no existe.")

def actualizar_marcadores(request):
    locations = Location.objects.all()

    # Obtener los datos de la ubicación actual y el zoom del mapa existente
    latitud = float(request.GET.get('latitud', 40.7128))
    longitud = float(request.GET.get('longitud', -74.0060))
    zoom = int(request.GET.get('zoom', 10))

    # Crear un mapa existente con la ubicación y el zoom actuales
    existing_map = folium.Map(location=[latitud, longitud], zoom_start=zoom)

    # Añadir marcadores al mapa
    for location in locations:
        coordinates = (location.lat, location.lng)
        popup_content = f'Lugar: {location.name}<br>IP: {location.direccion_ip}'
        marker_color = 'green' if location.ping_responde else 'red'
        tooltip_content = location.name
        marker = folium.Marker(
            location=coordinates,
            popup=folium.Popup(html=popup_content, parse_html=True),
            icon=folium.Icon(color=marker_color)
        )
        marker.add_child(folium.Tooltip(tooltip_content))
        marker.add_to(existing_map)

    # Guardar el HTML del mapa en una variable y devolverlo como respuesta
    map_html = existing_map._repr_html_()
    return HttpResponse(map_html)