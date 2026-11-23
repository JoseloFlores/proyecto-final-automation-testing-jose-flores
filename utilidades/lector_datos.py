# Funciones para leer los archivos JSON con datos de prueba

import json
import os

from utilidades.configuracion import CARPETA_DATOS


def cargar_json(nombre_archivo):
    # Arma la ruta completa dentro de la carpeta datos y devuelve el contenido
    ruta = os.path.join(CARPETA_DATOS, nombre_archivo)
    with open(ruta, "r", encoding="utf-8") as archivo:
        datos = json.load(archivo)
    return datos
