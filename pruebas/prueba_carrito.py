# Pruebas del carrito de compras

from paginas.pagina_carrito import PaginaCarrito
from paginas.pagina_inventario import PaginaInventario
from paginas.pagina_login import PaginaLogin
from utilidades.lector_datos import cargar_json


def prueba_agregar_producto_al_carrito(navegador):
    # Iniciamos sesion con el usuario valido
    usuario = cargar_json("usuarios.json")["valido"]

    pagina_login = PaginaLogin(navegador)
    pagina_login.abrir_login()
    pagina_login.iniciar_sesion(usuario["usuario"], usuario["clave"])

    # Agregamos el primer producto y revisamos el numerito del carrito
    pagina_inventario = PaginaInventario(navegador)
    pagina_inventario.esperar_que_cargue()
    nombre_producto = pagina_inventario.agregar_primer_producto()

    assert pagina_inventario.leer_contador_carrito() == "1"

    # Entramos al carrito y verificamos que aparezca el producto
    pagina_inventario.ir_al_carrito()
    pagina_carrito = PaginaCarrito(navegador)
    pagina_carrito.esperar_que_cargue()

    productos_en_carrito = pagina_carrito.leer_nombres_productos()
    assert nombre_producto in productos_en_carrito


def prueba_quitar_producto_del_carrito(navegador):
    # Iniciamos sesion con el usuario valido
    usuario = cargar_json("usuarios.json")["valido"]

    pagina_login = PaginaLogin(navegador)
    pagina_login.abrir_login()
    pagina_login.iniciar_sesion(usuario["usuario"], usuario["clave"])

    # Agregamos el primer producto y enseguida lo quitamos
    pagina_inventario = PaginaInventario(navegador)
    pagina_inventario.esperar_que_cargue()
    pagina_inventario.agregar_primer_producto()
    pagina_inventario.quitar_primer_producto()

    assert not pagina_inventario.tiene_contador_carrito()

    # Entramos al carrito y confirmamos que esta vacio
    pagina_inventario.ir_al_carrito()
    pagina_carrito = PaginaCarrito(navegador)

    assert pagina_carrito.contar_productos() == 0
