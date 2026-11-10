"""Datos del inventario e operaciones CRUD."""

from datos.constantes import ESPECIES
from datos.inventario import (
    actualizar_animal,
    animales_iniciales,
    borrar_animal,
    crear_animal,
    leer_animal,
)

__all__ = [
    "ESPECIES",
    "animales_iniciales",
    "crear_animal",
    "leer_animal",
    "actualizar_animal",
    "borrar_animal",
]
