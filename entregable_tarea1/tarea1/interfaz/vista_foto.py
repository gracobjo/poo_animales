"""Carga de miniaturas para la interfaz (Tk / Pillow)."""

from __future__ import annotations

import tkinter as tk
from pathlib import Path
from typing import Optional, Tuple, Union

Photo = Union[tk.PhotoImage, object]


def cargar_miniatura(
    ruta: str,
    max_lado: int = 160,
) -> Tuple[Optional[Photo], str]:
    """Devuelve ``(imagen_tk, mensaje)``.

    Si no hay archivo o no se puede leer, ``imagen_tk`` es ``None`` y
    ``mensaje`` explica el estado para mostrarlo en un ``Label``.
    """
    if not ruta or not str(ruta).strip():
        return None, "Sin foto"
    path = Path(ruta)
    if not path.is_file():
        return None, "Foto no encontrada"

    try:
        imagen = tk.PhotoImage(file=str(path))
    except tk.TclError:
        try:
            from PIL import Image, ImageTk  # type: ignore

            with Image.open(path) as im:
                im = im.convert("RGB")
                im.thumbnail((max_lado, max_lado))
                return ImageTk.PhotoImage(im), ""
        except Exception:
            return None, "Sin vista previa\n(PNG/GIF o Pillow)"

    factor = max(1, imagen.width() // max_lado, imagen.height() // max_lado)
    if factor > 1:
        imagen = imagen.subsample(factor, factor)
    return imagen, ""
