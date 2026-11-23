"""Pruebas básicas de responsividad en tres tamaños de pantalla."""

import pytest

from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from utils.data_loader import cargar_json
from utils.screenshots import guardar_evidencia

TAMANOS = [
    (1920, 1080),
    (768, 1024),
    (390, 844),
]


@pytest.mark.parametrize("ancho,alto", TAMANOS, ids=["desktop", "tablet", "movil"])
def test_responsive_paginas(driver, ancho, alto):
    """El flujo principal debe funcionar en desktop, tablet y móvil."""
    driver.set_window_size(ancho, alto)
    usuario = cargar_json("usuarios.json")["valido"]

    login = LoginPage(driver)
    login.abrir_login()
    assert login.esta_visible(LoginPage.USUARIO)
    guardar_evidencia(driver, f"responsive_{ancho}_login")

    login.iniciar_sesion(usuario["usuario"], usuario["clave"])

    inventario = InventoryPage(driver)
    inventario.esperar_carga()
    assert inventario.obtener_titulo() == "Products"
    guardar_evidencia(driver, f"responsive_{ancho}_inventario")

    inventario.agregar_primer_producto()
    inventario.ir_al_carrito()

    carrito = CartPage(driver)
    carrito.esperar_carga()
    assert len(carrito.obtener_nombres()) >= 1
    guardar_evidencia(driver, f"responsive_{ancho}_carrito")

    carrito.ir_a_checkout()
    checkout = CheckoutPage(driver)
    assert checkout.esta_visible(CheckoutPage.NOMBRE)
    guardar_evidencia(driver, f"responsive_{ancho}_checkout")
