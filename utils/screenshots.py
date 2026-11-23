"""Función auxiliar para guardar capturas de evidencia."""

from utils.config import EVIDENCIAS_DIR


def guardar_evidencia(driver, nombre):
    """Guarda una captura con un nombre fijo dentro de docs/evidencias."""
    EVIDENCIAS_DIR.mkdir(parents=True, exist_ok=True)
    ruta = EVIDENCIAS_DIR / f"{nombre}.png"
    driver.save_screenshot(str(ruta))
    return ruta
