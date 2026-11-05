# Pruebas automatizadas — Refugio Animal

## 1. Qué se prueba

Los tests viven en `tarea1/tests/` y usan el módulo estándar **`unittest`**.

| Archivo | Cobertura |
| --- | --- |
| `test_datos.py` | Inventario y CRUD |
| `test_validaciones.py` | `validar_datos()` |
| `test_interfaz.py` | GUI (`GestorAnimales`): CRUD, filtros, diálogos |
| `test_exportacion_pdf.py` | Exportación PDF y botón Exportar |
| `test_ficha_clinica.py` | Tratamientos, vacunas, documentos, foto |
| `test_modelos_poo.py` | Herencia ABC, `@property`, decoradores, adaptador dict↔objeto |

La interfaz se prueba con la ventana oculta (`withdraw`) y `messagebox` / diálogos simulados (`unittest.mock`), para no bloquear la batería.

---

## 2. Cómo ejecutarlos

### Opción A — Recomendada (consola + informe en disco)

Desde la **raíz del repositorio**:

```bash
python tarea1/ejecutar_tests.py
```

Desde la carpeta **`tarea1/`**:

```bash
python ejecutar_tests.py
```

Este script:

1. Descubre todos los `test_*.py` de `tarea1/tests/`.
2. Muestra el detalle en la **consola**.
3. **Guarda** el mismo informe en disco (ver sección 3).
4. Devuelve código de salida `0` si todo pasa, `1` si hay fallos.

### Opción B — Solo consola (`unittest` directo)

Desde la raíz del repo:

```bash
python -m unittest discover -s tarea1/tests -v
```

Desde `tarea1/`:

```bash
python -m unittest discover -s tests -v
```

Un solo módulo:

```bash
python -m unittest tarea1.tests.test_interfaz -v
```

(o, estando en `tarea1/` con el path correcto)

```bash
cd tarea1
python -m unittest tests.test_interfaz -v
```

### Opción C — Redirigir la salida tú mismo

```bash
python -m unittest discover -s tarea1/tests -v > tarea1/tests/resultados/manual.txt 2>&1
```

En PowerShell:

```powershell
python -m unittest discover -s tarea1/tests -v *>&1 | Tee-Object -FilePath tarea1/tests/resultados/manual.txt
```

---

## 3. Dónde se guarda el resultado

| Destino | Contenido |
| --- | --- |
| **Consola** | Salida inmediata (OK / FAIL por test y resumen final). Siempre. |
| `tarea1/tests/resultados/ultimo_informe.txt` | Copia del último informe generado por `ejecutar_tests.py` (se sobrescribe). |
| `tarea1/tests/resultados/informe_YYYYMMDD_HHMMSS.txt` | Histórico fechado; no se borra al volver a ejecutar. |

Los informes incluyen: fecha, número de tests, errores, fallos, omitidos, veredicto OK/FALLO y el log verbose de `unittest`.

**Nota:** la carpeta `resultados/` está en `.gitignore` (salvo `.gitkeep`), para no versionar informes locales. En la defensa puedes abrir `ultimo_informe.txt` o regenerarlo al momento.

Los PDFs de exportación de fichas **no** son el resultado de los tests; se guardan donde elijas en el diálogo «Guardar». Los adjuntos clínicos van a `tarea1/adjuntos/<id>/`.

---

## 4. Cómo interpretar el resumen

Ejemplo de final correcto:

```text
----------------------------------------------------------------------
Ran 53 tests in 2.231s

OK
```

Si falla:

```text
FAILED (failures=1)
```

El detalle del assert aparece encima, con el nombre del test (`test_...`).

Código de salida del proceso:

- `0` → batería en verde  
- distinto de `0` → hay fallos o errores  

---

## 5. Dependencias para la batería

| Paquete | Para qué |
| --- | --- |
| Biblioteca estándar | `unittest`, `tkinter`, `unittest.mock` |
| `fpdf2` | Tests de exportación PDF |
| `Pillow` (opcional) | No obligatorio para los tests actuales |

```bash
pip install fpdf2
```

---

## 6. Datos de muestra para importación manual

Además de los tests automáticos, la carpeta `tarea1/muestras/` aporta ficheros listos para la demo:

- Fotos PNG en `muestras/fotos/`
- Tratamientos y vacunas en PDF/DOCX en `muestras/documentos/`

Ver [../muestras/README.md](../muestras/README.md). No sustituyen a `unittest`; sirven para probar la importación en la GUI.

---

## 7. Relación con la defensa

- Señalar `tarea1/tests/` como evidencia de testabilidad (RNF-07).
- Ejecutar `python tarea1/ejecutar_tests.py` y mostrar `tests/resultados/ultimo_informe.txt`.
- Explicar que la GUI se prueba sin `mainloop` y con diálogos mockeados.
- Mostrar importación de foto/documento desde `muestras/`.
