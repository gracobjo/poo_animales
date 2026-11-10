"""Pruebas del lector de portapapeles (Windows CF_HDROP / texto)."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path
from unittest.mock import patch

RAIZ_PROGRAMA = Path(__file__).resolve().parents[1]
if str(RAIZ_PROGRAMA) not in sys.path:
    sys.path.insert(0, str(RAIZ_PROGRAMA))

from interfaz.portapapeles import (  # noqa: E402
    leer_portapapeles,
    primer_archivo_valido,
)


class TestPortapapeles(unittest.TestCase):
    def test_hdrop_tiene_prioridad(self) -> None:
        with patch(
            "interfaz.portapapeles._archivos_cf_hdrop",
            return_value=[r"C:\tmp\doc.pdf"],
        ), patch(
            "interfaz.portapapeles._imagen_pillow", return_value=None
        ), patch(
            "interfaz.portapapeles._texto_tkinter", return_value=""
        ):
            tipo, dato = leer_portapapeles()
        self.assertEqual(tipo, "archivos")
        self.assertEqual(dato, [r"C:\tmp\doc.pdf"])

    def test_texto_ruta_si_existe_archivo(self) -> None:
        muestra = (
            Path(__file__).resolve().parents[1]
            / "muestras"
            / "documentos"
            / "consentimiento_adopcion_ejemplo.txt"
        )
        if not muestra.is_file():
            self.skipTest("Falta muestra txt")
        with patch(
            "interfaz.portapapeles._archivos_cf_hdrop", return_value=[]
        ), patch(
            "interfaz.portapapeles._imagen_pillow", return_value=None
        ), patch(
            "interfaz.portapapeles._texto_tkinter",
            return_value=str(muestra),
        ):
            tipo, dato = leer_portapapeles()
        self.assertEqual(tipo, "archivos")
        self.assertEqual(dato, [str(muestra)])

    def test_texto_plano(self) -> None:
        with patch(
            "interfaz.portapapeles._archivos_cf_hdrop", return_value=[]
        ), patch(
            "interfaz.portapapeles._imagen_pillow", return_value=None
        ), patch(
            "interfaz.portapapeles._texto_tkinter",
            return_value="Hola mundo",
        ):
            tipo, dato = leer_portapapeles()
        self.assertEqual(tipo, "texto")
        self.assertEqual(dato, "Hola mundo")

    def test_primer_archivo_valido(self) -> None:
        with self.assertRaises(ValueError):
            primer_archivo_valido([r"C:\no\existe.xyz"])


if __name__ == "__main__":
    unittest.main()
