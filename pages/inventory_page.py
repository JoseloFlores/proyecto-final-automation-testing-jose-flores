"""Página del inventario de productos."""

import logging

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

from pages.base_page import BasePage

logger = logging.getLogger(__name__)


class InventoryPage(BasePage):
    """Acciones y elementos del listado de productos."""

    TITULO = (By.CLASS_NAME, "title")
    LOGO = (By.CLASS_NAME, "app_logo")
    PRODUCTOS = (By.CLASS_NAME, "inventory_item")
    NOMBRES = (By.CLASS_NAME, "inventory_item_name")
    BOTONES_AGREGAR = (By.CSS_SELECTOR, "button[data-test^='add-to-cart']")
    BOTONES_QUITAR = (By.CSS_SELECTOR, "button[data-test^='remove']")
    BADGE_CARRITO = (By.CLASS_NAME, "shopping_cart_badge")
    LINK_CARRITO = (By.CLASS_NAME, "shopping_cart_link")
    SELECTOR_ORDEN = (By.CSS_SELECTOR, "[data-test='product-sort-container']")
    PRECIOS = (By.CLASS_NAME, "inventory_item_price")
    PRIMER_PRECIO = (By.CSS_SELECTOR, ".inventory_item_price")

    def esperar_carga(self):
        """Espera a que el inventario esté visible."""
        self.encontrar(self.TITULO)
        self.wait.until(EC.visibility_of_element_located(self.PRODUCTOS))

    def obtener_titulo(self):
        """Devuelve el título de la página."""
        return self.obtener_texto(self.TITULO)

    def obtener_logo(self):
        """Devuelve el texto del logo."""
        return self.obtener_texto(self.LOGO)

    def agregar_primer_producto(self):
        """Agrega el primer producto y devuelve su nombre."""
        self.esperar_carga()
        nombre = self.driver.find_elements(*self.NOMBRES)[0].text
        logger.info("Agregando el producto '%s' al carrito", nombre)
        boton = self.wait.until(EC.element_to_be_clickable(self.BOTONES_AGREGAR))
        # En pantallas chicas el clic normal a veces se pierde por el scroll.
        self.driver.execute_script("arguments[0].click();", boton)
        self.wait.until(EC.text_to_be_present_in_element(self.BADGE_CARRITO, "1"))
        return nombre

    def obtener_badge(self):
        """Devuelve el número que muestra el carrito."""
        return self.obtener_texto(self.BADGE_CARRITO)

    def badge_visible(self):
        """Indica si el badge del carrito está visible."""
        return len(self.driver.find_elements(*self.BADGE_CARRITO)) > 0

    def quitar_primer_producto(self):
        """Quita el primer producto del carrito desde el inventario."""
        logger.info("Quitando el primer producto del carrito")
        boton = self.wait.until(EC.element_to_be_clickable(self.BOTONES_QUITAR))
        self.driver.execute_script("arguments[0].click();", boton)
        self.wait.until(EC.invisibility_of_element_located(self.BADGE_CARRITO))

    def ir_al_carrito(self):
        """Navega a la página del carrito."""
        logger.info("Navegando al carrito")
        enlace = self.wait.until(EC.element_to_be_clickable(self.LINK_CARRITO))
        self.driver.execute_script("arguments[0].click();", enlace)
        self.esperar_url("/cart.html")

    def ordenar_por_precio(self, orden="lohi"):
        """Ordena los productos usando el selector de la página."""
        logger.info("Ordenando los productos con el criterio '%s'", orden)
        selector = Select(self.encontrar(self.SELECTOR_ORDEN))
        selector.select_by_value(orden)
        # El primer precio de SauceDemo al ordenar de menor a mayor es $7.99
        self.wait.until(EC.text_to_be_present_in_element(self.PRIMER_PRECIO, "$7.99"))

    def obtener_precios(self):
        """Devuelve la lista de precios visibles."""
        return [elemento.text for elemento in self.driver.find_elements(*self.PRECIOS)]
