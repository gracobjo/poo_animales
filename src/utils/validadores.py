"""Validaciones numéricas reutilizables.

Estas funciones centralizan las comprobaciones que usan las propiedades
de los modelos. Lanzan ``ValueError`` cuando un dato no cumple la regla,
para que el resto del programa no tenga que repetir la misma lógica.
"""

from typing import Union

Numero = Union[int, float]


def validar_positivo(valor: Numero, nombre_campo: str) -> Numero:
    """Comprueba que un valor sea numérico y estrictamente mayor que cero.

    El cero no se considera positivo: un peso o una ración de comida de
    0 no tienen sentido en este dominio. ``bool`` se rechaza aparte porque
    en Python es una subclase de ``int`` (``True == 1``).

    Args:
        valor: Número a validar.
        nombre_campo: Nombre del dato, usado en el mensaje de error.

    Returns:
        El mismo valor si supera la validación.

    Raises:
        ValueError: Si el valor no es numérico o no es mayor que cero.
    """
    if isinstance(valor, bool) or not isinstance(valor, (int, float)):
        raise ValueError(f"'{nombre_campo}' debe ser un número.")
    if valor <= 0:
        raise ValueError(f"'{nombre_campo}' debe ser mayor que cero.")
    return valor


def validar_rango(
    valor: Numero,
    minimo: Numero,
    maximo: Numero,
    nombre_campo: str,
) -> Numero:
    """Comprueba que un valor numérico esté dentro de un intervalo cerrado.

    Los extremos se incluyen: un valor igual a ``minimo`` o a ``maximo``
    es válido. Sirve, por ejemplo, para la edad (0 a 30) y la energía
    (0 a 100).

    Args:
        valor: Número a validar.
        minimo: Límite inferior permitido.
        maximo: Límite superior permitido.
        nombre_campo: Nombre del dato, usado en el mensaje de error.

    Returns:
        El mismo valor si está dentro del rango.

    Raises:
        ValueError: Si los límites son inválidos, el valor no es numérico
            o queda fuera del intervalo.
    """
    if isinstance(minimo, bool) or isinstance(maximo, bool):
        raise ValueError("Los límites del rango deben ser numéricos.")
    limites_validos = (
        isinstance(minimo, (int, float)) and isinstance(maximo, (int, float))
    )
    if not limites_validos:
        raise ValueError("Los límites del rango deben ser numéricos.")
    if minimo > maximo:
        raise ValueError("El mínimo no puede ser mayor que el máximo.")
    if isinstance(valor, bool) or not isinstance(valor, (int, float)):
        raise ValueError(f"'{nombre_campo}' debe ser un número.")
    if valor < minimo or valor > maximo:
        raise ValueError(
            f"'{nombre_campo}' debe estar entre {minimo} y {maximo}."
        )
    return valor
