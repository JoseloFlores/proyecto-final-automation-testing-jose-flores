# Pruebas de API usando Requests sobre JSONPlaceholder

from utilidades.cliente_api import crear, eliminar, obtener


def prueba_obtener_una_publicacion():
    # Pedimos la publicacion numero 1 y revisamos que tenga todos los campos
    respuesta = obtener("/posts/1")

    assert respuesta.status_code == 200

    datos = respuesta.json()
    assert datos["id"] == 1
    assert "title" in datos
    assert "body" in datos
    assert "userId" in datos


def prueba_obtener_publicaciones_de_usuario():
    # Pedimos todas las publicaciones del usuario 1
    respuesta = obtener("/posts", parametros={"userId": 1})

    assert respuesta.status_code == 200

    publicaciones = respuesta.json()
    assert type(publicaciones) is list
    assert len(publicaciones) > 0

    for publicacion in publicaciones:
        assert publicacion["userId"] == 1


def prueba_crear_una_publicacion():
    # Enviamos una publicacion nueva con POST
    nueva_publicacion = {
        "title": "Prueba de automatizacion",
        "body": "Texto de prueba para la entrega final",
        "userId": 1,
    }

    respuesta = crear("/posts", nueva_publicacion)

    assert respuesta.status_code == 201

    datos = respuesta.json()
    assert datos["title"] == nueva_publicacion["title"]
    assert datos["body"] == nueva_publicacion["body"]
    assert datos["userId"] == nueva_publicacion["userId"]
    assert "id" in datos


def prueba_obtener_usuario_y_sus_publicaciones():
    # Prueba encadenada: primero buscamos un usuario y luego sus publicaciones
    respuesta_usuario = obtener("/users/1")
    assert respuesta_usuario.status_code == 200

    usuario = respuesta_usuario.json()
    id_usuario = usuario["id"]

    respuesta_publicaciones = obtener("/posts", parametros={"userId": id_usuario})
    assert respuesta_publicaciones.status_code == 200

    publicaciones = respuesta_publicaciones.json()
    assert len(publicaciones) > 0

    for publicacion in publicaciones:
        assert publicacion["userId"] == id_usuario


def prueba_eliminar_una_publicacion():
    # Borramos la publicacion 1 con DELETE
    respuesta = eliminar("/posts/1")

    assert respuesta.status_code == 200 or respuesta.status_code == 204


def prueba_buscar_publicacion_inexistente():
    # Si pedimos un numero que no existe, la API debe responder 404
    respuesta = obtener("/posts/999999")

    assert respuesta.status_code == 404
