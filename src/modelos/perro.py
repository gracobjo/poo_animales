"""Modelo concreto de un perro."""

from src.modelos.animal import Animal
from src.utils.validadores import validar_positivo, validar_rango


class Perro(Animal):
    """Perro que hereda el contrato de ``Animal``.

    El peso, el color, la energía y el estado de vacunación son atributos
    privados estrictos (doble guion bajo). Python les aplica *name mangling*:
    desde fuera de la clase ``__peso`` no existe; el nombre interno pasa a
    ser ``_Perro__peso``. El acceso recomendado es mediante propiedades,
    que validan cada cambio.

    Atributos de clase:
        ENERGIA_MINIMA: Energía más baja permitida.
        ENERGIA_MAXIMA: Energía más alta permitida.
        COSTO_ENERGIA_JUGAR: Energía que consume ``jugar``.
        RECUPERACION_DESCANSO: Energía que recupera ``descansar``.
        RECUPERACION_COMIDA: Energía que recupera ``comer``.
    """

    ENERGIA_MINIMA = 0
    ENERGIA_MAXIMA = 100
    COSTO_ENERGIA_JUGAR = 20
    RECUPERACION_DESCANSO = 25
    RECUPERACION_COMIDA = 15

    def __init__(
        self,
        nombre: str,
        edad: int,
        peso: float,
        color: str,
        energia: float = 100,
    ) -> None:
        """Crea un perro sin vacunar.

        Args:
            nombre: Nombre del perro.
            edad: Edad en años.
            peso: Peso en kilogramos, mayor que cero.
            color: Color del pelaje, texto no vacío.
            energia: Energía inicial, entre 0 y 100. Por defecto, 100.

        Raises:
            ValueError: Si algún dato no supera su validación.
        """
        super().__init__(nombre, edad)
        self.__vacunado = False
        self.peso = peso
        self.color = color
        self.energia = energia

    @property
    def peso(self) -> float:
        """Peso del perro en kilogramos."""
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
    def vacunado(self) -> bool:
        """``True`` si el perro ya fue vacunado.

        Es de solo lectura: cambia únicamente al llamar a ``vacunar``.
        """
        return self.__vacunado

    def hacer_sonido(self) -> str:
        """Implementa el método abstracto delegando en ``ladrar``."""
        return self.ladrar()

    def tipo_alimentacion(self) -> str:
        """Devuelve el tipo de alimentación del perro."""
        return "omnívoro"

    def ladrar(self) -> str:
        """Devuelve el ladrido del perro."""
        return f"{self.nombre} dice: ¡Guau!"

    def comer(self, gramos: float) -> str:
        """Come una ración: sube el peso y recupera energía.

        Cada 1000 g suman 1 kg. La energía no puede pasar de
        ``ENERGIA_MAXIMA``. Si los gramos no son válidos, el perro no
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

    def jugar(self) -> str:
        """Gasta energía jugando.

        Returns:
            Mensaje con la energía que queda.

        Raises:
            ValueError: Si no hay energía suficiente. En ese caso el
                estado no cambia.
        """
        if self.energia < self.COSTO_ENERGIA_JUGAR:
            raise ValueError(
                "Energía insuficiente para jugar. "
                f"Se necesitan {self.COSTO_ENERGIA_JUGAR} "
                f"y hay {self.energia}."
            )
        self.energia = self.energia - self.COSTO_ENERGIA_JUGAR
        return (
            f"{self.nombre} juega y gasta energía. "
            f"Energía restante: {self.energia}."
        )

    def descansar(self) -> str:
        """Recupera energía sin superar el máximo.

        Returns:
            Mensaje con la energía actual.
        """
        self.energia = min(
            self.ENERGIA_MAXIMA,
            self.energia + self.RECUPERACION_DESCANSO,
        )
        return f"{self.nombre} descansa. Energía actual: {self.energia}."

    def vacunar(self) -> str:
        """Marca al perro como vacunado.

        Returns:
            Mensaje de confirmación.

        Raises:
            ValueError: Si ya estaba vacunado.
        """
        if self.__vacunado:
            raise ValueError(f"{self.nombre} ya está vacunado.")
        self.__vacunado = True
        return f"{self.nombre} ha sido vacunado."

    def __str__(self) -> str:
        """Representación legible del perro."""
        estado_vacuna = "vacunado" if self.vacunado else "sin vacunar"
        return (
            f"Perro: {self.nombre}, {self.edad} años, "
            f"{self.peso} kg, color {self.color}, "
            f"energía {self.energia}, {estado_vacuna}."
        )
