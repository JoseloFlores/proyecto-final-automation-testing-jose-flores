# Pruebas del proceso de compra completo y sus validaciones

import pytest

from paginas.pagina_carrito import PaginaCarrito
from paginas.pagina_compra import PaginaCompra
from paginas.pagina_inventario import PaginaInventario
from paginas.pagina_login import PaginaLogin
from utilidades.lector_datos import cargar_json

DATOS_COMPRA = cargar_json("compra.json")
LISTA_CLIENTES = DATOS_COMPRA["clientes"]
NOMBRES_CLIENTES = []
for cliente in LISTA_CLIENTES:
    NOMBRES_CLIENTES.append(cliente["caso"])


@pytest.mark.parametrize("cliente", LISTA_CLIENTES, ids=NOMBRES_CLIENTES)
def prueba_compra_completa(navegador, cliente):
    # 1. Iniciar sesion
    usuario = cargar_json("usuarios.json")["valido"]
    pagina_login = PaginaLogin(navegador)
    pagina_login.abrir_login()
    pagina_login.iniciar_sesion(usuario["usuario"], usuario["clave"])

    # 2. Agregar producto y pasar al carrito
    pagina_inventario = PaginaInventario(navegador)
    pagina_inventario.esperar_que_cargue()
    nombre_producto = pagina_inventario.agregar_primer_producto()
    pagina_inventario.ir_al_carrito()

    # 3. Revisar el carrito e ir al formulario de compra
    pagina_carrito = PaginaCarrito(navegador)
    pagina_carrito.esperar_que_cargue()
    assert nombre_producto in pagina_carrito.leer_nombres_productos()
    pagina_carrito.ir_a_pagar()

    # 4. Completar datos del comprador y confirmar la compra
    pagina_compra = PaginaCompra(navegador)
    pagina_compra.completar_datos(
        cliente["nombre"],
        cliente["apellido"],
        cliente["codigo_postal"],
    )
    pagina_compra.continuar()
    pagina_compra.finalizar_compra()

    mensaje_final = pagina_compra.leer_confirmacion()
    assert "Thank you for your order!" in mensaje_final


def prueba_compra_sin_datos_obligatorios(navegador):
    # 1. Iniciar sesion
    usuario = cargar_json("usuarios.json")["valido"]
    pagina_login = PaginaLogin(navegador)
    pagina_login.abrir_login()
    pagina_login.iniciar_sesion(usuario["usuario"], usuario["clave"])

    # 2. Agregar producto e ir al formulario de compra
    pagina_inventario = PaginaInventario(navegador)
    pagina_inventario.esperar_que_cargue()
    pagina_inventario.agregar_primer_producto()
    pagina_inventario.ir_al_carrito()

    pagina_carrito = PaginaCarrito(navegador)
    pagina_carrito.esperar_que_cargue()
    pagina_carrito.ir_a_pagar()

    # 3. Intentar seguir sin llenar los campos
    pagina_compra = PaginaCompra(navegador)
    pagina_compra.intentar_continuar_sin_datos()

    mensaje_error = pagina_compra.leer_error()
    assert "First Name is required" in mensaje_error
