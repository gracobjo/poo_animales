# Tarea 1 — Refugio Animal (programa + documentación)

## Qué hay aquí

| Pieza | Rol |
| --- | --- |
| **Programa ejecutable** | Aplicación Tkinter CRUD |
| **Documentación** | Markdown, PDF y el cuaderno en la raíz del repo |

El cuaderno `../gestion_animales_tkinter.ipynb` se usa como **guion didáctico y documentación** paso a paso. El programa real son los `.py` de esta carpeta.

### Cuaderno vs programa (`app.py` / `main.py`)

Las dos interfaces **no son idénticas**. El cuaderno enseña el núcleo; la entrega es `tarea1/`.

| Aspecto | Cuaderno (`gestion_animales_tkinter.ipynb`) | Programa (`python app.py` o `main.py`) |
| --- | --- | --- |
| Rol | Guion didáctico | Entrega ejecutable |
| Código | Celdas autocontenidas | Módulos (`interfaz/gestor.py`, …) |
| CRUD + filtros + tabla | Sí | Sí |
| Panel ficha POO (`generar_ficha`) | Sí (versión compacta) | Sí |
| Scrollbars en ficha (comportamiento / alimentación / cuidados) | Sí | Sí |
| Especies personalizadas (`EspeciePersonalizada`) | Demo celdas + §5.2 JSON | Completo: *Gestionar especies* + JSON |
| Miniatura de foto en el formulario | Explicado §5.4 | Sí |
| Botón ficha clínica / adjuntos | Demo esquema §5.3 | Sí (diálogo completo) |
| Exportar PDF | Explicado §5.4 | Sí |
| Persistencia inventario (`inventario.json`) | Demo §5.1 | Sí |
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
| `tests/test_gestor_especies.py` | Catálogo dinámico y JSON de especies |
| `tests/test_portapapeles.py` | Lectura del portapapeles |
| `tests/test_persistencia_inventario.py` | `inventario.json` carga/guarda |

Dependencia PDF: `pip install fpdf2`

## Estructura del programa

```text
tarea1/
├── app.py / main.py
├── ejecutar_tests.py / probar_crud.py
├── pyproject.toml / .python-version
├── datos/
│   ├── constantes.py / inventario.py / persistencia_inventario.py
│   ├── ficha.py / adjuntos.py / recursos.py
│   ├── modelos.py / decoradores.py / adaptador_poo.py
│   ├── gestor_especies.py / especies_personalizadas.json
│   └── inventario.json            # (runtime; no va en el ZIP)
├── validaciones/reglas.py
├── interfaz/
│   ├── gestor.py / dialogo_especies.py / ficha_clinica.py
│   ├── estilos.py / vista_foto.py / portapapeles.py
├── exportacion/pdf_fichas.py
├── adjuntos/                      # plantilla vacía en el entregable
├── muestras/                      # fotos y documentos de prueba
├── tests/
│   ├── test_datos.py / test_validaciones.py / test_persistencia_inventario.py
│   ├── test_modelos_poo.py / test_gestor_especies.py
│   ├── test_interfaz.py / test_ficha_clinica.py
│   ├── test_portapapeles.py / test_exportacion_pdf.py
│   └── resultados/
├── docs/                          # requisitos, CU, UML, manuales, pruebas, PDF arquitectura
├── Enunciado_oficial_Tarea_1.pdf
├── Analisis_gestion_animales.md / Tarea_1.pdf
├── generar_pdf.py / generar_arquitectura_docs.py
├── refugio.jpg
└── README.md
```

En la raíz del ZIP `entregable_tarea1/` también van:

- `gestion_animales_tkinter.ipynb`
- `arquitectura_refugio_animal_v3.ipynb`

### Responsabilidades por módulo

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
| [Analisis_gestion_animales.md](Analisis_gestion_animales.md) | Análisis breve del proyecto |
| [Tarea_1.pdf](Tarea_1.pdf) | El mismo análisis en PDF |
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
