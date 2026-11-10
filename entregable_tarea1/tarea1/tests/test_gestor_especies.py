"""Pruebas del catálogo de especies nativas y personalizadas."""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

RAIZ_PROGRAMA = Path(__file__).resolve().parents[1]
if str(RAIZ_PROGRAMA) not in sys.path:
    sys.path.insert(0, str(RAIZ_PROGRAMA))

from datos.constantes import ESPECIES  # noqa: E402
from datos.gestor_especies import (  # noqa: E402
    CatalogoEspecies,
    reiniciar_catalogo_global,
)


def _huron(**extra):
    base = {
        "nombre": "Hurón",
        "sonido": "Emite pequeños sonidos y chillidos",
        "alimentacion": "Carnívoro",
        "cuidados": "Necesita un entorno seguro y supervisión",
    }
    base.update(extra)
    return base


class TestCatalogoEspecies(unittest.TestCase):
    def setUp(self) -> None:
        reiniciar_catalogo_global()
        self.tmp = tempfile.TemporaryDirectory()
        self.ruta = Path(self.tmp.name) / "especies_personalizadas.json"
        self.cat = CatalogoEspecies(self.ruta)

    def tearDown(self) -> None:
        reiniciar_catalogo_global()
        self.tmp.cleanup()

    def test_carga_nativas(self) -> None:
        self.assertEqual(self.cat.nativas(), ESPECIES)
        self.assertTrue(self.cat.es_nativa("Perro"))
        self.assertTrue(self.cat.es_nativa("  gato  "))

    def test_crea_archivo_si_no_existe(self) -> None:
        self.assertTrue(self.ruta.is_file())
        self.assertEqual(json.loads(self.ruta.read_text(encoding="utf-8")), [])

    def test_alta_personalizada_y_persistencia(self) -> None:
        self.cat.anadir(_huron())
        otro = CatalogoEspecies(self.ruta)
        hallada = otro.obtener_personalizada("hurón")
        self.assertIsNotNone(hallada)
        assert hallada is not None
        self.assertEqual(hallada["nombre"], "Hurón")
        self.assertTrue(hallada["activa"])
        self.assertIn("Hurón", otro.nombres_activos_para_alta())

    def test_rechaza_nombre_vacio(self) -> None:
        with self.assertRaisesRegex(ValueError, "nombre"):
            self.cat.anadir(_huron(nombre="  "))

    def test_rechaza_duplicado(self) -> None:
        self.cat.anadir(_huron())
        with self.assertRaisesRegex(ValueError, "Ya existe"):
            self.cat.anadir(_huron(nombre="hurón"))

    def test_rechaza_nativa(self) -> None:
        with self.assertRaisesRegex(ValueError, "nativa"):
            self.cat.anadir(_huron(nombre="Perro"))

    def test_edicion(self) -> None:
        self.cat.anadir(_huron())
        actualizada = self.cat.actualizar(
            "Hurón",
            _huron(alimentacion="Omnívoro ocasional"),
        )
        self.assertEqual(actualizada["alimentacion"], "Omnívoro ocasional")

    def test_desactivacion(self) -> None:
        self.cat.anadir(_huron())
        self.cat.desactivar("Hurón")
        self.assertNotIn("Hurón", self.cat.nombres_activos_para_alta())
        self.assertIn("Hurón", self.cat.nombres_para_filtro())
        cfg = self.cat.obtener_personalizada("Hurón")
        assert cfg is not None
        self.assertFalse(cfg["activa"])

    def test_no_elimina_si_hay_animales(self) -> None:
        self.cat.anadir(_huron())
        with self.assertRaisesRegex(ValueError, "animales registrados"):
            self.cat.eliminar("Hurón", especies_en_uso=["Hurón", "Perro"])

    def test_elimina_si_no_hay_uso(self) -> None:
        self.cat.anadir(_huron())
        self.cat.eliminar("Hurón", especies_en_uso=["Perro"])
        self.assertIsNone(self.cat.obtener_personalizada("Hurón"))

    def test_json_corrupto_no_sobrescribe(self) -> None:
        self.ruta.write_text("{no-es-json", encoding="utf-8")
        cat = CatalogoEspecies(self.ruta)
        self.assertEqual(cat.personalizadas(), [])
        self.assertEqual(self.ruta.read_text(encoding="utf-8"), "{no-es-json")


if __name__ == "__main__":
    unittest.main()
