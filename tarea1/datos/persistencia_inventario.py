"""Persistencia del inventario de animales en JSON (separada del catálogo).

El catálogo de especies vive en ``especies_personalizadas.json``.
Los registros de animales viven en ``inventario.json``.
"""

from __future__ import annotations

import json
import tempfile
from copy import deepcopy
from pathlib import Path
from typing import Any, Dict, Optional

from datos.ficha import asegurar_campos_clinicos
from datos.inventario import Inventario, animales_iniciales

RUTA_POR_DEFECTO = Path(__file__).resolve().parent / "inventario.json"


def _a_jsonable(inventario: Inventario) -> Dict[str, Any]:
    """Claves string (JSON) y copia profunda de cada registro."""
    return {
        str(animal_id): deepcopy(registro)
        for animal_id, registro in inventario.items()
    }


def _desde_jsonable(datos: Any) -> Inventario:
    if not isinstance(datos, dict):
        raise ValueError("El inventario JSON debe ser un objeto/diccionario.")
    inventario: Inventario = {}
    for clave, registro in datos.items():
        if not isinstance(registro, dict):
            continue
        try:
            animal_id = int(clave)
        except (TypeError, ValueError):
            continue
        inventario[animal_id] = asegurar_campos_clinicos(deepcopy(registro))
    return inventario


def guardar_inventario(
    inventario: Inventario,
    ruta: Optional[Path | str] = None,
) -> Path:
    """Guarda el inventario con escritura atómica (UTF-8)."""
    destino = Path(ruta) if ruta is not None else RUTA_POR_DEFECTO
    destino.parent.mkdir(parents=True, exist_ok=True)
    contenido = json.dumps(
        _a_jsonable(inventario),
        ensure_ascii=False,
        indent=2,
    ) + "\n"
    with tempfile.NamedTemporaryFile(
        mode="w",
        encoding="utf-8",
        delete=False,
        dir=str(destino.parent),
        prefix=".inventario_",
        suffix=".tmp",
    ) as tmp:
        tmp.write(contenido)
        tmp_path = Path(tmp.name)
    tmp_path.replace(destino)
    return destino


def cargar_inventario(ruta: Optional[Path | str] = None) -> Inventario:
    """Carga el inventario desde JSON.

    Si el archivo no existe, siembra ``animales_iniciales()`` y lo persiste.
    Si el JSON está corrupto, no lo sobrescribe: arranca con el ejemplo en memoria.
    """
    destino = Path(ruta) if ruta is not None else RUTA_POR_DEFECTO
    if not destino.is_file():
        inventario = animales_iniciales()
        guardar_inventario(inventario, destino)
        return inventario
    try:
        texto = destino.read_text(encoding="utf-8")
        datos = json.loads(texto) if texto.strip() else {}
        inventario = _desde_jsonable(datos)
    except (OSError, json.JSONDecodeError, UnicodeError, ValueError):
        return animales_iniciales()
    if not inventario:
        inventario = animales_iniciales()
        guardar_inventario(inventario, destino)
    return inventario
