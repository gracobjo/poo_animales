"""Rutas de recursos estáticos del programa (logo, etc.)."""

from __future__ import annotations

from pathlib import Path
from typing import Optional

# Carpeta tarea1/ (donde vive app.py).
_RAIZ_PROGRAMA = Path(__file__).resolve().parents[1]
# Raíz del repositorio (padre de tarea1/), por si el logo está ahí.
_RAIZ_REPO = _RAIZ_PROGRAMA.parent

_NOMBRES_LOGO = (
    "refugio.png",
    "refugio.jpg",
    "refugio.jpeg",
    "refugio.webp",
)


def ruta_logo_refugio() -> Optional[Path]:
    """Devuelve la ruta del logo del refugio si existe.

    Busca ``refugio.png`` / ``.jpg`` en ``tarea1/`` y, en su defecto,
    en la raíz del repositorio.
    """
    for base in (_RAIZ_PROGRAMA, _RAIZ_REPO):
        for nombre in _NOMBRES_LOGO:
            candidata = base / nombre
            if candidata.is_file():
                return candidata
    return None
