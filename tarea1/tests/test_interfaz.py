"""Casos de prueba de la interfaz gráfica (GestorAnimales / Tkinter).

Se evita mostrar la ventana (`withdraw`) y se simulan los diálogos
(`messagebox`) para que las pruebas no queden bloqueadas.
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path
from unittest.mock import patch

RAIZ_PROGRAMA = Path(__file__).resolve().parents[1]
if str(RAIZ_PROGRAMA) not in sys.path:
    sys.path.insert(0, str(RAIZ_PROGRAMA))

import tkinter as tk  # noqa: E402
import tkinter.font as tkfont  # noqa: E402

from datos.inventario import animales_iniciales  # noqa: E402
from interfaz.estilos import FUENTE_ENTRADA  # noqa: E402
from interfaz.gestor import GestorAnimales  # noqa: E402


def _tk_disponible() -> bool:
    try:
        raiz = tk.Tk()
        raiz.destroy()
        return True
    except tk.TclError:
        return False


@unittest.skipUnless(_tk_disponible(), "Tkinter no disponible en este entorno")
class TestGestorAnimales(unittest.TestCase):
    """Cubre formulario, tabla, CRUD, filtros y diálogos de la GUI."""

    def setUp(self) -> None:
        self.raiz = tk.Tk()
        self.raiz.withdraw()
        self.inventario = animales_iniciales()
        self.gestor = GestorAnimales(self.raiz, self.inventario)
        self.raiz.update_idletasks()

    def tearDown(self) -> None:
        self.raiz.destroy()

    def _rellenar_formulario(
        self,
        *,
        nombre: str = "Nube",
        especie: str = "Gato",
        edad: str = "2",
        peso: str = "3.8",
        color: str = "Gris",
        observaciones: str = "Prueba GUI",
    ) -> None:
        self.gestor.nombre_var.set(nombre)
        self.gestor.especie_var.set(especie)
        self.gestor.edad_var.set(edad)
        self.gestor.peso_var.set(peso)
        self.gestor.color_var.set(color)
        self.gestor.observaciones_text.delete("1.0", "end")
        self.gestor.observaciones_text.insert("1.0", observaciones)

    def _filas_tabla(self) -> list:
        return list(self.gestor.tabla.get_children())

    def _valores_fila(self, iid: str) -> tuple:
        return self.gestor.tabla.item(iid, "values")

    # --- arranque e inventario inicial ---

    def test_titulo_ventana(self) -> None:
        self.assertIn("Refugio Animal", self.raiz.title())

    def test_logo_cabecera_si_existe_recurso(self) -> None:
        from datos.recursos import ruta_logo_refugio

        logo = ruta_logo_refugio()
        if logo is None:
            self.skipTest("No hay refugio.png / refugio.jpg")
        self.assertIsNotNone(self.gestor._logo_tk)

    def test_desplegable_incluye_especies_del_catalogo(self) -> None:
        valores = self.gestor.combo_especie.cget("values")
        self.assertIn("Perro", valores)
        self.assertIn("Gato", valores)

    def test_abrir_gestion_especies_crea_toplevel(self) -> None:
        dialogo = None
        try:
            self.gestor._abrir_gestion_especies()
            hijos = [
                w
                for w in self.raiz.winfo_children()
                if w.winfo_class() == "Toplevel"
                or w.__class__.__name__ == "DialogoGestionEspecies"
            ]
            self.assertTrue(hijos)
            dialogo = hijos[-1]
            self.assertIn("especies", str(dialogo.title()).casefold())
        finally:
            if dialogo is not None:
                dialogo.destroy()

    def test_observaciones_usa_fuente_de_la_guia(self) -> None:
        """El Text no debe quedarse con la monoespaciada por defecto."""
        real = tkfont.Font(font=self.gestor.observaciones_text.cget("font"))
        self.assertEqual(real.actual("family"), FUENTE_ENTRADA[0])
        self.assertEqual(real.actual("size"), FUENTE_ENTRADA[1])
        self.assertNotIn(
            real.actual("family").casefold(),
            {"courier", "courier new", "consolas", "fixedsys"},
        )

    def test_seleccionar_muestra_foto_en_formulario(self) -> None:
        from pathlib import Path

        muestra = (
            Path(__file__).resolve().parents[1]
            / "muestras"
            / "fotos"
            / "gato_atigrado.png"
        )
        if not muestra.is_file():
            self.skipTest("Falta muestra de foto")
        self.inventario[2]["foto"] = str(muestra)
        self.gestor.tabla.selection_set("2")
        self.gestor._seleccionar()
        self.assertIsNotNone(self.gestor._foto_tk)
        self.assertEqual(self.gestor.lbl_foto.cget("text"), "")

    def test_limpiar_quita_foto_del_formulario(self) -> None:
        from pathlib import Path

        muestra = (
            Path(__file__).resolve().parents[1]
            / "muestras"
            / "fotos"
            / "loro_verde.png"
        )
        if not muestra.is_file():
            self.skipTest("Falta muestra de foto")
        self.inventario[3]["foto"] = str(muestra)
        self.gestor.tabla.selection_set("3")
        self.gestor._seleccionar()
        self.gestor._limpiar()
        self.assertIsNone(self.gestor._foto_tk)
        self.assertIn("Sin foto", self.gestor.lbl_foto.cget("text"))

    def test_tabla_carga_inventario_inicial(self) -> None:
        self.assertEqual(len(self._filas_tabla()), 4)
        self.assertIn("1", self._filas_tabla())
        self.assertEqual(self._valores_fila("1")[1], "Luna")

    def test_estado_inicial_muestra_conteos(self) -> None:
        estado = self.gestor.estado_var.get()
        self.assertIn("Registros totales: 4", estado)
        self.assertIn("visibles: 4", estado)

    # --- lectura del formulario ---

    def test_datos_del_formulario_convierte_edad_y_peso(self) -> None:
        self._rellenar_formulario(edad="5", peso="4,5")
        datos = self.gestor._datos_del_formulario()
        self.assertEqual(datos["edad"], 5)
        self.assertAlmostEqual(datos["peso"], 4.5)
        self.assertEqual(datos["nombre"], "Nube")

    def test_datos_del_formulario_edad_invalida(self) -> None:
        self._rellenar_formulario(edad="dos")
        with self.assertRaisesRegex(ValueError, "edad"):
            self.gestor._datos_del_formulario()

    def test_datos_del_formulario_peso_invalido(self) -> None:
        self._rellenar_formulario(peso="xxx")
        with self.assertRaisesRegex(ValueError, "peso"):
            self.gestor._datos_del_formulario()

    # --- limpiar ---

    def test_limpiar_vacia_formulario(self) -> None:
        self._rellenar_formulario()
        self.gestor.tabla.selection_set("1")
        self.gestor._limpiar()
        self.assertEqual(self.gestor.nombre_var.get(), "")
        self.assertEqual(self.gestor.edad_var.get(), "")
        self.assertEqual(self.gestor.peso_var.get(), "")
        self.assertEqual(self.gestor.color_var.get(), "")
        self.assertEqual(
            self.gestor.observaciones_text.get("1.0", "end-1c"), ""
        )
        self.assertEqual(self.gestor.tabla.selection(), ())

    # --- selección ---

    def test_seleccionar_carga_formulario(self) -> None:
        self.gestor.tabla.selection_set("2")
        self.gestor._seleccionar()
        self.assertEqual(self.gestor.nombre_var.get(), "Misi")
        self.assertEqual(self.gestor.especie_var.get(), "Gato")
        self.assertEqual(self.gestor.edad_var.get(), "3")
        self.assertEqual(self.gestor.peso_var.get(), "4.2")
        self.assertEqual(self.gestor.color_var.get(), "Blanco y gris")
        self.assertIn(
            "familia",
            self.gestor.observaciones_text.get("1.0", "end-1c"),
        )
        self.assertIn("2", self.gestor.estado_var.get())

    def test_ficha_poo_vacia_al_inicio(self) -> None:
        self.assertIn(
            "Selecciona un animal",
            self.gestor.ficha_aviso_var.get(),
        )
        self.assertEqual(
            self.gestor._leer_texto_ficha(self.gestor.lbl_ficha_generales), ""
        )

    def test_seleccionar_actualiza_ficha_poo(self) -> None:
        self.gestor.tabla.selection_set("2")
        self.gestor._seleccionar()
        generales = self.gestor._leer_texto_ficha(self.gestor.lbl_ficha_generales)
        self.assertIn("Misi", generales)
        self.assertIn("Gato", generales)
        self.assertIn(
            "Miau",
            self.gestor._leer_texto_ficha(self.gestor.txt_ficha_comportamiento),
        )
        self.assertEqual(
            self.gestor._leer_texto_ficha(self.gestor.txt_ficha_alimentacion),
            "carnívoro",
        )
        self.assertIn(
            "arenero",
            self.gestor._leer_texto_ficha(self.gestor.txt_ficha_cuidados).casefold(),
        )

    def test_seleccionar_otro_animal_cambia_ficha_poo(self) -> None:
        self.gestor.tabla.selection_set("2")
        self.gestor._seleccionar()
        self.assertIn(
            "Miau",
            self.gestor._leer_texto_ficha(self.gestor.txt_ficha_comportamiento),
        )

        self.gestor.tabla.selection_set("1")
        self.gestor._seleccionar()
        self.assertIn(
            "Guau",
            self.gestor._leer_texto_ficha(self.gestor.txt_ficha_comportamiento),
        )
        self.assertIn(
            "Luna",
            self.gestor._leer_texto_ficha(self.gestor.lbl_ficha_generales),
        )
        self.assertIn(
            "paseos",
            self.gestor._leer_texto_ficha(self.gestor.txt_ficha_cuidados).casefold(),
        )

    def test_limpiar_restaura_ficha_poo_vacia(self) -> None:
        self.gestor.tabla.selection_set("1")
        self.gestor._seleccionar()
        self.gestor._limpiar()
        self.assertIn(
            "Selecciona un animal",
            self.gestor.ficha_aviso_var.get(),
        )
        self.assertEqual(
            self.gestor._leer_texto_ficha(self.gestor.lbl_ficha_generales), ""
        )

    def test_secciones_ficha_con_scrollbar(self) -> None:
        for widget in (
            self.gestor.txt_ficha_comportamiento,
            self.gestor.txt_ficha_alimentacion,
            self.gestor.txt_ficha_cuidados,
        ):
            with self.subTest(widget=str(widget)):
                self.assertIsInstance(widget, tk.Text)
                self.assertTrue(str(widget.cget("yscrollcommand")))

    def test_ficha_poo_error_especie_desconocida(self) -> None:
        self.inventario[99] = {
            "nombre": "Dragón",
            "especie": "Dragón",
            "edad": 1,
            "peso": 1.0,
            "color": "Rojo",
            "observaciones": "",
            "tratamientos": [],
            "vacunaciones": [],
            "documentos": [],
            "foto": None,
        }
        self.gestor._actualizar_tabla()
        self.gestor.tabla.selection_set("99")
        self.gestor._seleccionar()
        self.assertIn(
            "No se pudo generar la ficha POO",
            self.gestor.ficha_aviso_var.get(),
        )

    # --- crear ---

    @patch("interfaz.gestor.messagebox")
    def test_crear_animal_valido(self, mock_msg) -> None:
        self._rellenar_formulario()
        self.gestor._crear()
        self.assertIn(5, self.inventario)
        self.assertEqual(self.inventario[5]["nombre"], "Nube")
        self.assertIn("5", self._filas_tabla())
        self.assertIn("creado", self.gestor.estado_var.get().lower())
        self.assertEqual(self.gestor.nombre_var.get(), "")
        mock_msg.showerror.assert_not_called()

    @patch("interfaz.gestor.messagebox")
    def test_crear_muestra_error_si_faltan_datos(self, mock_msg) -> None:
        self._rellenar_formulario(nombre="", color="")
        self.gestor._crear()
        mock_msg.showerror.assert_called_once()
        self.assertNotIn(5, self.inventario)
        self.assertEqual(len(self._filas_tabla()), 4)

    # --- actualizar ---

    @patch("interfaz.gestor.messagebox")
    def test_actualizar_sin_seleccion_advierte(self, mock_msg) -> None:
        self._rellenar_formulario()
        self.gestor._actualizar()
        mock_msg.showwarning.assert_called_once()
        mock_msg.showerror.assert_not_called()

    @patch("interfaz.gestor.messagebox")
    def test_actualizar_registro_seleccionado(self, mock_msg) -> None:
        self.gestor.tabla.selection_set("1")
        self.gestor._seleccionar()
        self.gestor.edad_var.set("6")
        self.gestor.color_var.set("Dorado")
        self.gestor._actualizar()
        self.assertEqual(self.inventario[1]["edad"], 6)
        self.assertEqual(self.inventario[1]["color"], "Dorado")
        self.assertEqual(self._valores_fila("1")[3], "6")
        self.assertIn("actualizado", self.gestor.estado_var.get().lower())
        mock_msg.showerror.assert_not_called()

    @patch("interfaz.gestor.messagebox")
    def test_actualizar_con_datos_invalidos(self, mock_msg) -> None:
        self.gestor.tabla.selection_set("1")
        self.gestor._seleccionar()
        self.gestor.nombre_var.set("")
        self.gestor._actualizar()
        mock_msg.showerror.assert_called_once()
        self.assertEqual(self.inventario[1]["nombre"], "Luna")

    # --- borrar ---

    @patch("interfaz.gestor.messagebox")
    def test_borrar_sin_seleccion_advierte(self, mock_msg) -> None:
        self.gestor._borrar()
        mock_msg.showwarning.assert_called_once()
        self.assertEqual(len(self.inventario), 4)

    @patch("interfaz.gestor.messagebox")
    def test_borrar_cancelado_no_elimina(self, mock_msg) -> None:
        mock_msg.askyesno.return_value = False
        self.gestor.tabla.selection_set("3")
        self.gestor._borrar()
        mock_msg.askyesno.assert_called_once()
        self.assertIn(3, self.inventario)
        self.assertIn("3", self._filas_tabla())

    @patch("interfaz.gestor.messagebox")
    def test_borrar_confirmado_elimina(self, mock_msg) -> None:
        mock_msg.askyesno.return_value = True
        self.gestor.tabla.selection_set("3")
        self.gestor._borrar()
        self.assertNotIn(3, self.inventario)
        self.assertNotIn("3", self._filas_tabla())
        self.assertIn("eliminado", self.gestor.estado_var.get().lower())
        self.assertEqual(self.gestor.nombre_var.get(), "")

    # --- filtros y búsqueda ---

    def test_filtro_por_especie(self) -> None:
        self.gestor.filtro_var.set("Perro")
        self.gestor._actualizar_tabla()
        ids = self._filas_tabla()
        self.assertEqual(set(ids), {"1", "4"})
        self.assertIn("visibles: 2", self.gestor.estado_var.get())

    def test_busqueda_por_nombre(self) -> None:
        self.gestor.busqueda_var.set("ki")
        self.gestor._actualizar_tabla()
        ids = self._filas_tabla()
        self.assertEqual(ids, ["3"])
        self.assertEqual(self._valores_fila("3")[1], "Kiko")

    def test_busqueda_y_filtro_combinados(self) -> None:
        self.gestor.filtro_var.set("Perro")
        self.gestor.busqueda_var.set("to")
        self.gestor._actualizar_tabla()
        self.assertEqual(self._filas_tabla(), ["4"])

    def test_filtro_sin_coincidencias(self) -> None:
        self.gestor.busqueda_var.set("zzzz")
        self.gestor._actualizar_tabla()
        self.assertEqual(self._filas_tabla(), [])
        self.assertIn("visibles: 0", self.gestor.estado_var.get())

    def test_filtro_todas_restaura_lista(self) -> None:
        self.gestor.filtro_var.set("Gato")
        self.gestor._actualizar_tabla()
        self.gestor.filtro_var.set("Todas")
        self.gestor.busqueda_var.set("")
        self.gestor._actualizar_tabla()
        self.assertEqual(len(self._filas_tabla()), 4)


if __name__ == "__main__":
    unittest.main()
