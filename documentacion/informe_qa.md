# Entrega Final — Informe de QA

**Alumno:** Jose Flores  
**Plataforma:** SauceDemo (sitio web de practica)  
**URL:** https://www.saucedemo.com  
**Repositorio:** https://github.com/JoseloFlores/proyecto-final-automation-testing-jose-flores  
**Fecha:** Noviembre de 2026  
**Entrega:** Framework de automatizacion de pruebas + informe de QA

> **Nota:** este informe sigue el modelo de entregable del curso. El proyecto
> principal es el framework de automatizacion que esta en el repositorio. Las
> secciones de Jira y Zephyr son simuladas porque no se tuvo acceso a esas
> herramientas. Los datos de SauceDemo son publicos y se usan solo para el curso.

---

## Indice

1. [Historia de usuario (Storytelling)](#1-historia-de-usuario-storytelling)
2. [Requerimientos agiles](#2-requerimientos-agiles)
3. [Plan de pruebas](#3-plan-de-pruebas)
4. [Casos de prueba](#4-casos-de-prueba)
5. [Ejecucion de pruebas](#5-ejecucion-de-pruebas)
6. [Gestion de defectos](#6-gestion-de-defectos)
7. [Metricas y cobertura](#7-metricas-y-cobertura)
8. [Jira y Zephyr](#8-jira-y-zephyr)

---

## 1. Historia de usuario (Storytelling)

Lucia Gomez necesita comprar una mochila para su computadora. Entra a
**SauceDemo**, inicia sesion con `standard_user`, ordena los productos de menor
a mayor precio y agrega **Sauce Labs Backpack** al carrito. Revisa que el
producto este cargado en el carrito, completa sus datos de compra y recibe el
mensaje **"Thank you for your order!"**.

El flujo automatizado es:

**Inicio de sesion -> Inventario -> Carrito -> Compra -> Confirmacion**

Tambien se probaron casos negativos: usuario bloqueado, clave incorrecta y
formulario de compra sin completar los campos obligatorios.

---

## 2. Requerimientos agiles

**Epica:** Compra online en SauceDemo.

| Funcionalidad | Historia de usuario | Aceptacion funcional | Aceptacion no funcional | Manejo de errores |
|---|---|---|---|---|
| Inicio de sesion | Como visitante, quiero iniciar sesion para ver el catalogo. | El formulario recibe usuario y clave. Al ingresar, abre `/inventory.html` y muestra "Products". | La pagina carga en menos de 2 segundos en condiciones normales. | Si el usuario esta bloqueado o la clave no coincide, muestra error y no entra. |
| Catalogo y carrito | Como comprador, quiero agregar y quitar productos del carrito. | El boton "Add to cart" suma el producto, actualiza el contador y lo muestra en `/cart.html`. | El contador cambia sin recargar toda la pagina. | Si el carrito queda vacio, no debe mostrarse el contador. |
| Compra | Como comprador, quiero cargar mis datos y terminar el pedido. | El formulario pide nombre, apellido y codigo postal. Al finalizar muestra la confirmacion. | Debe funcionar en escritorio, tableta y celular. | Si falta un campo obligatorio, avisa con un mensaje y no avanza. |
| Ordenamiento | Como comprador, quiero ordenar los productos por precio. | Al elegir "Price (low to high)", los precios quedan de menor a mayor. | La lista se ordena al instante. | Si no ordena bien, se reporta como defecto. |

---

## 3. Plan de pruebas

### 3.1 Alcance

Se validan estas pantallas y servicios:

1. Inicio de sesion.
2. Inventario de productos.
3. Carrito de compras.
4. Formulario y confirmacion de compra.
5. Ordenamiento por precio.
6. Vista en tres tamaños de pantalla (escritorio, tableta y celular).
7. API publica JSONPlaceholder usando Requests.

### 3.2 Objetivos

- Automatizar los flujos principales de compra.
- Cubrir escenarios negativos.
- Leer los datos de prueba desde archivos JSON.
- Aplicar el patron Page Object Model para ordenar el codigo.
- Generar un reporte HTML con resultado y duracion.
- Sacar capturas automaticas cuando falla una prueba.
- Guardar un registro detallado de pasos en un archivo de log.
- Ejecutar las pruebas automaticamente en GitHub Actions.

### 3.3 Estrategia

| Tipo de prueba | Como se aplica |
|---|---|
| Funcional automatizada | Pruebas de interfaz con Selenium y pruebas de API con Requests. |
| Negativa | Usuario bloqueado, clave incorrecta y compra sin datos. |
| Parametrizada | Usuarios y clientes leidos desde `datos/usuarios.json` y `datos/compra.json`. |
| Exploratoria | Revision manual y con script sobre los usuarios especiales de SauceDemo (`problem_user`, `performance_glitch_user`, `visual_user`, `error_user`). |
| No funcional basica | Tiempo de carga del inventario y pruebas en tres resoluciones de pantalla. |
| Regresion | Toda la bateria corre en cada push con GitHub Actions. |

### 3.4 Recursos y roles

| Recurso | Descripcion |
|---|---|
| Responsable | Jose Flores (codigo, ejecucion y documentacion). |
| Equipo | PC con Linux y Google Chrome 158. |
| Navegador | Chrome con ventana y en modo sin pantalla (`SIN_VENTANA=true`). |
| Herramientas | Python 3.13, Selenium, pytest, pytest-html, Requests, GitHub Actions. |
| Datos | `datos/usuarios.json` y `datos/compra.json`. |
| Evidencias | `documentacion/evidencias/` y `reportes/capturas/`. |

### 3.5 Cronograma

| Dia | Actividad |
|---|---|
| Dia 1 | Preparacion del entorno, carpetas y datos en JSON. |
| Dia 2 | Clases del Page Object Model y pruebas de login y carrito. |
| Dia 3 | Pruebas de compra, ordenamiento y tamaños de pantalla. |
| Dia 4 | Pruebas de API, exploracion de errores y reporte HTML. |
| Dia 5 | Documentacion, GitHub Actions y revision final. |

---

## 4. Casos de prueba

### 4.1 Casos de interfaz

| ID | Caso | Tipo | Pasos | Datos | Resultado esperado |
|---|---|---|---|---|---|
| CP-001 | Inicio de sesion valido | Funcional | 1. Abrir SauceDemo.<br>2. Cargar usuario y clave.<br>3. Clic en Login. | `standard_user` / `secret_sauce` | Abre `/inventory.html` y muestra "Products". |
| CP-002 | Usuario bloqueado | Negativo | 1. Abrir SauceDemo.<br>2. Cargar usuario bloqueado.<br>3. Clic en Login. | `locked_out_user` / `secret_sauce` | Muestra "Sorry, this user has been locked out." y no ingresa. |
| CP-003 | Clave incorrecta | Negativo | 1. Abrir SauceDemo.<br>2. Cargar usuario valido y clave mala.<br>3. Clic en Login. | `standard_user` / `clave_mala` | Muestra "Username and password do not match any user in this service". |
| CP-004 | Agregar producto | Funcional | 1. Iniciar sesion.<br>2. Clic en "Add to cart" del primer producto. | Sauce Labs Backpack | El contador del carrito muestra `1`. |
| CP-005 | Quitar producto | Funcional | 1. Iniciar sesion.<br>2. Agregar el primer producto.<br>3. Clic en "Remove". | Sauce Labs Backpack | El contador desaparece y el carrito queda vacio. |
| CP-006 | Producto en carrito | Funcional | 1. Iniciar sesion.<br>2. Agregar producto.<br>3. Abrir el carrito. | Sauce Labs Backpack | El producto aparece en `/cart.html`. |
| CP-007 | Ordenar por precio | Funcional | 1. Iniciar sesion.<br>2. Elegir "Price (low to high)". | Orden `lohi` | Los precios quedan ordenados de menor a mayor. |
| CP-008 | Compra completa | Funcional | 1. Agregar producto.<br>2. Ir al carrito y al formulario.<br>3. Cargar datos.<br>4. Continuar y finalizar. | Dos clientes de `datos/compra.json` | Muestra "Thank you for your order!". |
| CP-009 | Compra sin datos | Negativo | 1. Agregar producto.<br>2. Ir al formulario.<br>3. Clic en Continue sin escribir nada. | Campos vacios | Muestra "First Name is required" y no avanza. |
| CP-010 | Pantallas distintas | No funcional | 1. Ejecutar el flujo en 1920x1080, 768x1024 y 390x844. | Tres resoluciones | El flujo anda en las tres pantallas. |

### 4.2 Casos de API

API publica usada: **JSONPlaceholder** (`https://jsonplaceholder.typicode.com`).

| ID | Metodo | Ruta | Datos | Resultado esperado |
|---|---|---|---|---|
| API-001 | GET | `/posts/1` | — | Codigo 200 y JSON con `id`, `title`, `body` y `userId`. |
| API-002 | GET | `/posts?userId=1` | `userId=1` | Codigo 200, lista no vacia y todas del usuario 1. |
| API-003 | POST | `/posts` | `title`, `body`, `userId` | Codigo 201 y los mismos datos en la respuesta. |
| API-004 | GET + GET | `/users/1` y `/posts?userId=1` | `id` obtenido | Codigo 200 y publicaciones del usuario encontrado. |
| API-005 | DELETE | `/posts/1` | — | Codigo 200 o 204. |
| API-006 | GET | `/posts/999999` | — | Codigo 404. |

---

## 5. Ejecucion de pruebas

### 5.1 Resumen general

| Dato | Resultado |
|---|---|
| Pruebas automatizadas | 18 |
| Pruebas ejecutadas | 18 |
| Pruebas pasadas | 18 |
| Pruebas fallidas | 0 |
| Duracion aproximada | 19 segundos |
| Navegador | Google Chrome 158 (modo sin pantalla) |
| Sistema | Linux |

### 5.2 Ejecucion de interfaz

| ID | Caso | Resultado | Evidencia |
|---|---|---|---|
| CP-001 | Inicio de sesion valido | ✅ Paso | [CP-001](evidencias/CP-001_inicio_sesion_exitoso.png) |
| CP-002 | Usuario bloqueado | ✅ Paso | [CP-002](evidencias/CP-002_usuario_bloqueado.png) |
| CP-003 | Clave incorrecta | ✅ Paso | [CP-003](evidencias/CP-003_clave_incorrecta.png) |
| CP-004 | Agregar producto | ✅ Paso | [CP-004](evidencias/CP-004_agregar_producto.png) |
| CP-005 | Quitar producto | ✅ Paso | [CP-005](evidencias/CP-005_quitar_producto.png) |
| CP-006 | Producto en carrito | ✅ Paso | [CP-006](evidencias/CP-006_producto_en_carrito.png) |
| CP-007 | Ordenar por precio | ✅ Paso | [CP-007](evidencias/CP-007_ordenar_por_precio.png) |
| CP-008 | Compra completa | ✅ Paso | [CP-008](evidencias/CP-008_compra_completa.png) |
| CP-009 | Compra sin datos | ✅ Paso | [CP-009](evidencias/CP-009_compra_campos_obligatorios.png) |
| CP-010 | Pantallas distintas | ✅ Paso | [Escritorio](evidencias/responsivo_1920_login.png), [Tableta](evidencias/responsivo_768_login.png), [Celular](evidencias/responsivo_390_login.png) |

### 5.3 Ejecucion de API

| ID | Caso | Resultado | Evidencia |
|---|---|---|---|
| API-001 | Obtener una publicacion | ✅ Paso | Reporte HTML |
| API-002 | Publicaciones por usuario | ✅ Paso | Reporte HTML |
| API-003 | Crear publicacion | ✅ Paso | Reporte HTML |
| API-004 | Usuario y luego sus publicaciones | ✅ Paso | Reporte HTML |
| API-005 | Eliminar publicacion | ✅ Paso | Reporte HTML |
| API-006 | Publicacion inexistente | ✅ Paso | Reporte HTML |

El detalle completo se ve en `reportes/reporte.html`.

### 5.4 Tabla de pantallas (responsividad)

| Seccion | Escritorio 1920x1080 | Tableta 768x1024 | Celular 390x844 | Observaciones |
|---|---|---|---|---|
| Inicio de sesion | [Captura](evidencias/responsivo_1920_login.png) | [Captura](evidencias/responsivo_768_login.png) | [Captura](evidencias/responsivo_390_login.png) | El formulario se ve completo en las tres pantallas. |
| Inventario | [Captura](evidencias/responsivo_1920_inventario.png) | [Captura](evidencias/responsivo_768_inventario.png) | [Captura](evidencias/responsivo_390_inventario.png) | En celular los productos se apilan en una sola columna. |
| Carrito | [Captura](evidencias/responsivo_1920_carrito.png) | [Captura](evidencias/responsivo_768_carrito.png) | [Captura](evidencias/responsivo_390_carrito.png) | El boton de continuar compra queda visible en las tres vistas. |
| Compra | [Captura](evidencias/responsivo_1920_compra.png) | [Captura](evidencias/responsivo_768_compra.png) | [Captura](evidencias/responsivo_390_compra.png) | El formulario se puede completar sin problemas. |

---

## 6. Gestion de defectos

### 6.1 Proceso de reporte y ciclo de vida

1. **Deteccion:** al probar un caso aparece un comportamiento distinto al esperado.
2. **Registro:** se anota resumen, pasos, esperado, obtenido, severidad, prioridad y captura.
3. **Asignacion:** se asigna a quien corresponda corregirlo.
4. **Correccion:** se arregla el codigo del sitio.
5. **Verificacion:** se vuelve a ejecutar el caso de prueba.
6. **Cierre:** si pasa, se cierra; si sigue fallando, se reabre.

En este proyecto los errores registrados son comportamientos que SauceDemo trae
a proposito en sus usuarios especiales. La bateria principal corre con
`standard_user` y pasa completa.

### 6.2 Tabla de reportes de errores

| ID | Pantalla | Resumen | Pasos para reproducir | Esperado | Obtenido | Severidad | Prioridad | Estado | Caso | Evidencia |
|---|---|---|---|---|---|---|---|---|---|---|
| ERROR-001 | Inventario | Imagenes rotas y orden incorrecto con `problem_user`. | 1. Entrar con `problem_user`.<br>2. Mirar las fotos.<br>3. Ordenar de menor a mayor precio. | Todas las imagenes se ven bien y los precios quedan ordenados. | Varias imagenes muestran la foto de error y el primer precio queda en `$29.99` en lugar de `$7.99`. | Alta | Alta | Abierto | CP-007 | [Captura](evidencias/ERROR-001_usuario_problema_inventario.png) |
| ERROR-002 | Inicio de sesion | Demora de mas de 5 segundos al entrar con `performance_glitch_user`. | 1. Entrar con `performance_glitch_user`.<br>2. Medir cuanto tarda en cargar `/inventory.html`. | Menos de 2 segundos. | Tarda alrededor de 5,3 segundos. | Media | Alta | Abierto | CP-001 | [Captura](evidencias/ERROR-002_usuario_lento.png) |
| ERROR-003 | Inventario | Precios desordenados con `visual_user`. | 1. Entrar con `visual_user`.<br>2. Elegir "Price (low to high)". | Precios ordenados de menor a mayor. | Muestra valores como `$45.08`, `$3.6` y `$36.89` sin orden. | Media | Media | Abierto | CP-007 | [Captura](evidencias/ERROR-003_usuario_visual_orden.png) |
| ERROR-004 | Inventario | Alerta de error al ordenar con `error_user`. | 1. Entrar con `error_user`.<br>2. Elegir "Price (low to high)". | La lista se ordena normalmente. | Sale una alerta del navegador: "Sorting is broken! This error has been reported to Backtrace." | Alta | Alta | Abierto | CP-007 | [Captura](evidencias/ERROR-004_usuario_error.png) |

### 6.3 Ejemplo de ciclo de vida (ERROR-001)

1. **Abierto:** se detecta que `problem_user` tiene fotos rotas y no ordena.
2. **En progreso:** se revisa si falla el codigo de prueba o la web.
3. **Revision:** se confirma que es un fallo intencional del sitio de practica.
4. **En prueba:** se verifica que el usuario normal (`standard_user`) sigue andando bien.
5. **Cerrado:** queda anotado como hallazgo de la plataforma.

---

## 7. Metricas y cobertura

| Metrica | Valor | Referencia | Observacion |
|---|---|---|---|
| Ejecucion de pruebas automatizadas | 18/18 = 100 % | >= 90 % | Todas las pruebas pasan. |
| Tasa de defectos encontrados | 4/10 = 40 % | < 20 % | Son errores propios de los usuarios especiales de SauceDemo. |
| Severidad (Alta / Media / Baja) | 50 % / 50 % / 0 % | — | Dos altos y dos medios. |
| Desviacion del tiempo | 9 h reales / 8 h estimadas = +12,5 % | <= 0 % | La exploracion y la documentacion llevaron un poco mas. |
| Cobertura de funciones criticas | 4/4 = 100 % | >= 80 % | Login, carrito, compra y ordenamiento. |

### Mejoras para una proxima etapa

- Sumar pruebas de cierre de sesion (logout).
- Probar que el carrito mantenga los productos al recargar la pagina.
- Dejar un margen del 10 % extra en las estimaciones para documentar.

---

## 8. Jira y Zephyr

> **Aclaracion:** no se conto con acceso a Jira ni a Zephyr. Estas tablas son
> una simulacion academica para mostrar como se organizaria el trabajo.

### 8.1 Lista de pendientes (Backlog)

| Historia | Prioridad | Puntos | Estado |
|---|---|---|---|
| Inicio de sesion | Alta | 2 | Hecho |
| Carrito de compras | Alta | 3 | Hecho |
| Formulario de compra | Alta | 3 | Hecho |
| Ordenamiento por precio | Media | 2 | Hecho |

### 8.2 Sprint

| Dato | Valor |
|---|---|
| Duracion | 1 semana |
| Historias | 4 |
| Puntos planeados | 10 |
| Puntos terminados | 10 |
| Inicio | 16/11/2026 |
| Cierre | 22/11/2026 |

### 8.3 Ciclo de pruebas (Test Cycle)

| Casos | Historia | Resultado | Evidencia |
|---|---|---|---|
| CP-001 a CP-010 | Login, carrito, compra y ordenamiento | Paso | `documentacion/evidencias/` |
| API-001 a API-006 | Pruebas de API | Paso | `reportes/reporte.html` |

### 8.4 Avance del sprint (Burndown)

| Dia | Puntos pendientes |
|---|---|
| Dia 1 | 10 |
| Dia 2 | 7 |
| Dia 3 | 4 |
| Dia 4 | 1 |
| Dia 5 | 0 |

### 8.5 Resumen del sprint

- Historias terminadas: 4 de 4.
- Puntos terminados: 10 de 10.
- Pruebas automatizadas pasando: 18.
- Defectos anotados: 4 (usuarios especiales de SauceDemo).

---

## Anexo: relacion entre casos y pruebas automatizadas

| Caso | Prueba automatizada |
|---|---|
| CP-001 | `pruebas/prueba_login.py::prueba_inicio_sesion_exitoso` |
| CP-002 | `pruebas/prueba_login.py::prueba_inicio_sesion_fallido[usuario_bloqueado]` |
| CP-003 | `pruebas/prueba_login.py::prueba_inicio_sesion_fallido[clave_incorrecta]` |
| CP-004 | `pruebas/prueba_carrito.py::prueba_agregar_producto_al_carrito` |
| CP-005 | `pruebas/prueba_carrito.py::prueba_quitar_producto_del_carrito` |
| CP-006 | `pruebas/prueba_carrito.py::prueba_agregar_producto_al_carrito` |
| CP-007 | `pruebas/prueba_inventario.py::prueba_ordenar_productos_por_precio` |
| CP-008 | `pruebas/prueba_compra.py::prueba_compra_completa` |
| CP-009 | `pruebas/prueba_compra.py::prueba_compra_sin_datos_obligatorios` |
| CP-010 | `pruebas/prueba_responsivo.py::prueba_flujo_en_distintas_pantallas` |
| API-001 a API-006 | `pruebas/prueba_api.py` |
