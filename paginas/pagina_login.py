# Pagina de inicio de sesion de SauceDemo

import logging

from selenium.webdriver.common.by import By as Por

from paginas.pagina_base import PaginaBase
from utilidades.configuracion import URL_SITIO

registro = logging.getLogger(__name__)


class PaginaLogin(PaginaBase):
    # Elementos de la pantalla de login
    CAMPO_USUARIO = (Por.ID, "user-name")
    CAMPO_CLAVE = (Por.ID, "password")
    BOTON_INGRESAR = (Por.ID, "login-button")
    MENSAJE_ERROR = (Por.CSS_SELECTOR, "[data-test='error']")

    def abrir_login(self):
        self.abrir(URL_SITIO)
        self.buscar_elemento(self.CAMPO_USUARIO)

    def iniciar_sesion(self, usuario, clave):
        registro.info("Iniciando sesion con el usuario: %s", usuario)
        self.escribir(self.CAMPO_USUARIO, usuario)
        self.escribir(self.CAMPO_CLAVE, clave)
        self.hacer_clic(self.BOTON_INGRESAR)

    def leer_error(self):
        return self.leer_texto(self.MENSAJE_ERROR)
