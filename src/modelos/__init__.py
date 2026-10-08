"""Modelos de animales: clase abstracta y especies concretas."""

from src.modelos.animal import Animal
from src.modelos.gato import Gato
from src.modelos.loro import Loro
from src.modelos.perro import Perro

__all__ = ["Animal", "Perro", "Gato", "Loro"]
