"""Funciones para leer los datos de prueba desde archivos JSON."""

import json

from utils.config import DATOS_DIR


def cargar_json(nombre_archivo):
    """Lee un archivo JSON de la carpeta datos y devuelve su contenido."""
    ruta = DATOS_DIR / nombre_archivo
    with open(ruta, encoding="utf-8") as archivo:
        return json.load(archivo)
