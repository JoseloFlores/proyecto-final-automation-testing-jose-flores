"""Configuración general de pytest y del navegador."""

import base64
import logging
import re
import shutil
from datetime import datetime

import pytest
import pytest_html
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

from utils.config import EVIDENCIAS_DIR, HEADLESS, REPORTS_DIR

logger = logging.getLogger(__name__)


def _nombre_seguro(texto):
    """Reemplaza caracteres que no sirven para un nombre de archivo."""
    return re.sub(r"[^A-Za-z0-9_-]", "_", texto)


def guardar_captura(driver, nombre_test):
    """Guarda una captura con fecha, hora y nombre del test."""
    fecha = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    nombre = f"{fecha}_{_nombre_seguro(nombre_test)}.png"
    EVIDENCIAS_DIR.mkdir(parents=True, exist_ok=True)
    ruta = EVIDENCIAS_DIR / nombre
    driver.save_screenshot(str(ruta))
    logger.info("Captura guardada en %s", ruta)
    return ruta


def copiar_captura_a_reportes(ruta):
    """Copia la captura a la carpeta de reportes."""
    destino = REPORTS_DIR / "screenshots" / ruta.name
    destino.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(ruta, destino)
    return destino


def pytest_configure(config):
    """Crea las carpetas necesarias antes de ejecutar las pruebas."""
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    EVIDENCIAS_DIR.mkdir(parents=True, exist_ok=True)
    # webdriver-manager es muy hablador; solo mostramos sus advertencias.
    logging.getLogger("WDM").setLevel(logging.WARNING)


@pytest.fixture(scope="function")
def driver(request):
    """Crea un Chrome nuevo para cada test y lo cierra al final."""
    options = webdriver.ChromeOptions()

    if HEADLESS:
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

    options.add_argument("--window-size=1366,768")
    # Evita avisos de contraseña guardada que a veces tapan los botones.
    options.add_argument("--incognito")
    options.add_experimental_option(
        "prefs",
        {
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,
            "profile.password_manager_leak_detection": False,
        },
    )

    service = ChromeService(ChromeDriverManager().install())
    navegador = webdriver.Chrome(service=service, options=options)
    navegador.implicitly_wait(0)

    logger.info("Navegador iniciado para el test: %s", request.node.name)

    yield navegador

    fallo = getattr(request.node, "rep_call", None) and request.node.rep_call.failed

    # Si el test pasó, igual guardamos una captura como evidencia.
    if not fallo:
        try:
            guardar_captura(navegador, request.node.name)
        except Exception as error:
            logger.warning("No se pudo guardar la evidencia: %s", error)

    navegador.quit()
    logger.info("Navegador cerrado")


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Detecta fallos y adjunta la captura al reporte HTML."""
    outcome = yield
    report = outcome.get_result()
    setattr(item, "rep_" + report.when, report)

    if report.when == "call" and report.failed:
        navegador = item.funcargs.get("driver")
        if navegador is not None:
            try:
                ruta = guardar_captura(navegador, item.name)
                copiar_captura_a_reportes(ruta)

                # Se pasa la imagen en base64 para que quede dentro del HTML.
                with open(ruta, "rb") as archivo:
                    imagen_base64 = base64.b64encode(archivo.read()).decode("utf-8")

                extras = getattr(report, "extras", [])
                extras.append(pytest_html.extras.image(imagen_base64, "Captura del fallo"))
                report.extras = extras
            except Exception as error:
                logger.warning("No se pudo adjuntar la captura: %s", error)
