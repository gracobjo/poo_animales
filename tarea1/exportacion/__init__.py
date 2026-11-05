"""Exportación de datos del refugio (p. ej. PDF de fichas)."""

__all__ = ["exportar_fichas_pdf"]


def __getattr__(name: str):
    """Carga perezosa para no exigir ``fpdf2`` al arrancar la GUI."""
    if name == "exportar_fichas_pdf":
        from exportacion.pdf_fichas import exportar_fichas_pdf

        return exportar_fichas_pdf
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
