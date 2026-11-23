"""Pruebas de API con JSONPlaceholder."""

from utils.api_client import delete, get, post


def test_get_post():
    """GET de un post existente."""
    respuesta = get("/posts/1")

    assert respuesta.status_code == 200

    datos = respuesta.json()
    assert datos["id"] == 1
    assert "title" in datos
    assert "body" in datos
    assert "userId" in datos


def test_get_posts_por_usuario():
    """GET de los posts de un usuario."""
    respuesta = get("/posts", params={"userId": 1})

    assert respuesta.status_code == 200

    datos = respuesta.json()
    assert isinstance(datos, list)
    assert len(datos) > 0
    assert all(post["userId"] == 1 for post in datos)


def test_crear_post():
    """POST para crear un post."""
    nuevo_post = {
        "title": "Prueba de automatizacion",
        "body": "Contenido de prueba",
        "userId": 1,
    }

    respuesta = post("/posts", nuevo_post)

    assert respuesta.status_code == 201

    datos = respuesta.json()
    assert datos["title"] == nuevo_post["title"]
    assert datos["body"] == nuevo_post["body"]
    assert datos["userId"] == nuevo_post["userId"]
    assert "id" in datos


def test_crear_y_consultar():
    """Encadenamiento: primero un usuario y después sus posts."""
    respuesta_usuario = get("/users/1")
    assert respuesta_usuario.status_code == 200

    usuario_id = respuesta_usuario.json()["id"]

    respuesta_posts = get("/posts", params={"userId": usuario_id})
    assert respuesta_posts.status_code == 200

    posts = respuesta_posts.json()
    assert len(posts) > 0
    assert all(post["userId"] == usuario_id for post in posts)


def test_eliminar_post():
    """DELETE de un post."""
    respuesta = delete("/posts/1")

    assert respuesta.status_code in (200, 204)


def test_post_inexistente():
    """GET de un post que no existe."""
    respuesta = get("/posts/999999")

    assert respuesta.status_code == 404
