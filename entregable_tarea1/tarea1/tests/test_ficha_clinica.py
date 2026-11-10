"""Pruebas de ficha clinica, adjuntos y preservacion en el CRUD."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

RAIZ_PROGRAMA = Path(__file__).resolve().parents[1]
if str(RAIZ_PROGRAMA) not in sys.path:
    sys.path.insert(0, str(RAIZ_PROGRAMA))

from datos.adjuntos import (  # noqa: E402
    TAMANO_MAX_BYTES,
    registrar_documento,
    registrar_foto,
    registrar_foto_bytes,
)
from datos.inventario import (  # noqa: E402
    actualizar_animal,
    animales_iniciales,
    crear_animal,
    leer_animal,
)
from validaciones.reglas import validar_datos  # noqa: E402


class TestCamposClinicos(unittest.TestCase):
    def test_ejemplo_incluye_vacunas_luna(self) -> None:
        inv = animales_iniciales()
        self.assertTrue(inv[1]["vacunaciones"])
        self.assertEqual(inv[1]["vacunaciones"][0]["vacuna"], "Rabia")

    def test_crear_incluye_listas_vacias(self) -> None:
        inv: dict = {}
        nuevo = crear_animal(
            {
                "nombre": "Nube",
                "especie": "Gato",
                "edad": 2,
                "peso": 3.5,
                "color": "Gris",
                "observaciones": "",
            },
            inv,
        )
        reg = inv[nuevo]
        self.assertEqual(reg["foto"], "")
        self.assertEqual(reg["tratamientos"], [])
        self.assertEqual(reg["vacunaciones"], [])
        self.assertEqual(reg["documentos"], [])

    def test_actualizar_preserva_clinica_si_no_viene_en_formulario(self) -> None:
        inv = animales_iniciales()
        actualizar_animal(
            1,
            {
                "nombre": "Luna",
                "especie": "Perro",
                "edad": 5,
                "peso": 19.0,
                "color": "Canela",
                "observaciones": "Ok",
            },
            inv,
        )
        self.assertEqual(inv[1]["edad"], 5)
        self.assertTrue(inv[1]["vacunaciones"])
        self.assertTrue(inv[1]["tratamientos"])

    def test_validar_tratamiento_sin_descripcion(self) -> None:
        with self.assertRaisesRegex(ValueError, "descripci"):
            validar_datos(
                {
                    "nombre": "A",
                    "especie": "Perro",
                    "edad": 1,
                    "peso": 2,
                    "color": "N",
                    "observaciones": "",
                    "tratamientos": [{"fecha": "2026-01-01", "descripcion": ""}],
                }
            )


class TestAdjuntos(unittest.TestCase):
    def test_importar_documento_y_foto(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            origen_doc = Path(tmp) / "analisis.txt"
            origen_doc.write_text("ok", encoding="utf-8")
            origen_foto = Path(tmp) / "foto.png"
            # PNG minimo 1x1
            origen_foto.write_bytes(
                b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01"
                b"\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00"
                b"\x00\x0cIDATx\x9cc\xf8\x0f\x00\x00\x01\x01\x00\x05"
                b"\x18\xd8N\x00\x00\x00\x00IEND\xaeB`\x82"
            )
            with patch("datos.adjuntos.RAIZ_ADJUNTOS", Path(tmp) / "adj"):
                doc = registrar_documento(99, str(origen_doc))
                foto = registrar_foto(99, str(origen_foto))
            self.assertTrue(Path(doc["ruta"]).is_file())
            self.assertTrue(Path(foto).is_file())
            self.assertEqual(doc["nombre"], "analisis.txt")

    def test_rechaza_archivo_mayor_de_5_mb(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            grande = Path(tmp) / "grande.bin"
            # Crear fichero justo por encima del límite sin llenar RAM de más
            with grande.open("wb") as fh:
                fh.truncate(TAMANO_MAX_BYTES + 1)
            with patch("datos.adjuntos.RAIZ_ADJUNTOS", Path(tmp) / "adj"):
                with self.assertRaisesRegex(ValueError, "5 MB"):
                    registrar_documento(1, str(grande))

    def test_guardar_bytes_foto_respeta_limite(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            with patch("datos.adjuntos.RAIZ_ADJUNTOS", Path(tmp) / "adj"):
                with self.assertRaisesRegex(ValueError, "5 MB"):
                    registrar_foto_bytes(
                        1, b"x" * (TAMANO_MAX_BYTES + 10), ".png"
                    )


@unittest.skipUnless(
    __import__("tkinter", fromlist=["Tk"]),
    "Tkinter requerido",
)
class TestBotonFichaClinica(unittest.TestCase):
    def setUp(self) -> None:
        import tkinter as tk

        from interfaz.gestor import GestorAnimales

        self.raiz = tk.Tk()
        self.raiz.withdraw()
        self.inventario = animales_iniciales()
        self.gestor = GestorAnimales(
            self.raiz, self.inventario, persistir=False
        )
        self.raiz.update_idletasks()

    def tearDown(self) -> None:
        self.raiz.destroy()

    @patch("interfaz.gestor.DialogoFichaClinica")
    @patch("interfaz.gestor.messagebox")
    def test_abre_dialogo_con_seleccion(self, _msg, mock_dialog) -> None:
        self.gestor.tabla.selection_set("1")
        self.gestor._abrir_ficha_clinica()
        mock_dialog.assert_called_once()
        args, kwargs = mock_dialog.call_args
        self.assertEqual(args[1], 1)

    @patch("interfaz.gestor.messagebox")
    def test_sin_seleccion_advierte(self, mock_msg) -> None:
        self.gestor._abrir_ficha_clinica()
        mock_msg.showwarning.assert_called_once()


if __name__ == "__main__":
    unittest.main()
