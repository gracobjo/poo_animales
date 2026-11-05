"""Decoradores didácticos usados por el modelo POO del refugio."""

from __future__ import annotations

from functools import wraps
from typing import Any, Callable, TypeVar

F = TypeVar("F", bound=Callable[..., Any])


def cuenta_usos(metodo: F) -> F:
    """Decorador de método de instancia: cuenta cuántas veces se invoca.

    El contador vive en ``self._usos_<nombre_metodo>``. Sirve en defensa
    para mostrar un decorador propio además de ``@property`` / ``@abstractmethod``.
    """

    @wraps(metodo)
    def envoltura(self: Any, *args: Any, **kwargs: Any) -> Any:
        atributo = f"_usos_{metodo.__name__}"
        setattr(self, atributo, getattr(self, atributo, 0) + 1)
        return metodo(self, *args, **kwargs)

    return envoltura  # type: ignore[return-value]
