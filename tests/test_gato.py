"""Pruebas unitarias de la clase Gato."""

import sys
import unittest
from pathlib import Path

# Permite ejecutar este archivo directamente, no solo como módulo.
RAIZ_PROYECTO = Path(__file__).resolve().parents[1]
if str(RAIZ_PROYECTO) not in sys.path:
    sys.path.insert(0, str(RAIZ_PROYECTO))

from src.modelos.animal import Animal  # noqa: E402
from src.modelos.gato import Gato  # noqa: E402


class TestGato(unittest.TestCase):
    """Cubre sonido, comportamiento, propiedades y validaciones del gato."""

    def setUp(self) -> None:
        """Crea un gato nuevo antes de cada prueba."""
        self.gato = Gato("Misi", 3, 4.5, "blanco", energia=60)

    def test_es_instancia_de_animal(self) -> None:
        self.assertIsInstance(self.gato, Animal)

    def test_maullar(self) -> None:
        self.assertEqual(self.gato.maullar(), "Misi dice: ¡Miau!")

    def test_hacer_sonido_delega_en_maullar(self) -> None:
        self.assertEqual(self.gato.hacer_sonido(), "Misi dice: ¡Miau!")

    def test_tipo_alimentacion(self) -> None:
        self.assertEqual(self.gato.tipo_alimentacion(), "carnívoro")

    def test_ronronear(self) -> None:
        self.assertEqual(self.gato.ronronear(), "Misi ronronea: Prrr...")

    def test_ronronear_sin_energia_no_cambia_el_estado(self) -> None:
        cansado = Gato("Nube", 2, 3.5, "gris", energia=5)
        with self.assertRaises(ValueError):
            cansado.ronronear()
        self.assertEqual(cansado.energia, 5)

    def test_comer_aumenta_peso_y_energia(self) -> None:
        mensaje = self.gato.comer(500)
        self.assertAlmostEqual(self.gato.peso, 5.0)
        self.assertEqual(self.gato.energia, 60 + Gato.RECUPERACION_COMIDA)
        self.assertIn("Misi", mensaje)

    def test_comer_no_supera_energia_maxima(self) -> None:
        self.gato.energia = 95
        self.gato.comer(100)
        self.assertEqual(self.gato.energia, Gato.ENERGIA_MAXIMA)

    def test_comer_invalido_no_cambia_el_estado(self) -> None:
        with self.assertRaises(ValueError):
            self.gato.comer(-5)
        self.assertEqual(self.gato.peso, 4.5)
        self.assertEqual(self.gato.energia, 60)

    def test_cazar_reduce_energia_y_suma_una_presa(self) -> None:
        mensaje = self.gato.cazar()
        self.assertEqual(self.gato.energia, 60 - Gato.COSTO_ENERGIA_CAZAR)
        self.assertEqual(self.gato.presas_cazadas, 1)
        self.assertIn("presa", mensaje)

    def test_cazar_dos_veces_acumula_presas(self) -> None:
        self.gato.cazar()
        self.gato.cazar()
        self.assertEqual(self.gato.presas_cazadas, 2)

    def test_cazar_sin_energia_no_suma_presas(self) -> None:
        cansado = Gato("Nube", 2, 3.5, "gris", energia=10)
        with self.assertRaises(ValueError):
            cansado.cazar()
        self.assertEqual(cansado.presas_cazadas, 0)
        self.assertEqual(cansado.energia, 10)

    def test_dormir_recupera_energia(self) -> None:
        self.gato.dormir()
        self.assertEqual(self.gato.energia, 60 + Gato.RECUPERACION_DORMIR)

    def test_dormir_no_supera_el_maximo(self) -> None:
        self.gato.energia = 80
        self.gato.dormir()
        self.assertEqual(self.gato.energia, Gato.ENERGIA_MAXIMA)

    def test_getters_devuelven_los_datos_iniciales(self) -> None:
        self.assertEqual(self.gato.nombre, "Misi")
        self.assertEqual(self.gato.edad, 3)
        self.assertEqual(self.gato.peso, 4.5)
        self.assertEqual(self.gato.color, "blanco")
        self.assertEqual(self.gato.energia, 60)
        self.assertEqual(self.gato.presas_cazadas, 0)

    def test_setter_peso_no_positivo_no_cambia_el_valor(self) -> None:
        with self.assertRaises(ValueError) as contexto:
            self.gato.peso = 0
        self.assertIn("peso", str(contexto.exception))
        self.assertEqual(self.gato.peso, 4.5)

    def test_setter_color_normaliza_espacios(self) -> None:
        self.gato.color = "  atigrado  "
        self.assertEqual(self.gato.color, "atigrado")

    def test_setter_color_vacio_lanza_value_error(self) -> None:
        with self.assertRaises(ValueError):
            self.gato.color = ""
        self.assertEqual(self.gato.color, "blanco")

    def test_setter_edad_negativa_no_cambia_el_valor(self) -> None:
        with self.assertRaises(ValueError):
            self.gato.edad = -1
        self.assertEqual(self.gato.edad, 3)

    def test_setter_energia_fuera_de_rango_lanza_value_error(self) -> None:
        with self.assertRaises(ValueError):
            self.gato.energia = 120
        self.assertEqual(self.gato.energia, 60)

    def test_peso_no_es_un_atributo_publico(self) -> None:
        self.assertFalse(hasattr(self.gato, "__peso"))

    def test_presas_cazadas_es_de_solo_lectura(self) -> None:
        with self.assertRaises(AttributeError):
            self.gato.presas_cazadas = 5  # type: ignore[misc]

    def test_str_incluye_nombre_y_presas(self) -> None:
        texto = str(self.gato)
        self.assertIn("Misi", texto)
        self.assertIn("blanco", texto)
        self.assertIn("presas cazadas 0", texto)

    def test_info_basica_incluye_nombre_y_edad(self) -> None:
        texto = self.gato.info_basica()
        self.assertIn("Misi", texto)
        self.assertIn("3", texto)
        self.assertIn("Gato", texto)

    def test_constructor_rechaza_peso_no_positivo(self) -> None:
        with self.assertRaises(ValueError):
            Gato("Luna", 1, -2, "negro")

    def test_nombre_se_recorta(self) -> None:
        gato = Gato("  Luna  ", 1, 3.0, "negro")
        self.assertEqual(gato.nombre, "Luna")


if __name__ == "__main__":
    unittest.main()
