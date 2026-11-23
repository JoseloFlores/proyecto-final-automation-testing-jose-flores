"""Cliente simple para las pruebas de API con Requests."""

import time

import requests

from utils.config import API_URL, TIMEOUT


def _enviar(metodo, endpoint, **kwargs):
    """Envía una petición y reintenta si la API pública devuelve un error 5xx."""
    url = f"{API_URL}{endpoint}"
    respuesta = requests.request(metodo, url, timeout=TIMEOUT, **kwargs)
    if respuesta.status_code >= 500:
        time.sleep(1)
        respuesta = requests.request(metodo, url, timeout=TIMEOUT, **kwargs)
    return respuesta


def get(endpoint, params=None):
    """Hace una petición GET a la API."""
    return _enviar("GET", endpoint, params=params)


def post(endpoint, data):
    """Hace una petición POST con un cuerpo JSON."""
    return _enviar("POST", endpoint, json=data)


def delete(endpoint):
    """Hace una petición DELETE."""
    return _enviar("DELETE", endpoint)
