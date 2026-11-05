"""Campos ampliados de la ficha: clínica, vacunas, documentos y foto."""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Dict, List

CAMPOS_CLINICOS = ("foto", "tratamientos", "vacunaciones", "documentos")


def ficha_vacia_clinica() -> Dict[str, Any]:
    """Valores por defecto de la parte clínica / adjuntos."""
    return {
        "foto": "",
        "tratamientos": [],
        "vacunaciones": [],
        "documentos": [],
    }


def asegurar_campos_clinicos(registro: Dict[str, Any]) -> Dict[str, Any]:
    """Garantiza que el registro tenga foto, listas clínicas y documentos."""
    base = ficha_vacia_clinica()
    for clave, valor in base.items():
        if clave not in registro or registro[clave] is None:
            registro[clave] = deepcopy(valor)
    return registro


def normalizar_tratamientos(raw: Any) -> List[Dict[str, str]]:
    if not raw:
        return []
    if not isinstance(raw, list):
        raise ValueError("Los tratamientos deben ser una lista.")
    limpios: List[Dict[str, str]] = []
    for item in raw:
        if not isinstance(item, dict):
            raise ValueError("Cada tratamiento debe ser un diccionario.")
        fecha = str(item.get("fecha", "")).strip()
        descripcion = str(item.get("descripcion", "")).strip()
        veterinario = str(item.get("veterinario", "")).strip()
        if not descripcion:
            raise ValueError("El tratamiento necesita una descripción.")
        limpios.append(
            {
                "fecha": fecha,
                "descripcion": descripcion,
                "veterinario": veterinario,
            }
        )
    return limpios


def normalizar_vacunaciones(raw: Any) -> List[Dict[str, str]]:
    if not raw:
        return []
    if not isinstance(raw, list):
        raise ValueError("Las vacunaciones deben ser una lista.")
    limpios: List[Dict[str, str]] = []
    for item in raw:
        if not isinstance(item, dict):
            raise ValueError("Cada vacunación debe ser un diccionario.")
        vacuna = str(item.get("vacuna", "")).strip()
        if not vacuna:
            raise ValueError("Indica el nombre de la vacuna.")
        limpios.append(
            {
                "fecha": str(item.get("fecha", "")).strip(),
                "vacuna": vacuna,
                "proxima": str(item.get("proxima", "")).strip(),
            }
        )
    return limpios


def normalizar_documentos(raw: Any) -> List[Dict[str, str]]:
    if not raw:
        return []
    if not isinstance(raw, list):
        raise ValueError("Los documentos deben ser una lista.")
    limpios: List[Dict[str, str]] = []
    for item in raw:
        if not isinstance(item, dict):
            raise ValueError("Cada documento debe ser un diccionario.")
        nombre = str(item.get("nombre", "")).strip()
        ruta = str(item.get("ruta", "")).strip()
        if not nombre or not ruta:
            raise ValueError("Cada documento necesita nombre y ruta.")
        limpios.append(
            {
                "nombre": nombre,
                "ruta": ruta,
                "fecha": str(item.get("fecha", "")).strip(),
            }
        )
    return limpios
