"""Lectura del portapapeles (archivos, texto o imagen) para pegar adjuntos.

En Windows se usa ``CF_HDROP`` (Explorador) con firmas ctypes correctas.
El texto se lee preferentemente con Tkinter para evitar violaciones de acceso
al hacer ``wstring_at`` sobre handles mal tipados.
"""

from __future__ import annotations

import io
import sys
from pathlib import Path
from typing import List, Optional, Tuple, Union

_EXT_DOC = {".pdf", ".doc", ".docx", ".txt", ".png", ".jpg", ".jpeg", ".gif", ".webp"}
_EXT_FOTO = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp"}


def _archivos_cf_hdrop() -> List[str]:
    """Rutas de ficheros copiados en el Explorador (CF_HDROP)."""
    if not sys.platform.startswith("win"):
        return []

    import ctypes
    from ctypes import wintypes

    user32 = ctypes.windll.user32
    shell32 = ctypes.windll.shell32
    kernel32 = ctypes.windll.kernel32

    CF_HDROP = 15

    user32.OpenClipboard.argtypes = [wintypes.HWND]
    user32.OpenClipboard.restype = wintypes.BOOL
    user32.CloseClipboard.argtypes = []
    user32.CloseClipboard.restype = wintypes.BOOL
    user32.IsClipboardFormatAvailable.argtypes = [wintypes.UINT]
    user32.IsClipboardFormatAvailable.restype = wintypes.BOOL
    user32.GetClipboardData.argtypes = [wintypes.UINT]
    user32.GetClipboardData.restype = wintypes.HANDLE

    kernel32.GlobalLock.argtypes = [wintypes.HGLOBAL]
    kernel32.GlobalLock.restype = ctypes.c_void_p
    kernel32.GlobalUnlock.argtypes = [wintypes.HGLOBAL]
    kernel32.GlobalUnlock.restype = wintypes.BOOL

    shell32.DragQueryFileW.argtypes = [
        ctypes.c_void_p,
        wintypes.UINT,
        wintypes.LPWSTR,
        wintypes.UINT,
    ]
    shell32.DragQueryFileW.restype = wintypes.UINT

    if not user32.OpenClipboard(None):
        return []
    try:
        if not user32.IsClipboardFormatAvailable(CF_HDROP):
            return []
        handle = user32.GetClipboardData(CF_HDROP)
        if not handle:
            return []
        # HDROP válido tras GlobalLock
        locked = kernel32.GlobalLock(handle)
        if not locked:
            return []
        try:
            n = shell32.DragQueryFileW(locked, 0xFFFFFFFF, None, 0)
            rutas: List[str] = []
            for i in range(int(n)):
                longitud = shell32.DragQueryFileW(locked, i, None, 0)
                buf = ctypes.create_unicode_buffer(longitud + 1)
                shell32.DragQueryFileW(locked, i, buf, longitud + 1)
                if buf.value:
                    rutas.append(buf.value)
            return rutas
        finally:
            kernel32.GlobalUnlock(handle)
    except OSError:
        return []
    finally:
        user32.CloseClipboard()


def _texto_tkinter() -> str:
    """Texto del portapapeles vía Tk (seguro desde la app gráfica)."""
    try:
        import tkinter as tk
    except ImportError:
        return ""
    raiz = getattr(tk, "_default_root", None)
    if raiz is None:
        return ""
    try:
        return str(raiz.clipboard_get())
    except tk.TclError:
        return ""


def _imagen_pillow():
    try:
        from PIL import ImageGrab  # type: ignore
    except ImportError:
        return None
    try:
        data = ImageGrab.grabclipboard()
    except Exception:
        return None
    if data is None or isinstance(data, list):
        return None
    return data


def leer_portapapeles() -> Tuple[str, Optional[Union[List[str], object, str]]]:
    """Devuelve ``(tipo, dato)``.

    - ``(\"archivos\", [rutas...])``
    - ``(\"imagen\", PIL.Image)``
    - ``(\"texto\", str)``
    - ``(\"vacio\", None)``
    """
    try:
        rutas = _archivos_cf_hdrop()
    except OSError:
        rutas = []
    if rutas:
        return "archivos", rutas

    imagen = _imagen_pillow()
    if imagen is not None:
        return "imagen", imagen

    texto = _texto_tkinter().strip().strip('"')
    if texto:
        candidato = Path(texto)
        try:
            if candidato.is_file():
                return "archivos", [str(candidato)]
        except OSError:
            pass
        return "texto", texto

    # Respaldo: ImageGrab a veces devuelve lista de paths
    try:
        from PIL import ImageGrab  # type: ignore

        data = ImageGrab.grabclipboard()
        if isinstance(data, list) and data:
            return "archivos", [str(p) for p in data if p]
    except ImportError as error:
        raise ValueError(
            "Para pegar imágenes hace falta Pillow (pip install Pillow)."
        ) from error
    except Exception:
        pass

    return "vacio", None


def imagen_a_png_bytes(imagen) -> bytes:
    """Serializa una imagen PIL a PNG en memoria."""
    buffer = io.BytesIO()
    if getattr(imagen, "mode", "") not in ("RGB", "RGBA", "L"):
        imagen = imagen.convert("RGBA")
    imagen.save(buffer, format="PNG", optimize=True)
    return buffer.getvalue()


def primer_archivo_valido(
    rutas: List[str],
    *,
    para_foto: bool = False,
) -> Path:
    """Elige el primer archivo existente con extensión admitida."""
    permitidas = _EXT_FOTO if para_foto else _EXT_DOC
    for ruta in rutas:
        path = Path(ruta)
        if path.is_file() and path.suffix.lower() in permitidas:
            return path
    raise ValueError(
        "En el portapapeles no hay un archivo compatible "
        + ("de imagen." if para_foto else "de documento o imagen.")
    )
