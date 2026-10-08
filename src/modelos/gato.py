"""Modelo concreto de un gato."""

from src.modelos.animal import Animal
from src.utils.validadores import validar_positivo, validar_rango


class Gato(Animal):
    """Gato que hereda el contrato de ``Animal``.

    Igual que ``Perro``, encapsula peso, color y energía con atributos
    privados estrictos y propiedades validadas. Además lleva la cuenta
    de presas cazadas, que solo aumenta dentro de ``cazar``.

    Atributos de clase:
        ENERGIA_MINIMA: Energía más baja permitida.
        ENERGIA_MAXIMA: Energía más alta permitida.
        COSTO_ENERGIA_CAZAR: Energía que consume ``cazar``.
        RECUPERACION_DORMIR: Energía que recupera ``dormir``.
        RECUPERACION_COMIDA: Energía que recupera ``comer``.
        ENERGIA_MINIMA_RONRONEO: Energía mínima para poder ronronear.
    """

    ENERGIA_MINIMA = 0
    ENERGIA_MAXIMA = 100
    COSTO_ENERGIA_CAZAR = 25
    RECUPERACION_DORMIR = 40
    RECUPERACION_COMIDA = 10
    ENERGIA_MINIMA_RONRONEO = 20

    def __init__(
        self,
        nombre: str,
        edad: int,
        peso: float,
        color: str,
        energia: float = 100,
    ) -> None:
        """Crea un gato sin presas cazadas.

        Args:
            nombre: Nombre del gato.
            edad: Edad en años.
            peso: Peso en kilogramos, mayor que cero.
            color: Color del pelaje, texto no vacío.
            energia: Energía inicial, entre 0 y 100. Por defecto, 100.

        Raises:
            ValueError: Si algún dato no supera su validación.
        """
        super().__init__(nombre, edad)
        self.__presas_cazadas = 0
        self.peso = peso
        self.color = color
        self.energia = energia

    @property
    def peso(self) -> float:
        """Peso del gato en kilogramos."""
        return self.__peso

    @peso.setter
    def peso(self, valor: float) -> None:
        """Actualiza el peso si es un número mayor que cero.

        Raises:
            ValueError: Si el peso no es positivo.
        """
        self.__peso = validar_positivo(valor, "peso")

    @property
    def color(self) -> str:
        """Color del pelaje."""
        return self.__color

    @color.setter
    def color(self, valor: str) -> None:
        """Actualiza el color si es un texto no vacío.

        Raises:
            ValueError: Si el color está vacío o no es texto.
        """
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("color debe ser un texto no vacío.")
        self.__color = valor.strip()

    @property
    def energia(self) -> float:
        """Nivel de energía, entre 0 y 100."""
        return self.__energia

    @energia.setter
    def energia(self, valor: float) -> None:
        """Actualiza la energía si está entre 0 y 100.

        Raises:
            ValueError: Si la energía queda fuera de rango.
        """
        validar_rango(
            valor,
            self.ENERGIA_MINIMA,
            self.ENERGIA_MAXIMA,
            "energia",
        )
        self.__energia = valor

    @property
    def presas_cazadas(self) -> int:
        """Número de presas cazadas.

        Es de solo lectura: aumenta únicamente al llamar a ``cazar``.
        """
        return self.__presas_cazadas

    def hacer_sonido(self) -> str:
        """Implementa el método abstracto delegando en ``maullar``."""
        return self.maullar()

    def tipo_alimentacion(self) -> str:
        """Devuelve el tipo de alimentación del gato."""
        return "carnívoro"

    def maullar(self) -> str:
        """Devuelve el maullido del gato."""
        return f"{self.nombre} dice: ¡Miau!"

    def ronronear(self) -> str:
        """Ronronea si tiene energía suficiente.

        No consume energía: solo exige un mínimo para estar a gusto.

        Returns:
            El ronroneo del gato.

        Raises:
            ValueError: Si la energía está por debajo del mínimo.
        """
        if self.energia < self.ENERGIA_MINIMA_RONRONEO:
            raise ValueError(
                "Energía insuficiente para ronronear. "
                f"Se necesitan al menos {self.ENERGIA_MINIMA_RONRONEO}."
            )
        return f"{self.nombre} ronronea: Prrr..."

    def cazar(self) -> str:
        """Caza una presa y descuenta energía.

        Returns:
            Mensaje con el total de presas cazadas.

        Raises:
            ValueError: Si no hay energía suficiente. En ese caso no
                aumenta el contador de presas.
        """
        if self.energia < self.COSTO_ENERGIA_CAZAR:
            raise ValueError(
                "Energía insuficiente para cazar. "
                f"Se necesitan {self.COSTO_ENERGIA_CAZAR} "
                f"y hay {self.energia}."
            )
        self.energia = self.energia - self.COSTO_ENERGIA_CAZAR
        self.__presas_cazadas += 1
        return (
            f"{self.nombre} cazó una presa. "
            f"Presas: {self.presas_cazadas}."
        )

    def comer(self, gramos: float) -> str:
        """Come una ración: sube el peso y recupera energía.

        Cada 1000 g suman 1 kg. La energía no puede pasar de
        ``ENERGIA_MAXIMA``. Si los gramos no son válidos, el gato no
        cambia de estado.

        Args:
            gramos: Cantidad de comida, mayor que cero.

        Returns:
            Mensaje con el peso actualizado.

        Raises:
            ValueError: Si los gramos no son un número positivo.
        """
        validar_positivo(gramos, "gramos")
        self.peso = self.peso + (gramos / 1000)
        self.energia = min(
            self.ENERGIA_MAXIMA,
            self.energia + self.RECUPERACION_COMIDA,
        )
        return (
            f"{self.nombre} come {gramos} g. "
            f"Peso actual: {self.peso:.2f} kg."
        )

    def dormir(self) -> str:
        """Duerme y recupera energía sin superar el máximo.

        Returns:
            Mensaje con la energía actual.
        """
        self.energia = min(
            self.ENERGIA_MAXIMA,
            self.energia + self.RECUPERACION_DORMIR,
        )
        return f"{self.nombre} duerme. Energía actual: {self.energia}."

    def __str__(self) -> str:
        """Representación legible del gato."""
        return (
            f"Gato: {self.nombre}, {self.edad} años, "
            f"{self.peso} kg, color {self.color}, "
            f"energía {self.energia}, "
            f"presas cazadas {self.presas_cazadas}."
        )
