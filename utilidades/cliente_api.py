# Funciones simples para hacer pedidos a la API de prueba

import time
import requests

from utilidades.configuracion import TIEMPO_ESPERA, URL_API


def obtener(ruta, parametros=None):
    # Hace un pedido GET a la API
    url = URL_API + ruta
    respuesta = requests.get(url, params=parametros, timeout=TIEMPO_ESPERA)

    # A veces la API publica da un error 502 por un segundo, asi que reintentamos una vez
    if respuesta.status_code >= 500:
        time.sleep(1)
        respuesta = requests.get(url, params=parametros, timeout=TIEMPO_ESPERA)

    return respuesta


def crear(ruta, datos):
    # Hace un pedido POST enviando datos en formato JSON
    url = URL_API + ruta
    respuesta = requests.post(url, json=datos, timeout=TIEMPO_ESPERA)

    if respuesta.status_code >= 500:
        time.sleep(1)
        respuesta = requests.post(url, json=datos, timeout=TIEMPO_ESPERA)

    return respuesta


def eliminar(ruta):
    # Hace un pedido DELETE a la API
    url = URL_API + ruta
    respuesta = requests.delete(url, timeout=TIEMPO_ESPERA)

    if respuesta.status_code >= 500:
        time.sleep(1)
        respuesta = requests.delete(url, timeout=TIEMPO_ESPERA)

    return respuesta
