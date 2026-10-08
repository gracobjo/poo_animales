"""Servicios polimórficos sobre colecciones de animales."""

from src.servicios.gestion_animales import (
    alimentar,
    animales_mayores_de,
    emitir_sonido,
    listar_info,
    total_peso,
)

__all__ = [
    "emitir_sonido",
    "alimentar",
    "listar_info",
    "animales_mayores_de",
    "total_peso",
]
