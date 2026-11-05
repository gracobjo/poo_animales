"""Diálogo modal: tratamientos, vacunas, documentos y foto."""

from __future__ import annotations

import os
import tkinter as tk
from datetime import date
from pathlib import Path
from tkinter import filedialog, messagebox, ttk
from typing import Any, Callable, Dict, Optional

from datos.adjuntos import (
    TAMANO_MAX_MB,
    registrar_documento,
    registrar_documento_bytes,
    registrar_foto,
    registrar_foto_bytes,
)
from datos.ficha import asegurar_campos_clinicos
from interfaz.estilos import aplicar_tema
from interfaz.portapapeles import (
    imagen_a_png_bytes,
    leer_portapapeles,
    primer_archivo_valido,
)
from interfaz.vista_foto import cargar_miniatura

# Carpeta de ejemplos empaquetada con el programa (fotos / PDF / DOCX).
_CARPETA_MUESTRAS = Path(__file__).resolve().parents[1] / "muestras"
_MUESTRAS_FOTOS = _CARPETA_MUESTRAS / "fotos"
_MUESTRAS_DOCS = _CARPETA_MUESTRAS / "documentos"


class DialogoFichaClinica(tk.Toplevel):
    """Ventana para la ficha clínica y adjuntos de un animal concreto."""

    def __init__(
        self,
        padre: tk.Misc,
        animal_id: int,
        registro: Dict[str, Any],
        al_guardar: Optional[Callable[[], None]] = None,
    ) -> None:
        super().__init__(padre)
        self.animal_id = animal_id
        self.registro = asegurar_campos_clinicos(registro)
        self.al_guardar = al_guardar
        self._foto_tk = None  # evita que el GC borre la imagen

        self.title(f"Ficha clínica — {self.registro.get('nombre', '')} (ID {animal_id})")
        self.geometry("720x520")
        self.minsize(640, 440)
        self.transient(padre.winfo_toplevel())
        self.grab_set()
        aplicar_tema(self)

        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)

        self.tab_tratamientos = ttk.Frame(notebook, padding=8)
        self.tab_vacunas = ttk.Frame(notebook, padding=8)
        self.tab_documentos = ttk.Frame(notebook, padding=8)
        self.tab_foto = ttk.Frame(notebook, padding=8)
        notebook.add(self.tab_tratamientos, text="Tratamientos")
        notebook.add(self.tab_vacunas, text="Vacunaciones")
        notebook.add(self.tab_documentos, text="Documentos")
        notebook.add(self.tab_foto, text="Foto")

        self._montar_tratamientos()
        self._montar_vacunas()
        self._montar_documentos()
        self._montar_foto()

        ttk.Button(self, text="Cerrar", command=self.destroy).pack(
            anchor="e", padx=10, pady=(0, 10)
        )

    def _avisar_cambio(self) -> None:
        if self.al_guardar:
            self.al_guardar()

    # --- tratamientos ---

    def _montar_tratamientos(self) -> None:
        cols = ("fecha", "descripcion", "veterinario")
        self.tabla_trat = ttk.Treeview(
            self.tab_tratamientos, columns=cols, show="headings", height=8
        )
        for c, t, w in (
            ("fecha", "Fecha", 100),
            ("descripcion", "Descripción", 280),
            ("veterinario", "Veterinario", 140),
        ):
            self.tabla_trat.heading(c, text=t)
            self.tabla_trat.column(c, width=w)
        self.tabla_trat.pack(fill="both", expand=True)

        form = ttk.Frame(self.tab_tratamientos)
        form.pack(fill="x", pady=6)
        self.trat_fecha = tk.StringVar(value=date.today().isoformat())
        self.trat_desc = tk.StringVar()
        self.trat_vet = tk.StringVar()
        ttk.Label(form, text="Fecha:").grid(row=0, column=0, sticky="w")
        ttk.Entry(form, textvariable=self.trat_fecha, width=12).grid(
            row=0, column=1, padx=4
        )
        ttk.Label(form, text="Descripción:").grid(row=0, column=2, sticky="w")
        ttk.Entry(form, textvariable=self.trat_desc, width=28).grid(
            row=0, column=3, padx=4
        )
        ttk.Label(form, text="Veterinario:").grid(row=0, column=4, sticky="w")
        ttk.Entry(form, textvariable=self.trat_vet, width=16).grid(
            row=0, column=5, padx=4
        )

        botones = ttk.Frame(self.tab_tratamientos)
        botones.pack(fill="x")
        ttk.Button(botones, text="Añadir", command=self._add_tratamiento).pack(
            side="left", padx=3
        )
        ttk.Button(
            botones, text="Eliminar seleccionado", command=self._del_tratamiento
        ).pack(side="left", padx=3)
        self._refrescar_tratamientos()

    def _refrescar_tratamientos(self) -> None:
        self.tabla_trat.delete(*self.tabla_trat.get_children())
        for i, item in enumerate(self.registro["tratamientos"]):
            self.tabla_trat.insert(
                "",
                "end",
                iid=str(i),
                values=(item["fecha"], item["descripcion"], item["veterinario"]),
            )

    def _add_tratamiento(self) -> None:
        desc = self.trat_desc.get().strip()
        if not desc:
            messagebox.showwarning(
                "Falta descripción",
                "Indica en qué consiste el tratamiento.",
                parent=self,
            )
            return
        self.registro["tratamientos"].append(
            {
                "fecha": self.trat_fecha.get().strip(),
                "descripcion": desc,
                "veterinario": self.trat_vet.get().strip(),
            }
        )
        self.trat_desc.set("")
        self.trat_vet.set("")
        self._refrescar_tratamientos()
        self._avisar_cambio()

    def _del_tratamiento(self) -> None:
        sel = self.tabla_trat.selection()
        if not sel:
            return
        idx = int(sel[0])
        del self.registro["tratamientos"][idx]
        self._refrescar_tratamientos()
        self._avisar_cambio()

    # --- vacunas ---

    def _montar_vacunas(self) -> None:
        cols = ("fecha", "vacuna", "proxima")
        self.tabla_vac = ttk.Treeview(
            self.tab_vacunas, columns=cols, show="headings", height=8
        )
        for c, t, w in (
            ("fecha", "Fecha", 100),
            ("vacuna", "Vacuna", 280),
            ("proxima", "Próxima", 100),
        ):
            self.tabla_vac.heading(c, text=t)
            self.tabla_vac.column(c, width=w)
        self.tabla_vac.pack(fill="both", expand=True)

        form = ttk.Frame(self.tab_vacunas)
        form.pack(fill="x", pady=6)
        self.vac_fecha = tk.StringVar(value=date.today().isoformat())
        self.vac_nombre = tk.StringVar()
        self.vac_proxima = tk.StringVar()
        ttk.Label(form, text="Fecha:").grid(row=0, column=0)
        ttk.Entry(form, textvariable=self.vac_fecha, width=12).grid(
            row=0, column=1, padx=4
        )
        ttk.Label(form, text="Vacuna:").grid(row=0, column=2)
        ttk.Entry(form, textvariable=self.vac_nombre, width=28).grid(
            row=0, column=3, padx=4
        )
        ttk.Label(form, text="Próxima:").grid(row=0, column=4)
        ttk.Entry(form, textvariable=self.vac_proxima, width=12).grid(
            row=0, column=5, padx=4
        )

        botones = ttk.Frame(self.tab_vacunas)
        botones.pack(fill="x")
        ttk.Button(botones, text="Añadir", command=self._add_vacuna).pack(
            side="left", padx=3
        )
        ttk.Button(
            botones, text="Eliminar seleccionada", command=self._del_vacuna
        ).pack(side="left", padx=3)
        self._refrescar_vacunas()

    def _refrescar_vacunas(self) -> None:
        self.tabla_vac.delete(*self.tabla_vac.get_children())
        for i, item in enumerate(self.registro["vacunaciones"]):
            self.tabla_vac.insert(
                "",
                "end",
                iid=str(i),
                values=(item["fecha"], item["vacuna"], item["proxima"]),
            )

    def _add_vacuna(self) -> None:
        nombre = self.vac_nombre.get().strip()
        if not nombre:
            messagebox.showwarning(
                "Falta vacuna", "Indica el nombre de la vacuna.", parent=self
            )
            return
        self.registro["vacunaciones"].append(
            {
                "fecha": self.vac_fecha.get().strip(),
                "vacuna": nombre,
                "proxima": self.vac_proxima.get().strip(),
            }
        )
        self.vac_nombre.set("")
        self.vac_proxima.set("")
        self._refrescar_vacunas()
        self._avisar_cambio()

    def _del_vacuna(self) -> None:
        sel = self.tabla_vac.selection()
        if not sel:
            return
        del self.registro["vacunaciones"][int(sel[0])]
        self._refrescar_vacunas()
        self._avisar_cambio()

    # --- documentos ---

    def _montar_documentos(self) -> None:
        cols = ("nombre", "fecha", "ruta")
        self.tabla_docs = ttk.Treeview(
            self.tab_documentos, columns=cols, show="headings", height=8
        )
        for c, t, w in (
            ("nombre", "Nombre", 180),
            ("fecha", "Fecha", 100),
            ("ruta", "Ruta", 320),
        ):
            self.tabla_docs.heading(c, text=t)
            self.tabla_docs.column(c, width=w)
        self.tabla_docs.pack(fill="both", expand=True)

        botones = ttk.Frame(self.tab_documentos)
        botones.pack(fill="x", pady=6)
        ttk.Button(
            botones, text="Importar documento...", command=self._importar_doc
        ).pack(side="left", padx=3)
        ttk.Button(
            botones, text="Pegar", command=self._pegar_doc
        ).pack(side="left", padx=3)
        ttk.Button(
            botones, text="Abrir seleccionado", command=self._abrir_doc
        ).pack(side="left", padx=3)
        ttk.Button(
            botones, text="Eliminar seleccionado", command=self._del_doc
        ).pack(side="left", padx=3)
        ttk.Label(
            self.tab_documentos,
            text=f"Máximo {TAMANO_MAX_MB} MB por archivo. Atajo: Ctrl+V",
            style="Subtitulo.TLabel",
        ).pack(anchor="w", pady=(4, 0))
        self.tab_documentos.bind("<Control-v>", lambda e: self._pegar_doc())
        self.tabla_docs.bind("<Control-v>", lambda e: self._pegar_doc())
        self._refrescar_docs()

    def _refrescar_docs(self) -> None:
        self.tabla_docs.delete(*self.tabla_docs.get_children())
        for i, item in enumerate(self.registro["documentos"]):
            self.tabla_docs.insert(
                "",
                "end",
                iid=str(i),
                values=(item["nombre"], item["fecha"], item["ruta"]),
            )

    def _importar_doc(self) -> None:
        inicial = (
            str(_MUESTRAS_DOCS) if _MUESTRAS_DOCS.is_dir() else None
        )
        ruta = filedialog.askopenfilename(
            parent=self,
            title="Importar documentación",
            initialdir=inicial,
            filetypes=[
                ("PDF / Word / texto", "*.pdf;*.docx;*.doc;*.txt"),
                ("Imágenes escaneadas", "*.png;*.jpg;*.jpeg"),
                ("Todos", "*.*"),
            ],
        )
        if not ruta:
            return
        try:
            entrada = registrar_documento(self.animal_id, ruta)
        except ValueError as error:
            messagebox.showerror("No se pudo importar", str(error), parent=self)
            return
        self.registro["documentos"].append(entrada)
        self._refrescar_docs()
        self._avisar_cambio()

    def _pegar_doc(self, evento=None) -> None:
        """Pega un archivo, texto o imagen del portapapeles como documento."""
        try:
            tipo, dato = leer_portapapeles()
            if tipo == "vacio":
                raise ValueError(
                    "No se detectó nada usable en el portapapeles.\n\n"
                    "Prueba una de estas opciones:\n"
                    "• En el Explorador: clic derecho en el archivo → Copiar\n"
                    "  (no copies solo el nombre desde el editor)\n"
                    "• O usa «Importar documento...»"
                )
            if tipo == "archivos":
                path = primer_archivo_valido(dato)  # type: ignore[arg-type]
                entrada = registrar_documento(self.animal_id, str(path))
            elif tipo == "texto":
                contenido = str(dato).encode("utf-8")
                nombre = f"pegado_{date.today().isoformat()}.txt"
                entrada = registrar_documento_bytes(
                    self.animal_id, contenido, nombre
                )
            else:
                png = imagen_a_png_bytes(dato)
                nombre = f"pegado_{date.today().isoformat()}.png"
                entrada = registrar_documento_bytes(
                    self.animal_id, png, nombre
                )
        except (ValueError, OSError) as error:
            messagebox.showerror("No se pudo pegar", str(error), parent=self)
            return
        self.registro["documentos"].append(entrada)
        self._refrescar_docs()
        self._avisar_cambio()
        messagebox.showinfo(
            "Documento pegado",
            f"Se ha añadido: {entrada['nombre']}",
            parent=self,
        )

    def _abrir_doc(self) -> None:
        sel = self.tabla_docs.selection()
        if not sel:
            return
        ruta = self.registro["documentos"][int(sel[0])]["ruta"]
        if not Path(ruta).is_file():
            messagebox.showerror(
                "Archivo no encontrado",
                f"No existe:\n{ruta}",
                parent=self,
            )
            return
        os.startfile(ruta)  # type: ignore[attr-defined]

    def _del_doc(self) -> None:
        sel = self.tabla_docs.selection()
        if not sel:
            return
        del self.registro["documentos"][int(sel[0])]
        self._refrescar_docs()
        self._avisar_cambio()

    # --- foto ---

    def _montar_foto(self) -> None:
        self.lbl_foto = ttk.Label(
            self.tab_foto,
            text="Sin foto asignada.",
            anchor="center",
        )
        self.lbl_foto.pack(fill="both", expand=True, pady=8)
        botones = ttk.Frame(self.tab_foto)
        botones.pack(fill="x")
        ttk.Button(
            botones, text="Elegir / importar foto...", command=self._importar_foto
        ).pack(side="left", padx=3)
        ttk.Button(botones, text="Pegar", command=self._pegar_foto).pack(
            side="left", padx=3
        )
        ttk.Button(botones, text="Quitar foto", command=self._quitar_foto).pack(
            side="left", padx=3
        )
        ttk.Label(
            self.tab_foto,
            text=f"Máximo {TAMANO_MAX_MB} MB. Atajo: Ctrl+V",
            style="Subtitulo.TLabel",
        ).pack(anchor="w", pady=(6, 0))
        self.tab_foto.bind("<Control-v>", lambda e: self._pegar_foto())
        self.lbl_foto.bind("<Control-v>", lambda e: self._pegar_foto())
        self._mostrar_foto()

    def _mostrar_foto(self) -> None:
        ruta = self.registro.get("foto") or ""
        imagen, mensaje = cargar_miniatura(ruta, max_lado=360)
        self._foto_tk = imagen
        if imagen is not None:
            self.lbl_foto.configure(image=imagen, text="")
        else:
            texto = mensaje if mensaje != "Sin foto" else "Sin foto asignada."
            self.lbl_foto.configure(image="", text=texto)

    def _importar_foto(self) -> None:
        inicial = (
            str(_MUESTRAS_FOTOS) if _MUESTRAS_FOTOS.is_dir() else None
        )
        ruta = filedialog.askopenfilename(
            parent=self,
            title="Seleccionar foto",
            initialdir=inicial,
            filetypes=[
                ("Imágenes", "*.png;*.gif;*.jpg;*.jpeg;*.webp"),
                ("Todos", "*.*"),
            ],
        )
        if not ruta:
            return
        try:
            guardada = registrar_foto(self.animal_id, ruta)
        except ValueError as error:
            messagebox.showerror("No se pudo importar", str(error), parent=self)
            return
        self.registro["foto"] = guardada
        self._mostrar_foto()
        self._avisar_cambio()

    def _pegar_foto(self, evento=None) -> None:
        """Pega una imagen o un archivo de imagen del portapapeles como foto."""
        try:
            tipo, dato = leer_portapapeles()
            if tipo == "vacio":
                raise ValueError(
                    "No se detectó una imagen en el portapapeles.\n\n"
                    "Copia un archivo de imagen en el Explorador "
                    "o usa «Copiar imagen» / una captura."
                )
            if tipo == "texto":
                raise ValueError(
                    "El portapapeles tiene texto, no una imagen.\n"
                    "Copia un PNG/JPG desde el Explorador o una captura."
                )
            if tipo == "archivos":
                path = primer_archivo_valido(dato, para_foto=True)  # type: ignore[arg-type]
                guardada = registrar_foto(self.animal_id, str(path))
            else:
                png = imagen_a_png_bytes(dato)
                guardada = registrar_foto_bytes(self.animal_id, png, ".png")
        except (ValueError, OSError) as error:
            messagebox.showerror("No se pudo pegar", str(error), parent=self)
            return
        self.registro["foto"] = guardada
        self._mostrar_foto()
        self._avisar_cambio()

    def _quitar_foto(self) -> None:
        self.registro["foto"] = ""
        self._mostrar_foto()
        self._avisar_cambio()
