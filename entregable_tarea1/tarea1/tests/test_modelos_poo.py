"""Pruebas de herencia, @property, decoradores y adaptador dict↔objeto."""

from __future__ import annotations

import unittest
from abc import ABC

import tempfile
from pathlib import Path

from datos.adaptador_poo import (
    animal_a_campos,
    registro_a_animal,
    resumen_polimorfico,
)
from datos.gestor_especies import CatalogoEspecies, reiniciar_catalogo_global
from datos.modelos import (
    AnimalRefugio,
    Conejo,
    EspeciePersonalizada,
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


def _ejemplares():
    return [
        Perro("Toby", 1, 8.3, "Negro", "Juguetón"),
        Gato("Misi", 3, 4.2, "Gris", "Tranquilo"),
        Conejo("Nube", 2, 1.5, "Blanco"),
        Loro("Kiko", 5, 0.4, "Verde"),
        Hamster("Pip", 1, 0.12, "Marrón"),
    ]


class TestHerenciaYPolimorfismo(unittest.TestCase):
    def test_animal_es_abstracto(self) -> None:
        self.assertTrue(issubclass(AnimalRefugio, ABC))
        with self.assertRaises(TypeError):
            AnimalRefugio("X", 1, 1.0, "gris")  # type: ignore[abstract]

    def test_subclases_y_sonidos(self) -> None:
        animales = _ejemplares()
        sonidos = [a.hacer_sonido() for a in animales]
        self.assertEqual(len(set(sonidos)), 5)
        self.assertIn("Guau", sonidos[0])
        self.assertIn("Miau", sonidos[1])

    def test_todas_implementan_cuidados_especificos(self) -> None:
        for animal in _ejemplares():
            texto = animal.cuidados_especificos()
            self.assertIsInstance(texto, str)
            self.assertGreater(len(texto.strip()), 20)

    def test_cuidados_distintos_por_especie(self) -> None:
        cuidados = [a.cuidados_especificos() for a in _ejemplares()]
        self.assertEqual(len(set(cuidados)), 5)

    def test_super_inicializa_campos_comunes(self) -> None:
        gato = Gato("Misi", 3, 4.2, "Gris", "Tranquilo")
        self.assertEqual(gato.especie, "Gato")
        self.assertEqual(gato.observaciones, "Tranquilo")
        self.assertEqual(gato.tipo_alimentacion(), "carnívoro")


class TestGenerarFicha(unittest.TestCase):
    def test_ficha_incluye_secciones_esperadas(self) -> None:
        perro = Perro("Toby", 1, 8.3, "Negro", "Juguetón")
        ficha = perro.generar_ficha()
        self.assertEqual(
            set(ficha),
            {"generales", "comportamiento", "alimentacion", "cuidados"},
        )
        generales = ficha["generales"]
        for trozo in (
            "Toby",
            "Perro",
            "1 años",
            "8.30 kg",
            "Negro",
            "Juguetón",
        ):
            self.assertIn(trozo, generales)

    def test_ficha_usa_metodos_polimorficos_perro(self) -> None:
        perro = Perro("Toby", 1, 8.3, "Negro")
        ficha = perro.generar_ficha()
        self.assertEqual(ficha["comportamiento"], perro.hacer_sonido())
        self.assertEqual(ficha["alimentacion"], perro.tipo_alimentacion())
        self.assertEqual(ficha["cuidados"], perro.cuidados_especificos())
        self.assertIn("Guau", ficha["comportamiento"])
        self.assertEqual(ficha["alimentacion"], "omnívoro")
        self.assertIn("paseos", ficha["cuidados"].casefold())

    def test_ficha_usa_metodos_polimorficos_gato(self) -> None:
        gato = Gato("Misi", 3, 4.2, "Gris")
        ficha = gato.generar_ficha()
        self.assertIn("Miau", ficha["comportamiento"])
        self.assertEqual(ficha["alimentacion"], "carnívoro")
        self.assertIn("arenero", ficha["cuidados"].casefold())

    def test_ficha_conejo_loro_hamster(self) -> None:
        casos = [
            (Conejo("Nube", 2, 1.5, "Blanco"), "herbívoro", "heno"),
            (Loro("Kiko", 5, 0.4, "Verde"), "granívoro", "perchas"),
            (Hamster("Pip", 1, 0.12, "Marrón"), "omnívoro", "nocturno"),
        ]
        for animal, alimentacion, pista_cuidado in casos:
            with self.subTest(especie=animal.especie):
                ficha = animal.generar_ficha()
                self.assertIn(animal.nombre, ficha["generales"])
                self.assertIn(animal.especie, ficha["generales"])
                self.assertEqual(ficha["alimentacion"], alimentacion)
                self.assertIn(pista_cuidado, ficha["cuidados"].casefold())
                self.assertEqual(ficha["comportamiento"], animal.hacer_sonido())


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


class TestEspeciePersonalizada(unittest.TestCase):
    def test_instancia_y_metodos(self) -> None:
        huron = EspeciePersonalizada(
            "Nico",
            2,
            1.2,
            "Marrón",
            "Curioso",
            nombre_especie="Hurón",
            sonido="Emite pequeños chillidos",
            alimentacion="Carnívoro",
            cuidados="Entorno seguro y supervisión",
        )
        self.assertEqual(huron.especie, "Hurón")
        self.assertIn("chillidos", huron.hacer_sonido())
        self.assertEqual(huron.tipo_alimentacion(), "Carnívoro")
        self.assertIn("seguro", huron.cuidados_especificos().casefold())
        ficha = huron.generar_ficha()
        self.assertIn("Hurón", ficha["generales"])
        self.assertIn("Nico", ficha["generales"])
        self.assertEqual(ficha["alimentacion"], "Carnívoro")
        huron.info_basica()
        self.assertEqual(huron._usos_info_basica, 1)

    def test_hereda_validacion_peso(self) -> None:
        with self.assertRaisesRegex(ValueError, "peso"):
            EspeciePersonalizada(
                "Nico",
                2,
                150,
                "Marrón",
                nombre_especie="Hurón",
                sonido="Chillido",
                alimentacion="Carnívoro",
                cuidados="Cuidado",
            )


class TestAdaptador(unittest.TestCase):
    def test_ida_y_vuelta_basica(self) -> None:
        original = _ficha()
        animal = registro_a_animal(original)
        self.assertIsInstance(animal, Perro)
        campos = animal_a_campos(animal)
        self.assertEqual(campos["especie"], "Perro")
        self.assertAlmostEqual(campos["peso"], 8.3)

    def test_registro_a_animal_genera_ficha(self) -> None:
        animal = registro_a_animal(_ficha(especie="Gato", nombre="Misi"))
        self.assertIsInstance(animal, Gato)
        ficha = animal.generar_ficha()
        self.assertIn("Misi", ficha["generales"])
        self.assertIn("Miau", ficha["comportamiento"])

    def test_resumen_polimorfico(self) -> None:
        texto = resumen_polimorfico(_ficha(especie="Gato", nombre="Misi"))
        self.assertIn("Misi", texto)
        self.assertIn("Miau", texto)
        self.assertIn("carnívoro", texto)

    def test_especie_desconocida(self) -> None:
        with self.assertRaisesRegex(ValueError, "clase POO"):
            registro_a_animal(_ficha(especie="Dragón"))

    def test_huron_personalizado(self) -> None:
        reiniciar_catalogo_global()
        with tempfile.TemporaryDirectory() as tmp:
            ruta = Path(tmp) / "especies.json"
            cat = CatalogoEspecies(ruta)
            cat.anadir(
                {
                    "nombre": "Hurón",
                    "sonido": "Emite pequeños chillidos",
                    "alimentacion": "Carnívoro",
                    "cuidados": "Entorno seguro",
                }
            )
            animal = registro_a_animal(
                _ficha(especie="Hurón", nombre="Nico", peso=1.2),
                catalogo=cat,
            )
            self.assertIsInstance(animal, EspeciePersonalizada)
            self.assertEqual(animal.especie, "Hurón")
            ficha = animal.generar_ficha()
            self.assertIn("Nico", ficha["generales"])
            self.assertIn("chillidos", ficha["comportamiento"])
            self.assertEqual(ficha["alimentacion"], "Carnívoro")
        reiniciar_catalogo_global()


if __name__ == "__main__":
    unittest.main()
