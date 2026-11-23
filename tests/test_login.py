"""Pruebas de inicio de sesión."""

import pytest

from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from utils.data_loader import cargar_json

DATOS_USUARIOS = cargar_json("usuarios.json")


def test_login_exitoso(driver):
    """Un usuario válido debe entrar al inventario."""
    usuario = DATOS_USUARIOS["valido"]

    login = LoginPage(driver)
    login.abrir_login()
    login.iniciar_sesion(usuario["usuario"], usuario["clave"])

    inventario = InventoryPage(driver)
    inventario.esperar_carga()

    assert "/inventory.html" in driver.current_url
    assert inventario.obtener_titulo() == "Products"
    assert inventario.obtener_logo() == "Swag Labs"


@pytest.mark.parametrize(
    "caso",
    DATOS_USUARIOS["invalidos"],
    ids=[caso["caso"] for caso in DATOS_USUARIOS["invalidos"]],
)
def test_login_fallido(driver, caso):
    """Un usuario bloqueado o con mala contraseña no debe entrar."""
    login = LoginPage(driver)
    login.abrir_login()
    login.iniciar_sesion(caso["usuario"], caso["clave"])

    error = login.obtener_error()

    assert caso["error_esperado"] in error
    assert "/inventory.html" not in driver.current_url
