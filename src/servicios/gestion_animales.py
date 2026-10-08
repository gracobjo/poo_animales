"""Operaciones que funcionan con cualquier tipo de animal.

Estas funciones no preguntan si el objeto es un perro o un gato. Llaman
a los métodos definidos en el contrato de ``Animal`` (o al método
``comer`` / la propiedad ``peso``, que comparten las subclases). El
resultado cambia según la clase real del objeto: eso es el polimorfismo.
"""

from typing import List, Sequence

from src.modelos.animal import Animal


def _como_lista(animales: Sequence[Animal]) -> List[Animal]:
    """Convierte la entrada en una lista de animales.

    Args:
        animales: Secuencia de animales. No se acepta un texto.

    Returns:
        Una lista nueva con los mismos elementos.

    Raises:
        ValueError: Si el argumento no es una secuencia de animales.
    """
    if isinstance(animales, (str, bytes)):
        raise ValueError("Se esperaba una secuencia de animales.")
    try:
        return list(animales)
    except TypeError as error:
        raise ValueError("Se esperaba una secuencia de animales.") from error


def emitir_sonido(animal: Animal) -> str:
    """Pide a un animal que emita su sonido, sea cual sea su especie.

    Args:
        animal: Instancia de una subclase de ``Animal``.

    Returns:
        El texto que devuelve ``hacer_sonido``.

    Raises:
        ValueError: Si el objeto no implementa ``hacer_sonido``.
    """
    try:
        return animal.hacer_sonido()
    except AttributeError as error:
        raise ValueError(
            "El objeto recibido no implementa hacer_sonido()."
        ) from error


def alimentar(animal: Animal, gramos: float) -> str:
    """Alimenta a un animal delegando en su propio método ``comer``.

    Perro y gato comparten el nombre del método, pero cada uno actualiza
    su energía con reglas distintas. La función no necesita distinguirlos.

    Args:
        animal: Animal que sepa comer.
        gramos: Cantidad de comida, mayor que cero.

    Returns:
        El mensaje que devuelve ``comer``.

    Raises:
        ValueError: Si el animal no puede comer o los gramos no son válidos.
    """
    comer = getattr(animal, "comer", None)
    if not callable(comer):
        raise ValueError(
            f"{getattr(animal, 'nombre', 'El animal')} "
            "no tiene un comportamiento de alimentación."
        )
    return comer(gramos)


def listar_info(animales: Sequence[Animal]) -> List[str]:
    """Recoge la información básica de cada animal.

    Args:
        animales: Secuencia de animales.

    Returns:
        Lista de textos producidos por ``info_basica``.

    Raises:
        ValueError: Si la entrada no es una secuencia o algún elemento
            no implementa ``info_basica``.
    """
    informacion: List[str] = []
    try:
        for animal in _como_lista(animales):
            informacion.append(animal.info_basica())
    except AttributeError as error:
        raise ValueError(
            "Todos los elementos deben implementar info_basica()."
        ) from error
    return informacion


def animales_mayores_de(
    animales: Sequence[Animal],
    edad_minima: int,
) -> List[Animal]:
    """Filtra los animales cuya edad es mayor o igual que la indicada.

    Args:
        animales: Secuencia de animales.
        edad_minima: Edad entera mínima, a partir de cero (inclusive).

    Returns:
        Lista con los animales que cumplen el filtro. Puede estar vacía.

    Raises:
        ValueError: Si la edad mínima no es un entero mayor o igual que
            cero, o si la entrada no es una secuencia válida.
    """
    if isinstance(edad_minima, bool) or not isinstance(edad_minima, int):
        raise ValueError("'edad_minima' debe ser un número entero.")
    if edad_minima < 0:
        raise ValueError("'edad_minima' no puede ser negativa.")

    try:
        return [
            animal
            for animal in _como_lista(animales)
            if animal.edad >= edad_minima
        ]
    except AttributeError as error:
        raise ValueError(
            "Todos los elementos deben exponer la propiedad edad."
        ) from error


def total_peso(animales: Sequence[Animal]) -> float:
    """Suma el peso de todos los animales de la secuencia.

    Args:
        animales: Secuencia de animales con la propiedad ``peso``.

    Returns:
        Suma de los pesos en kilogramos. Cero si la secuencia está vacía.

    Raises:
        ValueError: Si la entrada no es una secuencia o algún elemento
            no tiene peso numérico.
    """
    total = 0.0
    try:
        for animal in _como_lista(animales):
            total += animal.peso
    except AttributeError as error:
        raise ValueError(
            "Todos los elementos deben exponer la propiedad peso."
        ) from error
    except TypeError as error:
        raise ValueError(
            "El peso de cada animal debe ser numérico."
        ) from error
    return total
