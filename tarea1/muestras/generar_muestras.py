"""Genera fotos y documentos de ejemplo para probar la importacion.

Ejecutar desde cualquier sitio::

    python tarea1/muestras/generar_muestras.py
"""

from __future__ import annotations

import zipfile
from pathlib import Path
from xml.sax.saxutils import escape

from fpdf import FPDF
from PIL import Image, ImageDraw, ImageFont

CARPETA = Path(__file__).resolve().parent
FOTOS = CARPETA / "fotos"
DOCS = CARPETA / "documentos"


def _fuente(draw: ImageDraw.ImageDraw, size: int = 28):
    for nombre in (
        "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/segoeui.ttf",
    ):
        path = Path(nombre)
        if path.is_file():
            return ImageFont.truetype(str(path), size=size)
    return ImageFont.load_default()


def _foto(
    nombre: str,
    color_fondo: tuple[int, int, int],
    color_figura: tuple[int, int, int],
    etiqueta: str,
    figura: str,
) -> None:
    """Crea una imagen PNG generica (no foto real) para pruebas."""
    FOTOS.mkdir(parents=True, exist_ok=True)
    img = Image.new("RGB", (480, 360), color_fondo)
    draw = ImageDraw.Draw(img)
    # Marco
    draw.rectangle((20, 20, 460, 340), outline=(40, 40, 40), width=3)

    if figura == "perro":
        draw.ellipse((150, 80, 330, 240), fill=color_figura)
        draw.ellipse((130, 60, 190, 130), fill=color_figura)  # oreja
        draw.ellipse((290, 60, 350, 130), fill=color_figura)
        draw.ellipse((200, 150, 230, 180), fill=(20, 20, 20))
        draw.ellipse((250, 150, 280, 180), fill=(20, 20, 20))
    elif figura == "gato":
        draw.ellipse((160, 90, 320, 250), fill=color_figura)
        draw.polygon([(170, 90), (150, 40), (210, 100)], fill=color_figura)
        draw.polygon([(310, 90), (330, 40), (270, 100)], fill=color_figura)
        draw.ellipse((205, 150, 230, 175), fill=(20, 180, 80))
        draw.ellipse((250, 150, 275, 175), fill=(20, 180, 80))
    elif figura == "loro":
        draw.ellipse((180, 100, 300, 260), fill=color_figura)
        draw.ellipse((220, 60, 300, 140), fill=color_figura)
        draw.polygon([(300, 90), (360, 110), (300, 130)], fill=(230, 140, 40))
        draw.ellipse((250, 95, 270, 115), fill=(20, 20, 20))
    elif figura == "conejo":
        draw.ellipse((170, 140, 310, 280), fill=color_figura)
        draw.ellipse((190, 40, 230, 160), fill=color_figura)
        draw.ellipse((250, 40, 290, 160), fill=color_figura)
        draw.ellipse((210, 180, 235, 205), fill=(20, 20, 20))
        draw.ellipse((245, 180, 270, 205), fill=(20, 20, 20))
    else:  # hamster
        draw.ellipse((160, 120, 320, 270), fill=color_figura)
        draw.ellipse((200, 160, 230, 190), fill=(20, 20, 20))
        draw.ellipse((250, 160, 280, 190), fill=(20, 20, 20))
        draw.ellipse((230, 200, 250, 220), fill=(180, 100, 100))

    font = _fuente(draw, 26)
    draw.text((30, 300), etiqueta, fill=(20, 20, 20), font=font)
    destino = FOTOS / nombre
    img.save(destino, format="PNG")
    print("Foto:", destino)


def _pdf(nombre: str, titulo: str, lineas: list[str]) -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    pdf = FPDF()
    pdf.set_compression(True)
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(
        0,
        12,
        titulo.encode("latin-1", "replace").decode("latin-1"),
        new_x="LMARGIN",
        new_y="NEXT",
    )
    pdf.ln(4)
    pdf.set_font("Helvetica", size=11)
    for linea in lineas:
        texto = linea.encode("latin-1", "replace").decode("latin-1")
        pdf.set_x(pdf.l_margin)
        if not texto.strip():
            pdf.ln(5)
            continue
        pdf.multi_cell(0, 7, texto)
    destino = DOCS / nombre
    pdf.output(str(destino))
    print("PDF:", destino)


def _docx(nombre: str, titulo: str, lineas: list[str]) -> None:
    """DOCX minimo (Office Open XML) sin dependencias externas."""
    DOCS.mkdir(parents=True, exist_ok=True)
    destino = DOCS / nombre

    def parrafo(texto: str, negrita: bool = False) -> str:
        contenido = escape(texto)
        rpr = "<w:b/>" if negrita else ""
        return (
            f"<w:p><w:r><w:rPr>{rpr}</w:rPr>"
            f"<w:t xml:space=\"preserve\">{contenido}</w:t></w:r></w:p>"
        )

    body = parrafo(titulo, negrita=True) + "".join(parrafo(x) for x in lineas)
    document_xml = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
        f"<w:body>{body}<w:sectPr/></w:body></w:document>"
    )
    content_types = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
</Types>
"""
    rels = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>
"""
    doc_rels = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"/>
"""
    with zipfile.ZipFile(destino, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("[Content_Types].xml", content_types)
        zf.writestr("_rels/.rels", rels)
        zf.writestr("word/document.xml", document_xml)
        zf.writestr("word/_rels/document.xml.rels", doc_rels)
    print("DOCX:", destino)


def main() -> None:
    _foto("perro_labrador.png", (230, 240, 255), (180, 120, 60), "Perro (ejemplo)", "perro")
    _foto("gato_atigrado.png", (255, 240, 230), (200, 150, 90), "Gato (ejemplo)", "gato")
    _foto("loro_verde.png", (230, 255, 230), (40, 160, 70), "Loro (ejemplo)", "loro")
    _foto("conejo_blanco.png", (245, 245, 255), (235, 235, 240), "Conejo (ejemplo)", "conejo")
    _foto("hamster_dorado.png", (255, 248, 230), (210, 150, 70), "Hamster (ejemplo)", "hamster")

    tratamientos = [
        "Centro: Clínica Veterinaria Ejemplo",
        "Paciente: (asignar al importar en la app)",
        "",
        "1. Fecha: 2025-06-01  |  Desparasitación interna  |  Dra. Ruiz",
        "2. Fecha: 2025-09-12  |  Revisión otitis / oídos  |  Dr. Pérez",
        "3. Fecha: 2025-11-03  |  Analgésico postoperatorio  |  Dra. Ruiz",
        "",
        "Notas: documento simulado para probar la importación de adjuntos.",
    ]
    vacunas = [
        "Hoja de vacunación (simulada)",
        "Centro: Clínica Veterinaria Ejemplo",
        "",
        "Vacuna                  Fecha        Próxima",
        "------------------------------------------------",
        "Rabia                   2025-03-10   2026-03-10",
        "Polivalente             2025-03-10   2026-03-10",
        "Trivalente felina       2025-01-20   2026-01-20",
        "",
        "Firma veterinario: ____________________",
        "Documento de prueba para importar en Ficha clínica > Documentos.",
    ]

    _pdf("tratamiento_medico_ejemplo.pdf", "Informe de tratamientos médicos", tratamientos)
    _pdf("hoja_vacunacion_ejemplo.pdf", "Hoja de vacunación", vacunas)
    _docx("tratamiento_medico_ejemplo.docx", "Informe de tratamientos médicos", tratamientos)
    _docx("hoja_vacunacion_ejemplo.docx", "Hoja de vacunación", vacunas)

    # TXT extra por si se quiere probar otro tipo
    txt = DOCS / "consentimiento_adopcion_ejemplo.txt"
    txt.write_text(
        "Consentimiento simulado de adopción\n"
        "Fecha: 2026-01-15\n"
        "El adoptante declara haber recibido información sobre cuidados básicos.\n",
        encoding="utf-8",
    )
    print("TXT:", txt)
    print("Listo. Carpeta:", CARPETA)


if __name__ == "__main__":
    main()
