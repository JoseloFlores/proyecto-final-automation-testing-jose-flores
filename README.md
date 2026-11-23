# Proyecto Final — Automatizacion de Pruebas | SauceDemo

Proyecto de automatizacion de pruebas para [SauceDemo](https://www.saucedemo.com),
armado con **Python, Selenium WebDriver, pytest y Requests**.

Incluye pruebas de interfaz grafica, pruebas de API, patron Page Object Model,
datos de prueba en archivos JSON, reportes en HTML, capturas automaticas,
registros de ejecucion y ejecucion automatica en GitHub Actions.

**Autor:** Jose Flores

---

## Proposito

Automatizar los flujos principales de SauceDemo y varios endpoints de una API
publica, aplicando los temas vistos en el curso:

- Pruebas de interfaz web con Selenium.
- Pruebas de API con Requests.
- Patron Page Object Model para separar los localizadores de las pruebas.
- Datos de prueba en archivos JSON externos.
- Reportes en HTML y capturas automaticas cuando una prueba falla.
- Registros de pasos en consola y en archivo.
- Integracion continua con GitHub Actions.

El informe complementario de QA se encuentra en
[`documentacion/informe_qa.md`](documentacion/informe_qa.md).

---

## Tecnologias usadas

| Herramienta | Para que se usa |
|---|---|
| Python 3.13 | Lenguaje principal |
| Selenium WebDriver | Control del navegador Chrome |
| pytest | Ejecucion de las pruebas |
| pytest-html | Generacion del reporte en HTML |
| Requests | Pruebas de API |
| webdriver-manager | Descarga automatica de ChromeDriver |
| GitHub Actions | Ejecucion automatica en cada push |

---

## Estructura del proyecto

```text
.
├── conftest.py                 # Apertura de Chrome, capturas y reporte
├── pytest.ini                  # Configuracion de pytest, reporte y registros
├── requirements.txt
├── README.md
├── datos/
│   ├── usuarios.json           # Usuarios validos e invalidos
│   └── compra.json             # Datos de clientes para el formulario de compra
├── documentacion/
│   ├── informe_qa.md           # Informe QA del proyecto
│   └── evidencias/             # Capturas usadas en el informe
├── paginas/
│   ├── pagina_base.py          # Acciones repetidas en todas las paginas
│   ├── pagina_login.py         # Pantalla de inicio de sesion
│   ├── pagina_inventario.py    # Listado de productos
│   ├── pagina_carrito.py       # Carrito de compras
│   └── pagina_compra.py        # Formulario y confirmacion de compra
├── pruebas/
│   ├── prueba_login.py
│   ├── prueba_carrito.py
│   ├── prueba_inventario.py
│   ├── prueba_compra.py
│   ├── prueba_responsivo.py
│   └── prueba_api.py
├── utilidades/
│   ├── configuracion.py        # Direcciones, tiempos y carpetas
│   ├── lector_datos.py         # Lectura de archivos JSON
│   ├── cliente_api.py          # Funciones obtener, crear y eliminar
│   └── capturas.py             # Guardado de imagenes de evidencia
├── registros/                  # Archivo de log de la ejecucion
└── reportes/                   # Reporte HTML y capturas de fallos
```

---

## Requisitos previos

- Python 3.10 o superior.
- Google Chrome instalado.
- Git.

---

## Instalacion

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

En Windows, el entorno virtual se activa asi:

```bash
venv\Scripts\activate
```

---

## Como ejecutar las pruebas

Ejecutar todas las pruebas viendo la ventana de Chrome:

```bash
pytest -v
```

Ejecutar todas las pruebas sin abrir ventana (modo sin pantalla):

```bash
SIN_VENTANA=true pytest -v
```

Ejecutar solo las pruebas de interfaz:

```bash
pytest pruebas/prueba_login.py pruebas/prueba_carrito.py pruebas/prueba_inventario.py pruebas/prueba_compra.py pruebas/prueba_responsivo.py -v
```

Ejecutar solo las pruebas de API:

```bash
pytest pruebas/prueba_api.py -v
```

Ejecutar una sola prueba:

```bash
pytest pruebas/prueba_login.py::prueba_inicio_sesion_exitoso -v
```

El reporte HTML se guarda siempre en `reportes/reporte.html`.

---

## Casos de prueba de interfaz

| Prueba | Que valida |
|---|---|
| `prueba_inicio_sesion_exitoso` | Ingreso con `standard_user` y llegada al inventario. |
| `prueba_inicio_sesion_fallido[usuario_bloqueado]` | Usuario bloqueado: muestra mensaje de error y no entra. |
| `prueba_inicio_sesion_fallido[clave_incorrecta]` | Clave incorrecta: muestra mensaje de error y no entra. |
| `prueba_agregar_producto_al_carrito` | Agrega el primer producto, contador en `1` y producto visible en el carrito. |
| `prueba_quitar_producto_del_carrito` | Quita el producto, desaparece el contador y el carrito queda vacio. |
| `prueba_ordenar_productos_por_precio` | Ordena de menor a mayor y comprueba la lista de precios. |
| `prueba_compra_completa` | Compra completa parametrizada con dos clientes. |
| `prueba_compra_sin_datos_obligatorios` | Impide continuar si faltan los datos obligatorios. |
| `prueba_flujo_en_distintas_pantallas` | Recorre el flujo en escritorio, tableta y celular. |

Los usuarios y clientes se leen desde `datos/usuarios.json` y `datos/compra.json`.

---

## Casos de prueba de API

Se usa [JSONPlaceholder](https://jsonplaceholder.typicode.com), una API publica
gratuita que no pide clave.

| Prueba | Metodo | Que valida |
|---|---|---|
| `prueba_obtener_una_publicacion` | GET | Codigo 200 y campos de la publicacion. |
| `prueba_obtener_publicaciones_de_usuario` | GET | Lista filtrada por `userId`. |
| `prueba_crear_una_publicacion` | POST | Codigo 201 y datos devueltos en la respuesta. |
| `prueba_obtener_usuario_y_sus_publicaciones` | GET + GET | Flujo encadenado: usuario y luego sus publicaciones. |
| `prueba_eliminar_una_publicacion` | DELETE | Codigo 200 o 204. |
| `prueba_buscar_publicacion_inexistente` | GET | Codigo 404 cuando el numero no existe. |

---

## Reportes y evidencias

Al terminar `pytest`, se generan estos archivos:

| Ubicacion | Contenido |
|---|---|
| `reportes/reporte.html` | Reporte con pruebas ejecutadas, resultado y duracion. |
| `reportes/capturas/` | Capturas de las pruebas que fallaron. |
| `documentacion/evidencias/` | Capturas de evidencia de cada ejecucion. |
| `registros/ejecucion.log` | Registro paso a paso de lo que hizo cada prueba. |

El reporte es autocontenido: si una prueba falla, la captura queda incrustada
dentro del archivo HTML.

Para abrir el reporte en Linux:

```bash
xdg-open reportes/reporte.html
```

En macOS:

```bash
open reportes/reporte.html
```

---

## Capturas automaticas

Cada prueba guarda una captura al terminar. Si falla, ademas guarda una copia
en `reportes/capturas/` y la pega en el reporte HTML.

Los nombres incluyen fecha, hora y nombre de la prueba, por ejemplo:

```text
2026-11-23_10-30-00_prueba_inicio_sesion_exitoso.png
```

---

## Registros de ejecucion

El archivo `registros/ejecucion.log` guarda:

- Cuando se abre y se cierra el navegador.
- Que pagina se abre y con que usuario se inicia sesion.
- Que producto se agrega o se quita.
- El paso al carrito y al formulario de compra.
- Donde se guardo cada captura.
- Advertencias o errores.

---

## Integracion continua

El archivo `.github/workflows/pruebas.yml` corre las pruebas automaticamente
cuando se hace un push o un pull request a `main`, usando `SIN_VENTANA=true`,
y sube los reportes, registros y evidencias como artefacto.

---

## Repositorio

https://github.com/JoseloFlores/proyecto-final-automation-testing-jose-flores
