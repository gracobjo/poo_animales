"""Modelo POO del refugio: herencia, propiedades y métodos abstractos.

El CRUD y la GUI siguen trabajando con ``dict``. Estas clases demuestran
Tema 2 (ABC, herencia, ``@property`` / setters, decoradores) y se conectan
al inventario mediante ``datos.adaptador_poo``.
"""

from __future__ import annotations

import math
from abc import ABC, abstractmethod
from typing import Any, Dict, Type

from datos.constantes import PESO_MAX_KG, PESO_MIN_KG
from datos.decoradores import cuenta_usos


class AnimalRefugio(ABC):
    """Contrato común de un animal del refugio (no instanciable).

    Atributos protegidos (``_nombre``, ``_edad``, …) con acceso público
    mediante getters/setters ``@property``. Cada subclase fija ``ESPECIE``
    e implementa sonido y alimentación (polimorfismo).
    """

    ESPECIE: str = ""
    EDAD_MINIMA = 0
    EDAD_MAXIMA = 30

    def __init__(
        self,
        nombre: str,
        edad: int,
        peso: float,
        color: str,
        observaciones: str = "",
    ) -> None:
        self.nombre = nombre
        self.edad = edad
        self.peso = peso
        self.color = color
        self.observaciones = observaciones

    # --- Getters / setters (encapsulación) ---

    @property
    def nombre(self) -> str:
        """Nombre del animal."""
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("El nombre es obligatorio.")
        self._nombre = valor.strip()

    @property
    def edad(self) -> int:
        """Edad en años (0-30)."""
        return self._edad

    @edad.setter
    def edad(self, valor: int) -> None:
        if isinstance(valor, bool) or not isinstance(valor, int):
            raise ValueError("La edad debe ser un número entero.")
        if valor < self.EDAD_MINIMA or valor > self.EDAD_MAXIMA:
            raise ValueError(
                f"La edad debe estar entre {self.EDAD_MINIMA} y "
                f"{self.EDAD_MAXIMA} años."
            )
        self._edad = valor

    @property
    def peso(self) -> float:
        """Peso en kg dentro del rango del refugio."""
        return self._peso

    @peso.setter
    def peso(self, valor: float) -> None:
        try:
            peso = float(valor)
        except (TypeError, ValueError) as error:
            raise ValueError("El peso debe ser un número válido.") from error
        if not math.isfinite(peso):
            raise ValueError("El peso debe ser un número finito.")
        if peso < PESO_MIN_KG or peso > PESO_MAX_KG:
            raise ValueError(
                f"El peso debe estar entre {PESO_MIN_KG} y {PESO_MAX_KG} kg."
            )
        self._peso = peso

    @property
    def color(self) -> str:
        """Color del pelaje o plumaje."""
        return self._color

    @color.setter
    def color(self, valor: str) -> None:
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("El color es obligatorio.")
        self._color = valor.strip()

    @property
    def observaciones(self) -> str:
        """Notas libres del refugio."""
        return self._observaciones

    @observaciones.setter
    def observaciones(self, valor: str) -> None:
        self._observaciones = str(valor or "").strip()

    @property
    def especie(self) -> str:
        """Especie fijada por la subclase (solo lectura)."""
        return self.ESPECIE

    # --- Comportamiento polimórfico ---

    @cuenta_usos
    def info_basica(self) -> str:
        """Resumen corto; decorado con ``@cuenta_usos``."""
        return (
            f"{self.nombre} ({self.especie}), "
            f"{self.edad} años, {self.peso:.2f} kg"
        )

    @abstractmethod
    def hacer_sonido(self) -> str:
        """Sonido característico (cada especie lo implementa)."""

    @abstractmethod
    def tipo_alimentacion(self) -> str:
        """Tipo de alimentación de la especie."""

    @classmethod
    def campos_desde_dict(cls, datos: Dict[str, Any]) -> Dict[str, Any]:
        """Factory auxiliar: extrae kwargs comunes desde un ``dict`` de ficha."""
        return {
            "nombre": datos.get("nombre", ""),
            "edad": datos.get("edad"),
            "peso": datos.get("peso"),
            "color": datos.get("color", ""),
            "observaciones": datos.get("observaciones", ""),
        }

    def __str__(self) -> str:
        return (
            f"{self.especie}: {self.nombre}, {self.edad} años, "
            f"{self.peso} kg, {self.color}."
        )


class Perro(AnimalRefugio):
    """Perro del refugio."""

    ESPECIE = "Perro"

    def hacer_sonido(self) -> str:
        return f"{self.nombre} dice: ¡Guau!"

    def tipo_alimentacion(self) -> str:
        return "omnívoro"


class Gato(AnimalRefugio):
    """Gato del refugio."""

    ESPECIE = "Gato"

    def hacer_sonido(self) -> str:
        return f"{self.nombre} dice: ¡Miau!"

    def tipo_alimentacion(self) -> str:
        return "carnívoro"


class Conejo(AnimalRefugio):
    """Conejo del refugio."""

    ESPECIE = "Conejo"

    def hacer_sonido(self) -> str:
        return f"{self.nombre} dice: … (silencio típico de conejo)"

    def tipo_alimentacion(self) -> str:
        return "herbívoro"


class Loro(AnimalRefugio):
    """Loro del refugio."""

    ESPECIE = "Loro"

    def hacer_sonido(self) -> str:
        return f"{self.nombre} dice: ¡Aaah!"

    def tipo_alimentacion(self) -> str:
        return "granívoro"


class Hamster(AnimalRefugio):
    """Hámster del refugio."""

    ESPECIE = "Hámster"

    def hacer_sonido(self) -> str:
        return f"{self.nombre} dice: ¡Iiik!"

    def tipo_alimentacion(self) -> str:
        return "omnívoro"


CLASES_POR_ESPECIE: Dict[str, Type[AnimalRefugio]] = {
    Perro.ESPECIE: Perro,
    Gato.ESPECIE: Gato,
    Conejo.ESPECIE: Conejo,
    Loro.ESPECIE: Loro,
    Hamster.ESPECIE: Hamster,
}
