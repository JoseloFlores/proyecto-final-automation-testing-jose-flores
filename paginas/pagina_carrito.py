# Pagina del carrito de compras

import logging

from selenium.webdriver.common.by import By as Por
from selenium.webdriver.support import expected_conditions as condiciones

from paginas.pagina_base import PaginaBase

registro = logging.getLogger(__name__)


class PaginaCarrito(PaginaBase):
    # Elementos del carrito
    FILAS_CARRITO = (Por.CLASS_NAME, "cart_item")
    NOMBRES_PRODUCTOS = (Por.CLASS_NAME, "inventory_item_name")
    BOTON_CONTINUAR_COMPRA = (Por.ID, "checkout")

    def esperar_que_cargue(self):
        self.esperar_direccion("/cart.html")
        self.espera.until(condiciones.visibility_of_element_located(self.FILAS_CARRITO))

    def leer_nombres_productos(self):
        elementos = self.navegador.find_elements(*self.NOMBRES_PRODUCTOS)
        nombres = []
        for elemento in elementos:
            nombres.append(elemento.text)
        return nombres

    def contar_productos(self):
        elementos = self.navegador.find_elements(*self.FILAS_CARRITO)
        return len(elementos)

    def ir_a_pagar(self):
        registro.info("Pasando al formulario de compra")
        self.hacer_clic_seguro(self.BOTON_CONTINUAR_COMPRA)
        self.esperar_direccion("/checkout-step-one.html")
