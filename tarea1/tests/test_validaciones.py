"""Pruebas de validar_datos (reglas usadas por la interfaz)."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

RAIZ_PROGRAMA = Path(__file__).resolve().parents[1]
if str(RAIZ_PROGRAMA) not in sys.path:
    sys.path.insert(0, str(RAIZ_PROGRAMA))

from validaciones.reglas import validar_datos  # noqa: E402


def _base(**overrides):
    datos = {
        "nombre": "Nube",
        "especie": "Gato",
        "edad": 2,
        "peso": 3.5,
        "color": "Gris",
        "observaciones": "  ok  ",
    }
    datos.update(overrides)
    return datos


class TestValidarDatos(unittest.TestCase):
    def test_registro_valido(self) -> None:
        limpio = validar_datos(_base())
        self.assertEqual(limpio["nombre"], "Nube")
        self.assertEqual(limpio["especie"], "Gato")
        self.assertEqual(limpio["edad"], 2)
        self.assertAlmostEqual(limpio["peso"], 3.5)
        self.assertEqual(limpio["color"], "Gris")
        self.assertEqual(limpio["observaciones"], "ok")

    def test_nombre_obligatorio(self) -> None:
        with self.assertRaisesRegex(ValueError, "nombre"):
            validar_datos(_base(nombre="  "))

    def test_especie_invalida(self) -> None:
        with self.assertRaisesRegex(ValueError, "especie"):
            validar_datos(_base(especie="Hamster"))

    def test_color_obligatorio(self) -> None:
        with self.assertRaisesRegex(ValueError, "color"):
            validar_datos(_base(color=""))

    def test_edad_no_entera(self) -> None:
        with self.assertRaisesRegex(ValueError, "edad"):
            validar_datos(_base(edad="2"))

    def test_edad_fuera_de_rango(self) -> None:
        with self.assertRaisesRegex(ValueError, "0 y 30"):
            validar_datos(_base(edad=31))

    def test_peso_invalido(self) -> None:
        with self.assertRaisesRegex(ValueError, "peso"):
            validar_datos(_base(peso="abc"))

    def test_peso_no_positivo(self) -> None:
        with self.assertRaisesRegex(ValueError, "entre"):
            validar_datos(_base(peso=0))

    def test_peso_demasiado_alto(self) -> None:
        with self.assertRaisesRegex(ValueError, "entre"):
            validar_datos(_base(peso=150))

    def test_peso_en_limite_superior(self) -> None:
        limpio = validar_datos(_base(peso=100))
        self.assertAlmostEqual(limpio["peso"], 100.0)

    def test_peso_alto_pero_valido(self) -> None:
        limpio = validar_datos(_base(peso=83))
        self.assertAlmostEqual(limpio["peso"], 83.0)


if __name__ == "__main__":
    unittest.main()
