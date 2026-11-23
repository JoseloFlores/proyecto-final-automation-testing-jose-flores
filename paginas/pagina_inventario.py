# Pagina donde se muestran todos los productos de la tienda

import logging

from selenium.webdriver.common.by import By as Por
from selenium.webdriver.support import expected_conditions as condiciones
from selenium.webdriver.support.ui import Select as Selector

from paginas.pagina_base import PaginaBase

registro = logging.getLogger(__name__)


class PaginaInventario(PaginaBase):
    # Elementos del listado de productos
    TITULO = (Por.CLASS_NAME, "title")
    LOGO = (Por.CLASS_NAME, "app_logo")
    TARJETAS_PRODUCTOS = (Por.CLASS_NAME, "inventory_item")
    NOMBRES_PRODUCTOS = (Por.CLASS_NAME, "inventory_item_name")
    BOTON_AGREGAR = (Por.CSS_SELECTOR, "button[data-test^='add-to-cart']")
    BOTON_QUITAR = (Por.CSS_SELECTOR, "button[data-test^='remove']")
    CONTADOR_CARRITO = (Por.CLASS_NAME, "shopping_cart_badge")
    ENLACE_CARRITO = (Por.CLASS_NAME, "shopping_cart_link")
    SELECTOR_ORDEN = (Por.CSS_SELECTOR, "[data-test='product-sort-container']")
    PRECIOS = (Por.CLASS_NAME, "inventory_item_price")
    PRIMER_PRECIO = (Por.CSS_SELECTOR, ".inventory_item_price")

    def esperar_que_cargue(self):
        self.buscar_elemento(self.TITULO)
        self.espera.until(condiciones.visibility_of_element_located(self.TARJETAS_PRODUCTOS))

    def leer_titulo(self):
        return self.leer_texto(self.TITULO)

    def leer_logo(self):
        return self.leer_texto(self.LOGO)

    def agregar_primer_producto(self):
        self.esperar_que_cargue()
        lista_nombres = self.navegador.find_elements(*self.NOMBRES_PRODUCTOS)
        nombre_producto = lista_nombres[0].text
        registro.info("Agregando el producto '%s' al carrito", nombre_producto)
        self.hacer_clic_seguro(self.BOTON_AGREGAR)
        # Esperamos a que el numerito del carrito muestre 1
        self.espera.until(condiciones.text_to_be_present_in_element(self.CONTADOR_CARRITO, "1"))
        return nombre_producto

    def leer_contador_carrito(self):
        return self.leer_texto(self.CONTADOR_CARRITO)

    def tiene_contador_carrito(self):
        elementos = self.navegador.find_elements(*self.CONTADOR_CARRITO)
        return len(elementos) > 0

    def quitar_primer_producto(self):
        registro.info("Quitando el primer producto del carrito")
        self.hacer_clic_seguro(self.BOTON_QUITAR)
        # Cuando no quedan productos el numerito desaparece
        self.espera.until(condiciones.invisibility_of_element_located(self.CONTADOR_CARRITO))

    def ir_al_carrito(self):
        registro.info("Yendo a la pagina del carrito")
        self.hacer_clic_seguro(self.ENLACE_CARRITO)
        self.esperar_direccion("/cart.html")

    def ordenar_por_precio_menor_a_mayor(self):
        registro.info("Ordenando productos de menor a mayor precio")
        lista_desplegable = Selector(self.buscar_elemento(self.SELECTOR_ORDEN))
        lista_desplegable.select_by_value("lohi")
        # El producto mas barato de SauceDemo sale $7.99
        self.espera.until(condiciones.text_to_be_present_in_element(self.PRIMER_PRECIO, "$7.99"))

    def leer_precios(self):
        elementos_precio = self.navegador.find_elements(*self.PRECIOS)
        lista_precios = []
        for elemento in elementos_precio:
            texto = elemento.text.replace("$", "")
            lista_precios.append(float(texto))
        return lista_precios
