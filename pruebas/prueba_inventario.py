# Pruebas del listado de productos

from paginas.pagina_inventario import PaginaInventario
from paginas.pagina_login import PaginaLogin
from utilidades.lector_datos import cargar_json


def prueba_ordenar_productos_por_precio(navegador):
    # Iniciamos sesion con el usuario valido
    usuario = cargar_json("usuarios.json")["valido"]

    pagina_login = PaginaLogin(navegador)
    pagina_login.abrir_login()
    pagina_login.iniciar_sesion(usuario["usuario"], usuario["clave"])

    # Ordenamos de menor a mayor precio
    pagina_inventario = PaginaInventario(navegador)
    pagina_inventario.esperar_que_cargue()
    pagina_inventario.ordenar_por_precio_menor_a_mayor()

    precios = pagina_inventario.leer_precios()
    precios_ordenados = sorted(precios)

    assert len(precios) > 0
    assert precios == precios_ordenados
