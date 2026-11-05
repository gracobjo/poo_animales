"""Genera Tarea_1.pdf a partir del análisis de defensa (Unicode con Arial)."""

from pathlib import Path

from fpdf import FPDF

CARPETA = Path(__file__).resolve().parent
FUENTE = Path(r"C:\Windows\Fonts\arial.ttf")
FUENTE_B = Path(r"C:\Windows\Fonts\arialbd.ttf")
SALIDA = CARPETA / "Tarea_1.pdf"


class PdfTarea(FPDF):
    def header(self) -> None:
        if self.page_no() == 1:
            return
        self.set_font("ArialDoc", "B", 9)
        self.set_text_color(80, 80, 80)
        self.cell(
            0,
            8,
            "Tarea 1 — Análisis y defensa · Refugio Animal (Tkinter)",
            new_x="LMARGIN",
            new_y="NEXT",
        )
        self.ln(2)

    def footer(self) -> None:
        self.set_y(-15)
        self.set_font("ArialDoc", size=8)
        self.set_text_color(120, 120, 120)
        self.cell(0, 10, f"Página {self.page_no()}/{{nb}}", align="C")


def _reset_x(pdf: PdfTarea) -> None:
    pdf.set_x(pdf.l_margin)


def escribir_parrafo(pdf: PdfTarea, texto: str, size: int = 11) -> None:
    _reset_x(pdf)
    pdf.set_font("ArialDoc", size=size)
    pdf.set_text_color(20, 20, 20)
    pdf.multi_cell(0, 6, texto)
    pdf.ln(1)
    _reset_x(pdf)


def escribir_titulo(pdf: PdfTarea, texto: str, level: int = 1) -> None:
    pdf.ln(3 if level == 1 else 2)
    _reset_x(pdf)
    if level == 1:
        pdf.set_font("ArialDoc", "B", 14)
    else:
        pdf.set_font("ArialDoc", "B", 12)
    pdf.set_text_color(20, 40, 80)
    pdf.multi_cell(0, 7, texto)
    pdf.ln(1)
    _reset_x(pdf)


def escribir_viñeta(pdf: PdfTarea, texto: str) -> None:
    _reset_x(pdf)
    pdf.set_font("ArialDoc", size=11)
    pdf.set_text_color(20, 20, 20)
    pdf.multi_cell(0, 6, f"  -  {texto}")
    _reset_x(pdf)


def tabla_simple(pdf: PdfTarea, filas: list, anchos: list) -> None:
    _reset_x(pdf)
    pdf.set_font("ArialDoc", "B", 9)
    pdf.set_fill_color(230, 235, 245)
    for i, celda in enumerate(filas[0]):
        pdf.cell(anchos[i], 7, celda, border=1, fill=True)
    pdf.ln()
    _reset_x(pdf)
    pdf.set_font("ArialDoc", size=9)
    for fila in filas[1:]:
        for i, celda in enumerate(fila):
            pdf.cell(anchos[i], 7, celda[:80], border=1)
        pdf.ln()
        _reset_x(pdf)
    pdf.ln(2)
    _reset_x(pdf)


def main() -> None:
    pdf = PdfTarea(format="A4")
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=18)
    pdf.add_font("ArialDoc", "", str(FUENTE))
    pdf.add_font("ArialDoc", "B", str(FUENTE_B))
    pdf.add_page()

    pdf.set_font("ArialDoc", "B", 18)
    pdf.set_text_color(15, 35, 70)
    _reset_x(pdf)
    pdf.multi_cell(0, 9, "Tarea 1")
    _reset_x(pdf)
    pdf.set_font("ArialDoc", "B", 14)
    pdf.multi_cell(0, 8, "Analisis y defensa del proyecto")
    pdf.ln(2)
    _reset_x(pdf)
    escribir_parrafo(
        pdf,
        "Programa: Refugio Animal — gestor CRUD con Tkinter. "
        "Cuaderno: gestion_animales_tkinter.ipynb. "
        "Enunciado: Enunciado_oficial_Tarea_1.pdf. "
        "Entrega: 12 de noviembre de 2026.",
    )
    escribir_parrafo(
        pdf,
        "Documento para explicar y defender el trabajo: organización, "
        "relación con Tema 2 (POO/estructuras) y Tema 3 (Tkinter), "
        "y respuestas a posibles cambios de refactorización.",
    )

    escribir_titulo(pdf, "1. Relación con el enunciado")
    tabla_simple(
        pdf,
        [
            ["Requisito", "Cómo se cumple"],
            ["Temática libre", "Refugio / inventario de animales"],
            ["Diccionario complejo", "animales: ID -> ficha con varios campos"],
            ["CRUD", "Crear, leer, actualizar, borrar"],
            ["Interfaz tkinter", "Clase GestorAnimales + tk/ttk"],
            ["Presentación / cambios", "Sección de preguntas de refactorización"],
        ],
        [55, 135],
    )
    escribir_parrafo(
        pdf,
        "Dato clave: los datos viven en un diccionario EN MEMORIA. "
        "No hay base de datos. Es deliberado: el objetivo es practicar "
        "Tkinter y estructuras del lenguaje, no la persistencia.",
    )

    escribir_titulo(pdf, "2. Idea general")
    escribir_parrafo(
        pdf,
        "Aplicación de escritorio con las cuatro operaciones CRUD. "
        "Create: crear_animal / _crear. Read: leer_animal / _seleccionar / "
        "_actualizar_tabla. Update: actualizar_animal / _actualizar. "
        "Delete: borrar_animal / _borrar.",
    )
    escribir_parrafo(
        pdf,
        "Frase de apertura recomendada: «Es una aplicación CRUD con Tkinter "
        "que separa la lógica de datos (funciones sobre un diccionario) de la "
        "lógica de interfaz (clase GestorAnimales).»",
    )

    escribir_titulo(pdf, "3. Mapa con el temario")
    escribir_titulo(pdf, "3.1 Tema 2 — POO y estructuras", 2)
    escribir_parrafo(
        pdf,
        "El enunciado pide diccionarios, no clases Animal. Aun así se vinculan "
        "ideas del Tema 2: identidad por ID; funciones CRUD como comportamiento "
        "separado de la GUI; validar_datos como contrato con ValueError; "
        "evolución posible hacia clases Animal/Perro/Gato/Loro del proyecto poo_animales.",
    )
    escribir_titulo(pdf, "3.2 Tema 3 — Interfaces gráficas", 2)
    for linea in [
        "Gestores de geometría: pack en bloques; grid dentro de LabelFrame.",
        "Variables de control: StringVar en Entry/Combobox.",
        "Frame/LabelFrame: formulario, filtros y zona de tabla.",
        "Button/Entry: acciones CRUD y campos de texto.",
        "Eventos: KeyRelease, ComboboxSelected, TreeviewSelect.",
        "Cajas de diálogo: showerror, showinfo, askyesno.",
        "TTK, Combobox, Text y Treeview (tabla con iid = ID).",
    ]:
        escribir_viñeta(pdf, linea)

    escribir_titulo(pdf, "4. Datos iniciales (diccionario)")
    escribir_parrafo(
        pdf,
        "ESPECIES = (Perro, Gato, Loro) alimenta los Combobox. "
        "animales usa un ID numérico como clave y un diccionario como valor. "
        "Ventaja frente a una lista: acceso O(1) por ID, actualizar/borrar "
        "sin recorrer, y el ID actúa como clave primaria.",
    )

    escribir_titulo(pdf, "5. Funciones CRUD puras")
    escribir_parrafo(
        pdf,
        "validar_datos limpia con strip, obliga nombre/especie/color, "
        "valida edad 0-30 y peso finito > 0; si falla lanza ValueError. "
        "crear/leer/actualizar/borrar reciben el inventario como argumento. "
        "leer_animal usa copy(). crear_animal calcula max(inventario, default=0)+1. "
        "Punto fuerte: se pueden probar sin abrir ninguna ventana.",
    )

    escribir_titulo(pdf, "6. Prueba rápida")
    escribir_parrafo(
        pdf,
        "inventario_prueba = {} independiente. Flujo: Crear -> Leer -> "
        "Actualizar (edad 2 a 3) -> Borrar (quedan 0). Mini prueba manual; "
        "en un proyecto real se usaría unittest/pytest.",
    )

    escribir_titulo(pdf, "7. Interfaz gráfica (GestorAnimales)")
    for linea in [
        "Variables StringVar enlazan formulario y datos.",
        "Layout: pack en el padre; grid dentro de cada LabelFrame (sin mezclar en el mismo contenedor).",
        "Treeview: show=headings, selectmode=browse, iid=str(id).",
        "Eventos: búsqueda en tiempo real, filtro de especie, carga al seleccionar fila.",
        "Acciones: try/except ValueError -> messagebox; borrado con askyesno.",
        "_actualizar_tabla reconstruye filas aplicando filtros de texto y especie.",
    ]:
        escribir_viñeta(pdf, linea)

    escribir_titulo(pdf, "8. Ejecución")
    escribir_parrafo(
        pdf,
        "raiz = tk.Tk(); aplicacion = GestorAnimales(raiz, animales); "
        "raiz.mainloop().",
    )

    escribir_titulo(pdf, "9. Preguntas de refactorización (respuestas cortas)")
    preguntas = [
        "1. Nueva especie Conejo: añadirla a ESPECIES; Combobox y filtro se actualizan solos.",
        "2. Persistencia: JSON (simple), CSV, o SQLite (más correcto); las firmas CRUD apenas cambian.",
        "3. Módulos: datos.py (CRUD), validaciones.py, interfaz.py (GestorAnimales), main.py (arranque).",
        "4. Campo chip: registro + validación + Checkbutton/BooleanVar + columna Treeview + seleccionar/formulario.",
        "5. ¿Por qué no clases? El enunciado pedía diccionarios; POO sería una segunda versión.",
        "6. Nombres repetidos: no hay problema; el único es el ID.",
        "7. Estadísticas: Toplevel con Counter por especie y medias; opcional Canvas/matplotlib.",
        "8. ¿Por qué borrar/reinsertar la tabla? Con filtros es más simple; en inventarios pequeños es suficiente.",
        "9. Peso con coma: replace(',', '.') antes de float.",
        "10. Confirmar salida: protocol WM_DELETE_WINDOW + askyesno.",
    ]
    for p in preguntas:
        escribir_viñeta(pdf, p)

    escribir_titulo(pdf, "10. Consejos para la defensa")
    for linea in [
        "Empieza por lo general: CRUD + separación datos/GUI.",
        "Nombra principios: validación con excepciones, variables de control, gestores de geometría.",
        "Si piden un cambio en vivo: lee, explica el plan, luego edita.",
        "Si algo no está: «lo haría así…» y describe el enfoque.",
        "Domina pack / grid / place (aquí no se usa place).",
    ]:
        escribir_viñeta(pdf, linea)

    escribir_titulo(pdf, "11. Checklist antes de presentar")
    for linea in [
        "Ejecutar el cuaderno completo (datos, CRUD, prueba, GUI).",
        "Probar crear/editar/borrar y filtros.",
        "Provocar un error de validación y mostrar el messagebox.",
        "Señalar validar_datos y el Treeview.",
        "Tener listas las respuestas de especie nueva y JSON.",
        "Relacionar al menos 5 widgets con lecciones del Tema 3.",
    ]:
        escribir_viñeta(pdf, linea)

    pdf.output(str(SALIDA))
    print(f"Generado: {SALIDA}")


if __name__ == "__main__":
    main()
