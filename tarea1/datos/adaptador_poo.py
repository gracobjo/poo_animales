"""Puente entre el inventario ``dict`` y las clases ``AnimalRefugio``.

El enunciado exige diccionarios para el CRUD. Este módulo permite usar
herencia / propiedades sin sustituir la estructura principal de datos.
"""

from __future__ import annotations

from typing import Any, Dict, Optional, TYPE_CHECKING

from datos.modelos import (
    CLASES_POR_ESPECIE,
    AnimalRefugio,
    EspeciePersonalizada,
)

if TYPE_CHECKING:
    from datos.gestor_especies import CatalogoEspecies


def registro_a_animal(
    registro: Dict[str, Any],
    catalogo: Optional["CatalogoEspecies"] = None,
) -> AnimalRefugio:
    """Construye la subclase nativa o ``EspeciePersonalizada`` desde un ``dict``.

    Raises:
        ValueError: Si la especie no está en el catálogo o fallan los setters.
    """
    especie = str(registro.get("especie", "")).strip()
    clase = CLASES_POR_ESPECIE.get(especie)
    if clase is not None:
        kwargs = clase.campos_desde_dict(registro)
        return clase(**kwargs)

    if catalogo is None:
        from datos.gestor_especies import get_catalogo

        catalogo = get_catalogo()

    config = catalogo.obtener_personalizada(especie, solo_activas=False)
    if config is None:
        raise ValueError(
            f"No hay clase POO ni especie personalizada para '{especie}'."
        )

    kwargs = EspeciePersonalizada.campos_desde_dict(registro)
    return EspeciePersonalizada(
        **kwargs,
        nombre_especie=config["nombre"],
        sonido=config["sonido"],
        alimentacion=config["alimentacion"],
        cuidados=config["cuidados"],
    )


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


def resumen_polimorfico(
    registro: Dict[str, Any],
    catalogo: Optional["CatalogoEspecies"] = None,
) -> str:
    """Texto de demo: info + sonido (mismo método, distinto comportamiento)."""
    animal = registro_a_animal(registro, catalogo=catalogo)
    return (
        f"{animal.info_basica()} | {animal.hacer_sonido()} | "
        f"alimentación: {animal.tipo_alimentacion()}"
    )
