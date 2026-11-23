# Proyecto Final — Automatización de Pruebas | SauceDemo

Framework de automatización de pruebas para [SauceDemo](https://www.saucedemo.com),
hecho con **Python, Selenium WebDriver, pytest y Requests**.

El proyecto incluye pruebas de interfaz, pruebas de API, Page Object Model,
datos de prueba en JSON, reportes HTML, capturas automáticas, logging y
ejecución automática con GitHub Actions.

**Autor:** José Flores

---

## Propósito

El objetivo es automatizar los flujos principales de SauceDemo y algunos
endpoints de una API pública, aplicando lo visto durante el curso:

- Pruebas de UI con Selenium.
- Pruebas de API con Requests.
- Page Object Model para separar los tests de los localizadores.
- Datos de prueba externos en archivos JSON.
- Reportes HTML y capturas cuando un test falla.
- Logging de los pasos importantes.
- Integración continua con GitHub Actions.

La documentación complementaria de QA está en
[`docs/informe_qa.md`](docs/informe_qa.md).

---

## Tecnologías

| Herramienta | Uso |
|---|---|
| Python 3.13 | Lenguaje principal |
| Selenium WebDriver | Automatización del navegador |
| pytest | Ejecución de los tests |
| pytest-html | Reporte HTML |
| Requests | Pruebas de API |
| webdriver-manager | Descarga del ChromeDriver |
| GitHub Actions | Ejecución automática en cada push |

---

## Estructura del proyecto

```text
.
├── conftest.py                 # Fixture del navegador, capturas y hooks
├── pytest.ini                  # Configuración de pytest, reporte y logs
├── requirements.txt
├── README.md
├── datos/
│   ├── usuarios.json           # Usuarios válidos e inválidos
│   └── checkout.json           # Datos de clientes para el checkout
├── docs/
│   ├── informe_qa.md           # Informe QA con el formato de entrega
│   └── evidencias/             # Capturas usadas en el informe
├── pages/
│   ├── base_page.py            # Acciones comunes
│   ├── login_page.py
│   ├── inventory_page.py
│   ├── cart_page.py
│   └── checkout_page.py
├── tests/
│   ├── test_login.py
│   ├── test_carrito.py
│   ├── test_inventario.py
│   ├── test_checkout.py
│   ├── test_responsive.py
│   └── test_api.py
├── utils/
│   ├── config.py               # URLs, timeout y rutas
│   ├── data_loader.py          # Lectura de JSON
│   ├── api_client.py           # GET, POST y DELETE
│   └── screenshots.py          # Capturas de evidencia
├── logs/                       # Log de la ejecución
└── reports/                    # Reporte HTML y capturas de fallos
```

---

## Requisitos

- Python 3.10 o superior.
- Google Chrome instalado.
- Git.

---

## Instalación

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

En Windows, la activación del entorno es:

```bash
venv\Scripts\activate
```

---

## Ejecución de las pruebas

Ejecutar todo:

```bash
pytest -v
```

Ejecutar sin abrir la ventana de Chrome:

```bash
HEADLESS=true pytest -v
```

Ejecutar solo las pruebas de UI:

```bash
pytest tests/test_login.py tests/test_carrito.py tests/test_inventario.py tests/test_checkout.py tests/test_responsive.py -v
```

Ejecutar solo las pruebas de API:

```bash
pytest tests/test_api.py -v
```

Ejecutar un test puntual:

```bash
pytest tests/test_login.py::test_login_exitoso -v
```

El reporte HTML se genera siempre en `reports/reporte.html`.

---

## Casos de prueba de UI

| Test | Qué valida |
|---|---|
| `test_login_exitoso` | Login con `standard_user` y llegada al inventario. |
| `test_login_fallido[usuario_bloqueado]` | Usuario bloqueado: muestra el error y no entra. |
| `test_login_fallido[clave_incorrecta]` | Contraseña incorrecta: muestra el error y no entra. |
| `test_agregar_producto` | Agrega el primer producto, badge en `1` y producto en el carrito. |
| `test_quitar_producto` | Quita el producto, desaparece el badge y el carrito queda vacío. |
| `test_ordenar_por_precio` | Ordena de menor a mayor y verifica los precios. |
| `test_checkout_completo` | Compra completa con dos juegos de datos. |
| `test_checkout_campos_obligatorios` | No deja continuar si falta el nombre. |
| `test_responsive_paginas` | Flujo principal en desktop, tablet y móvil. |

Los datos de los usuarios y del checkout se leen desde `datos/*.json`.

---

## Casos de prueba de API

Se usa [JSONPlaceholder](https://jsonplaceholder.typicode.com), una API pública
que no necesita clave.

| Test | Método | Qué valida |
|---|---|---|
| `test_get_post` | GET | Status 200 y estructura del post. |
| `test_get_posts_por_usuario` | GET | Lista filtrada por `userId`. |
| `test_crear_post` | POST | Status 201 y datos enviados. |
| `test_crear_y_consultar` | GET + GET | Encadenamiento usuario → posts. |
| `test_eliminar_post` | DELETE | Status 200 o 204. |
| `test_post_inexistente` | GET | Status 404 para un post que no existe. |

---

## Reportes

Después de ejecutar `pytest`, se generan estos archivos:

| Archivo | Contenido |
|---|---|
| `reports/reporte.html` | Reporte HTML con tests, estado y duración. |
| `reports/screenshots/` | Capturas de los tests que fallaron. |
| `docs/evidencias/` | Capturas de evidencia de todos los tests. |
| `logs/ejecucion.log` | Log detallado de la ejecución. |

El reporte es autocontenido: las capturas de los fallos quedan incrustadas
dentro del HTML, no como archivos separados.

Para abrir el reporte:

```bash
xdg-open reports/reporte.html
```

En macOS:

```bash
open reports/reporte.html
```

---

## Capturas automáticas

Cada test guarda una captura al finalizar. Si el test falla, además se guarda
una copia en `reports/screenshots/` y se adjunta al reporte HTML.

El nombre del archivo incluye la fecha, la hora y el nombre del test:

```text
2026-11-22_12-59-01_test_login_exitoso.png
```

---

## Logging

El archivo `logs/ejecucion.log` registra:

- Inicio y cierre del navegador.
- Usuario con el que se inicia sesión.
- Producto que se agrega o se quita.
- Navegación al carrito y al checkout.
- Capturas guardadas.
- Errores y advertencias.

También se muestran los logs por consola durante la ejecución.

---

## Integración continua

El workflow `.github/workflows/pruebas.yml` se ejecuta en cada push o pull
request a `main`.

Hace lo siguiente:

1. Instala Python y las dependencias.
2. Ejecuta `pytest` en modo headless.
3. Sube el reporte, los logs y las evidencias como artefactos.

---

## Notas

- SauceDemo tiene usuarios con errores intencionales (`problem_user`,
  `performance_glitch_user`, `visual_user`, `error_user`). Esos usuarios se
  usan en la exploración documentada en `docs/informe_qa.md`, no en la suite
  principal.
- Cada test crea su propio navegador, por eso son independientes.
- Las credenciales de SauceDemo son públicas y están en `datos/usuarios.json`.
- No se guardan contraseñas reales ni claves de API.

---

## Repositorio

https://github.com/JoseloFlores/proyecto-final-automation-testing-jose-flores
