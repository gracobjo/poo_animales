"""Interfaz Tkinter para consultar y gestionar el inventario."""

from __future__ import annotations

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from typing import Any, Dict, List, Optional

from datos.adaptador_poo import resumen_polimorfico
from datos.constantes import ESPECIES
from datos.inventario import (
    actualizar_animal,
    borrar_animal,
    crear_animal,
    leer_animal,
)
from datos.ficha import asegurar_campos_clinicos
from interfaz.estilos import aplicar_tema, configurar_texto
from interfaz.ficha_clinica import DialogoFichaClinica
from interfaz.vista_foto import cargar_miniatura


class GestorAnimales:
    """Ventana principal del refugio: formulario, filtros y tabla."""

    def __init__(self, raiz: tk.Tk, inventario: Dict[int, Dict[str, Any]]) -> None:
        self.raiz = raiz
        self.inventario = inventario
        self.nombre_var = tk.StringVar()
        self.especie_var = tk.StringVar(value=ESPECIES[0])
        self.edad_var = tk.StringVar()
        self.peso_var = tk.StringVar()
        self.color_var = tk.StringVar()
        self.busqueda_var = tk.StringVar()
        self.filtro_var = tk.StringVar(value="Todas")
        self.estado_var = tk.StringVar(
            value="Selecciona un animal o completa el formulario."
        )
        self._foto_tk = None  # referencia para que el GC no borre la imagen

        self.raiz.title("Refugio Animal - Gestión de animales")
        self.raiz.geometry("1180x780")
        self.raiz.minsize(960, 660)
        aplicar_tema(self.raiz)
        self._crear_controles()
        self._actualizar_tabla()
        self._mostrar_foto_formulario(None)

    def _crear_controles(self) -> None:
        """Construye el formulario, los filtros y la tabla."""
        contenedor = ttk.Frame(self.raiz, padding=12)
        contenedor.pack(fill="both", expand=True)

        ttk.Label(
            contenedor, text="Refugio Animal", style="Titulo.TLabel"
        ).pack(anchor="w")
        ttk.Label(
            contenedor,
            text="Registro de animales del refugio (dict + capa POO)",
            style="Subtitulo.TLabel",
        ).pack(anchor="w", pady=(0, 10))

        zona_datos = ttk.Frame(contenedor)
        zona_datos.pack(fill="x", pady=(0, 10))
        zona_datos.columnconfigure(0, weight=1)

        formulario = ttk.LabelFrame(
            zona_datos, text="Datos del animal", padding=10
        )
        formulario.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
        formulario.columnconfigure(1, weight=1)
        formulario.columnconfigure(3, weight=1)

        marco_foto = ttk.LabelFrame(zona_datos, text="Foto", padding=8)
        marco_foto.grid(row=0, column=1, sticky="ns")
        self.lbl_foto = ttk.Label(
            marco_foto,
            text="Sin foto",
            width=22,
            anchor="center",
            justify="center",
        )
        self.lbl_foto.pack(fill="both", expand=True)
        ttk.Label(
            marco_foto,
            text="(Ficha clínica → Foto)",
            style="Subtitulo.TLabel",
        ).pack(anchor="center", pady=(6, 0))

        ttk.Label(formulario, text="Nombre:").grid(
            row=0, column=0, sticky="w", padx=5, pady=4
        )
        ttk.Entry(formulario, textvariable=self.nombre_var).grid(
            row=0, column=1, sticky="ew", padx=5, pady=4
        )
        ttk.Label(formulario, text="Especie:").grid(
            row=0, column=2, sticky="w", padx=5, pady=4
        )
        ttk.Combobox(
            formulario,
            textvariable=self.especie_var,
            values=ESPECIES,
            state="readonly",
        ).grid(row=0, column=3, sticky="ew", padx=5, pady=4)

        ttk.Label(formulario, text="Edad (0-30):").grid(
            row=1, column=0, sticky="w", padx=5, pady=4
        )
        ttk.Entry(formulario, textvariable=self.edad_var).grid(
            row=1, column=1, sticky="ew", padx=5, pady=4
        )
        ttk.Label(formulario, text="Peso (0.01-100 kg):").grid(
            row=1, column=2, sticky="w", padx=5, pady=4
        )
        ttk.Entry(formulario, textvariable=self.peso_var).grid(
            row=1, column=3, sticky="ew", padx=5, pady=4
        )

        ttk.Label(formulario, text="Color:").grid(
            row=2, column=0, sticky="w", padx=5, pady=4
        )
        ttk.Entry(formulario, textvariable=self.color_var).grid(
            row=2, column=1, sticky="ew", padx=5, pady=4
        )
        ttk.Label(formulario, text="Observaciones:").grid(
            row=2, column=2, sticky="nw", padx=5, pady=4
        )
        self.observaciones_text = tk.Text(formulario, height=3, width=35)
        configurar_texto(self.observaciones_text)
        self.observaciones_text.grid(
            row=2, column=3, sticky="ew", padx=5, pady=4
        )

        botones = ttk.Frame(formulario)
        botones.grid(row=3, column=0, columnspan=4, sticky="ew", pady=(8, 0))
        ttk.Button(botones, text="Crear", command=self._crear).pack(
            side="left", padx=3
        )
        ttk.Button(botones, text="Actualizar", command=self._actualizar).pack(
            side="left", padx=3
        )
        ttk.Button(botones, text="Borrar", command=self._borrar).pack(
            side="left", padx=3
        )
        ttk.Button(botones, text="Limpiar", command=self._limpiar).pack(
            side="left", padx=3
        )
        ttk.Button(
            botones, text="Exportar PDF", command=self._exportar_pdf
        ).pack(side="left", padx=3)
        ttk.Button(
            botones,
            text="Ficha clínica / adjuntos",
            command=self._abrir_ficha_clinica,
        ).pack(side="left", padx=3)

        filtros = ttk.LabelFrame(contenedor, text="Buscar y filtrar", padding=8)
        filtros.pack(fill="x", pady=(0, 8))
        ttk.Label(filtros, text="Nombre:").pack(side="left", padx=(0, 5))
        busqueda = ttk.Entry(filtros, textvariable=self.busqueda_var, width=28)
        busqueda.pack(side="left", padx=(0, 14))
        busqueda.bind("<KeyRelease>", lambda evento: self._actualizar_tabla())
        ttk.Label(filtros, text="Especie:").pack(side="left", padx=(0, 5))
        filtro = ttk.Combobox(
            filtros,
            textvariable=self.filtro_var,
            values=("Todas",) + ESPECIES,
            state="readonly",
            width=14,
        )
        filtro.pack(side="left")
        filtro.bind(
            "<<ComboboxSelected>>",
            lambda evento: self._actualizar_tabla(),
        )

        tabla_marco = ttk.Frame(contenedor)
        tabla_marco.pack(fill="both", expand=True)
        columnas = (
            "id",
            "nombre",
            "especie",
            "edad",
            "peso",
            "color",
            "observaciones",
        )
        self.tabla = ttk.Treeview(
            tabla_marco,
            columns=columnas,
            show="headings",
            selectmode="browse",
            height=10,
        )
        encabezados = {
            "id": "ID",
            "nombre": "Nombre",
            "especie": "Especie",
            "edad": "Edad",
            "peso": "Peso (kg)",
            "color": "Color",
            "observaciones": "Observaciones",
        }
        anchos = {
            "id": 45,
            "nombre": 110,
            "especie": 85,
            "edad": 55,
            "peso": 75,
            "color": 100,
            "observaciones": 300,
        }
        for columna in columnas:
            self.tabla.heading(columna, text=encabezados[columna])
            self.tabla.column(columna, width=anchos[columna], anchor="w")
        barra_vertical = ttk.Scrollbar(
            tabla_marco, orient="vertical", command=self.tabla.yview
        )
        barra_horizontal = ttk.Scrollbar(
            tabla_marco, orient="horizontal", command=self.tabla.xview
        )
        self.tabla.configure(
            yscrollcommand=barra_vertical.set,
            xscrollcommand=barra_horizontal.set,
        )
        self.tabla.grid(row=0, column=0, sticky="nsew")
        barra_vertical.grid(row=0, column=1, sticky="ns")
        barra_horizontal.grid(row=1, column=0, sticky="ew")
        tabla_marco.rowconfigure(0, weight=1)
        tabla_marco.columnconfigure(0, weight=1)
        self.tabla.bind("<<TreeviewSelect>>", self._seleccionar)

        ttk.Label(
            contenedor,
            textvariable=self.estado_var,
            style="Estado.TLabel",
        ).pack(anchor="w", pady=(8, 0))

    def _datos_del_formulario(self) -> Dict[str, Any]:
        """Lee los controles y convierte edad y peso a valores numéricos."""
        try:
            edad = int(self.edad_var.get().strip())
        except ValueError as error:
            raise ValueError(
                "La edad debe escribirse como un número entero."
            ) from error
        try:
            peso = float(self.peso_var.get().strip().replace(",", "."))
        except ValueError as error:
            raise ValueError(
                "El peso debe escribirse como un número, por ejemplo 4.5."
            ) from error

        return {
            "nombre": self.nombre_var.get(),
            "especie": self.especie_var.get(),
            "edad": edad,
            "peso": peso,
            "color": self.color_var.get(),
            "observaciones": self.observaciones_text.get("1.0", "end"),
        }

    def _id_seleccionado(self) -> Optional[int]:
        """Devuelve el ID de la fila seleccionada o muestra una advertencia."""
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showwarning(
                "Falta seleccionar",
                "Selecciona un animal de la tabla.",
            )
            return None
        return int(seleccion[0])

    def _crear(self) -> None:
        try:
            animal_id = crear_animal(
                self._datos_del_formulario(), self.inventario
            )
        except ValueError as error:
            messagebox.showerror("No se pudo crear el registro", str(error))
            return
        self._actualizar_tabla()
        self._limpiar()
        self.estado_var.set(
            f"Animal creado con el identificador {animal_id}."
        )

    def _actualizar(self) -> None:
        animal_id = self._id_seleccionado()
        if animal_id is None:
            return
        try:
            actualizar_animal(
                animal_id, self._datos_del_formulario(), self.inventario
            )
        except ValueError as error:
            messagebox.showerror(
                "No se pudo actualizar el registro", str(error)
            )
            return
        self._actualizar_tabla()
        self.estado_var.set(f"Registro {animal_id} actualizado.")

    def _borrar(self) -> None:
        animal_id = self._id_seleccionado()
        if animal_id is None:
            return
        nombre = self.inventario[animal_id]["nombre"]
        if not messagebox.askyesno(
            "Confirmar borrado", f"¿Quieres borrar a {nombre}?"
        ):
            return
        try:
            borrar_animal(animal_id, self.inventario)
        except ValueError as error:
            messagebox.showerror("No se pudo borrar el registro", str(error))
            return
        self._actualizar_tabla()
        self._limpiar()
        self.estado_var.set(f"Registro {animal_id} eliminado.")

    def _seleccionar(self, evento=None) -> None:
        seleccion = self.tabla.selection()
        if not seleccion:
            return
        animal_id = int(seleccion[0])
        registro = leer_animal(animal_id, self.inventario)
        self.nombre_var.set(registro["nombre"])
        self.especie_var.set(registro["especie"])
        self.edad_var.set(str(registro["edad"]))
        self.peso_var.set(str(registro["peso"]))
        self.color_var.set(registro["color"])
        self.observaciones_text.delete("1.0", "end")
        self.observaciones_text.insert("1.0", registro["observaciones"])
        self._mostrar_foto_formulario(registro.get("foto"))
        n_trat = len(registro.get("tratamientos", []))
        n_vac = len(registro.get("vacunaciones", []))
        n_docs = len(registro.get("documentos", []))
        foto = "sí" if registro.get("foto") else "no"
        try:
            demo_poo = resumen_polimorfico(registro)
        except ValueError:
            demo_poo = registro["especie"]
        self.estado_var.set(
            f"Registro {animal_id} | {demo_poo} | "
            f"clínica: trat. {n_trat}, vac. {n_vac}, "
            f"docs {n_docs}, foto {foto}"
        )

    def _abrir_ficha_clinica(self) -> None:
        """Abre el diálogo de tratamientos, vacunas, documentos y foto."""
        animal_id = self._id_seleccionado()
        if animal_id is None:
            return
        asegurar_campos_clinicos(self.inventario[animal_id])
        DialogoFichaClinica(
            self.raiz,
            animal_id,
            self.inventario[animal_id],
            al_guardar=lambda: self._tras_cambio_clinico(animal_id),
        )

    def _tras_cambio_clinico(self, animal_id: int) -> None:
        if animal_id in self.inventario:
            self._mostrar_foto_formulario(self.inventario[animal_id].get("foto"))
        if animal_id in self.inventario and self.tabla.selection():
            self._seleccionar()
        else:
            self.estado_var.set(
                f"Ficha clínica del registro {animal_id} actualizada."
            )

    def _mostrar_foto_formulario(self, ruta: Optional[str]) -> None:
        """Actualiza la miniatura del panel Foto del formulario principal."""
        imagen, mensaje = cargar_miniatura(ruta or "", max_lado=150)
        self._foto_tk = imagen
        if imagen is not None:
            self.lbl_foto.configure(image=imagen, text="")
        else:
            self.lbl_foto.configure(image="", text=mensaje)

    def _limpiar(self) -> None:
        self.nombre_var.set("")
        self.especie_var.set(ESPECIES[0])
        self.edad_var.set("")
        self.peso_var.set("")
        self.color_var.set("")
        self.observaciones_text.delete("1.0", "end")
        self._mostrar_foto_formulario(None)
        seleccion = self.tabla.selection()
        if seleccion:
            self.tabla.selection_remove(seleccion)

    def _ids_visibles(self) -> List[int]:
        """IDs que aparecen ahora en la tabla (respetan búsqueda y filtro)."""
        return [int(iid) for iid in self.tabla.get_children()]

    def _ids_seleccionados(self) -> List[int]:
        """IDs de las filas marcadas con el ratón o el teclado."""
        return [int(iid) for iid in self.tabla.selection()]

    def _exportar_pdf(self) -> None:
        """Exporta la selección; si no hay ninguna, los animales visibles."""
        seleccionados = self._ids_seleccionados()
        if seleccionados:
            ids = seleccionados
            ambito = "seleccionados"
        else:
            ids = self._ids_visibles()
            ambito = "visibles"
            if not ids:
                messagebox.showwarning(
                    "Nada que exportar",
                    "No hay animales visibles. Quita filtros o crea un registro.",
                )
                return
            if not messagebox.askyesno(
                "Exportar inventario visible",
                "No hay ninguna fila seleccionada.\n\n"
                f"¿Exportar las {len(ids)} ficha(s) visibles en la tabla?",
            ):
                return

        if len(ids) == 1:
            nombre = self.inventario[ids[0]]["nombre"]
            inicial = f"ficha_{ids[0]}_{nombre}.pdf"
            titulo_dialogo = "Guardar ficha en PDF"
        else:
            inicial = "fichas_animales.pdf"
            titulo_dialogo = "Guardar fichas en PDF"

        ruta = filedialog.asksaveasfilename(
            title=titulo_dialogo,
            defaultextension=".pdf",
            filetypes=[("PDF", "*.pdf"), ("Todos los archivos", "*.*")],
            initialfile=inicial,
        )
        if not ruta:
            return

        try:
            from exportacion.pdf_fichas import exportar_fichas_pdf
        except ModuleNotFoundError as error:
            messagebox.showerror(
                "Falta dependencia",
                "Para exportar PDF instala fpdf2 en el entorno:\n\n"
                "pip install fpdf2\n\n"
                f"Detalle: {error}",
            )
            return

        try:
            total = exportar_fichas_pdf(
                self.inventario,
                ruta,
                ids=ids,
                incluir_portada=len(ids) > 1,
            )
        except Exception as error:  # noqa: BLE001 — mostrar cualquier fallo al usuario
            messagebox.showerror(
                "No se pudo exportar el PDF",
                str(error),
            )
            return

        self.estado_var.set(
            f"PDF exportado ({ambito}): {total} ficha(s) → {ruta}"
        )
        messagebox.showinfo(
            "Exportación completada",
            f"Se han guardado {total} ficha(s) ({ambito}) en:\n{ruta}",
        )

    def _actualizar_tabla(self) -> None:
        """Vuelve a dibujar los registros aplicando búsqueda y filtro."""
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)

        texto = self.busqueda_var.get().strip().casefold()
        especie = self.filtro_var.get()
        visibles = 0
        for animal_id, registro in self.inventario.items():
            coincide_nombre = texto in registro["nombre"].casefold()
            coincide_especie = (
                especie == "Todas" or registro["especie"] == especie
            )
            if coincide_nombre and coincide_especie:
                self.tabla.insert(
                    "",
                    "end",
                    iid=str(animal_id),
                    values=(
                        animal_id,
                        registro["nombre"],
                        registro["especie"],
                        registro["edad"],
                        f"{registro['peso']:.2f}",
                        registro["color"],
                        registro["observaciones"],
                    ),
                )
                visibles += 1
        self.estado_var.set(
            f"Registros totales: {len(self.inventario)} | "
            f"visibles: {visibles}"
        )
