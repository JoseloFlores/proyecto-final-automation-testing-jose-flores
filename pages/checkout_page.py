"""Páginas del proceso de checkout."""

import logging
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage

logger = logging.getLogger(__name__)


class CheckoutPage(BasePage):
    """Acciones y elementos del formulario y la confirmación de compra."""

    NOMBRE = (By.ID, "first-name")
    APELLIDO = (By.ID, "last-name")
    CODIGO_POSTAL = (By.ID, "postal-code")
    BOTON_CONTINUAR = (By.ID, "continue")
    BOTON_FINALIZAR = (By.ID, "finish")
    MENSAJE_CONFIRMACION = (By.CLASS_NAME, "complete-header")
    MENSAJE_ERROR = (By.CSS_SELECTOR, "[data-test='error']")

    def completar_datos(self, nombre, apellido, codigo_postal):
        """Completa los datos del comprador."""
        logger.info("Completando los datos de checkout")
        self.escribir(self.NOMBRE, nombre)
        self.escribir(self.APELLIDO, apellido)
        self.escribir(self.CODIGO_POSTAL, codigo_postal)
        # Espera corta para que el formulario termine de actualizarse.
        time.sleep(0.5)

    def continuar(self):
        """Avanza al resumen de la compra."""
        boton = self.wait.until(EC.element_to_be_clickable(self.BOTON_CONTINUAR))
        self.driver.execute_script("arguments[0].click();", boton)
        self.esperar_url("/checkout-step-two.html")

    def finalizar(self):
        """Finaliza la compra."""
        logger.info("Finalizando la compra")
        boton = self.wait.until(EC.element_to_be_clickable(self.BOTON_FINALIZAR))
        self.driver.execute_script("arguments[0].click();", boton)
        self.esperar_url("/checkout-complete.html")

    def obtener_confirmacion(self):
        """Devuelve el mensaje final de la compra."""
        return self.obtener_texto(self.MENSAJE_CONFIRMACION)

    def continuar_sin_datos(self):
        """Hace clic en continuar sin completar el formulario."""
        self.hacer_clic(self.BOTON_CONTINUAR)

    def obtener_error(self):
        """Devuelve el mensaje de error del formulario."""
        return self.obtener_texto(self.MENSAJE_ERROR)
