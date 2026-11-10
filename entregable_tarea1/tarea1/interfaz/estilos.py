"""Guía de estilos de la interfaz (tipografía unificada).

``ttk`` usa la fuente del tema; ``tk.Text`` no: por defecto en Windows
suele ser monoespaciada (Courier). Esta guía fija la misma familia y
tamaños para etiquetas, entradas, botones, tabla y el área de texto.
"""

from __future__ import annotations

import sys
import tkinter as tk
from tkinter import ttk
# Familia: Segoe UI en Windows; Helvetica en el resto.
if sys.platform.startswith("win"):
    FAMILIA = "Segoe UI"
else:
    FAMILIA = "Helvetica"

TAMANO_BASE = 10
TAMANO_TITULO = 16
TAMANO_SUBTITULO = 10
TAMANO_TABLA = 10

# Tuplas de fuente Tk: (familia, tamaño) o (familia, tamaño, estilo).
FUENTE_BASE = (FAMILIA, TAMANO_BASE)
FUENTE_TITULO = (FAMILIA, TAMANO_TITULO, "bold")
FUENTE_SUBTITULO = (FAMILIA, TAMANO_SUBTITULO)
FUENTE_ETIQUETA = (FAMILIA, TAMANO_BASE)
FUENTE_ENTRADA = (FAMILIA, TAMANO_BASE)
FUENTE_BOTON = (FAMILIA, TAMANO_BASE)
FUENTE_TABLA = (FAMILIA, TAMANO_TABLA)
FUENTE_ESTADO = (FAMILIA, TAMANO_BASE)


def aplicar_tema(raiz: tk.Misc) -> ttk.Style:
    """Configura el tema ttk y las fuentes de todos los estilos usados."""
    # Respaldo global: algunos temas nativos ignoran font en TEntry/TCombobox.
    raiz.option_add("*Font", FUENTE_BASE)
    raiz.option_add("*TCombobox*Listbox.font", FUENTE_ENTRADA)

    estilo = ttk.Style(raiz)
    # "vista" / "xpnative" en Windows; "clam" como respaldo multiplataforma.
    for candidato in ("vista", "xpnative", "clam"):
        if candidato in estilo.theme_names():
            estilo.theme_use(candidato)
            break

    estilo.configure("TLabel", font=FUENTE_ETIQUETA)
    estilo.configure("Titulo.TLabel", font=FUENTE_TITULO)
    estilo.configure("Subtitulo.TLabel", font=FUENTE_SUBTITULO)
    estilo.configure("Estado.TLabel", font=FUENTE_ESTADO)
    estilo.configure("TLabelframe.Label", font=FUENTE_ETIQUETA)
    estilo.configure("TEntry", font=FUENTE_ENTRADA)
    estilo.configure("TCombobox", font=FUENTE_ENTRADA)
    estilo.configure("TButton", font=FUENTE_BOTON)
    estilo.configure(
        "Treeview",
        font=FUENTE_TABLA,
        rowheight=24,
    )
    estilo.configure("Treeview.Heading", font=FUENTE_BOTON)
    return estilo


def configurar_texto(widget: tk.Text) -> None:
    """Alinea ``tk.Text`` con la misma tipografía que los controles ttk."""
    widget.configure(
        font=FUENTE_ENTRADA,
        wrap="word",
        relief="solid",
        borderwidth=1,
        highlightthickness=0,
        padx=4,
        pady=4,
    )
