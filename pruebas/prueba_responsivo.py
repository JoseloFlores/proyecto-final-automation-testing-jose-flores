# Pruebas de pantalla en escritorio, tableta y celular

import pytest

from paginas.pagina_carrito import PaginaCarrito
from paginas.pagina_compra import PaginaCompra
from paginas.pagina_inventario import PaginaInventario
from paginas.pagina_login import PaginaLogin
from utilidades.capturas import guardar_evidencia
from utilidades.lector_datos import cargar_json

PANTALLAS = [
    (1920, 1080),
    (768, 1024),
    (390, 844),
]
NOMBRES_PANTALLAS = ["escritorio", "tableta", "celular"]


@pytest.mark.parametrize("ancho,alto", PANTALLAS, ids=NOMBRES_PANTALLAS)
def prueba_flujo_en_distintas_pantallas(navegador, ancho, alto):
    # Cambiamos el tamaño de la ventana antes de arrancar
    navegador.set_window_size(ancho, alto)
    usuario = cargar_json("usuarios.json")["valido"]

    pagina_login = PaginaLogin(navegador)
    pagina_login.abrir_login()
    assert pagina_login.esta_visible(PaginaLogin.CAMPO_USUARIO)
    guardar_evidencia(navegador, "responsivo_" + str(ancho) + "_login")

    pagina_login.iniciar_sesion(usuario["usuario"], usuario["clave"])

    pagina_inventario = PaginaInventario(navegador)
    pagina_inventario.esperar_que_cargue()
    assert pagina_inventario.leer_titulo() == "Products"
    guardar_evidencia(navegador, "responsivo_" + str(ancho) + "_inventario")

    pagina_inventario.agregar_primer_producto()
    pagina_inventario.ir_al_carrito()

    pagina_carrito = PaginaCarrito(navegador)
    pagina_carrito.esperar_que_cargue()
    assert len(pagina_carrito.leer_nombres_productos()) >= 1
    guardar_evidencia(navegador, "responsivo_" + str(ancho) + "_carrito")

    pagina_carrito.ir_a_pagar()
    pagina_compra = PaginaCompra(navegador)
    assert pagina_compra.esta_visible(PaginaCompra.CAMPO_NOMBRE)
    guardar_evidencia(navegador, "responsivo_" + str(ancho) + "_compra")
