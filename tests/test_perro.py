"""Pruebas unitarias de la clase Perro."""

import sys
import unittest
from pathlib import Path

# Permite ejecutar este archivo directamente, no solo como módulo.
RAIZ_PROYECTO = Path(__file__).resolve().parents[1]
if str(RAIZ_PROYECTO) not in sys.path:
    sys.path.insert(0, str(RAIZ_PROYECTO))

from src.modelos.animal import Animal  # noqa: E402
from src.modelos.perro import Perro  # noqa: E402


class TestPerro(unittest.TestCase):
    """Cubre sonido, comportamiento, propiedades y validaciones del perro."""

    def setUp(self) -> None:
        """Crea un perro nuevo antes de cada prueba."""
        self.perro = Perro("Rex", 4, 12.0, "marrón", energia=60)

    def test_es_instancia_de_animal(self) -> None:
        self.assertIsInstance(self.perro, Animal)

    def test_ladrar(self) -> None:
        self.assertEqual(self.perro.ladrar(), "Rex dice: ¡Guau!")

    def test_hacer_sonido_delega_en_ladrar(self) -> None:
        self.assertEqual(self.perro.hacer_sonido(), "Rex dice: ¡Guau!")

    def test_tipo_alimentacion(self) -> None:
        self.assertEqual(self.perro.tipo_alimentacion(), "omnívoro")

    def test_comer_aumenta_peso_y_energia(self) -> None:
        mensaje = self.perro.comer(500)
        self.assertAlmostEqual(self.perro.peso, 12.5)
        self.assertEqual(self.perro.energia, 60 + Perro.RECUPERACION_COMIDA)
        self.assertIn("Rex", mensaje)

    def test_comer_no_supera_energia_maxima(self) -> None:
        self.perro.energia = 95
        self.perro.comer(100)
        self.assertEqual(self.perro.energia, Perro.ENERGIA_MAXIMA)

    def test_comer_invalido_no_cambia_el_estado(self) -> None:
        with self.assertRaises(ValueError):
            self.perro.comer(0)
        self.assertEqual(self.perro.peso, 12.0)
        self.assertEqual(self.perro.energia, 60)

    def test_comer_negativo_lanza_value_error(self) -> None:
        with self.assertRaises(ValueError):
            self.perro.comer(-10)

    def test_jugar_reduce_energia(self) -> None:
        mensaje = self.perro.jugar()
        self.assertEqual(self.perro.energia, 60 - Perro.COSTO_ENERGIA_JUGAR)
        self.assertIn("juega", mensaje)

    def test_jugar_sin_energia_no_cambia_el_estado(self) -> None:
        cansado = Perro("Tobi", 2, 8.0, "blanco", energia=10)
        with self.assertRaises(ValueError):
            cansado.jugar()
        self.assertEqual(cansado.energia, 10)

    def test_descansar_recupera_energia(self) -> None:
        self.perro.descansar()
        self.assertEqual(self.perro.energia, 60 + Perro.RECUPERACION_DESCANSO)

    def test_descansar_no_supera_el_maximo(self) -> None:
        self.perro.energia = 90
        self.perro.descansar()
        self.assertEqual(self.perro.energia, Perro.ENERGIA_MAXIMA)

    def test_vacunar_marca_al_perro(self) -> None:
        self.assertFalse(self.perro.vacunado)
        mensaje = self.perro.vacunar()
        self.assertTrue(self.perro.vacunado)
        self.assertIn("vacunado", mensaje)

    def test_vacunar_dos_veces_lanza_value_error(self) -> None:
        self.perro.vacunar()
        with self.assertRaises(ValueError):
            self.perro.vacunar()
        self.assertTrue(self.perro.vacunado)

    def test_getters_devuelven_los_datos_iniciales(self) -> None:
        self.assertEqual(self.perro.nombre, "Rex")
        self.assertEqual(self.perro.edad, 4)
        self.assertEqual(self.perro.peso, 12.0)
        self.assertEqual(self.perro.color, "marrón")
        self.assertEqual(self.perro.energia, 60)

    def test_setter_peso_valido(self) -> None:
        self.perro.peso = 15
        self.assertEqual(self.perro.peso, 15)

    def test_setter_peso_no_positivo_no_cambia_el_valor(self) -> None:
        with self.assertRaises(ValueError) as contexto:
            self.perro.peso = -3
        self.assertIn("peso", str(contexto.exception))
        self.assertEqual(self.perro.peso, 12.0)

    def test_setter_color_normaliza_espacios(self) -> None:
        self.perro.color = "  negro  "
        self.assertEqual(self.perro.color, "negro")

    def test_setter_color_vacio_lanza_value_error(self) -> None:
        with self.assertRaises(ValueError):
            self.perro.color = "   "
        self.assertEqual(self.perro.color, "marrón")

    def test_setter_edad_acepta_los_extremos(self) -> None:
        self.perro.edad = Animal.EDAD_MINIMA
        self.assertEqual(self.perro.edad, 0)
        self.perro.edad = Animal.EDAD_MAXIMA
        self.assertEqual(self.perro.edad, 30)

    def test_setter_edad_fuera_de_rango_no_cambia_el_valor(self) -> None:
        with self.assertRaises(ValueError):
            self.perro.edad = 31
        self.assertEqual(self.perro.edad, 4)

    def test_setter_edad_no_entera_lanza_value_error(self) -> None:
        with self.assertRaises(ValueError):
            self.perro.edad = 4.5  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            self.perro.edad = True  # type: ignore[arg-type]

    def test_setter_energia_fuera_de_rango_lanza_value_error(self) -> None:
        with self.assertRaises(ValueError):
            self.perro.energia = 101
        with self.assertRaises(ValueError):
            self.perro.energia = -1
        self.assertEqual(self.perro.energia, 60)

    def test_peso_no_es_un_atributo_publico(self) -> None:
        self.assertFalse(hasattr(self.perro, "__peso"))

    def test_vacunado_es_de_solo_lectura(self) -> None:
        with self.assertRaises(AttributeError):
            self.perro.vacunado = True  # type: ignore[misc]

    def test_str_incluye_nombre_y_color(self) -> None:
        texto = str(self.perro)
        self.assertIn("Rex", texto)
        self.assertIn("marrón", texto)
        self.assertIn("sin vacunar", texto)

    def test_info_basica_incluye_nombre_y_edad(self) -> None:
        texto = self.perro.info_basica()
        self.assertIn("Rex", texto)
        self.assertIn("4", texto)
        self.assertIn("Perro", texto)

    def test_nombre_vacio_lanza_value_error(self) -> None:
        with self.assertRaises(ValueError):
            Perro("   ", 1, 5.0, "gris")

    def test_nombre_se_recorta(self) -> None:
        perro = Perro("  Luca  ", 1, 5.0, "gris")
        self.assertEqual(perro.nombre, "Luca")

    def test_animal_no_se_puede_instanciar(self) -> None:
        with self.assertRaises(TypeError):
            Animal("Fantasma", 1)


if __name__ == "__main__":
    unittest.main()
