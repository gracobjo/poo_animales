"""Pruebas de exportación de fichas a PDF."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

RAIZ_PROGRAMA = Path(__file__).resolve().parents[1]
if str(RAIZ_PROGRAMA) not in sys.path:
    sys.path.insert(0, str(RAIZ_PROGRAMA))

from datos.inventario import animales_iniciales  # noqa: E402
from datos.recursos import ruta_logo_refugio  # noqa: E402
from exportacion.pdf_fichas import exportar_fichas_pdf  # noqa: E402


class TestExportarFichasPdf(unittest.TestCase):
    def setUp(self) -> None:
        self.inventario = animales_iniciales()

    def test_exporta_todas_las_fichas(self) -> None:
        # Sin logo: el PDF debe seguir siendo muy ligero (fuentes estándar).
        with patch(
            "exportacion.pdf_fichas.ruta_logo_refugio", return_value=None
        ):
            with tempfile.TemporaryDirectory() as tmp:
                ruta = Path(tmp) / "fichas.pdf"
                total = exportar_fichas_pdf(self.inventario, ruta)
                self.assertEqual(total, 4)
                self.assertTrue(ruta.is_file())
                tamaño = ruta.stat().st_size
                self.assertGreater(tamaño, 500)
                self.assertLess(tamaño, 20_000)
                raw = ruta.read_bytes()
                self.assertNotIn(b"/FontFile", raw)

    def test_pdf_incluye_logo_si_existe(self) -> None:
        logo = ruta_logo_refugio()
        if logo is None:
            self.skipTest("No hay refugio.png / refugio.jpg en tarea1/ o raíz")
        with tempfile.TemporaryDirectory() as tmp:
            ruta = Path(tmp) / "con_logo.pdf"
            exportar_fichas_pdf(
                self.inventario, ruta, ids=[1], incluir_portada=True
            )
            raw = ruta.read_bytes()
            self.assertTrue(
                b"/XObject" in raw or b"/Image" in raw,
                "El PDF debería embeber el logo del refugio",
            )

    def test_exporta_solo_ids_indicados(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            ruta = Path(tmp) / "parcial.pdf"
            total = exportar_fichas_pdf(self.inventario, ruta, ids=[2, 4])
            self.assertEqual(total, 2)

    def test_inventario_vacio_falla(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            ruta = Path(tmp) / "vacio.pdf"
            with self.assertRaisesRegex(ValueError, "No hay animales"):
                exportar_fichas_pdf({}, ruta)

    def test_id_inexistente_falla(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            ruta = Path(tmp) / "malo.pdf"
            with self.assertRaisesRegex(ValueError, "No se ha encontrado"):
                exportar_fichas_pdf(self.inventario, ruta, ids=[99])

    def test_anade_extension_pdf(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            ruta = Path(tmp) / "sin_ext"
            exportar_fichas_pdf(self.inventario, ruta, ids=[1])
            self.assertTrue(ruta.with_suffix(".pdf").is_file())

    def test_pdf_incluye_imagen_si_hay_foto(self) -> None:
        muestra = (
            Path(__file__).resolve().parents[1]
            / "muestras"
            / "fotos"
            / "perro_labrador.png"
        )
        if not muestra.is_file():
            self.skipTest("Falta muestra de foto")
        self.inventario[1]["foto"] = str(muestra)
        with tempfile.TemporaryDirectory() as tmp:
            ruta = Path(tmp) / "con_foto.pdf"
            exportar_fichas_pdf(self.inventario, ruta, ids=[1], incluir_portada=False)
            raw = ruta.read_bytes()
            self.assertTrue(
                b"/XObject" in raw or b"/Image" in raw,
                "El PDF deberia embeber la foto",
            )


@unittest.skipUnless(
    __import__("tkinter", fromlist=["Tk"]),
    "Tkinter requerido",
)
class TestExportarDesdeInterfaz(unittest.TestCase):
    def setUp(self) -> None:
        import tkinter as tk

        from interfaz.gestor import GestorAnimales

        self.raiz = tk.Tk()
        self.raiz.withdraw()
        self.inventario = animales_iniciales()
        self.gestor = GestorAnimales(self.raiz, self.inventario)
        self.raiz.update_idletasks()

    def tearDown(self) -> None:
        self.raiz.destroy()

    def test_ids_visibles_respetan_filtro(self) -> None:
        self.gestor.filtro_var.set("Gato")
        self.gestor._actualizar_tabla()
        self.assertEqual(self.gestor._ids_visibles(), [2])

    @patch("interfaz.gestor.messagebox")
    @patch("interfaz.gestor.filedialog.asksaveasfilename", return_value="")
    def test_exportar_cancelado_no_escribe(self, _mock_dialog, mock_msg) -> None:
        mock_msg.askyesno.return_value = True
        self.gestor._exportar_pdf()
        mock_msg.showinfo.assert_not_called()

    @patch("interfaz.gestor.messagebox")
    @patch("interfaz.gestor.filedialog.asksaveasfilename")
    def test_exportar_sin_seleccion_pide_confirmacion(self, mock_dialog, mock_msg) -> None:
        mock_msg.askyesno.return_value = True
        with tempfile.TemporaryDirectory() as tmp:
            ruta = str(Path(tmp) / "out.pdf")
            mock_dialog.return_value = ruta
            self.gestor._exportar_pdf()
            self.assertTrue(Path(ruta).is_file())
            mock_msg.askyesno.assert_called_once()
            self.assertIn("visibles", self.gestor.estado_var.get())

    @patch("interfaz.gestor.messagebox")
    @patch("interfaz.gestor.filedialog.asksaveasfilename")
    def test_exportar_solo_fila_seleccionada(self, mock_dialog, mock_msg) -> None:
        self.gestor.tabla.selection_set("2")
        with tempfile.TemporaryDirectory() as tmp:
            ruta = str(Path(tmp) / "misi.pdf")
            mock_dialog.return_value = ruta
            self.gestor._exportar_pdf()
            self.assertTrue(Path(ruta).is_file())
            mock_msg.askyesno.assert_not_called()
            self.assertIn("seleccionados", self.gestor.estado_var.get())
            self.assertIn("1 ficha", self.gestor.estado_var.get())


if __name__ == "__main__":
    unittest.main()
