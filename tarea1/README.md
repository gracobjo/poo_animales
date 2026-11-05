# Tarea 1 — Refugio Animal (programa + defensa)

## Qué hay aquí

| Pieza | Rol |
| --- | --- |
| **Programa ejecutable** | Aplicación Tkinter CRUD |
| **Documentación / defensa** | Markdown, PDF y el cuaderno en la raíz del repo |

El cuaderno `../gestion_animales_tkinter.ipynb` se usa como **defensa y documentación** paso a paso. El programa real son los `.py` de esta carpeta.

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
│   ├── inventario.py      # animales_iniciales + CRUD
│   ├── ficha.py           # Tratamientos, vacunas, docs, foto
│   ├── adjuntos.py        # Copia de archivos a adjuntos/
│   ├── modelos.py         # ABC AnimalRefugio + herencia / @property
│   ├── decoradores.py     # Decorador propio @cuenta_usos
│   └── adaptador_poo.py   # Puente dict ↔ objeto
├── validaciones/
│   ├── __init__.py
│   └── reglas.py          # validar_datos()
├── interfaz/
│   ├── __init__.py
│   ├── estilos.py         # Guía de tipografía / ttk.Style
│   ├── gestor.py          # clase GestorAnimales (Tkinter)
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
│   ├── test_exportacion_pdf.py
│   └── test_ficha_clinica.py
├── docs/
│   ├── requisitos.md
│   ├── casos_de_uso.md
│   ├── manual_usuario.md
│   ├── manual_desarrollador.md
│   └── uml.md
├── Enunciado_oficial_Tarea_1.pdf
├── Analisis_defensa_gestion_animales.md
├── Tarea_1.pdf
├── generar_pdf.py
└── README.md
```

### Responsabilidades (como en la defensa)

| Módulo | Contenido |
| --- | --- |
| `datos/` | `ESPECIES`, inventario inicial y funciones CRUD |
| `validaciones/` | `validar_datos()` |
| `interfaz/` | Clase `GestorAnimales` |
| `app.py` / `main.py` | Arranque (pocas líneas) |

Los datos siguen en un **diccionario en memoria** (sin base de datos), como pide el enunciado.

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
| [Tarea_1.pdf](Tarea_1.pdf) | Defensa en PDF |
| [Enunciado_oficial_Tarea_1.pdf](Enunciado_oficial_Tarea_1.pdf) | Enunciado |
| [../gestion_animales_tkinter.ipynb](../gestion_animales_tkinter.ipynb) | Cuaderno = defensa / documentación narrada |

## Temario

- `Tema2-POO/` — diccionarios + capa `AnimalRefugio` (herencia, properties, decoradores)
- `Tema3-InterfacesGraficas/` — pack/grid, StringVar, Treeview, diálogos, etc.

### Capa POO (Tema 2) sin romper el enunciado

El inventario sigue siendo un **diccionario**. Las clases demuestran herencia / encapsulación y se enlazan con `adaptador_poo.py`. Al seleccionar un animal, la barra de estado muestra un resumen polimórfico (`hacer_sonido`, alimentación).
