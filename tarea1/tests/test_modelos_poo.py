"""Pruebas de herencia, @property, decoradores y adaptador dict↔objeto."""

from __future__ import annotations

import unittest
from abc import ABC

from datos.adaptador_poo import (
    animal_a_campos,
    registro_a_animal,
    resumen_polimorfico,
)
from datos.modelos import (
    AnimalRefugio,
    Conejo,
    Gato,
    Hamster,
    Loro,
    Perro,
)


def _ficha(**extra):
    base = {
        "nombre": "Toby",
        "especie": "Perro",
        "edad": 1,
        "peso": 8.3,
        "color": "Negro",
        "observaciones": "Juguetón",
    }
    base.update(extra)
    return base


class TestHerenciaYPolimorfismo(unittest.TestCase):
    def test_animal_es_abstracto(self) -> None:
        self.assertTrue(issubclass(AnimalRefugio, ABC))
        with self.assertRaises(TypeError):
            AnimalRefugio("X", 1, 1.0, "gris")  # type: ignore[abstract]

    def test_subclases_y_sonidos(self) -> None:
        animales = [
            Perro("Toby", 1, 8.3, "Negro"),
            Gato("Misi", 3, 4.2, "Gris"),
            Conejo("Nube", 2, 1.5, "Blanco"),
            Loro("Kiko", 5, 0.4, "Verde"),
            Hamster("Pip", 1, 0.12, "Marrón"),
        ]
        sonidos = [a.hacer_sonido() for a in animales]
        self.assertEqual(len(set(sonidos)), 5)
        self.assertIn("Guau", sonidos[0])
        self.assertIn("Miau", sonidos[1])

    def test_super_inicializa_campos_comunes(self) -> None:
        gato = Gato("Misi", 3, 4.2, "Gris", "Tranquilo")
        self.assertEqual(gato.especie, "Gato")
        self.assertEqual(gato.observaciones, "Tranquilo")
        self.assertEqual(gato.tipo_alimentacion(), "carnívoro")


class TestPropertyGettersSetters(unittest.TestCase):
    def test_setter_edad_rechaza_fuera_de_rango(self) -> None:
        perro = Perro("Toby", 1, 8.3, "Negro")
        with self.assertRaisesRegex(ValueError, "edad"):
            perro.edad = 40

    def test_setter_peso_rechaza_exceso(self) -> None:
        perro = Perro("Toby", 1, 8.3, "Negro")
        with self.assertRaisesRegex(ValueError, "peso"):
            perro.peso = 150

    def test_setter_nombre_y_color(self) -> None:
        perro = Perro("Toby", 1, 8.3, "Negro")
        perro.nombre = "  Rocky  "
        perro.color = " Marrón "
        self.assertEqual(perro.nombre, "Rocky")
        self.assertEqual(perro.color, "Marrón")
        with self.assertRaises(ValueError):
            perro.nombre = "   "


class TestDecoradorYClassmethod(unittest.TestCase):
    def test_cuenta_usos_en_info_basica(self) -> None:
        perro = Perro("Toby", 1, 8.3, "Negro")
        self.assertEqual(getattr(perro, "_usos_info_basica", 0), 0)
        perro.info_basica()
        perro.info_basica()
        self.assertEqual(perro._usos_info_basica, 2)

    def test_classmethod_campos_desde_dict(self) -> None:
        kwargs = Perro.campos_desde_dict(_ficha())
        self.assertEqual(kwargs["nombre"], "Toby")
        self.assertEqual(kwargs["edad"], 1)


class TestAdaptador(unittest.TestCase):
    def test_ida_y_vuelta_basica(self) -> None:
        original = _ficha()
        animal = registro_a_animal(original)
        self.assertIsInstance(animal, Perro)
        campos = animal_a_campos(animal)
        self.assertEqual(campos["especie"], "Perro")
        self.assertAlmostEqual(campos["peso"], 8.3)

    def test_resumen_polimorfico(self) -> None:
        texto = resumen_polimorfico(_ficha(especie="Gato", nombre="Misi"))
        self.assertIn("Misi", texto)
        self.assertIn("Miau", texto)
        self.assertIn("carnívoro", texto)

    def test_especie_desconocida(self) -> None:
        with self.assertRaisesRegex(ValueError, "clase POO"):
            registro_a_animal(_ficha(especie="Dragón"))


if __name__ == "__main__":
    unittest.main()
