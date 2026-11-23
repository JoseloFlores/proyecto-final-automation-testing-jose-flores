"""Configuración general del proyecto."""

import os
from pathlib import Path

# URL del sitio que se prueba
BASE_URL = "https://www.saucedemo.com"

# API pública para las pruebas de Requests
API_URL = "https://jsonplaceholder.typicode.com"

# Tiempo máximo de espera para los elementos web
TIMEOUT = 10

# Si la variable de entorno HEADLESS vale "true", Chrome corre sin ventana.
# Se usa en GitHub Actions y también se puede usar localmente.
HEADLESS = os.getenv("HEADLESS", "false").lower() == "true"

# Rutas principales del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent
DATOS_DIR = BASE_DIR / "datos"
REPORTS_DIR = BASE_DIR / "reports"
EVIDENCIAS_DIR = BASE_DIR / "docs" / "evidencias"
LOGS_DIR = BASE_DIR / "logs"
