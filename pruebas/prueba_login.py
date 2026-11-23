# Pruebas de inicio de sesion en SauceDemo

import pytest

from paginas.pagina_inventario import PaginaInventario
from paginas.pagina_login import PaginaLogin
from utilidades.lector_datos import cargar_json

DATOS_USUARIOS = cargar_json("usuarios.json")
CASOS_INVALIDOS = DATOS_USUARIOS["invalidos"]
NOMBRES_CASOS = []
for caso in CASOS_INVALIDOS:
    NOMBRES_CASOS.append(caso["caso"])


def prueba_inicio_sesion_exitoso(navegador):
    # Un usuario valido tiene que poder entrar al inventario
    datos = DATOS_USUARIOS["valido"]

    pagina_login = PaginaLogin(navegador)
    pagina_login.abrir_login()
    pagina_login.iniciar_sesion(datos["usuario"], datos["clave"])

    pagina_inventario = PaginaInventario(navegador)
    pagina_inventario.esperar_que_cargue()

    assert "/inventory.html" in navegador.current_url
    assert pagina_inventario.leer_titulo() == "Products"
    assert pagina_inventario.leer_logo() == "Swag Labs"


@pytest.mark.parametrize("caso", CASOS_INVALIDOS, ids=NOMBRES_CASOS)
def prueba_inicio_sesion_fallido(navegador, caso):
    # Si el usuario esta bloqueado o la clave esta mal, tiene que mostrar error
    pagina_login = PaginaLogin(navegador)
    pagina_login.abrir_login()
    pagina_login.iniciar_sesion(caso["usuario"], caso["clave"])

    mensaje = pagina_login.leer_error()

    assert caso["error_esperado"] in mensaje
    assert "/inventory.html" not in navegador.current_url
