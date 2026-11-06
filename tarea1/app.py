"""Punto de entrada del programa Refugio Animal (Tkinter).

Ejecutar desde la carpeta ``tarea1``::

    python app.py

o desde la raíz del repositorio::

    python tarea1/app.py
"""

from __future__ import annotations

import sys
from pathlib import Path

# Permite ejecutar tanto ``python app.py`` (cwd=tarea1)
# como ``python tarea1/app.py`` (cwd=raíz del repo).
RAIZ_PROGRAMA = Path(__file__).resolve().parent
if str(RAIZ_PROGRAMA) not in sys.path:
    sys.path.insert(0, str(RAIZ_PROGRAMA))

import tkinter as tk

from datos.persistencia_inventario import cargar_inventario
from interfaz.gestor import GestorAnimales


def main() -> None:
    """Crea la ventana, carga el inventario persistido y arranca Tkinter."""
    inventario = cargar_inventario()
    raiz = tk.Tk()
    GestorAnimales(raiz, inventario)
    raiz.mainloop()


if __name__ == "__main__":
    main()
