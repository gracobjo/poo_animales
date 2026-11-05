"""Pruebas del inventario y operaciones CRUD."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

RAIZ_PROGRAMA = Path(__file__).resolve().parents[1]
if str(RAIZ_PROGRAMA) not in sys.path:
    sys.path.insert(0, str(RAIZ_PROGRAMA))

from datos.inventario import (  # noqa: E402
    actualizar_animal,
    animales_iniciales,
    borrar_animal,
    crear_animal,
    leer_animal,
)


class TestInventario(unittest.TestCase):
    def setUp(self) -> None:
        self.inventario = animales_iniciales()

    def test_animales_iniciales_tiene_cuatro(self) -> None:
        self.assertEqual(len(self.inventario), 4)

    def test_crear_asigna_siguiente_id(self) -> None:
        nuevo = crear_animal(
            {
                "nombre": "Nube",
                "especie": "Gato",
                "edad": 2,
                "peso": 3.8,
                "color": "Gris",
                "observaciones": "",
            },
            self.inventario,
        )
        self.assertEqual(nuevo, 5)
        self.assertEqual(self.inventario[5]["nombre"], "Nube")

    def test_leer_devuelve_copia(self) -> None:
        copia = leer_animal(1, self.inventario)
        copia["nombre"] = "Otro"
        self.assertEqual(self.inventario[1]["nombre"], "Luna")

    def test_leer_inexistente(self) -> None:
        with self.assertRaises(ValueError):
            leer_animal(99, self.inventario)

    def test_actualizar(self) -> None:
        actualizar_animal(
            1,
            {
                "nombre": "Luna",
                "especie": "Perro",
                "edad": 5,
                "peso": 19.0,
                "color": "Canela",
                "observaciones": "Actualizado",
            },
            self.inventario,
        )
        self.assertEqual(self.inventario[1]["edad"], 5)
        self.assertEqual(self.inventario[1]["observaciones"], "Actualizado")

    def test_borrar(self) -> None:
        borrado = borrar_animal(2, self.inventario)
        self.assertEqual(borrado["nombre"], "Misi")
        self.assertNotIn(2, self.inventario)

    def test_borrar_inexistente(self) -> None:
        with self.assertRaises(ValueError):
            borrar_animal(99, self.inventario)


if __name__ == "__main__":
    unittest.main()
