"""Pruebas del carrito de compras."""

from pages.cart_page import CartPage
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from utils.data_loader import cargar_json


def _iniciar_sesion(driver):
    """Abre SauceDemo y deja al usuario en el inventario."""
    usuario = cargar_json("usuarios.json")["valido"]

    login = LoginPage(driver)
    login.abrir_login()
    login.iniciar_sesion(usuario["usuario"], usuario["clave"])

    inventario = InventoryPage(driver)
    inventario.esperar_carga()
    return inventario


def test_agregar_producto(driver):
    """Al agregar un producto el badge debe mostrar 1."""
    inventario = _iniciar_sesion(driver)
    nombre = inventario.agregar_primer_producto()

    assert inventario.obtener_badge() == "1"

    inventario.ir_al_carrito()
    carrito = CartPage(driver)
    carrito.esperar_carga()

    assert nombre in carrito.obtener_nombres()


def test_quitar_producto(driver):
    """Al quitar el único producto el carrito debe quedar vacío."""
    inventario = _iniciar_sesion(driver)
    inventario.agregar_primer_producto()
    inventario.quitar_primer_producto()

    assert not inventario.badge_visible()

    inventario.ir_al_carrito()
    carrito = CartPage(driver)

    assert carrito.cantidad_productos() == 0
