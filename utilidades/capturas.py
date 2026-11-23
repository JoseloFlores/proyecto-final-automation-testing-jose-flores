# Funcion auxiliar para guardar capturas de pantalla

import os

from utilidades.configuracion import CARPETA_EVIDENCIAS


def guardar_evidencia(navegador, nombre_archivo):
    # Crea la carpeta si no existe y guarda la imagen con el nombre elegido
    os.makedirs(CARPETA_EVIDENCIAS, exist_ok=True)
    ruta = os.path.join(CARPETA_EVIDENCIAS, nombre_archivo + ".png")
    navegador.save_screenshot(ruta)
    return ruta
