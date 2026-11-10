"""Inventario inicial y operaciones CRUD sobre diccionarios.

La clave de ``animales`` es un ID numérico (como una clave primaria).
El valor es otro diccionario con los campos del animal, incluida la
ficha clínica (tratamientos, vacunas, documentos y foto).
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Dict

from datos.adjuntos import borrar_adjuntos_animal
from datos.constantes import ESPECIES
from datos.ficha import asegurar_campos_clinicos, ficha_vacia_clinica
from validaciones.reglas import validar_datos

Inventario = Dict[int, Dict[str, Any]]

__all__ = [
    "ESPECIES",
    "Inventario",
    "animales_iniciales",
    "crear_animal",
    "leer_animal",
    "actualizar_animal",
    "borrar_animal",
]


def _ejemplo(base: Dict[str, Any], **clinica: Any) -> Dict[str, Any]:
    registro = {**base, **ficha_vacia_clinica()}
    registro.update(clinica)
    return asegurar_campos_clinicos(registro)


def animales_iniciales() -> Inventario:
    """Devuelve una copia del inventario de ejemplo del refugio."""
    return {
        1: _ejemplo(
            {
                "nombre": "Luna",
                "especie": "Perro",
                "edad": 4,
                "peso": 18.5,
                "color": "Canela",
                "observaciones": "Sociable; disfruta de los paseos.",
            },
            vacunaciones=[
                {
                    "fecha": "2025-03-10",
                    "vacuna": "Rabia",
                    "proxima": "2026-03-10",
                }
            ],
            tratamientos=[
                {
                    "fecha": "2025-06-01",
                    "descripcion": "Desparasitación interna",
                    "veterinario": "Dra. Ruiz",
                }
            ],
        ),
        2: _ejemplo(
            {
                "nombre": "Misi",
                "especie": "Gato",
                "edad": 3,
                "peso": 4.2,
                "color": "Blanco y gris",
                "observaciones": "Tranquilo; busca una familia paciente.",
            },
            vacunaciones=[
                {
                    "fecha": "2025-01-20",
                    "vacuna": "Trivalente felina",
                    "proxima": "2026-01-20",
                }
            ],
        ),
        3: _ejemplo(
            {
                "nombre": "Kiko",
                "especie": "Loro",
                "edad": 7,
                "peso": 0.6,
                "color": "Verde",
                "observaciones": "Le gusta escuchar música.",
            }
        ),
        4: _ejemplo(
            {
                "nombre": "Toby",
                "especie": "Perro",
                "edad": 1,
                "peso": 8.3,
                "color": "Negro",
                "observaciones": "Juguetón y con mucha energía.",
            },
            tratamientos=[
                {
                    "fecha": "2025-11-01",
                    "descripcion": "Revisión otitis",
                    "veterinario": "Dr. Pérez",
                }
            ],
        ),
    }


def crear_animal(datos: Dict[str, Any], inventario: Inventario) -> int:
    """Valida y añade un animal; devuelve el nuevo identificador."""
    registro = validar_datos(datos)
    nuevo_id = max(inventario, default=0) + 1
    inventario[nuevo_id] = registro
    return nuevo_id


def leer_animal(animal_id: int, inventario: Inventario) -> Dict[str, Any]:
    """Devuelve una copia profunda del registro."""
    if animal_id not in inventario:
        raise ValueError("No se ha encontrado ese animal.")
    copia = deepcopy(inventario[animal_id])
    return asegurar_campos_clinicos(copia)


def actualizar_animal(
    animal_id: int,
    datos: Dict[str, Any],
    inventario: Inventario,
) -> None:
    """Valida y sustituye los datos del animal indicado.

    Si ``datos`` no trae campos clínicos, se conservan los del registro actual.
    """
    if animal_id not in inventario:
        raise ValueError("No se ha encontrado ese animal.")
    actual = inventario[animal_id]
    fusion = {
        "foto": datos["foto"] if "foto" in datos else actual.get("foto", ""),
        "tratamientos": (
            datos["tratamientos"]
            if "tratamientos" in datos
            else actual.get("tratamientos", [])
        ),
        "vacunaciones": (
            datos["vacunaciones"]
            if "vacunaciones" in datos
            else actual.get("vacunaciones", [])
        ),
        "documentos": (
            datos["documentos"]
            if "documentos" in datos
            else actual.get("documentos", [])
        ),
    }
    completo = {**datos, **fusion}
    inventario[animal_id] = validar_datos(
        completo,
        especie_previa=str(actual.get("especie", "")),
    )


def borrar_animal(animal_id: int, inventario: Inventario) -> Dict[str, Any]:
    """Elimina el animal, sus adjuntos en disco y devuelve sus datos."""
    if animal_id not in inventario:
        raise ValueError("No se ha encontrado ese animal.")
    borrado = inventario.pop(animal_id)
    borrar_adjuntos_animal(animal_id)
    return borrado
