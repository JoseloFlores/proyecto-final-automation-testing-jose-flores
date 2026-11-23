"""Página del carrito de compras."""

import logging

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage

logger = logging.getLogger(__name__)


class CartPage(BasePage):
    """Acciones y elementos de la página del carrito."""

    ITEMS = (By.CLASS_NAME, "cart_item")
    NOMBRES = (By.CLASS_NAME, "inventory_item_name")
    BOTON_CHECKOUT = (By.ID, "checkout")

    def esperar_carga(self):
        """Espera a que el carrito tenga al menos un producto."""
        self.esperar_url("/cart.html")
        self.wait.until(EC.visibility_of_element_located(self.ITEMS))

    def obtener_nombres(self):
        """Devuelve los nombres de los productos del carrito."""
        return [elemento.text for elemento in self.driver.find_elements(*self.NOMBRES)]

    def cantidad_productos(self):
        """Devuelve la cantidad de productos del carrito."""
        return len(self.driver.find_elements(*self.ITEMS))

    def ir_a_checkout(self):
        """Avanza al primer paso del checkout."""
        logger.info("Iniciando el checkout")
        boton = self.wait.until(EC.element_to_be_clickable(self.BOTON_CHECKOUT))
        # En pantallas chicas el clic normal a veces se pierde por el scroll.
        self.driver.execute_script("arguments[0].click();", boton)
        self.esperar_url("/checkout-step-one.html")
