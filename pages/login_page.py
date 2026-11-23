"""Página de inicio de sesión de SauceDemo."""

import logging

from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from utils.config import BASE_URL

logger = logging.getLogger(__name__)


class LoginPage(BasePage):
    """Acciones y elementos de la pantalla de login."""

    USUARIO = (By.ID, "user-name")
    CLAVE = (By.ID, "password")
    BOTON_LOGIN = (By.ID, "login-button")
    MENSAJE_ERROR = (By.CSS_SELECTOR, "[data-test='error']")

    def abrir_login(self):
        """Abre la página principal y espera el formulario."""
        self.abrir(BASE_URL)
        self.encontrar(self.USUARIO)

    def iniciar_sesion(self, usuario, clave):
        """Completa el formulario y hace clic en Login."""
        logger.info("Iniciando sesión con el usuario '%s'", usuario)
        self.escribir(self.USUARIO, usuario)
        self.escribir(self.CLAVE, clave)
        self.hacer_clic(self.BOTON_LOGIN)

    def obtener_error(self):
        """Devuelve el mensaje de error que muestra el login."""
        return self.obtener_texto(self.MENSAJE_ERROR)
