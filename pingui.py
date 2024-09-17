from ping3 import ping
import time
import sqlite3
import pytz
import datetime
import concurrent.futures


def crear_tabla():
    # Conectar a la base de datos (o crearla si no existe)
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()

    # Crear la tabla si no existe
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS resultados_ping (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            direccion_ip TEXT,
            tiempo_respuesta REAL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Guardar los cambios y cerrar la conexión
    conn.commit()
    conn.close()

def insertar_resultado_ping(direccion_ip, tiempo_respuesta):
    # Conectar a la base de datos
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()

    # Obtener la marca de tiempo actual en la zona horaria de América/Buenos_Aires
    tz_buenos_aires = pytz.timezone('America/Buenos_Aires')
    timestamp = datetime.datetime.now(tz_buenos_aires).strftime('%Y-%m-%d %H:%M:%S')

    # Insertar datos en la tabla
    cursor.execute('''
        INSERT INTO resultados_ping (direccion_ip, tiempo_respuesta, timestamp)
        VALUES (?, ?, ?)
    ''', (direccion_ip, tiempo_respuesta, timestamp))

    # Guardar los cambios y cerrar la conexión
    conn.commit()
    conn.close()

    # Actualizar el campo ping_responde en la tabla map_location
    actualizar_ping_responde(direccion_ip, tiempo_respuesta)

def actualizar_ping_responde(direccion_ip, tiempo_respuesta):
    # Conectar a la base de datos
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()

    # Determinar si el ping fue exitoso
    ping_exitoso = tiempo_respuesta != 6969

    # Actualizar el campo ping_responde en la tabla map_location
    cursor.execute('''
        UPDATE map_location
        SET ping_responde = ?
        WHERE direccion_ip = ?
    ''', (ping_exitoso, direccion_ip))

    # Guardar los cambios y cerrar la conexión
    conn.commit()
    conn.close()

def obtener_direcciones_ip():
    # Conectar a la base de datos
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()

    # Obtener direcciones IP de la tabla map_location
    cursor.execute('SELECT direccion_ip FROM map_location')
    direcciones_ip = [row[0] for row in cursor.fetchall()]

    # Cerrar la conexión
    conn.close()

    return direcciones_ip

def ping_and_insert(direccion_ip):
    # Realizar ping y obtener tiempo de respuesta
    if (ping(direccion_ip, unit='ms')) == False:
        response_time = 6969
    else:
        response_time = round(ping(direccion_ip, unit='ms'), 2)



    print(f'{direccion_ip}: {response_time} ms')

    # Insertar resultado del ping en la tabla resultados_ping
    insertar_resultado_ping(direccion_ip, response_time)

def main():
    # Crear tablas si no existen
    crear_tabla()
    

    # Obtener direcciones IP de la tabla map_location
    direcciones_ip = obtener_direcciones_ip()

    # Realizar pings en paralelo
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(ping_and_insert, direcciones_ip)

if __name__ == "__main__":
    main()

