"""Ejecuta la batería de pruebas y guarda un informe en disco.

Uso (desde ``tarea1/`` o desde la raíz del repo)::

    python ejecutar_tests.py
    python tarea1/ejecutar_tests.py

El resumen se muestra en consola y se escribe en::

    tarea1/tests/resultados/ultimo_informe.txt
    tarea1/tests/resultados/informe_<fecha_hora>.txt
"""

from __future__ import annotations

import sys
import unittest
from datetime import datetime
from io import StringIO
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
CARPETA_TESTS = RAIZ / "tests"
CARPETA_RESULTADOS = CARPETA_TESTS / "resultados"


def main() -> int:
    if str(RAIZ) not in sys.path:
        sys.path.insert(0, str(RAIZ))

    CARPETA_RESULTADOS.mkdir(parents=True, exist_ok=True)

    cargador = unittest.TestLoader()
    suite = cargador.discover(start_dir=str(CARPETA_TESTS), pattern="test_*.py")

    buffer = StringIO()
    corredor = unittest.TextTestRunner(stream=buffer, verbosity=2)
    resultado = corredor.run(suite)
    informe = buffer.getvalue()

    sellado = datetime.now().strftime("%Y%m%d_%H%M%S")
    historico = CARPETA_RESULTADOS / f"informe_{sellado}.txt"
    ultimo = CARPETA_RESULTADOS / "ultimo_informe.txt"

    cabecera = (
        f"Refugio Animal — informe de pruebas\n"
        f"Fecha: {datetime.now().isoformat(timespec='seconds')}\n"
        f"Tests ejecutados: {resultado.testsRun}\n"
        f"Errores: {len(resultado.errors)}\n"
        f"Fallos: {len(resultado.failures)}\n"
        f"Omitidos: {len(resultado.skipped)}\n"
        f"{'OK' if resultado.wasSuccessful() else 'FALLO'}\n"
        f"{'-' * 60}\n"
    )
    texto = cabecera + informe
    historico.write_text(texto, encoding="utf-8")
    ultimo.write_text(texto, encoding="utf-8")

    # Misma salida en consola.
    print(texto)
    print(f"Informe guardado en:\n  {ultimo}\n  {historico}")

    return 0 if resultado.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
