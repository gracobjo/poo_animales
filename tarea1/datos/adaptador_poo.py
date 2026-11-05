"""Puente entre el inventario ``dict`` y las clases ``AnimalRefugio``.

El enunciado exige diccionarios para el CRUD. Este módulo permite usar
herencia / propiedades sin sustituir la estructura principal de datos.
"""

from __future__ import annotations

from typing import Any, Dict

from datos.modelos import CLASES_POR_ESPECIE, AnimalRefugio


def registro_a_animal(registro: Dict[str, Any]) -> AnimalRefugio:
    """Construye la subclase adecuada a partir de una ficha ``dict``.

    Raises:
        ValueError: Si la especie no tiene clase asociada o fallan los setters.
    """
    especie = str(registro.get("especie", "")).strip()
    clase = CLASES_POR_ESPECIE.get(especie)
    if clase is None:
        raise ValueError(f"No hay clase POO para la especie '{especie}'.")
    kwargs = clase.campos_desde_dict(registro)
    return clase(**kwargs)


def animal_a_campos(animal: AnimalRefugio) -> Dict[str, Any]:
    """Exporta los campos básicos del objeto (sin ficha clínica)."""
    return {
        "nombre": animal.nombre,
        "especie": animal.especie,
        "edad": animal.edad,
        "peso": animal.peso,
        "color": animal.color,
        "observaciones": animal.observaciones,
    }


def resumen_polimorfico(registro: Dict[str, Any]) -> str:
    """Texto de demo: info + sonido (mismo método, distinto comportamiento)."""
    animal = registro_a_animal(registro)
    return (
        f"{animal.info_basica()} | {animal.hacer_sonido()} | "
        f"alimentación: {animal.tipo_alimentacion()}"
    )
