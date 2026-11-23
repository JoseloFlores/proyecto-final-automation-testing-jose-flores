# Configuracion de pytest, apertura de Chrome y capturas automaticas

import base64
import logging
import os
import shutil
from datetime import datetime

import pytest
import pytest_html
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ServicioChrome
from webdriver_manager.chrome import ChromeDriverManager as GestorChromeDriver

from utilidades.configuracion import CARPETA_EVIDENCIAS, CARPETA_REPORTES, SIN_VENTANA

registro = logging.getLogger(__name__)


def limpiar_nombre(texto):
    # Cambia los caracteres raros por guion bajo para que sirva como nombre de archivo
    resultado = ""
    for letra in texto:
        if letra.isalnum() or letra == "_" or letra == "-":
            resultado = resultado + letra
        else:
            resultado = resultado + "_"
    return resultado


def sacar_captura(navegador, nombre_prueba):
    # Guarda la imagen con fecha, hora y el nombre de la prueba
    fecha_hora = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    nombre_archivo = fecha_hora + "_" + limpiar_nombre(nombre_prueba) + ".png"

    os.makedirs(CARPETA_EVIDENCIAS, exist_ok=True)
    ruta_imagen = os.path.join(CARPETA_EVIDENCIAS, nombre_archivo)
    navegador.save_screenshot(ruta_imagen)

    registro.info("Captura guardada en: %s", ruta_imagen)
    return ruta_imagen


def copiar_captura_fallo(ruta_origen):
    # Copia la captura del fallo dentro de reportes/capturas
    carpeta_capturas = os.path.join(CARPETA_REPORTES, "capturas")
    os.makedirs(carpeta_capturas, exist_ok=True)
    nombre_archivo = os.path.basename(ruta_origen)
    ruta_destino = os.path.join(carpeta_capturas, nombre_archivo)
    shutil.copy2(ruta_origen, ruta_destino)
    return ruta_destino


def pytest_configure(config):
    # Crea las carpetas antes de arrancar las pruebas
    os.makedirs(CARPETA_REPORTES, exist_ok=True)
    os.makedirs(CARPETA_EVIDENCIAS, exist_ok=True)
    # Silenciamos un poco los mensajes largos de webdriver-manager
    logging.getLogger("WDM").setLevel(logging.WARNING)


@pytest.fixture(scope="function")
def navegador(request):
    # Abre un Chrome nuevo para cada prueba y lo cierra al terminar
    opciones = webdriver.ChromeOptions()

    if SIN_VENTANA:
        opciones.add_argument("--headless=new")
        opciones.add_argument("--no-sandbox")
        opciones.add_argument("--disable-dev-shm-usage")

    opciones.add_argument("--window-size=1366,768")
    # Modo incognito y sin avisos de contraseñas para que no tapen los botones
    opciones.add_argument("--incognito")
    preferencias = {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "profile.password_manager_leak_detection": False,
    }
    opciones.add_experimental_option("prefs", preferencias)

    servicio = ServicioChrome(GestorChromeDriver().install())
    chrome = webdriver.Chrome(service=servicio, options=opciones)
    chrome.implicitly_wait(0)

    registro.info("Navegador abierto para: %s", request.node.name)

    yield chrome

    # Revisamos si la prueba fallo
    reporte_ejecucion = getattr(request.node, "rep_call", None)
    fallo = reporte_ejecucion is not None and reporte_ejecucion.failed

    # Si paso bien, igual guardamos una captura de evidencia
    if not fallo:
        try:
            sacar_captura(chrome, request.node.name)
        except Exception as error:
            registro.warning("No se pudo guardar la captura de evidencia: %s", error)

    chrome.quit()
    registro.info("Navegador cerrado")


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # Si una prueba falla, sacamos captura y la pegamos dentro del reporte HTML
    resultado = yield
    reporte = resultado.get_result()
    setattr(item, "rep_" + reporte.when, reporte)

    if reporte.when == "call" and reporte.failed:
        chrome = item.funcargs.get("navegador")
        if chrome is not None:
            try:
                ruta_imagen = sacar_captura(chrome, item.name)
                copiar_captura_fallo(ruta_imagen)

                # Convertimos la imagen a base64 para que quede metida dentro del HTML
                with open(ruta_imagen, "rb") as archivo:
                    imagen_base64 = base64.b64encode(archivo.read()).decode("utf-8")

                extras = getattr(reporte, "extras", [])
                extras.append(pytest_html.extras.image(imagen_base64, "Captura del fallo"))
                reporte.extras = extras
            except Exception as error:
                registro.warning("No se pudo adjuntar la captura al reporte: %s", error)
