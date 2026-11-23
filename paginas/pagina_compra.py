# Paginas del formulario de compra y confirmacion final

import logging
import time

from selenium.webdriver.common.by import By as Por

from paginas.pagina_base import PaginaBase

registro = logging.getLogger(__name__)


class PaginaCompra(PaginaBase):
    # Campos y botones del proceso de compra
    CAMPO_NOMBRE = (Por.ID, "first-name")
    CAMPO_APELLIDO = (Por.ID, "last-name")
    CAMPO_CODIGO_POSTAL = (Por.ID, "postal-code")
    BOTON_CONTINUAR = (Por.ID, "continue")
    BOTON_FINALIZAR = (Por.ID, "finish")
    MENSAJE_CONFIRMACION = (Por.CLASS_NAME, "complete-header")
    MENSAJE_ERROR = (Por.CSS_SELECTOR, "[data-test='error']")

    def completar_datos(self, nombre, apellido, codigo_postal):
        registro.info("Completando datos de compra para %s %s", nombre, apellido)
        self.escribir(self.CAMPO_NOMBRE, nombre)
        self.escribir(self.CAMPO_APELLIDO, apellido)
        self.escribir(self.CAMPO_CODIGO_POSTAL, codigo_postal)
        # Pequeña pausa para que el formulario termine de guardar los campos
        time.sleep(0.5)

    def continuar(self):
        self.hacer_clic_seguro(self.BOTON_CONTINUAR)
        self.esperar_direccion("/checkout-step-two.html")

    def finalizar_compra(self):
        registro.info("Finalizando la compra")
        self.hacer_clic_seguro(self.BOTON_FINALIZAR)
        self.esperar_direccion("/checkout-complete.html")

    def leer_confirmacion(self):
        return self.leer_texto(self.MENSAJE_CONFIRMACION)

    def intentar_continuar_sin_datos(self):
        self.hacer_clic_seguro(self.BOTON_CONTINUAR)

    def leer_error(self):
        return self.leer_texto(self.MENSAJE_ERROR)
