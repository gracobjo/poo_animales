"""Genera el cuaderno y el PDF de arquitectura (Refugio Animal v3).

Salidas:
- ../arquitectura_refugio_animal_v3.ipynb
- docs/Arquitectura_Refugio_Animal_v3.pdf
"""

from __future__ import annotations

import json
from pathlib import Path

from fpdf import FPDF

CARPETA = Path(__file__).resolve().parent
REPO = CARPETA.parent
NOTEBOOK = REPO / "arquitectura_refugio_animal_v3.ipynb"
PDF_SALIDA = CARPETA / "docs" / "Arquitectura_Refugio_Animal_v3.pdf"
FUENTE = Path(r"C:\Windows\Fonts\arial.ttf")
FUENTE_B = Path(r"C:\Windows\Fonts\arialbd.ttf")


def md(source: str) -> dict:
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": [line + "\n" for line in source.strip("\n").split("\n")],
    }


def code(source: str) -> dict:
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [line + "\n" for line in source.strip("\n").split("\n")],
    }


CELLS: list[dict] = [
    md(
        """# Refugio Animal – versión 3: arquitectura y código

Análisis detallado de la estructura del proyecto, la responsabilidad de cada fichero y el flujo de ejecución.

Esta versión incorpora la **gestión dinámica de especies** desde Tkinter y una **ficha informativa** que utiliza realmente el modelo POO. Además, el **inventario de animales** se persiste en JSON (separado del catálogo de especies).

## Distinción arquitectónica clave

- El inventario de animales utiliza **diccionarios** (+ persistencia `inventario.json`).
- Las especies **nativas** se representan mediante **clases Python**.
- Las especies **personalizadas** usan `EspeciePersonalizada` configurada con datos.
- El **adaptador** conecta registros del inventario con objetos POO.
- **Tkinter** usa esos objetos para mostrar información y comportamientos.

Es una arquitectura **híbrida**: programación estructurada + POO + persistencia JSON."""
    ),
    md(
        """## 1. Estructura general de carpetas

```text
entregable_tarea1/
│
├── gestion_animales_tkinter.ipynb
├── arquitectura_refugio_animal_v3.ipynb
│
└── tarea1/
    ├── app.py
    ├── main.py
    ├── ejecutar_tests.py
    ├── probar_crud.py
    ├── pyproject.toml
    ├── .python-version
    ├── README.md
    ├── refugio.jpg
    ├── Enunciado_oficial_Tarea_1.pdf
    ├── adjuntos/
    ├── datos/
    ├── docs/
    ├── exportacion/
    ├── interfaz/
    ├── muestras/
    ├── tests/
    └── validaciones/
```

Cada carpeta agrupa módulos por **responsabilidad**."""
    ),
    md(
        """## 2. Carpeta raíz `tarea1/`

| Archivo | Función |
| --- | --- |
| `app.py` | Punto de entrada: carga inventario, crea Tkinter e inicia la app |
| `main.py` | Alternativa de arranque que delega en `app.py` |
| `ejecutar_tests.py` | Ejecuta pruebas y genera informes |
| `probar_crud.py` | Comprueba el CRUD sin GUI |
| `pyproject.toml` | Metadatos, Python y dependencias |
| `.python-version` | Python 3.14 |
| `README.md` | Instalación, ejecución y estructura |
| `refugio.jpg` | Logo de la aplicación |
| `Enunciado_oficial_Tarea_1.pdf` | Enunciado del ejercicio |

`app.py` es deliberadamente pequeño: solo inicia, no contiene la lógica de negocio."""
    ),
    code(
        """# Esquema del arranque (equivalente a app.py)
from pathlib import Path
import sys

RAIZ_PROGRAMA = Path("tarea1").resolve()  # en la app real: Path(__file__).parent
if str(RAIZ_PROGRAMA) not in sys.path:
    sys.path.insert(0, str(RAIZ_PROGRAMA))

print("1. Se añade la carpeta del programa a sys.path")
print("2. cargar_inventario() lee o siembra datos/inventario.json")
print("3. tk.Tk() crea la ventana")
print("4. GestorAnimales(raiz, inventario) construye la UI")
print("5. mainloop() espera eventos del usuario")"""
    ),
    md(
        """### Instrucciones clave de `app.py`

1. `Path(__file__).resolve().parent` obtiene la carpeta de `app.py`.
2. Se añade esa ruta a `sys.path` para facilitar los imports.
3. `cargar_inventario()` carga (o siembra) `datos/inventario.json`.
4. `tk.Tk()` crea la ventana principal.
5. `GestorAnimales()` construye la interfaz con el inventario.
6. `mainloop()` inicia el bucle de eventos.

`main.py` solo hace `from app import main` y llama a `main()`."""
    ),
    md(
        """## 2.2. Carpeta `datos/` — núcleo de la aplicación

| Archivo | Responsabilidad |
| --- | --- |
| `__init__.py` | Identifica el paquete |
| `constantes.py` | Especies nativas y límites de peso |
| `inventario.py` | Operaciones CRUD sobre diccionarios |
| `persistencia_inventario.py` | Carga/guarda `inventario.json` (atómico) |
| `modelos.py` | Clases POO |
| `decoradores.py` | Decorador `cuenta_usos` |
| `adaptador_poo.py` | Dict ↔ objeto POO |
| `gestor_especies.py` | Catálogo dinámico de especies |
| `especies_personalizadas.json` | Especies creadas desde Tkinter |
| `inventario.json` | Animales persistidos (se crea al arrancar) |
| `ficha.py` | Tratamientos, vacunas, documentos, foto |
| `adjuntos.py` | Archivos físicos por animal |
| `recursos.py` | Localiza el logo |

**Separación importante:** el catálogo de especies y el inventario de animales son dos JSON distintos."""
    ),
    md(
        """### A. `constantes.py`

Define las cinco especies nativas (`Perro`, `Gato`, `Conejo`, `Loro`, `Hámster`) y los límites de peso. Las personalizadas **no** se añaden aquí: las gestiona `gestor_especies.py`."""
    ),
    code(
        """# Constantes nativas (resumen)
ESPECIES = ("Perro", "Gato", "Conejo", "Loro", "Hámster")
PESO_MIN_KG = 0.01
PESO_MAX_KG = 100.0
print(ESPECIES)"""
    ),
    md(
        """### B. `inventario.py`

Tipo: `Inventario = Dict[int, Dict[str, Any]]`.

| Función | CRUD | Responsabilidad |
| --- | --- | --- |
| `animales_iniciales()` | Init | Animales de ejemplo |
| `crear_animal()` | Create | Valida y registra |
| `leer_animal()` | Read | Copia del registro |
| `actualizar_animal()` | Update | Modifica datos |
| `borrar_animal()` | Delete | Elimina animal y adjuntos |

`crear_animal()` **no** es una función de Tkinter: recibe datos, valida y modifica el inventario. Así se puede probar sin GUI."""
    ),
    code(
        """# Forma del inventario (ejemplo)
inventario = {
    1: {
        "nombre": "Luna",
        "especie": "Perro",
        "edad": 4,
        "peso": 18.5,
        "color": "Canela",
        "observaciones": "Sociable",
        "foto": None,
        "tratamientos": [],
        "vacunaciones": [],
        "documentos": [],
    }
}
print("Clave = ID; valor = diccionario de campos")"""
    ),
    md(
        """### Persistencia del inventario (`persistencia_inventario.py`)

Novedad respecto al análisis anterior (solo especies en JSON):

- `cargar_inventario()`: si no existe el archivo, siembra `animales_iniciales()` y lo guarda.
- `guardar_inventario()`: escritura atómica (temporal + `replace()`).
- Tras crear / actualizar / borrar / cambiar ficha clínica, `GestorAnimales` llama a `guardar_inventario()`.
- El catálogo sigue en `especies_personalizadas.json` (independiente)."""
    ),
    code(
        """# Demostración de la API de persistencia (ruta temporal)
import sys
from pathlib import Path
import tempfile

raiz = Path.cwd() / "tarea1"
if not (raiz / "datos").is_dir():
    raiz = Path.cwd()
if str(raiz) not in sys.path:
    sys.path.insert(0, str(raiz))

from datos.persistencia_inventario import cargar_inventario, guardar_inventario
from datos.inventario import crear_animal

with tempfile.TemporaryDirectory() as tmp:
    ruta = Path(tmp) / "inventario.json"
    inv = cargar_inventario(ruta)
    crear_animal(
        {
            "nombre": "Nico",
            "especie": "Perro",
            "edad": 2,
            "peso": 1.2,
            "color": "Marrón",
            "observaciones": "Demo persistencia",
        },
        inv,
    )
    guardar_inventario(inv, ruta)
    otra = cargar_inventario(ruta)
    print("Animales tras recargar:", sorted(otra))
    print("Nuevo:", otra[max(otra)]["nombre"])"""
    ),
    md(
        """### C. `modelos.py` — POO

Jerarquía:

```text
AnimalRefugio (ABC)
├── Perro / Gato / Conejo / Loro / Hámster
└── EspeciePersonalizada  (Hurón, Tortuga, … vía configuración)
```

- **Encapsulación:** `@property` + setters (edad 0–30, peso, nombre…).
- **Abstracción:** `@abstractmethod` para `hacer_sonido`, `tipo_alimentacion`, `cuidados_especificos`.
- **Polimorfismo:** `generar_ficha()` llama esos métodos; cada clase responde distinto.
- **`EspeciePersonalizada`:** no es una clase nueva por especie; recibe sonido/alimentación/cuidados por parámetros."""
    ),
    code(
        """# Polimorfismo con generar_ficha (si el paquete está disponible)
import sys
from pathlib import Path

raiz = Path.cwd() / "tarea1"
if not (raiz / "datos").is_dir():
    raiz = Path.cwd()
if str(raiz) not in sys.path:
    sys.path.insert(0, str(raiz))

from datos.modelos import Perro, EspeciePersonalizada

luna = Perro("Luna", 4, 18.5, "Canela", "Sociable")
nico = EspeciePersonalizada(
    "Nico", 2, 1.2, "Marrón", "Curioso",
    nombre_especie="Hurón",
    sonido="Emite pequeños chillidos",
    alimentacion="Carnívoro",
    cuidados="Entorno seguro y supervisión",
)
for animal in (luna, nico):
    ficha = animal.generar_ficha()
    print("---", animal.especie, animal.nombre)
    print(ficha["comportamiento"])
    print(ficha["alimentacion"])"""
    ),
    md(
        """### D. `decoradores.py`

`@cuenta_usos` incrementa un contador `_usos_<metodo>` en el objeto cada vez que se llama (p. ej. `info_basica`). Demuestra ampliar comportamiento sin tocar la lógica original.

### E. `adaptador_poo.py`

| Función | Responsabilidad |
| --- | --- |
| `registro_a_animal()` | Dict → objeto (nativa o personalizada) |
| `animal_a_campos()` | Objeto → campos básicos |
| `resumen_polimorfico()` | Resumen vía métodos del objeto |

Flujo de `registro_a_animal()`: especie → clase nativa si existe → si no, config del catálogo → `EspeciePersonalizada` → error controlado si falla.

### F. `gestor_especies.py` — `CatalogoEspecies`

Persistencia / consultas / modificaciones del JSON de especies. La interfaz no escribe JSON a mano: llama `catalogo.anadir(datos)`.

### G–I. `ficha.py`, `adjuntos.py`, `recursos.py`

Clínica homogénea, archivos bajo `adjuntos/<id>/fotos|documentos/` (límite 5 MB) y localización del logo."""
    ),
    md(
        """## 2.3. `validaciones/`

`validar_datos(datos, especie_previa=None)` comprueba nombre, especie activa, color, edad, peso y estructuras clínicas. Consulta el catálogo dinámico (`especie_permitida_en_alta`). Con `especie_previa` se pueden conservar animales de especies desactivadas.

La validación es **lógica de dominio**, no del botón de Tkinter."""
    ),
    md(
        """## 2.4. `interfaz/`

| Archivo | Responsabilidad |
| --- | --- |
| `gestor.py` | Ventana principal y eventos |
| `dialogo_especies.py` | Gestionar especies (`Toplevel`) |
| `ficha_clinica.py` | Tratamientos, vacunas, docs, fotos |
| `estilos.py` | Tema y tipografía |
| `vista_foto.py` | Miniaturas |
| `portapapeles.py` | Ctrl+V (archivos / imagen / texto) |

### Ficha POO en `gestor.py`

Al seleccionar una fila: `registro_a_animal(registro)` → `animal.generar_ficha()` → paneles Tkinter. La UI **no** pregunta si es perro o hurón.

Tras CRUD o cambios clínicos: `_persistir_inventario()` escribe `inventario.json`."""
    ),
    md(
        """## 2.5–2.9. Otras carpetas

| Carpeta | Rol |
| --- | --- |
| `exportacion/` | PDF con `fpdf2` (`PdfFichas`) desde diccionarios |
| `muestras/` | Fotos/docs de prueba (`generar_muestras.py`) |
| `adjuntos/` | Archivos importados por el usuario |
| `tests/` | Unit tests + `resultados/` |
| `docs/` | Requisitos, casos de uso, manuales, UML, este PDF |"""
    ),
    md(
        """## 3. Flujos de ejecución

### 3.1 Arranque

`app.py` → `cargar_inventario()` → `GestorAnimales` → `mainloop()`

### 3.2 Alta de animal

Formulario → `_crear()` → `crear_animal()` → `validar_datos()` + catálogo → inventario → **`guardar_inventario()`** → tabla

### 3.3 Selección y POO

Treeview → dict → `registro_a_animal()` → `generar_ficha()` → panel Tkinter

### 3.4 Especie personalizada

*Gestionar especies* → `CatalogoEspecies.anadir()` → `especies_personalizadas.json` → refrescar combobox → alta de animales de esa especie"""
    ),
    md(
        """## 4. Conceptos POO demostrados

| Concepto | Aplicación |
| --- | --- |
| Clases y objetos | `AnimalRefugio`, nativas, `EspeciePersonalizada` |
| Abstracción | ABC + métodos abstractos |
| Herencia | Especies concretas |
| Encapsulación | Properties / setters |
| Polimorfismo | `generar_ficha()` / sonido / cuidados |
| Decoradores | `@cuenta_usos` |
| Métodos de clase | `campos_desde_dict()` |

Una especie personalizada **no** es una clase Python nueva: es un `EspeciePersonalizada` configurado (p. ej. como Hurón)."""
    ),
    md(
        """## 5. Dependencias y ejecución

```text
requires-python >= 3.14
dependencies: fpdf2>=2.9.0
Pillow opcional (imágenes / portapapeles)
```

```bash
cd tarea1
python app.py
python ejecutar_tests.py
# o: python -m unittest discover -s tests -v
```

Con uv: `uv sync` y `uv run python app.py`."""
    ),
    md(
        """## 6. Cuadernos Jupyter

| Característica | `gestion_animales_tkinter.ipynb` | App `tarea1/` | Este cuaderno |
| --- | --- | --- | --- |
| Rol | Demo didáctica CRUD/POO | Entrega completa | Documentación de arquitectura |
| Especies JSON | Demo | Completo | Explica |
| Persistencia inventario | No | Sí (`inventario.json`) | Explica + demo |
| Fotos / clínica / PDF | No | Sí | Describe |"""
    ),
    md(
        """## 7–9. Observaciones y evolución

1. **Persistencia:** especies en un JSON; animales en otro (`inventario.json`). Los adjuntos siguen en carpetas por ID.
2. **Acentos:** `Hámster` ≠ `Hamster` (casefold no quita tildes).
3. **README:** debe reflejar solo ficheros presentes en la entrega.
4. **Pruebas GUI:** requieren entorno gráfico Windows.

| Versión | Característica |
| --- | --- |
| 1 | CRUD + diccionarios + Tkinter |
| 2 | POO, adaptador, ficha polimórfica |
| 3 | Especies dinámicas + JSON + ficha POO completa |
| 3+ | Persistencia del inventario de animales |

**Recorrido recomendado para la defensa:** crear especie Hurón → registrar Nico → seleccionar → explicar adaptador + `EspeciePersonalizada` + `generar_ficha()` → cerrar y reabrir la app para mostrar que el inventario persistió."""
    ),
]


def construir_notebook() -> None:
    # nbformat quita el \n final duplicado en la última línea de source
    cells = []
    for cell in CELLS:
        src = cell["source"]
        if src and src[-1].endswith("\n"):
            src = src[:-1] + [src[-1].rstrip("\n")]
            cell = {**cell, "source": src}
        cells.append(cell)
    nb = {
        "nbformat": 4,
        "nbformat_minor": 5,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3",
            },
            "language_info": {"name": "python", "pygments_lexer": "ipython3"},
        },
        "cells": cells,
    }
    NOTEBOOK.write_text(
        json.dumps(nb, ensure_ascii=False, indent=1) + "\n",
        encoding="utf-8",
    )
    print(f"Notebook: {NOTEBOOK}")


class PdfArquitectura(FPDF):
    def header(self) -> None:
        if self.page_no() == 1:
            return
        self.set_font("ArialDoc", "B", 9)
        self.set_text_color(80, 80, 80)
        self.cell(
            0,
            8,
            "Refugio Animal v3 — Análisis de arquitectura",
            new_x="LMARGIN",
            new_y="NEXT",
        )
        self.ln(2)

    def footer(self) -> None:
        self.set_y(-15)
        self.set_font("ArialDoc", size=8)
        self.set_text_color(120, 120, 120)
        self.cell(0, 10, f"Página {self.page_no()}/{{nb}}", align="C")


def _parrafo(pdf: PdfArquitectura, texto: str, size: int = 11) -> None:
    pdf.set_x(pdf.l_margin)
    pdf.set_font("ArialDoc", size=size)
    pdf.set_text_color(20, 20, 20)
    pdf.multi_cell(0, 6, texto)
    pdf.ln(1)


def _titulo(pdf: PdfArquitectura, texto: str, level: int = 1) -> None:
    pdf.ln(3 if level == 1 else 2)
    pdf.set_x(pdf.l_margin)
    pdf.set_font("ArialDoc", "B", 14 if level == 1 else 12)
    pdf.set_text_color(20, 40, 80)
    pdf.multi_cell(0, 7, texto)
    pdf.ln(1)


def _viñeta(pdf: PdfArquitectura, texto: str) -> None:
    pdf.set_x(pdf.l_margin)
    pdf.set_font("ArialDoc", size=11)
    pdf.set_text_color(20, 20, 20)
    pdf.multi_cell(0, 6, f"  -  {texto}")


def _tabla(pdf: PdfArquitectura, filas: list[list[str]], anchos: list[float]) -> None:
    pdf.set_x(pdf.l_margin)
    pdf.set_font("ArialDoc", "B", 9)
    pdf.set_fill_color(230, 235, 245)
    for i, celda in enumerate(filas[0]):
        pdf.cell(anchos[i], 7, celda[:80], border=1, fill=True)
    pdf.ln()
    pdf.set_font("ArialDoc", size=9)
    for fila in filas[1:]:
        pdf.set_x(pdf.l_margin)
        for i, celda in enumerate(fila):
            pdf.cell(anchos[i], 7, celda[:80], border=1)
        pdf.ln()
        pdf.set_x(pdf.l_margin)
    pdf.ln(2)


def construir_pdf() -> None:
    pdf = PdfArquitectura()
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=18)
    pdf.add_font("ArialDoc", "", str(FUENTE))
    pdf.add_font("ArialDoc", "B", str(FUENTE_B))
    pdf.add_page()

    pdf.set_x(pdf.l_margin)
    pdf.set_font("ArialDoc", "B", 18)
    pdf.set_text_color(20, 40, 80)
    pdf.multi_cell(0, 10, "Refugio Animal – versión 3")
    pdf.set_x(pdf.l_margin)
    pdf.set_font("ArialDoc", "B", 14)
    pdf.multi_cell(0, 8, "Análisis de la arquitectura y del código")
    pdf.ln(4)
    pdf.set_x(pdf.l_margin)
    _parrafo(
        pdf,
        "La aplicación combina diccionarios para el inventario, clases POO "
        "para especies nativas, EspeciePersonalizada para especies dinámicas, "
        "un adaptador dict↔objeto, Tkinter para la UI y dos JSON de "
        "persistencia: especies_personalizadas.json e inventario.json.",
    )

    _titulo(pdf, "1. Distinción arquitectónica")
    for item in (
        "Inventario de animales: diccionarios + inventario.json",
        "Especies nativas: clases Python (Perro, Gato, …)",
        "Especies personalizadas: EspeciePersonalizada + JSON",
        "Adaptador: conecta registros con objetos POO",
        "Tkinter: muestra fichas polimórficas generadas por los objetos",
    ):
        _viñeta(pdf, item)

    _titulo(pdf, "2. Estructura de carpetas")
    _parrafo(
        pdf,
        "tarea1/ agrupa app.py, main.py, datos/, validaciones/, interfaz/, "
        "exportacion/, adjuntos/, muestras/, tests/ y docs/. El cuaderno "
        "arquitectura_refugio_animal_v3.ipynb documenta esta misma visión.",
    )

    _titulo(pdf, "3. Punto de entrada")
    _parrafo(
        pdf,
        "app.py añade la carpeta al sys.path, carga el inventario con "
        "cargar_inventario(), crea tk.Tk(), instancia GestorAnimales y "
        "arranca mainloop(). main.py solo delega en app.main().",
    )

    _titulo(pdf, "4. Paquete datos/")
    _tabla(
        pdf,
        [
            ["Archivo", "Responsabilidad"],
            ["inventario.py", "CRUD sobre Dict[int, dict]"],
            ["persistencia_inventario.py", "Carga/guarda inventario.json"],
            ["modelos.py", "ABC AnimalRefugio y especies"],
            ["adaptador_poo.py", "registro_a_animal / ficha"],
            ["gestor_especies.py", "Catálogo + JSON especies"],
            ["ficha.py / adjuntos.py", "Clínica y archivos"],
        ],
        [55, 125],
    )
    _parrafo(
        pdf,
        "crear_animal valida con validar_datos (que consulta el catálogo) y "
        "asigna un ID. La UI persiste tras cada alta, edición, borrado o "
        "cambio de ficha clínica. El guardado es atómico (tmp + replace).",
    )

    _titulo(pdf, "5. POO y ficha polimórfica")
    _parrafo(
        pdf,
        "AnimalRefugio define propiedades encapsuladas y tres métodos "
        "abstractos. Las clases nativas y EspeciePersonalizada los "
        "implementan. generar_ficha() ensambla generales, comportamiento, "
        "alimentación y cuidados. Al seleccionar una fila, gestor.py "
        "convierte el dict con el adaptador y pinta la ficha sin if por especie.",
    )

    _titulo(pdf, "6. Interfaz Tkinter")
    _parrafo(
        pdf,
        "GestorAnimales coordina formulario, tabla, filtros, ficha POO, "
        "diálogo de especies, ficha clínica y exportación PDF. "
        "dialogo_especies.py no escribe JSON a mano: usa CatalogoEspecies. "
        "Los tests de GUI pasan persistir=False para no ensuciar el JSON real.",
    )

    _titulo(pdf, "7. Flujos")
    for item in (
        "Arranque: app → cargar_inventario → GestorAnimales → mainloop",
        "Alta: formulario → crear_animal → validar → guardar_inventario",
        "Selección: Treeview → adaptador → generar_ficha → paneles",
        "Especie: DialogoGestionEspecies → CatalogoEspecies → JSON → combobox",
    ):
        _viñeta(pdf, item)

    _titulo(pdf, "8. Validaciones y exportacion")
    _parrafo(
        pdf,
        "validar_datos pertenece al dominio: nombre, especie activa "
        "(CatalogoEspecies), color, edad 0-30, peso finito en rango y "
        "estructuras clinicas. especie_previa permite conservar animales "
        "de especies desactivadas. La exportacion PDF (PdfFichas / fpdf2) "
        "lee diccionarios del inventario; no necesita objetos POO.",
    )

    _titulo(pdf, "9. Dependencias y pruebas")
    _parrafo(
        pdf,
        "Python >= 3.14 y fpdf2. Ejecucion: python app.py. Pruebas: "
        "python ejecutar_tests.py o unittest discover -s tests. "
        "test_persistencia_inventario.py cubre carga, guardado atomico y "
        "JSON corrupto. Pillow es opcional para imagenes / portapapeles.",
    )

    _titulo(pdf, "10. Observaciones")
    for item in (
        "Especies e inventario son JSON distintos; los adjuntos van por carpeta ID.",
        "Hámster nativo lleva tilde; casefold no unifica con Hamster.",
        "Las pruebas GUI usan persistir=False para no ensuciar inventario.json.",
        "El cuaderno didactico no incluye clinica/PDF; la app de tarea1/ si.",
    ):
        _viñeta(pdf, item)

    _titulo(pdf, "11. Evolucion y defensa")
    _tabla(
        pdf,
        [
            ["Version", "Aporte"],
            ["1", "CRUD + diccionarios + Tkinter"],
            ["2", "POO, adaptador, ficha polimorfica"],
            ["3", "Especies dinamicas + JSON"],
            ["3+", "Persistencia del inventario"],
        ],
        [30, 150],
    )
    _parrafo(
        pdf,
        "Recorrido recomendado: crear Huron, registrar a Nico, seleccionar "
        "y explicar EspeciePersonalizada + generar_ficha; reiniciar la app "
        "para demostrar que inventario.json conserva los registros. "
        "Detalle ampliado: arquitectura_refugio_animal_v3.ipynb.",
    )

    PDF_SALIDA.parent.mkdir(parents=True, exist_ok=True)
    pdf.output(str(PDF_SALIDA))
    print(f"PDF: {PDF_SALIDA}")


if __name__ == "__main__":
    construir_notebook()
    construir_pdf()
