"""Pruebas del listado de productos."""

from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from utils.data_loader import cargar_json


def test_ordenar_por_precio(driver):
    """Los precios deben quedar de menor a mayor."""
    usuario = cargar_json("usuarios.json")["valido"]

    login = LoginPage(driver)
    login.abrir_login()
    login.iniciar_sesion(usuario["usuario"], usuario["clave"])

    inventario = InventoryPage(driver)
    inventario.esperar_carga()
    inventario.ordenar_por_precio("lohi")

    precios = [float(precio.replace("$", "")) for precio in inventario.obtener_precios()]

    assert len(precios) > 0
    assert precios == sorted(precios)
