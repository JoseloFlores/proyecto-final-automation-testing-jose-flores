"""Pruebas del proceso de checkout."""

import pytest

from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from utils.data_loader import cargar_json

DATOS_CHECKOUT = cargar_json("checkout.json")


def _preparar_checkout(driver):
    """Deja un producto en el carrito y abre el formulario de checkout."""
    usuario = cargar_json("usuarios.json")["valido"]

    login = LoginPage(driver)
    login.abrir_login()
    login.iniciar_sesion(usuario["usuario"], usuario["clave"])

    inventario = InventoryPage(driver)
    inventario.esperar_carga()
    nombre = inventario.agregar_primer_producto()

    inventario.ir_al_carrito()
    carrito = CartPage(driver)
    carrito.esperar_carga()

    assert nombre in carrito.obtener_nombres()

    carrito.ir_a_checkout()
    return CheckoutPage(driver)


@pytest.mark.parametrize(
    "cliente",
    DATOS_CHECKOUT["clientes"],
    ids=[cliente["caso"] for cliente in DATOS_CHECKOUT["clientes"]],
)
def test_checkout_completo(driver, cliente):
    """El checkout debe terminar con el mensaje de confirmación."""
    checkout = _preparar_checkout(driver)

    checkout.completar_datos(cliente["nombre"], cliente["apellido"], cliente["codigo_postal"])
    checkout.continuar()
    checkout.finalizar()

    assert "Thank you for your order!" in checkout.obtener_confirmacion()


def test_checkout_campos_obligatorios(driver):
    """El checkout no debe avanzar si faltan los datos obligatorios."""
    checkout = _preparar_checkout(driver)

    checkout.continuar_sin_datos()
    error = checkout.obtener_error()

    assert "First Name is required" in error
