# Clase base con las acciones que se repiten en todas las paginas

import logging

from selenium.webdriver.support import expected_conditions as condiciones
from selenium.webdriver.support.ui import WebDriverWait as EsperaExplicita

from utilidades.configuracion import TIEMPO_ESPERA

registro = logging.getLogger(__name__)


class PaginaBase:
    # Guarda el navegador y prepara la espera explicita
    def __init__(self, navegador):
        self.navegador = navegador
        self.espera = EsperaExplicita(navegador, TIEMPO_ESPERA)

    def abrir(self, url):
        registro.info("Abriendo la pagina: %s", url)
        self.navegador.get(url)

    def buscar_elemento(self, localizador):
        # Espera a que el elemento se vea en pantalla
        return self.espera.until(condiciones.visibility_of_element_located(localizador))

    def hacer_clic(self, localizador):
        # Espera a que se pueda hacer clic en el elemento
        boton = self.espera.until(condiciones.element_to_be_clickable(localizador))
        boton.click()

    def hacer_clic_seguro(self, localizador):
        # En pantallas chicas el clic normal a veces falla por el scroll, asi que usamos JS
        boton = self.espera.until(condiciones.element_to_be_clickable(localizador))
        self.navegador.execute_script("arguments[0].click();", boton)

    def escribir(self, localizador, texto):
        campo = self.buscar_elemento(localizador)
        campo.click()
        campo.send_keys(texto)

    def leer_texto(self, localizador):
        elemento = self.buscar_elemento(localizador)
        return elemento.text

    def esta_visible(self, localizador):
        try:
            elemento = self.buscar_elemento(localizador)
            return elemento.is_displayed()
        except Exception:
            return False

    def esperar_direccion(self, texto_url):
        self.espera.until(condiciones.url_contains(texto_url))
