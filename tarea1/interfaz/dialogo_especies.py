"""Ventana Toplevel para gestionar especies personalizadas."""

from __future__ import annotations

import tkinter as tk
from tkinter import messagebox, ttk
from typing import Any, Callable, Dict, Optional

from datos.gestor_especies import (
    CatalogoEspecies,
    especies_usadas_en_inventario,
    get_catalogo,
)
from interfaz.estilos import aplicar_tema, configurar_texto


class DialogoGestionEspecies(tk.Toplevel):
    """Consulta nativas y CRUD de especies personalizadas."""

    def __init__(
        self,
        padre: tk.Misc,
        inventario: Dict[int, Dict[str, Any]],
        *,
        catalogo: Optional[CatalogoEspecies] = None,
        al_cambiar: Optional[Callable[[], None]] = None,
    ) -> None:
        super().__init__(padre)
        self.inventario = inventario
        self.catalogo = catalogo or get_catalogo()
        self.al_cambiar = al_cambiar
        self._nombre_seleccionado: Optional[str] = None

        self.title("Gestionar especies")
        self.geometry("720x560")
        self.minsize(640, 480)
        self.transient(padre)
        aplicar_tema(self)

        self.nombre_var = tk.StringVar()
        self.sonido_var = tk.StringVar()
        self.alimentacion_var = tk.StringVar()

        self._crear_controles()
        self._refrescar_listas()
        self.protocol("WM_DELETE_WINDOW", self.destroy)
        self.grab_set()

    def _crear_controles(self) -> None:
        contenedor = ttk.Frame(self, padding=12)
        contenedor.pack(fill="both", expand=True)

        ttk.Label(
            contenedor,
            text="Especies del refugio",
            style="Titulo.TLabel",
        ).pack(anchor="w")
        ttk.Label(
            contenedor,
            text=(
                "Las nativas usan clases POO fijas. Las personalizadas se "
                "guardan en JSON y usan EspeciePersonalizada."
            ),
            style="Subtitulo.TLabel",
            wraplength=680,
        ).pack(anchor="w", pady=(0, 8))

        listas = ttk.Frame(contenedor)
        listas.pack(fill="both", expand=True)
        listas.columnconfigure(0, weight=1)
        listas.columnconfigure(1, weight=1)
        listas.rowconfigure(0, weight=1)

        marco_nat = ttk.LabelFrame(listas, text="Nativas (solo lectura)", padding=8)
        marco_nat.grid(row=0, column=0, sticky="nsew", padx=(0, 6))
        self.lista_nativas = tk.Listbox(marco_nat, height=10, exportselection=False)
        self.lista_nativas.pack(fill="both", expand=True)

        marco_per = ttk.LabelFrame(
            listas, text="Personalizadas", padding=8
        )
        marco_per.grid(row=0, column=1, sticky="nsew", padx=(6, 0))
        self.lista_personalizadas = tk.Listbox(
            marco_per, height=10, exportselection=False
        )
        self.lista_personalizadas.pack(fill="both", expand=True)
        self.lista_personalizadas.bind("<<ListboxSelect>>", self._al_seleccionar)

        formulario = ttk.LabelFrame(
            contenedor, text="Alta / edición de especie personalizada", padding=8
        )
        formulario.pack(fill="x", pady=(10, 0))
        formulario.columnconfigure(1, weight=1)

        ttk.Label(formulario, text="Nombre:").grid(
            row=0, column=0, sticky="w", padx=4, pady=3
        )
        ttk.Entry(formulario, textvariable=self.nombre_var).grid(
            row=0, column=1, sticky="ew", padx=4, pady=3
        )
        ttk.Label(formulario, text="Sonido:").grid(
            row=1, column=0, sticky="w", padx=4, pady=3
        )
        ttk.Entry(formulario, textvariable=self.sonido_var).grid(
            row=1, column=1, sticky="ew", padx=4, pady=3
        )
        ttk.Label(formulario, text="Alimentación:").grid(
            row=2, column=0, sticky="w", padx=4, pady=3
        )
        ttk.Entry(formulario, textvariable=self.alimentacion_var).grid(
            row=2, column=1, sticky="ew", padx=4, pady=3
        )
        ttk.Label(formulario, text="Cuidados:").grid(
            row=3, column=0, sticky="nw", padx=4, pady=3
        )
        cuidados_marco = ttk.Frame(formulario)
        cuidados_marco.grid(row=3, column=1, sticky="nsew", padx=4, pady=3)
        cuidados_marco.columnconfigure(0, weight=1)
        self.cuidados_text = tk.Text(cuidados_marco, height=6, wrap="word")
        configurar_texto(self.cuidados_text)
        barra_cuidados = ttk.Scrollbar(
            cuidados_marco,
            orient="vertical",
            command=self.cuidados_text.yview,
        )
        self.cuidados_text.configure(yscrollcommand=barra_cuidados.set)
        self.cuidados_text.grid(row=0, column=0, sticky="nsew")
        barra_cuidados.grid(row=0, column=1, sticky="ns")

        botones = ttk.Frame(contenedor)
        botones.pack(fill="x", pady=(10, 0))
        ttk.Button(botones, text="Nueva", command=self._nueva).pack(
            side="left", padx=3
        )
        ttk.Button(botones, text="Guardar", command=self._guardar).pack(
            side="left", padx=3
        )
        ttk.Button(botones, text="Desactivar", command=self._desactivar).pack(
            side="left", padx=3
        )
        ttk.Button(botones, text="Activar", command=self._activar).pack(
            side="left", padx=3
        )
        ttk.Button(botones, text="Eliminar", command=self._eliminar).pack(
            side="left", padx=3
        )
        ttk.Button(botones, text="Cerrar", command=self.destroy).pack(
            side="right", padx=3
        )

    def _refrescar_listas(self) -> None:
        self.lista_nativas.delete(0, "end")
        for nombre in self.catalogo.nativas():
            self.lista_nativas.insert("end", nombre)

        self.lista_personalizadas.delete(0, "end")
        self._nombres_lista: list[str] = []
        for item in self.catalogo.personalizadas():
            estado = "activa" if item.get("activa", True) else "inactiva"
            self.lista_personalizadas.insert(
                "end", f"{item['nombre']} ({estado})"
            )
            self._nombres_lista.append(item["nombre"])

    def _datos_formulario(self) -> Dict[str, Any]:
        return {
            "nombre": self.nombre_var.get(),
            "sonido": self.sonido_var.get(),
            "alimentacion": self.alimentacion_var.get(),
            "cuidados": self.cuidados_text.get("1.0", "end"),
        }

    def _limpiar_formulario(self) -> None:
        self._nombre_seleccionado = None
        self.nombre_var.set("")
        self.sonido_var.set("")
        self.alimentacion_var.set("")
        self.cuidados_text.delete("1.0", "end")
        self.lista_personalizadas.selection_clear(0, "end")

    def _nueva(self) -> None:
        self._limpiar_formulario()

    def _al_seleccionar(self, _evento=None) -> None:
        seleccion = self.lista_personalizadas.curselection()
        if not seleccion:
            return
        nombre = self._nombres_lista[seleccion[0]]
        item = self.catalogo.obtener_personalizada(nombre)
        if item is None:
            return
        self._nombre_seleccionado = item["nombre"]
        self.nombre_var.set(item["nombre"])
        self.sonido_var.set(item["sonido"])
        self.alimentacion_var.set(item["alimentacion"])
        self.cuidados_text.delete("1.0", "end")
        self.cuidados_text.insert("1.0", item["cuidados"])

    def _notificar_cambio(self) -> None:
        if self.al_cambiar is not None:
            self.al_cambiar()

    def _guardar(self) -> None:
        datos = self._datos_formulario()
        try:
            if self._nombre_seleccionado is None:
                guardada = self.catalogo.anadir(datos)
                mensaje = f"Especie «{guardada['nombre']}» creada."
            else:
                guardada = self.catalogo.actualizar(
                    self._nombre_seleccionado, datos
                )
                mensaje = f"Especie «{guardada['nombre']}» actualizada."
        except ValueError as error:
            messagebox.showerror("No se pudo guardar", str(error), parent=self)
            return
        self._refrescar_listas()
        self._nombre_seleccionado = guardada["nombre"]
        self._notificar_cambio()
        messagebox.showinfo("Especies", mensaje, parent=self)

    def _desactivar(self) -> None:
        nombre = self._nombre_seleccionado
        if not nombre:
            messagebox.showwarning(
                "Falta seleccionar",
                "Selecciona una especie personalizada.",
                parent=self,
            )
            return
        try:
            self.catalogo.desactivar(nombre)
        except ValueError as error:
            messagebox.showerror("No se pudo desactivar", str(error), parent=self)
            return
        self._refrescar_listas()
        self._notificar_cambio()
        messagebox.showinfo(
            "Especies",
            f"«{nombre}» desactivada: no se podrá usar en altas nuevas, "
            "pero los animales existentes siguen consultables.",
            parent=self,
        )

    def _activar(self) -> None:
        nombre = self._nombre_seleccionado
        if not nombre:
            messagebox.showwarning(
                "Falta seleccionar",
                "Selecciona una especie personalizada.",
                parent=self,
            )
            return
        try:
            self.catalogo.activar(nombre)
        except ValueError as error:
            messagebox.showerror("No se pudo activar", str(error), parent=self)
            return
        self._refrescar_listas()
        self._notificar_cambio()
        messagebox.showinfo(
            "Especies", f"«{nombre}» activada de nuevo.", parent=self
        )

    def _eliminar(self) -> None:
        nombre = self._nombre_seleccionado
        if not nombre:
            messagebox.showwarning(
                "Falta seleccionar",
                "Selecciona una especie personalizada.",
                parent=self,
            )
            return
        if not messagebox.askyesno(
            "Confirmar eliminación",
            f"¿Eliminar definitivamente la especie «{nombre}»?",
            parent=self,
        ):
            return
        try:
            self.catalogo.eliminar(
                nombre,
                especies_en_uso=especies_usadas_en_inventario(self.inventario),
            )
        except ValueError as error:
            messagebox.showerror("No se pudo eliminar", str(error), parent=self)
            return
        self._limpiar_formulario()
        self._refrescar_listas()
        self._notificar_cambio()
        messagebox.showinfo(
            "Especies", f"«{nombre}» eliminada.", parent=self
        )
