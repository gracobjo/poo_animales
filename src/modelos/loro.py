"""Modelo concreto de un loro."""

from src.modelos.animal import Animal
from src.utils.validadores import validar_positivo, validar_rango


class Loro(Animal):
    """Loro que hereda el contrato de ``Animal``.

    Repite la misma base que perro y gato: peso, color y energía privados,
    con propiedades que validan. Lo propio de esta especie es una frase
    aprendida, que solo cambia con ``aprender``, y el vuelo, que gasta
    energía.

    Atributos de clase:
        ENERGIA_MINIMA: Energía más baja permitida.
        ENERGIA_MAXIMA: Energía más alta permitida.
        COSTO_ENERGIA_VOLAR: Energía que consume ``volar``.
        RECUPERACION_COMIDA: Energía que recupera ``comer``.
    """

    ENERGIA_MINIMA = 0
    ENERGIA_MAXIMA = 100
    COSTO_ENERGIA_VOLAR = 30
    RECUPERACION_COMIDA = 12

    def __init__(
        self,
        nombre: str,
        edad: int,
        peso: float,
        color: str,
        energia: float = 100,
    ) -> None:
        """Crea un loro que todavía no ha aprendido ninguna frase.

        Args:
            nombre: Nombre del loro.
            edad: Edad en años.
            peso: Peso en kilogramos, mayor que cero.
            color: Color del plumaje, texto no vacío.
            energia: Energía inicial, entre 0 y 100. Por defecto, 100.

        Raises:
            ValueError: Si algún dato no supera su validación.
        """
        super().__init__(nombre, edad)
        self.__frase = ""
        self.peso = peso
        self.color = color
        self.energia = energia

    @property
    def peso(self) -> float:
        """Peso del loro en kilogramos."""
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
        """Color del plumaje."""
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
    def frase(self) -> str:
        """Frase aprendida. Vacía si todavía no ha aprendido ninguna.

        Es de solo lectura: cambia únicamente al llamar a ``aprender``.
        """
        return self.__frase

    def hacer_sonido(self) -> str:
        """Implementa el método abstracto delegando en ``hablar``."""
        return self.hablar()

    def tipo_alimentacion(self) -> str:
        """Devuelve el tipo de alimentación del loro."""
        return "granívoro"

    def hablar(self) -> str:
        """Repite la frase aprendida, o un graznido si no hay ninguna."""
        if self.frase:
            return f"{self.nombre} dice: {self.frase}"
        return f"{self.nombre} dice: ¡Aaah!"

    def aprender(self, frase: str) -> str:
        """Guarda la frase que el loro repetirá a partir de ahora.

        Args:
            frase: Texto no vacío. Se recortan los espacios de los extremos.

        Returns:
            Mensaje con la frase guardada.

        Raises:
            ValueError: Si la frase está vacía o no es texto. En ese caso
                la frase anterior se conserva.
        """
        if not isinstance(frase, str) or not frase.strip():
            raise ValueError("frase debe ser un texto no vacío.")
        self.__frase = frase.strip()
        return f"{self.nombre} aprendió: {self.frase}."

    def volar(self) -> str:
        """Vuela y descuenta energía.

        Returns:
            Mensaje con la energía que queda.

        Raises:
            ValueError: Si no hay energía suficiente. En ese caso el
                estado no cambia.
        """
        if self.energia < self.COSTO_ENERGIA_VOLAR:
            raise ValueError(
                "Energía insuficiente para volar. "
                f"Se necesitan {self.COSTO_ENERGIA_VOLAR} "
                f"y hay {self.energia}."
            )
        self.energia = self.energia - self.COSTO_ENERGIA_VOLAR
        return (
            f"{self.nombre} vuela. "
            f"Energía restante: {self.energia}."
        )

    def comer(self, gramos: float) -> str:
        """Come una ración: sube el peso y recupera energía.

        Cada 1000 g suman 1 kg. La energía no puede pasar de
        ``ENERGIA_MAXIMA``. Si los gramos no son válidos, el loro no
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

    def __str__(self) -> str:
        """Representación legible del loro."""
        aprendida = self.frase if self.frase else "ninguna"
        return (
            f"Loro: {self.nombre}, {self.edad} años, "
            f"{self.peso} kg, color {self.color}, "
            f"energía {self.energia}, frase {aprendida}."
        )
