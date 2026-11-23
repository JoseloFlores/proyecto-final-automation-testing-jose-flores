# Entrega Final — Informe de QA

**Alumno:** José Flores  
**Plataforma:** SauceDemo (sitio web de práctica)  
**URL:** https://www.saucedemo.com  
**Repositorio:** https://github.com/JoseloFlores/proyecto-final-automation-testing-jose-flores  
**Fecha:** Noviembre de 2026  
**Entrega:** Framework de automatización de pruebas + informe de QA

> **Nota:** este informe sigue el modelo de entregable del curso. El proyecto
> real es el framework de automatización que está en el repositorio. Las
> secciones de Jira/Zephyr son simuladas porque no se tuvo acceso a esas
> herramientas. Los datos de SauceDemo son públicos y se usan solo con fines
> académicos.

---

## Índice

1. [Storytelling](#1-storytelling)
2. [Requerimientos ágiles](#2-requerimientos-ágiles)
3. [Plan de pruebas](#3-plan-de-pruebas)
4. [Casos de prueba](#4-casos-de-prueba)
5. [Ejecución de pruebas](#5-ejecución-de-pruebas)
6. [Gestión de defectos](#6-gestión-de-defectos)
7. [Métricas y cobertura](#7-métricas-y-cobertura)
8. [Jira y Zephyr](#8-jira-y-zephyr)

---

## 1. Storytelling

Lucía Gómez es analista y necesita una mochila para su notebook. Entra a
**SauceDemo**, inicia sesión con el usuario `standard_user`, ordena los
productos de menor a mayor precio y agrega la **Sauce Labs Backpack** al
carrito. Revisa que el producto esté en el carrito, completa el checkout con
sus datos y recibe el mensaje **“Thank you for your order!”**.

El flujo que se automatizó es:

**Login → Inventario → Carrito → Checkout → Confirmación**

También se probaron casos negativos, como un usuario bloqueado, una
contraseña incorrecta y un checkout sin los datos obligatorios.

---

## 2. Requerimientos ágiles

**Épica:** Compra online en SauceDemo.

| Feature | User Story | Aceptación funcional | Aceptación no funcional | Error handling |
|---|---|---|---|---|
| Login | Como visitante, quiero iniciar sesión para acceder al catálogo. | El formulario acepta usuario y contraseña. Al enviar, redirige a `/inventory.html` y muestra “Products”. | La página debe cargar en menos de 2 segundos en condiciones normales. | Si el usuario está bloqueado o la clave es incorrecta, se muestra un mensaje y no se accede. |
| Catálogo y carrito | Como comprador, quiero agregar y quitar productos del carrito. | El botón “Add to cart” agrega el producto. El badge muestra la cantidad. El producto aparece en `/cart.html`. | El badge debe actualizarse sin recargar la página. | Si el carrito queda vacío, no debe mostrarse un badge. |
| Checkout | Como comprador, quiero completar mis datos y finalizar la compra. | El formulario pide nombre, apellido y código postal. Al finalizar se muestra la confirmación. | El flujo debe funcionar en desktop, tablet y móvil. | Si falta un campo obligatorio, se muestra un error y no se avanza. |
| Ordenamiento | Como comprador, quiero ordenar los productos por precio. | Al elegir “Price (low to high)”, los precios quedan de menor a mayor. | La lista debe actualizarse sin recargar la página. | Si el orden no se aplica, se registra como defecto. |

---

## 3. Plan de pruebas

### 3.1 Alcance

Se validan estas partes de SauceDemo:

1. Login.
2. Inventario de productos.
3. Carrito de compras.
4. Checkout y confirmación.
5. Ordenamiento por precio.
6. Responsividad básica en tres tamaños de pantalla.
7. API pública JSONPlaceholder para las pruebas de Requests.

### 3.2 Objetivos

- Verificar los flujos principales de compra.
- Incluir al menos un escenario negativo.
- Parametrizar los datos desde archivos JSON.
- Separar la lógica de los tests de los localizadores con Page Object Model.
- Generar un reporte HTML con estado y duración.
- Guardar capturas cuando un test falla.
- Registrar los pasos importantes en un log.
- Ejecutar las pruebas de forma automática con GitHub Actions.

### 3.3 Estrategia

| Tipo de prueba | Cómo se aplica |
|---|---|
| Funcional automatizada | Tests de UI con Selenium y tests de API con Requests. |
| Negativa | Usuario bloqueado, contraseña incorrecta y checkout sin datos. |
| Parametrizada | Usuarios y clientes leídos desde `datos/*.json`. |
| Exploratoria | Pruebas con los usuarios problemáticos de SauceDemo (`problem_user`, `performance_glitch_user`, `visual_user`, `error_user`). |
| No funcional básica | Tiempo de carga del inventario y comportamiento en tres tamaños de pantalla. |
| Regresión | La suite completa se ejecuta en cada push con GitHub Actions. |

### 3.4 Recursos y roles

| Recurso | Descripción |
|---|---|
| Tester | José Flores (desarrollo, ejecución y documentación). |
| Dispositivo | PC con Linux y Google Chrome 158. |
| Navegador | Chrome en modo visible y headless. |
| Herramientas | Python 3.13, Selenium, pytest, pytest-html, Requests, GitHub Actions. |
| Datos | `datos/usuarios.json` y `datos/checkout.json`. |
| Evidencias | `docs/evidencias/` y `reports/screenshots/`. |

### 3.5 Cronograma

| Día | Actividad |
|---|---|
| Día 1 | Preparación del entorno, repositorio y datos de prueba. |
| Día 2 | Page Objects y tests de login y carrito. |
| Día 3 | Tests de checkout, ordenamiento y responsividad. |
| Día 4 | Tests de API, exploración con usuarios problemáticos y reporte. |
| Día 5 | Documentación, GitHub Actions y revisión final. |

---

## 4. Casos de prueba

### 4.1 Casos de UI

| ID | User Story | Tipo | Pasos | Datos de prueba | Resultado esperado |
|---|---|---|---|---|---|
| TC-001 | Login válido | Funcional | 1. Abrir SauceDemo.<br>2. Escribir usuario y clave.<br>3. Clic en Login. | `standard_user` / `secret_sauce` | Redirige a `/inventory.html` y muestra “Products”. |
| TC-002 | Usuario bloqueado | Negativo | 1. Abrir SauceDemo.<br>2. Escribir usuario bloqueado.<br>3. Clic en Login. | `locked_out_user` / `secret_sauce` | Muestra “Sorry, this user has been locked out.” y no entra. |
| TC-003 | Contraseña incorrecta | Negativo | 1. Abrir SauceDemo.<br>2. Escribir usuario válido y clave incorrecta.<br>3. Clic en Login. | `standard_user` / `clave_mala` | Muestra “Username and password do not match any user in this service”. |
| TC-004 | Agregar producto | Funcional | 1. Iniciar sesión.<br>2. Clic en “Add to cart” del primer producto. | Producto: Sauce Labs Backpack | El badge del carrito muestra `1`. |
| TC-005 | Quitar producto | Funcional | 1. Iniciar sesión.<br>2. Agregar el primer producto.<br>3. Clic en “Remove”. | Producto: Sauce Labs Backpack | El badge desaparece y el carrito queda vacío. |
| TC-006 | Producto en el carrito | Funcional | 1. Iniciar sesión.<br>2. Agregar un producto.<br>3. Abrir el carrito. | Sauce Labs Backpack | El nombre del producto aparece en `/cart.html`. |
| TC-007 | Ordenar por precio | Funcional | 1. Iniciar sesión.<br>2. Elegir “Price (low to high)”. | Orden `lohi` | Los precios quedan de menor a mayor. |
| TC-008 | Checkout completo | Funcional | 1. Agregar un producto.<br>2. Ir al carrito.<br>3. Checkout.<br>4. Completar datos.<br>5. Continuar y finalizar. | Dos clientes de `checkout.json` | Muestra “Thank you for your order!”. |
| TC-009 | Checkout sin datos | Negativo | 1. Agregar un producto.<br>2. Ir al checkout.<br>3. Clic en Continue sin completar. | Campos vacíos | Muestra “First Name is required” y no avanza. |
| TC-010 | Responsividad | No funcional | 1. Ejecutar el flujo principal en 1920×1080, 768×1024 y 390×844. | Tres tamaños de pantalla | El flujo funciona en los tres tamaños. |

### 4.2 Casos de API

API usada: **JSONPlaceholder** (`https://jsonplaceholder.typicode.com`).

| ID | Método | Endpoint | Datos | Resultado esperado |
|---|---|---|---|---|
| API-001 | GET | `/posts/1` | — | Status 200 y JSON con `id`, `title`, `body` y `userId`. |
| API-002 | GET | `/posts?userId=1` | `userId=1` | Status 200, lista no vacía y todos los posts del usuario 1. |
| API-003 | POST | `/posts` | `title`, `body`, `userId` | Status 201 y los datos enviados en la respuesta. |
| API-004 | GET + GET | `/users/1` y `/posts?userId=1` | `id` del usuario | Status 200 y posts del usuario consultado. |
| API-005 | DELETE | `/posts/1` | — | Status 200 o 204. |
| API-006 | GET | `/posts/999999` | — | Status 404. |

---

## 5. Ejecución de pruebas

### 5.1 Resultado general

| Métrica | Resultado |
|---|---|
| Tests automatizados | 18 |
| Tests ejecutados | 18 |
| Tests pasados | 18 |
| Tests fallidos | 0 |
| Duración aproximada | 16 segundos |
| Navegador | Google Chrome 158 en modo headless |
| Sistema | Linux |

### 5.2 Ejecución de los casos de UI

| ID | Caso | Resultado | Evidencia |
|---|---|---|---|
| TC-001 | Login válido | ✅ Pass | [TC-001](evidencias/TC-001_login_exitoso.png) |
| TC-002 | Usuario bloqueado | ✅ Pass | [TC-002](evidencias/TC-002_login_usuario_bloqueado.png) |
| TC-003 | Contraseña incorrecta | ✅ Pass | [TC-003](evidencias/TC-003_login_clave_incorrecta.png) |
| TC-004 | Agregar producto | ✅ Pass | [TC-004](evidencias/TC-004_agregar_producto.png) |
| TC-005 | Quitar producto | ✅ Pass | [TC-005](evidencias/TC-005_quitar_producto.png) |
| TC-006 | Producto en el carrito | ✅ Pass | [TC-006](evidencias/TC-006_carrito_producto.png) |
| TC-007 | Ordenar por precio | ✅ Pass | [TC-007](evidencias/TC-007_ordenar_por_precio.png) |
| TC-008 | Checkout completo | ✅ Pass | [TC-008](evidencias/TC-008_checkout_completo.png) |
| TC-009 | Checkout sin datos | ✅ Pass | [TC-009](evidencias/TC-009_checkout_obligatorios.png) |
| TC-010 | Responsividad | ✅ Pass | [Desktop](evidencias/responsive_1920_login.png), [Tablet](evidencias/responsive_768_login.png), [Móvil](evidencias/responsive_390_login.png) |

### 5.3 Ejecución de los casos de API

| ID | Caso | Resultado | Evidencia |
|---|---|---|---|
| API-001 | GET de un post | ✅ Pass | Reporte HTML |
| API-002 | GET filtrado por usuario | ✅ Pass | Reporte HTML |
| API-003 | POST de un post | ✅ Pass | Reporte HTML |
| API-004 | Encadenamiento usuario → posts | ✅ Pass | Reporte HTML |
| API-005 | DELETE de un post | ✅ Pass | Reporte HTML |
| API-006 | GET de un post inexistente | ✅ Pass | Reporte HTML |

El detalle de cada ejecución está en `reports/reporte.html`.

### 5.4 Responsividad

Se ejecutó el flujo completo en tres tamaños de pantalla. Las capturas se
guardan automáticamente en `docs/evidencias/`.

| Sección | Desktop 1920×1080 | Tablet 768×1024 | Móvil 390×844 | Observaciones |
|---|---|---|---|---|
| Login | [Captura](evidencias/responsive_1920_login.png) | [Captura](evidencias/responsive_768_login.png) | [Captura](evidencias/responsive_390_login.png) | El formulario se ve completo en los tres tamaños. |
| Inventario | [Captura](evidencias/responsive_1920_inventario.png) | [Captura](evidencias/responsive_768_inventario.png) | [Captura](evidencias/responsive_390_inventario.png) | En móvil los productos se muestran en una columna. |
| Carrito | [Captura](evidencias/responsive_1920_carrito.png) | [Captura](evidencias/responsive_768_carrito.png) | [Captura](evidencias/responsive_390_carrito.png) | El botón Checkout queda visible en los tres tamaños. |
| Checkout | [Captura](evidencias/responsive_1920_checkout.png) | [Captura](evidencias/responsive_768_checkout.png) | [Captura](evidencias/responsive_390_checkout.png) | El formulario se completa sin problemas. |

---

## 6. Gestión de defectos

### 6.1 Proceso de reporte y ciclo de vida

1. **Detección:** se ejecuta el caso de prueba y se observa un comportamiento
   distinto al esperado.
2. **Registro:** se completa el bug con resumen, pasos, resultado esperado,
   resultado obtenido, severidad, prioridad y evidencia.
3. **Asignación:** el bug se asigna al responsable del desarrollo.
4. **Corrección:** el desarrollador investiga y corrige.
5. **Verificación:** el tester vuelve a ejecutar el caso asociado.
6. **Cierre:** si el caso pasa, el bug se cierra; si falla, se reabre.

En este proyecto los bugs se encontraron en la exploración con los usuarios
problemáticos de SauceDemo. La suite principal usa `standard_user` y pasa
completa.

### 6.2 Tabla de bug reports

| Bug ID | User Story | Resumen | Pasos para reproducir | Resultado esperado | Resultado obtenido | Severidad | Prioridad | Estado | TC vinculado | Evidencia |
|---|---|---|---|---|---|---|---|---|---|---|
| BUG-001 | Catálogo | Imágenes rotas y ordenamiento incorrecto con `problem_user`. | 1. Login con `problem_user`.<br>2. Ver el inventario.<br>3. Ordenar por precio de menor a mayor. | Las 12 imágenes se ven y los precios quedan ordenados. | 6 de 12 imágenes no tienen `src`; las demás muestran la imagen 404. Al ordenar, el primer precio es `$29.99` y no `$7.99`. | Alta | Alta | Open | TC-007 | [Captura](evidencias/BUG-001_problem_user_inventory.png) |
| BUG-002 | Login / catálogo | El inventario tarda más de 5 segundos con `performance_glitch_user`. | 1. Login con `performance_glitch_user`.<br>2. Medir el tiempo hasta `/inventory.html`. | La carga debe ser menor a 2 segundos. | La carga tarda aproximadamente 5,3 segundos. | Media | Alta | Open | TC-001 | [Captura](evidencias/BUG-002_performance_glitch_user.png) |
| BUG-003 | Ordenamiento | Precios inconsistentes al ordenar con `visual_user`. | 1. Login con `visual_user`.<br>2. Elegir “Price (low to high)”. | Los precios quedan de menor a mayor. | Aparecen valores como `$45.08`, `$3.6` y `$36.89`, sin orden. | Media | Media | Open | TC-007 | [Captura](evidencias/BUG-003_visual_user_sort.png) |
| BUG-004 | Ordenamiento | Alerta de JavaScript al ordenar con `error_user`. | 1. Login con `error_user`.<br>2. Elegir “Price (low to high)”. | La lista se ordena sin errores. | Aparece la alerta “Sorting is broken! This error has been reported to Backtrace.” | Alta | Alta | Open | TC-007 | [Captura](evidencias/BUG-004_error_user.png) |

### 6.3 Ciclo de vida de un bug (ejemplo BUG-001)

1. **Open:** se detecta que `problem_user` muestra imágenes rotas y no ordena.
2. **In Progress:** se revisa si el problema es del sitio o del test.
3. **Code Review:** se documenta que el comportamiento es intencional en
   SauceDemo y no un error del framework.
4. **Testing:** se vuelve a ejecutar el flujo con `standard_user` y la suite
   principal sigue pasando.
5. **Closed:** el bug queda documentado como hallazgo de la plataforma de
   práctica.

---

## 7. Métricas y cobertura

| Métrica | Valor | Estándar | Observación |
|---|---|---|---|
| Ejecución de casos automatizados | 18/18 = 100 % | ≥ 90 % | Todos los tests de la suite pasan. |
| Tasa de defectos | 4/10 = 40 % | < 20 % | Los 4 bugs son de los usuarios problemáticos de SauceDemo, no del flujo principal. |
| Distribución por severidad | Alta 50 % / Media 50 % / Baja 0 % | — | Dos bugs altos y dos medios. |
| Desviación del tiempo estimado | 9 h reales / 8 h estimadas = +12,5 % | ≤ 0 % | La exploración y el informe llevaron más tiempo. |
| Cobertura de funciones críticas | 4/4 = 100 % | ≥ 80 % | Login, carrito, checkout y ordenamiento. |

### Interpretación y mejoras propuestas

- **Ejecución:** la suite automatizada cubre el 100 % de los casos definidos.
  Se puede seguir ampliando con más combinaciones de datos.
- **Defectos:** la tasa es alta porque SauceDemo incluye usuarios con errores
  intencionales. Esos bugs se documentan como hallazgos, no como fallos del
  framework.
- **Severidad:** conviene priorizar los bugs altos (imágenes rotas y alerta de
  ordenamiento) antes de los medios.
- **Tiempo:** para la próxima entrega conviene agregar un margen del 10 % al
  estimar las tareas de exploración y documentación.
- **Cobertura:** se puede agregar un caso de logout y otro de persistencia del
  carrito al recargar la página.

---

## 8. Jira y Zephyr

> **Aclaración:** no se tuvo acceso a Jira ni a Zephyr. Las tablas de esta
> sección son una simulación académica para mostrar cómo se organizaría el
> trabajo. No son capturas reales de las herramientas.

### 8.1 Backlog

| Historia | Prioridad | Estimación | Estado |
|---|---|---|---|
| Login de usuario | Alta | 2 puntos | Done |
| Carrito de compras | Alta | 3 puntos | Done |
| Checkout | Alta | 3 puntos | Done |
| Ordenamiento por precio | Media | 2 puntos | Done |

### 8.2 Sprint

| Campo | Valor |
|---|---|
| Duración | 1 semana |
| Historias | 4 |
| Puntos comprometidos | 10 |
| Puntos completados | 10 |
| Fecha de inicio | 16/11/2026 |
| Fecha de cierre | 22/11/2026 |

### 8.3 Test Cycle

| TC | Historia | Estado | Evidencia |
|---|---|---|---|
| TC-001 a TC-010 | Login, carrito, checkout y ordenamiento | Pass | `docs/evidencias/` |
| API-001 a API-006 | Pruebas de API | Pass | `reports/reporte.html` |

### 8.4 Diagrama de flujo acumulado (burndown)

| Día | Puntos restantes |
|---|---|
| Día 1 | 10 |
| Día 2 | 7 |
| Día 3 | 4 |
| Día 4 | 1 |
| Día 5 | 0 |

### 8.5 Sprint Report

- Historias completadas: 4 de 4.
- Puntos completados: 10 de 10.
- Tests automatizados: 18.
- Bugs documentados: 4 (todos de usuarios problemáticos de SauceDemo).
- Observación: el equipo quedó conforme con la cobertura del flujo principal.
- Próximo paso: agregar logout y persistencia del carrito.

---

## Anexo: trazabilidad entre casos y tests

| Caso | Test automatizado |
|---|---|
| TC-001 | `tests/test_login.py::test_login_exitoso` |
| TC-002 | `tests/test_login.py::test_login_fallido[usuario_bloqueado]` |
| TC-003 | `tests/test_login.py::test_login_fallido[clave_incorrecta]` |
| TC-004 | `tests/test_carrito.py::test_agregar_producto` |
| TC-005 | `tests/test_carrito.py::test_quitar_producto` |
| TC-006 | `tests/test_carrito.py::test_agregar_producto` |
| TC-007 | `tests/test_inventario.py::test_ordenar_por_precio` |
| TC-008 | `tests/test_checkout.py::test_checkout_completo` |
| TC-009 | `tests/test_checkout.py::test_checkout_campos_obligatorios` |
| TC-010 | `tests/test_responsive.py::test_responsive_paginas` |
| API-001 a API-006 | `tests/test_api.py` |

---

## Conclusión

El framework permite ejecutar las pruebas de UI y de API de forma consistente,
generar un reporte HTML, guardar evidencias y revisar los logs. La suite
principal pasa completa con `standard_user`. Los defectos documentados son
comportamientos intencionales de SauceDemo y sirven para mostrar cómo se
registraría un bug en un proyecto real.
