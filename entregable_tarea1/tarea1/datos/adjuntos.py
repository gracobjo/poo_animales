"""Copia de fotos y documentos a la carpeta local ``adjuntos/``."""

from __future__ import annotations

import shutil
from datetime import date, datetime
from pathlib import Path
from typing import Dict, Union

# tarea1/adjuntos/<id_animal>/...
RAIZ_ADJUNTOS = Path(__file__).resolve().parents[1] / "adjuntos"

# Límite de subida / pegado (5 MiB).
TAMANO_MAX_BYTES = 5 * 1024 * 1024
TAMANO_MAX_MB = TAMANO_MAX_BYTES // (1024 * 1024)


def carpeta_animal(animal_id: int) -> Path:
    destino = RAIZ_ADJUNTOS / str(animal_id)
    destino.mkdir(parents=True, exist_ok=True)
    return destino


def comprobar_tamano(ruta: Union[str, Path]) -> None:
    """Lanza ValueError si el fichero supera el límite de 5 MB."""
    path = Path(ruta)
    if not path.is_file():
        raise ValueError(f"No se encuentra el archivo: {ruta}")
    tamano = path.stat().st_size
    if tamano > TAMANO_MAX_BYTES:
        mb = tamano / (1024 * 1024)
        raise ValueError(
            f"El archivo pesa {mb:.1f} MB y el máximo permitido es "
            f"{TAMANO_MAX_MB} MB."
        )


def _destino_unico(destino_dir: Path, nombre: str) -> Path:
    destino = destino_dir / nombre
    if not destino.exists():
        return destino
    stem, suffix = Path(nombre).stem, Path(nombre).suffix
    n = 2
    while True:
        candidato = destino_dir / f"{stem}_{n}{suffix}"
        if not candidato.exists():
            return candidato
        n += 1


def importar_archivo(animal_id: int, origen: str, subcarpeta: str = "") -> Path:
    """Copia un archivo al almacén del animal y devuelve la ruta destino."""
    fuente = Path(origen)
    if not fuente.is_file():
        raise ValueError(f"No se encuentra el archivo: {origen}")
    comprobar_tamano(fuente)

    destino_dir = carpeta_animal(animal_id)
    if subcarpeta:
        destino_dir = destino_dir / subcarpeta
        destino_dir.mkdir(parents=True, exist_ok=True)

    destino = _destino_unico(destino_dir, fuente.name)
    shutil.copy2(fuente, destino)
    return destino


def guardar_bytes(
    animal_id: int,
    contenido: bytes,
    nombre: str,
    subcarpeta: str = "",
) -> Path:
    """Guarda bytes (p. ej. imagen pegada) respetando el límite de tamaño."""
    if len(contenido) > TAMANO_MAX_BYTES:
        mb = len(contenido) / (1024 * 1024)
        raise ValueError(
            f"El contenido pesa {mb:.1f} MB y el máximo permitido es "
            f"{TAMANO_MAX_MB} MB."
        )
    destino_dir = carpeta_animal(animal_id)
    if subcarpeta:
        destino_dir = destino_dir / subcarpeta
        destino_dir.mkdir(parents=True, exist_ok=True)
    destino = _destino_unico(destino_dir, nombre)
    destino.write_bytes(contenido)
    return destino


def registrar_documento(animal_id: int, origen: str) -> Dict[str, str]:
    """Importa un documento y devuelve el dict para la lista del inventario."""
    destino = importar_archivo(animal_id, origen, subcarpeta="documentos")
    return {
        "nombre": destino.name,
        "ruta": str(destino),
        "fecha": date.today().isoformat(),
    }


def registrar_documento_bytes(
    animal_id: int,
    contenido: bytes,
    nombre: str,
) -> Dict[str, str]:
    """Registra un documento creado desde el portapapeles (bytes)."""
    destino = guardar_bytes(
        animal_id, contenido, nombre, subcarpeta="documentos"
    )
    return {
        "nombre": destino.name,
        "ruta": str(destino),
        "fecha": date.today().isoformat(),
    }


def registrar_foto(animal_id: int, origen: str) -> str:
    """Importa una imagen como foto del animal; devuelve la ruta guardada."""
    destino = importar_archivo(animal_id, origen, subcarpeta="fotos")
    return str(destino)


def registrar_foto_bytes(animal_id: int, contenido: bytes, extension: str = ".png") -> str:
    """Guarda una foto pegada desde el portapapeles."""
    if not extension.startswith("."):
        extension = f".{extension}"
    nombre = f"pegado_{datetime.now().strftime('%Y%m%d_%H%M%S')}{extension}"
    destino = guardar_bytes(animal_id, contenido, nombre, subcarpeta="fotos")
    return str(destino)


def borrar_adjuntos_animal(animal_id: int) -> None:
    """Elimina la carpeta de adjuntos del animal (si existe)."""
    carpeta = RAIZ_ADJUNTOS / str(animal_id)
    if carpeta.is_dir():
        shutil.rmtree(carpeta, ignore_errors=True)
