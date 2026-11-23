# Configuracion basica del proyecto de pruebas

import os

# Direcciones de las paginas que vamos a probar
URL_SITIO = "https://www.saucedemo.com"
URL_API = "https://jsonplaceholder.typicode.com"

# Segundos maximos que esperamos a que aparezca un elemento
TIEMPO_ESPERA = 10

# Si SIN_VENTANA es "true", Chrome corre sin mostrar la ventana (sirve para GitHub Actions)
SIN_VENTANA = os.getenv("SIN_VENTANA", "false").lower() == "true"

# Carpetas del proyecto
CARPETA_PROYECTO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CARPETA_DATOS = os.path.join(CARPETA_PROYECTO, "datos")
CARPETA_REPORTES = os.path.join(CARPETA_PROYECTO, "reportes")
CARPETA_EVIDENCIAS = os.path.join(CARPETA_PROYECTO, "documentacion", "evidencias")
CARPETA_REGISTROS = os.path.join(CARPETA_PROYECTO, "registros")
