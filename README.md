##PASOS PARA EL DESARROLLO DE ESTA APLICACIÓN:

1. Creamos una carpeta "mapas"
2. Dentro de la carpeta "mapas" vamos a crear un entorno virtual para este proyecto:

        python -m venv venv

3. Activamos el entorno virtual:

        source venv/bin/activate

4. Instalamos django y folium

        pip install django

        pip install folium

5. Verificamos las librerías instaladas:

        pip list

6. Creamos el proyecto de django:

        django-admin startproject django_maps

7. Creamos una aplicación dentro del proyecto, que llamaremos "map"

        python manage.py startapp map

8. Registramos en INSTALLED_APPS del archivo settings.py del proyecto, la nueva aplicación creada
9.  Además, corregimos el tema de idiomas del proyecto:

        LANGUAGE_CODE = 'es-ar'
        TIME_ZONE = 'America/Buenos_Aires'

10. En la aplicación map, creamos una carpeta que se llame "templates" y dentro, creamos otra carpeta que se llame como la aplicación: "map". Dentro de esta última carpeta, voy a crear dos archivos: base.html y home.html
11. Después en la raíz de la aplicación map, voy a crear un archivo urls.py para definir las rutas de la aplicación
12. A continuación voy a trabajar con el archivo base.html y home.html utilizando bootstrap 5 como referencia
13. Una vez preparados los dos archivos html, me queda definir la vista en el archivo views.py y luego poder generar el path a la ruta en el archivo urls.py de la aplicación
14. Luego, voy a modificar el urls.py del proyecto para que pueda acceder al archivo urls.py de la aplicación. De esta forma, podría ya correr el servidor, para poder ver el esquema que definí en el home.html
15. Luego volvemos al archivo views.py para representar el mapa en nuestra página home.html


Tengo que ver la manera de implementar el ping sin que me clave toda la pagina
Agregar tooltip
Ver que el usuario cree vectores (lineas para crear enlaces o conexiones entre hosts)
Alertas? por correo o telegram
traceroute grafico
agregar a cada host la loopback y las interfaces