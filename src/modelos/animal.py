"""Clase base abstracta de todos los animales del proyecto."""

from abc import ABC, abstractmethod

from src.utils.validadores import validar_rango


class Animal(ABC):
    """Animal genérico. No se puede instanciar: solo sirve como contrato.

    Define los datos comunes (nombre y edad) y obliga a cada subclase a
    implementar cómo suena y de qué se alimenta. Eso es la abstracción:
    la superclase declara *qué* debe saber hacer un animal, y las clases
    concretas deciden *cómo*.

    Atributos:
        nombre: Nombre público del animal.
        _edad: Edad en años. El guion bajo indica que no debe leerse ni
            modificarse desde fuera; el acceso público es la propiedad
            ``edad``.
    """

    EDAD_MINIMA = 0
    EDAD_MAXIMA = 30

    def __init__(self, nombre: str, edad: int) -> None:
        """Inicializa el nombre y la edad.

        Args:
            nombre: Texto no vacío. Los espacios de los extremos se ignoran.
            edad: Años enteros, entre ``EDAD_MINIMA`` y ``EDAD_MAXIMA``.

        Raises:
            ValueError: Si el nombre o la edad no son válidos.
        """
        self.nombre = self._validar_nombre(nombre)
        # La asignación usa el setter, así la edad siempre queda validada.
        self.edad = edad

    @staticmethod
    def _validar_nombre(nombre: str) -> str:
        """Normaliza el nombre o lanza un error si no es utilizable."""
        if not isinstance(nombre, str) or not nombre.strip():
            raise ValueError("El nombre debe ser un texto no vacío.")
        return nombre.strip()

    @property
    def edad(self) -> int:
        """Edad del animal en años."""
        return self._edad

    @edad.setter
    def edad(self, valor: int) -> None:
        """Actualiza la edad si es un entero dentro del rango permitido.

        Raises:
            ValueError: Si la edad no es un entero o está fuera de rango.
        """
        if isinstance(valor, bool) or not isinstance(valor, int):
            raise ValueError("edad debe ser un número entero.")
        validar_rango(valor, self.EDAD_MINIMA, self.EDAD_MAXIMA, "edad")
        self._edad = valor

    def info_basica(self) -> str:
        """Devuelve una descripción corta válida para cualquier animal.

        Returns:
            Texto con el nombre, la clase concreta y la edad.
        """
        return (
            f"{self.nombre} es un {self.__class__.__name__} "
            f"de {self.edad} años."
        )

    @abstractmethod
    def hacer_sonido(self) -> str:
        """Devuelve el sonido característico del animal.

        Cada subclase concreta debe implementar este método.
        """

    @abstractmethod
    def tipo_alimentacion(self) -> str:
        """Devuelve el tipo de alimentación (por ejemplo, ``carnívoro``).

        Cada subclase concreta debe implementar este método.
        """
