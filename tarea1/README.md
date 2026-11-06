# Tarea 1 — Refugio Animal (programa + defensa)

## Qué hay aquí

| Pieza | Rol |
| --- | --- |
| **Programa ejecutable** | Aplicación Tkinter CRUD |
| **Documentación / defensa** | Markdown, PDF y el cuaderno en la raíz del repo |

El cuaderno `../gestion_animales_tkinter.ipynb` se usa como **defensa y documentación** paso a paso. El programa real son los `.py` de esta carpeta.

### Cuaderno vs programa (`app.py` / `main.py`)

Las dos interfaces **no son idénticas**. El cuaderno enseña el núcleo; la entrega es `tarea1/`.

| Aspecto | Cuaderno (`gestion_animales_tkinter.ipynb`) | Programa (`python app.py` o `main.py`) |
| --- | --- | --- |
| Rol | Guion didáctico / defensa | Entrega ejecutable |
| Código | Celdas autocontenidas | Módulos (`interfaz/gestor.py`, …) |
| CRUD + filtros + tabla | Sí | Sí |
| Panel ficha POO (`generar_ficha`) | Sí (versión compacta) | Sí |
| Scrollbars en ficha (comportamiento / alimentación / cuidados) | Sí | Sí |
| Especies personalizadas (`EspeciePersonalizada`) | Demo en celdas (+ JSON simple opcional) | Completo: *Gestionar especies* + JSON |
| Miniatura de foto en el formulario | No | Sí |
| Botón ficha clínica / adjuntos | No | Sí |
| Exportar PDF | No | Sí |
| Persistencia inventario (`inventario.json`) | No | Sí |
| Estilos / tipografía (`estilos.py`) | Básicos de ttk | Tema completo |
| Título de ventana | *…(demo cuaderno)* | *Refugio Animal - Gestión de animales* |

Para enseñar conceptos: el cuaderno. Para demostrar la entrega: **`cd tarea1` → `python app.py`** (o `python main.py`).

## Cómo ejecutar el programa

Desde esta carpeta:

```bash
cd tarea1
python app.py
```

Desde la raíz del repositorio:

```bash
python tarea1/app.py
```

También vale `python main.py` (delega en `app.py`).

Prueba de CRUD **sin GUI**:

```bash
python probar_crud.py
```

## Casos de prueba

Documentación completa: [docs/pruebas.md](docs/pruebas.md).

**Ejecutar (consola + informe en disco):**

```bash
python tarea1/ejecutar_tests.py
```

**Solo consola:**

```bash
python -m unittest discover -s tarea1/tests -v
```

**Dónde queda el resultado**

| Destino | Qué es |
| --- | --- |
| Consola | Detalle y resumen al momento |
| `tests/resultados/ultimo_informe.txt` | Último informe (lo escribe `ejecutar_tests.py`) |
| `tests/resultados/informe_YYYYMMDD_HHMMSS.txt` | Copia histórica fechada |

| Archivo | Qué cubre |
| --- | --- |
| `tests/test_interfaz.py` | GUI: CRUD, filtros, diálogos |
| `tests/test_datos.py` | Inventario y CRUD |
| `tests/test_validaciones.py` | `validar_datos()` |
| `tests/test_exportacion_pdf.py` | PDF de fichas |
| `tests/test_ficha_clinica.py` | Tratamientos, vacunas, docs, foto |
| `tests/test_modelos_poo.py` | Herencia, `@property`, decoradores, adaptador |
| `tests/test_persistencia_inventario.py` | `inventario.json` carga/guarda |

Dependencia PDF: `pip install fpdf2`

## Estructura del programa

```text
tarea1/
├── app.py                 # Punto de entrada (ventana + mainloop)
├── main.py                # Alias de app.py
├── ejecutar_tests.py      # Batería unittest + informe en disco
├── probar_crud.py         # Mini prueba Create/Read/Update/Delete
├── datos/
│   ├── __init__.py
│   ├── constantes.py      # ESPECIES, rangos de peso
│   ├── inventario.py              # animales_iniciales + CRUD
│   ├── persistencia_inventario.py # inventario.json (carga/guarda)
│   ├── ficha.py                   # Tratamientos, vacunas, docs, foto
│   ├── adjuntos.py                # Copia de archivos a adjuntos/
│   ├── modelos.py                 # ABC AnimalRefugio + EspeciePersonalizada
│   ├── decoradores.py             # Decorador propio @cuenta_usos
│   ├── adaptador_poo.py           # Puente dict ↔ objeto
│   ├── gestor_especies.py         # Catálogo nativas + personalizadas
│   ├── especies_personalizadas.json
│   ├── inventario.json            # (runtime) animales persistidos
│   └── recursos.py                # Logo refugio.png / .jpg
├── refugio.jpg            # (o refugio.png) logo GUI + PDF
├── validaciones/
│   ├── __init__.py
│   └── reglas.py          # validar_datos()
├── interfaz/
│   ├── __init__.py
│   ├── estilos.py         # Guía de tipografía / ttk.Style
│   ├── gestor.py          # clase GestorAnimales (Tkinter)
│   ├── dialogo_especies.py# Gestionar especies (Toplevel)
│   └── ficha_clinica.py   # Diálogo clínica / adjuntos
├── exportacion/
│   ├── __init__.py
│   └── pdf_fichas.py      # PDF: una ficha por animal (fpdf2)
├── adjuntos/              # Fotos y documentos importados por animal
├── muestras/              # Fotos/PDF/DOCX de ejemplo para probar importación
├── tests/
│   ├── test_interfaz.py
│   ├── test_datos.py
│   ├── test_validaciones.py
│   ├── test_persistencia_inventario.py
│   ├── test_exportacion_pdf.py
│   └── test_ficha_clinica.py
├── docs/
│   ├── requisitos.md
│   ├── casos_de_uso.md
│   ├── manual_usuario.md
│   ├── manual_desarrollador.md
│   ├── uml.md
│   ├── pruebas.md
│   └── Arquitectura_Refugio_Animal_v3.pdf
├── Enunciado_oficial_Tarea_1.pdf
├── Analisis_defensa_gestion_animales.md
├── generar_pdf.py
├── generar_arquitectura_docs.py
└── README.md
```

### Responsabilidades (como en la defensa)

| Módulo | Contenido |
| --- | --- |
| `datos/` | CRUD, modelos POO, catálogo de especies e `inventario.json` |
| `validaciones/` | `validar_datos()` |
| `interfaz/` | Clase `GestorAnimales` |
| `app.py` / `main.py` | Arranque (pocas líneas) |

El inventario se manipula en memoria como **diccionarios** y se **persiste** en `datos/inventario.json` (archivo distinto del catálogo de especies).

## Documentación

| Documento | Contenido |
| --- | --- |
| [docs/README.md](docs/README.md) | Índice de la documentación formal |
| [docs/README.md](docs/README.md) | Índice de toda la documentación |
| [docs/requisitos.md](docs/requisitos.md) | RF / RN / RNF (inventario, clínica, PDF, 5 MB, pegar) |
| [docs/casos_de_uso.md](docs/casos_de_uso.md) | UC01–UC12 |
| [docs/manual_usuario.md](docs/manual_usuario.md) | Manual de usuario |
| [docs/manual_desarrollador.md](docs/manual_desarrollador.md) | Manual de desarrollador |
| [docs/uml.md](docs/uml.md) | UML estructurales y de comportamiento |
| [docs/pruebas.md](docs/pruebas.md) | Tests e informes en `tests/resultados/` |
| [muestras/README.md](muestras/README.md) | Fotos y documentos de prueba |
| [Analisis_defensa_gestion_animales.md](Analisis_defensa_gestion_animales.md) | Guía corta de defensa oral |
| [docs/Arquitectura_Refugio_Animal_v3.pdf](docs/Arquitectura_Refugio_Animal_v3.pdf) | Análisis de arquitectura (PDF) |
| [Enunciado_oficial_Tarea_1.pdf](Enunciado_oficial_Tarea_1.pdf) | Enunciado |
| [../gestion_animales_tkinter.ipynb](../gestion_animales_tkinter.ipynb) | Cuaderno didáctico CRUD / POO |
| [../arquitectura_refugio_animal_v3.ipynb](../arquitectura_refugio_animal_v3.ipynb) | Cuaderno de arquitectura v3 |

## Temario

- `Tema2-POO/` — diccionarios + capa `AnimalRefugio` (herencia, properties, decoradores)
- `Tema3-InterfacesGraficas/` — pack/grid, StringVar, Treeview, diálogos, etc.

### Capa POO (Tema 2) sin romper el enunciado

El inventario sigue siendo un **diccionario**. Las clases demuestran herencia / encapsulación y se enlazan con `adaptador_poo.py`. Al seleccionar un animal, el panel **Información del animal seleccionado** muestra la ficha generada por el objeto (`generar_ficha()`), y la barra de estado mantiene un resumen breve.

## Aplicación práctica de la programación orientada a objetos

En esta fase la POO no es solo un ejemplo aislado: los objetos **proporcionan** la información específica de cada especie que muestra Tkinter.

| Principio | Cómo se ve en el proyecto |
| --- | --- |
| **Herencia** | `Perro`, `Gato`, `Conejo`, `Loro` y `Hamster` heredan de `AnimalRefugio`. |
| **Encapsulación** | `@property` / setters validan nombre, edad, peso, color y observaciones. |
| **Abstracción** | `AnimalRefugio` define el contrato (`hacer_sonido`, `tipo_alimentacion`, `cuidados_especificos`) y ensambla `generar_ficha()`. |
| **Polimorfismo** | La interfaz llama los mismos métodos; cada especie responde distinto (sonido, alimentación, cuidados). |

**Recorrido de los datos al seleccionar una fila:**

`Diccionario del inventario` → `registro_a_animal()` (adaptador) → objeto de la especie → `generar_ficha()` → panel Tkinter (*Datos generales*, *Comportamiento*, *Alimentación*, *Cuidados específicos*).

Las tres últimas secciones usan `Text` con **barra de desplazamiento** para textos largos (típico en especies personalizadas).

La interfaz **no** usa `if especie == "Perro"`: solo presenta las secciones que devuelve el objeto.

Los objetos son **representaciones temporales** para consultar la ficha. El CRUD, la persistencia conceptual y el inventario en memoria siguen basados en diccionarios.

## Gestión dinámica de especies y programación orientada a objetos

Puedes ampliar el catálogo **desde Tkinter** (botón *Gestionar especies*) sin editar código Python.

| Tipo | Ejemplos | Representación |
| --- | --- | --- |
| **Nativas** | Perro, Gato, Conejo, Loro, Hámster | Clases propias en `datos/modelos.py` |
| **Personalizadas** | Hurón, Tortuga, … | Una sola clase `EspeciePersonalizada` + JSON |

`EspeciePersonalizada` hereda de `AnimalRefugio` e implementa sonido, alimentación y cuidados con los textos configurados en el formulario. **No** se generan clases nuevas ni se usa `eval()`: el polimorfismo basta (mismo contrato, distinta configuración).

Persistencia: `datos/especies_personalizadas.json` (catálogo) e `datos/inventario.json` (animales). Ambos son UTF-8 y están separados a propósito.

```text
Usuario
  → Ventana Tkinter: Gestionar especies
  → CatalogoEspecies (datos/gestor_especies.py)
  → especies_personalizadas.json
  → Combobox del formulario de animales
  → Registro dict en el inventario
  → registro_a_animal() (adaptador)
  → AnimalRefugio / EspeciePersonalizada
  → Panel ficha dinámica (generar_ficha)
```

Desactivar una especie personalizada impide nuevas altas pero permite seguir consultando animales ya registrados. Eliminar solo es posible si ningún animal la usa.
