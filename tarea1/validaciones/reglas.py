"""Reglas de validación independientes de la interfaz gráfica."""

from __future__ import annotations

import math
from typing import Any, Dict, Optional

from datos.constantes import PESO_MAX_KG, PESO_MIN_KG
from datos.ficha import (
    normalizar_documentos,
    normalizar_tratamientos,
    normalizar_vacunaciones,
)


def validar_datos(
    datos: Dict[str, Any],
    *,
    especie_previa: Optional[str] = None,
) -> Dict[str, Any]:
    """Comprueba los datos del formulario y devuelve un registro limpio.

    Incluye campos clínicos opcionales: foto, tratamientos, vacunaciones
    y documentos. Si no vienen en ``datos``, quedan vacíos.

    La especie debe estar en el catálogo activo. Si ``especie_previa`` coincide
    con la especie del registro (p. ej. al actualizar un animal de una especie
    personalizada ya desactivada), se admite para no romper registros antiguos.

    Raises:
        ValueError: Si falta un campo obligatorio o un valor no es válido.
    """
    from datos.gestor_especies import get_catalogo, normalizar_nombre

    nombre = str(datos.get("nombre", "")).strip()
    especie = str(datos.get("especie", "")).strip()
    color = str(datos.get("color", "")).strip()
    observaciones = str(datos.get("observaciones", "")).strip()
    edad = datos.get("edad")
    foto = str(datos.get("foto", "") or "").strip()

    if not nombre:
        raise ValueError("El nombre es obligatorio.")
    if not especie:
        raise ValueError("Selecciona una especie de la lista.")

    catalogo = get_catalogo()
    permitida = catalogo.especie_permitida_en_alta(especie)
    misma_previa = (
        especie_previa is not None
        and normalizar_nombre(especie) == normalizar_nombre(especie_previa)
        and catalogo.especie_conocida(especie)
    )
    if not permitida and not misma_previa:
        raise ValueError("Selecciona una especie de la lista.")

    if not color:
        raise ValueError("El color es obligatorio.")
    if isinstance(edad, bool) or not isinstance(edad, int):
        raise ValueError("La edad debe ser un número entero.")
    if edad < 0 or edad > 30:
        raise ValueError("La edad debe estar entre 0 y 30 años.")

    try:
        peso = float(datos.get("peso"))
    except (TypeError, ValueError) as error:
        raise ValueError("El peso debe ser un número válido.") from error
    if not math.isfinite(peso):
        raise ValueError("El peso debe ser un número finito.")
    if peso < PESO_MIN_KG or peso > PESO_MAX_KG:
        raise ValueError(
            f"El peso debe estar entre {PESO_MIN_KG} y {PESO_MAX_KG} kg."
        )

    return {
        "nombre": nombre,
        "especie": especie,
        "edad": edad,
        "peso": peso,
        "color": color,
        "observaciones": observaciones,
        "foto": foto,
        "tratamientos": normalizar_tratamientos(datos.get("tratamientos")),
        "vacunaciones": normalizar_vacunaciones(datos.get("vacunaciones")),
        "documentos": normalizar_documentos(datos.get("documentos")),
    }
