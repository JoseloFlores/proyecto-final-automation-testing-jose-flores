"""Clase base para las páginas del sitio."""

import logging

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from utils.config import TIMEOUT

logger = logging.getLogger(__name__)


class BasePage:
    """Acciones comunes que comparten todas las páginas."""

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, TIMEOUT)

    def abrir(self, url):
        """Abre una URL en el navegador."""
        logger.info("Abriendo la página: %s", url)
        self.driver.get(url)

    def encontrar(self, localizador):
        """Espera a que un elemento sea visible y lo devuelve."""
        return self.wait.until(EC.visibility_of_element_located(localizador))

    def hacer_clic(self, localizador):
        """Espera a que un elemento sea clickeable y hace clic."""
        self.wait.until(EC.element_to_be_clickable(localizador)).click()

    def escribir(self, localizador, texto):
        """Escribe el texto indicado en un campo."""
        elemento = self.encontrar(localizador)
        elemento.click()
        elemento.send_keys(texto)

    def obtener_texto(self, localizador):
        """Devuelve el texto visible de un elemento."""
        return self.encontrar(localizador).text

    def esta_visible(self, localizador):
        """Devuelve True si el elemento está visible."""
        try:
            return self.encontrar(localizador).is_displayed()
        except Exception:
            return False

    def esperar_url(self, fragmento):
        """Espera a que la URL actual contenga un fragmento."""
        self.wait.until(EC.url_contains(fragmento))
