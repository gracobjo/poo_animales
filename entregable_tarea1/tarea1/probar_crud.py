"""Prueba rápida de las operaciones CRUD sin abrir la interfaz."""

from __future__ import annotations

import sys
from pathlib import Path

RAIZ_PROGRAMA = Path(__file__).resolve().parent
if str(RAIZ_PROGRAMA) not in sys.path:
    sys.path.insert(0, str(RAIZ_PROGRAMA))

from datos.inventario import (
    actualizar_animal,
    borrar_animal,
    crear_animal,
    leer_animal,
)


def main() -> None:
    inventario: dict = {}
    datos = {
        "nombre": "Nube",
        "especie": "Gato",
        "edad": 2,
        "peso": 3.8,
        "color": "Gris",
        "observaciones": "Ejemplo temporal",
    }
    animal_id = crear_animal(datos, inventario)
    print("Crear:", animal_id, inventario)
    print("Leer:", leer_animal(animal_id, inventario))

    datos["edad"] = 3
    actualizar_animal(animal_id, datos, inventario)
    print("Actualizar:", leer_animal(animal_id, inventario))

    borrar_animal(animal_id, inventario)
    print("Borrar: quedan", len(inventario), "registros.")
    print("CRUD OK")


if __name__ == "__main__":
    main()
