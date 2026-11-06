"""Genera un PDF ligero con una ficha por animal (fpdf2).

Usa fuentes PDF estándar (Helvetica): no embebe TTF, así el archivo
pesa poco y los visores lo abren al instante. Si hay foto en la ficha,
se inserta una miniatura (PNG/JPG) en la esquina superior derecha.
"""

from __future__ import annotations

import os
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable, Mapping, Optional, Sequence, Tuple, Union

from fpdf import FPDF

from datos.recursos import ruta_logo_refugio

Inventario = Mapping[int, Mapping[str, Any]]
Ruta = Union[str, Path]

_REEMPLAZOS = str.maketrans(
    {
        "—": "-",
        "–": "-",
        "…": "...",
        "“": '"',
        "”": '"',
        "‘": "'",
        "’": "'",
        "€": "EUR",
        "\xa0": " ",
    }
)


def _texto_pdf(valor: Any) -> str:
    """Prepara un texto compatible con Helvetica (latin-1)."""
    texto = str(valor).translate(_REEMPLAZOS)
    return texto.encode("latin-1", errors="replace").decode("latin-1")


class PdfFichas(FPDF):
    """PDF de fichas del refugio con pie de página simple."""

    def __init__(self) -> None:
        super().__init__(orientation="P", unit="mm", format="A4")
        self.set_compression(True)
        self.set_auto_page_break(auto=True, margin=18)
        # Evitar OpenAction /FitH (por defecto en fpdf2): en Edge, Chrome y
        # el visor de Cursor puede hacer que el PDF tarde mucho en abrirse.
        self.set_display_mode(zoom=100, layout="single")

    def footer(self) -> None:
        self.set_y(-15)
        self.set_font("Helvetica", size=8)
        self.set_text_color(120, 120, 120)
        self.cell(0, 10, _texto_pdf(f"Página {self.page_no()}"), align="C")


def _campo(
    pdf: PdfFichas,
    etiqueta: str,
    valor: str,
    ancho_etiq: float = 40,
    ancho_valor: float = 95,
) -> None:
    pdf.set_x(25)
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(40, 60, 90)
    pdf.cell(ancho_etiq, 8, _texto_pdf(etiqueta))
    pdf.set_font("Helvetica", size=11)
    pdf.set_text_color(20, 20, 20)
    pdf.multi_cell(ancho_valor, 8, _texto_pdf(valor))
    pdf.ln(1)


def _preparar_imagen_para_pdf(ruta: Path, max_px: int = 420) -> Optional[Path]:
    """Devuelve una ruta de imagen usable por fpdf (original o miniatura temporal)."""
    if not ruta.is_file():
        return None
    sufijo = ruta.suffix.lower()
    try:
        from PIL import Image  # type: ignore

        with Image.open(ruta) as original:
            trabajo = original.convert("RGB")
            necesita_temp = (
                max(trabajo.size) > max_px or sufijo not in {".png", ".jpg", ".jpeg"}
            )
            if not necesita_temp:
                return ruta
            trabajo.thumbnail((max_px, max_px))
            tmp = tempfile.NamedTemporaryFile(suffix=".jpg", delete=False)
            tmp_path = Path(tmp.name)
            tmp.close()
            trabajo.save(tmp_path, format="JPEG", quality=85, optimize=True)
            return tmp_path
    except Exception:
        return ruta if sufijo in {".png", ".jpg", ".jpeg"} else None


def _dibujar_imagen(
    pdf: PdfFichas,
    ruta: Path,
    *,
    x: float,
    y: float,
    ancho: float,
    max_px: int = 420,
    con_marco: bool = False,
) -> bool:
    """Inserta una imagen (logo o foto). Devuelve True si se embebió."""
    imagen = _preparar_imagen_para_pdf(ruta, max_px=max_px)
    if imagen is None:
        return False
    temporales = []
    if imagen != ruta:
        temporales.append(imagen)
    try:
        pdf.image(str(imagen), x=x, y=y, w=ancho)
        if con_marco:
            pdf.set_draw_color(60, 90, 140)
            pdf.rect(x - 1, y - 1, ancho + 2, ancho + 2)
        return True
    except Exception:
        return False
    finally:
        for tmp in temporales:
            try:
                tmp.unlink(missing_ok=True)
            except OSError:
                pass


def _dibujar_logo(
    pdf: PdfFichas,
    *,
    x: float,
    y: float,
    ancho: float,
) -> bool:
    """Inserta el logo ``refugio.png`` / ``.jpg`` si está disponible."""
    logo = ruta_logo_refugio()
    if logo is None:
        return False
    return _dibujar_imagen(
        pdf, logo, x=x, y=y, ancho=ancho, max_px=280, con_marco=False
    )


def _dibujar_foto(
    pdf: PdfFichas,
    ruta_foto: str,
    x: float = 135,
    y: float = 28,
    ancho: float = 50,
) -> bool:
    """Inserta la foto en la ficha. Devuelve True si se embebió."""
    return _dibujar_imagen(
        pdf,
        Path(ruta_foto),
        x=x,
        y=y,
        ancho=ancho,
        max_px=420,
        con_marco=True,
    )


def _dibujar_ficha(
    pdf: PdfFichas,
    animal_id: int,
    registro: Mapping[str, Any],
) -> None:
    pdf.add_page()
    pdf.set_draw_color(60, 90, 140)
    pdf.set_line_width(0.5)
    pdf.rect(15, 18, 180, 250)

    tiene_logo = _dibujar_logo(pdf, x=20, y=22, ancho=18)
    titulo_x = 42 if tiene_logo else 20
    pdf.set_xy(titulo_x, 24)
    pdf.set_font("Helvetica", "B", 18)
    pdf.set_text_color(20, 40, 80)
    pdf.cell(0, 10, _texto_pdf("Ficha del animal"), new_x="LMARGIN", new_y="NEXT")

    pdf.set_x(titulo_x)
    pdf.set_font("Helvetica", size=10)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(
        0,
        6,
        _texto_pdf("Refugio Animal - inventario interno"),
        new_x="LMARGIN",
        new_y="NEXT",
    )
    pdf.ln(4)

    foto = str(registro.get("foto", "") or "").strip()
    tiene_foto = bool(foto) and _dibujar_foto(pdf, foto)

    _campo(pdf, "Identificador:", str(animal_id))
    _campo(pdf, "Nombre:", str(registro.get("nombre", "")))
    _campo(pdf, "Especie:", str(registro.get("especie", "")))
    _campo(pdf, "Edad:", f"{registro.get('edad', '')} años")
    peso = registro.get("peso", "")
    try:
        peso_txt = f"{float(peso):.2f} kg"
    except (TypeError, ValueError):
        peso_txt = str(peso)
    _campo(pdf, "Peso:", peso_txt)
    _campo(pdf, "Color:", str(registro.get("color", "")))
    if not tiene_foto:
        _campo(pdf, "Foto:", "(sin foto)")

    # Bajar el cursor si la foto ocupa espacio a la derecha
    if tiene_foto and pdf.get_y() < 90:
        pdf.set_y(90)

    pdf.ln(2)
    pdf.set_x(25)
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(40, 60, 90)
    pdf.cell(0, 8, _texto_pdf("Observaciones:"), new_x="LMARGIN", new_y="NEXT")
    pdf.set_x(25)
    pdf.set_font("Helvetica", size=11)
    pdf.set_text_color(20, 20, 20)
    observaciones = str(registro.get("observaciones", "")).strip() or "-"
    pdf.multi_cell(160, 7, _texto_pdf(observaciones))

    _seccion_lista(
        pdf,
        "Tratamientos médicos",
        registro.get("tratamientos") or [],
        lambda t: f"{t.get('fecha', '')} | {t.get('descripcion', '')} "
        f"({t.get('veterinario', '-')})",
    )
    _seccion_lista(
        pdf,
        "Vacunaciones",
        registro.get("vacunaciones") or [],
        lambda v: f"{v.get('fecha', '')} | {v.get('vacuna', '')} "
        f"(próxima: {v.get('proxima', '-')})",
    )
    _seccion_lista(
        pdf,
        "Documentación adjunta",
        registro.get("documentos") or [],
        lambda d: f"{d.get('fecha', '')} | {d.get('nombre', '')}",
    )


def _seccion_lista(
    pdf: PdfFichas,
    titulo: str,
    items: Sequence[Mapping[str, Any]],
    formatear,
) -> None:
    pdf.ln(3)
    pdf.set_x(25)
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(40, 60, 90)
    pdf.cell(0, 8, _texto_pdf(titulo + ":"), new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", size=10)
    pdf.set_text_color(20, 20, 20)
    if not items:
        pdf.set_x(25)
        pdf.multi_cell(160, 6, _texto_pdf("- (sin registros)"))
        return
    for item in items:
        pdf.set_x(25)
        pdf.multi_cell(160, 6, _texto_pdf(f"- {formatear(item)}"))


def _portada(pdf: PdfFichas, total: int) -> None:
    pdf.add_page()
    # Logo centrado encima del título (si existe refugio.png / .jpg).
    logo = ruta_logo_refugio()
    if logo is not None:
        ancho_logo = 42.0
        x_logo = (210.0 - ancho_logo) / 2.0
        _dibujar_logo(pdf, x=x_logo, y=40, ancho=ancho_logo)
        pdf.set_y(90)
    else:
        pdf.set_y(80)
    pdf.set_font("Helvetica", "B", 22)
    pdf.set_text_color(20, 40, 80)
    pdf.cell(0, 12, _texto_pdf("Refugio Animal"), align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)
    pdf.set_font("Helvetica", size=14)
    pdf.set_text_color(60, 60, 60)
    pdf.cell(
        0,
        10,
        _texto_pdf("Listado de fichas de animales"),
        align="C",
        new_x="LMARGIN",
        new_y="NEXT",
    )
    pdf.ln(8)
    pdf.set_font("Helvetica", size=11)
    fecha = datetime.now().strftime("%d/%m/%Y %H:%M")
    pdf.cell(
        0,
        8,
        _texto_pdf(f"Generado: {fecha}"),
        align="C",
        new_x="LMARGIN",
        new_y="NEXT",
    )
    pdf.cell(
        0,
        8,
        _texto_pdf(f"Total de fichas: {total}"),
        align="C",
        new_x="LMARGIN",
        new_y="NEXT",
    )


def _iter_animales(
    inventario: Inventario,
    ids: Optional[Sequence[int]] = None,
) -> Iterable[Tuple[int, Mapping[str, Any]]]:
    if ids is None:
        ordenados = sorted(inventario.keys())
    else:
        ordenados = list(ids)
    for animal_id in ordenados:
        if animal_id not in inventario:
            raise ValueError(
                f"No se ha encontrado el animal con ID {animal_id}."
            )
        yield animal_id, inventario[animal_id]


def exportar_fichas_pdf(
    inventario: Inventario,
    ruta: Ruta,
    *,
    ids: Optional[Sequence[int]] = None,
    incluir_portada: bool = True,
) -> int:
    """Escribe un PDF con una ficha por animal y devuelve cuántas se exportaron."""
    animales = list(_iter_animales(inventario, ids))
    if not animales:
        raise ValueError("No hay animales para exportar.")

    destino = Path(ruta)
    if destino.suffix.lower() != ".pdf":
        destino = destino.with_suffix(".pdf")

    pdf = PdfFichas()
    if incluir_portada:
        _portada(pdf, total=len(animales))

    for animal_id, registro in animales:
        _dibujar_ficha(pdf, animal_id, registro)

    destino.parent.mkdir(parents=True, exist_ok=True)
    # Escritura vía temporal: si el PDF destino está abierto en un visor,
    # Windows suele devolver Permission denied al sobrescribirlo.
    temporal = destino.with_name(
        f".{destino.stem}_{os.getpid()}.pdf.tmp"
    )
    try:
        pdf.output(str(temporal))
        try:
            temporal.replace(destino)
        except PermissionError as error:
            try:
                temporal.unlink(missing_ok=True)
            except OSError:
                pass
            raise PermissionError(
                f"No se pudo guardar '{destino.name}'.\n\n"
                "El archivo está bloqueado (normalmente porque ya está abierto "
                "en un visor de PDF o en el explorador).\n\n"
                "Cierra ese PDF e inténtalo de nuevo, o elige otro nombre "
                "o carpeta en el diálogo Guardar."
            ) from error
    except PermissionError:
        raise
    except OSError as error:
        try:
            temporal.unlink(missing_ok=True)
        except OSError:
            pass
        if getattr(error, "errno", None) == 13 or "Permission" in str(error):
            raise PermissionError(
                f"No se pudo guardar '{destino.name}'.\n\n"
                "Permiso denegado al escribir el archivo. Comprueba que no "
                "esté abierto en otro programa y que la carpeta sea escribible."
            ) from error
        raise
    return len(animales)
