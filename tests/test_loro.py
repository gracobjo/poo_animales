"""Pruebas unitarias de la clase Loro."""

import sys
import unittest
from pathlib import Path

RAIZ_PROYECTO = Path(__file__).resolve().parents[1]
if str(RAIZ_PROYECTO) not in sys.path:
    sys.path.insert(0, str(RAIZ_PROYECTO))

from src.modelos.animal import Animal  # noqa: E402
from src.modelos.loro import Loro  # noqa: E402


class TestLoro(unittest.TestCase):
    """Cubre sonido, vuelo, frase aprendida y validaciones del loro."""

    def setUp(self) -> None:
        """Crea un loro nuevo antes de cada prueba."""
        self.loro = Loro("Kiko", 4, 0.4, "verde", energia=60)

    def test_es_instancia_de_animal(self) -> None:
        self.assertIsInstance(self.loro, Animal)

    def test_hablar_sin_frase_grazna(self) -> None:
        self.assertEqual(self.loro.hablar(), "Kiko dice: ¡Aaah!")

    def test_hacer_sonido_delega_en_hablar(self) -> None:
        self.assertEqual(self.loro.hacer_sonido(), self.loro.hablar())

    def test_tipo_alimentacion(self) -> None:
        self.assertEqual(self.loro.tipo_alimentacion(), "granívoro")

    def test_aprender_guarda_la_frase(self) -> None:
        self.loro.aprender("  Hola  ")
        self.assertEqual(self.loro.frase, "Hola")
        self.assertEqual(self.loro.hablar(), "Kiko dice: Hola")

    def test_aprender_vacio_no_cambia_la_frase(self) -> None:
        self.loro.aprender("Hola")
        with self.assertRaises(ValueError):
            self.loro.aprender("   ")
        self.assertEqual(self.loro.frase, "Hola")

    def test_volar_reduce_energia(self) -> None:
        self.loro.volar()
        self.assertEqual(
            self.loro.energia,
            60 - Loro.COSTO_ENERGIA_VOLAR,
        )

    def test_volar_sin_energia_no_cambia_el_estado(self) -> None:
        cansado = Loro("Luna", 1, 0.3, "azul", energia=10)
        with self.assertRaises(ValueError):
            cansado.volar()
        self.assertEqual(cansado.energia, 10)

    def test_comer_aumenta_peso_y_energia(self) -> None:
        self.loro.comer(200)
        self.assertAlmostEqual(self.loro.peso, 0.6)
        self.assertEqual(
            self.loro.energia,
            60 + Loro.RECUPERACION_COMIDA,
        )

    def test_comer_invalido_no_cambia_el_estado(self) -> None:
        with self.assertRaises(ValueError):
            self.loro.comer(0)
        self.assertEqual(self.loro.peso, 0.4)
        self.assertEqual(self.loro.energia, 60)

    def test_setter_peso_no_positivo_no_cambia_el_valor(self) -> None:
        with self.assertRaises(ValueError):
            self.loro.peso = -1
        self.assertEqual(self.loro.peso, 0.4)

    def test_frase_es_de_solo_lectura(self) -> None:
        with self.assertRaises(AttributeError):
            self.loro.frase = "Adiós"  # type: ignore[misc]

    def test_peso_no_es_un_atributo_publico(self) -> None:
        self.assertFalse(hasattr(self.loro, "__peso"))

    def test_str_incluye_nombre_y_frase(self) -> None:
        texto = str(self.loro)
        self.assertIn("Kiko", texto)
        self.assertIn("frase ninguna", texto)


if __name__ == "__main__":
    unittest.main()
