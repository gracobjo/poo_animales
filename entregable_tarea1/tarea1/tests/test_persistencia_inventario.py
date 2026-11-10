"""Persistencia del inventario de animales en JSON."""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

RAIZ_PROGRAMA = Path(__file__).resolve().parents[1]
if str(RAIZ_PROGRAMA) not in sys.path:
    sys.path.insert(0, str(RAIZ_PROGRAMA))

from datos.inventario import animales_iniciales, crear_animal  # noqa: E402
from datos.persistencia_inventario import (  # noqa: E402
    cargar_inventario,
    guardar_inventario,
)


class TestPersistenciaInventario(unittest.TestCase):
    def test_guardar_y_cargar_redondea_trip(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            ruta = Path(tmp) / "inventario.json"
            original = animales_iniciales()
            crear_animal(
                {
                    "nombre": "Nico",
                    "especie": "Perro",
                    "edad": 2,
                    "peso": 1.2,
                    "color": "Marrón",
                    "observaciones": "Persistencia",
                },
                original,
            )
            guardar_inventario(original, ruta)
            self.assertTrue(ruta.is_file())
            cargado = cargar_inventario(ruta)
            self.assertEqual(set(cargado), set(original))
            self.assertEqual(cargado[5]["nombre"], "Nico")
            self.assertIn("tratamientos", cargado[1])

    def test_cargar_sin_archivo_siembra_ejemplo(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            ruta = Path(tmp) / "nuevo.json"
            inventario = cargar_inventario(ruta)
            self.assertTrue(ruta.is_file())
            self.assertEqual(len(inventario), 4)
            self.assertEqual(inventario[1]["nombre"], "Luna")

    def test_json_claves_string(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            ruta = Path(tmp) / "inventario.json"
            guardar_inventario(animales_iniciales(), ruta)
            datos = json.loads(ruta.read_text(encoding="utf-8"))
            self.assertTrue(all(isinstance(k, str) for k in datos))

    def test_json_corrupto_no_rompe_arranque(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            ruta = Path(tmp) / "roto.json"
            ruta.write_text("{no-es-json", encoding="utf-8")
            inventario = cargar_inventario(ruta)
            self.assertEqual(inventario[1]["nombre"], "Luna")
            # No sobrescribe el archivo corrupto automáticamente
            self.assertEqual(ruta.read_text(encoding="utf-8"), "{no-es-json")


if __name__ == "__main__":
    unittest.main()
