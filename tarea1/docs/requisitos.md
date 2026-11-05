# Requisitos — Refugio Animal

Sistema: aplicación de escritorio (Tkinter) para gestionar el inventario de un refugio con CRUD sobre un **diccionario en memoria**, capa POO didáctica (herencia / properties), ficha clínica, adjuntos, exportación PDF y batería de pruebas.

---

## 1. Requisitos funcionales (RF)

### 1.1 Inventario e interfaz principal

| ID | Requisito | Prioridad | Cumplimiento |
| --- | --- | --- | --- |
| RF-01 | Mantener un inventario de animales con ID numérico único. | Alta | `datos/inventario.py` |
| RF-02 | Cada ficha incluye nombre, especie, edad, peso, color y observaciones. | Alta | Esquema del `dict` |
| RF-03 | Especies admitidas: Perro, Gato, Conejo, Loro, Hámster. | Alta | `datos/constantes.py` → `ESPECIES` |
| RF-03b | Capa POO paralela: `AnimalRefugio` + subclases, `@property`, decoradores; adaptador dict↔objeto; resumen polimórfico al seleccionar. | Media | `datos/modelos.py`, `decoradores.py`, `adaptador_poo.py` |
| RF-04 | **Crear** animal desde el formulario. | Alta | Botón Crear |
| RF-05 | **Consultar** (leer) al seleccionar una fila; rellenar formulario y mostrar foto si existe. | Alta | `<<TreeviewSelect>>` |
| RF-06 | **Actualizar** el animal seleccionado (conservando datos clínicos si no se envían). | Alta | Botón Actualizar |
| RF-07 | **Borrar** el seleccionado tras confirmación (y borrar sus adjuntos en disco). | Alta | Botón Borrar + `askyesno` |
| RF-08 | **Validar** datos antes de crear/actualizar. | Alta | `validaciones/reglas.py` |
| RF-09 | **Filtrar** la tabla por especie. | Media | Combobox filtro |
| RF-10 | **Buscar** por fragmento de nombre (sin distinguir mayúsculas). | Media | Entry + `KeyRelease` |
| RF-11 | **Limpiar** formulario, selección y panel de foto. | Media | Botón Limpiar |
| RF-12 | Mostrar **estado** (totales, visibles, última acción, resumen clínico). | Media | `estado_var` |
| RF-13 | Ante errores o falta de selección, mostrar **diálogos** claros. | Alta | `messagebox` |
| RF-14 | Al arrancar, cargar **inventario de ejemplo** (sin persistencia de sesión). | Alta | `animales_iniciales()` |

### 1.2 Exportación PDF

| ID | Requisito | Prioridad | Cumplimiento |
| --- | --- | --- | --- |
| RF-15 | **Exportar a PDF**: selección → solo esa ficha; sin selección → visibles (con confirmación). Una página por animal; portada si hay más de uno. Incluye datos clínicos y foto embebida si existe. | Alta | `exportacion/pdf_fichas.py` |

### 1.3 Ficha clínica y adjuntos

| ID | Requisito | Prioridad | Cumplimiento |
| --- | --- | --- | --- |
| RF-16 | Registrar **tratamientos médicos** (fecha, descripción, veterinario). | Alta | Ficha clínica → Tratamientos |
| RF-17 | Registrar **vacunaciones** (fecha, vacuna, próxima dosis). | Alta | Ficha clínica → Vacunaciones |
| RF-18 | **Importar o pegar** documentación (copia a `adjuntos/<id>/documentos`). | Alta | Documentos + `portapapeles.py` |
| RF-19 | **Asignar, pegar o quitar foto**; vista en formulario principal y en PDF. | Alta | Foto + `vista_foto.py` |
| RF-20 | Límite de **5 MB** por fichero importado o pegado. | Alta | `TAMANO_MAX_BYTES` |
| RF-21 | Pegar con botón **Pegar** o **Ctrl+V** (archivo del Explorador, imagen o texto → `.txt`). | Media | `interfaz/portapapeles.py` |

### Reglas de negocio (RN)

| ID | Regla |
| --- | --- |
| RN-01 | Nombre y color obligatorios (tras `strip`). |
| RN-02 | Especie ∈ `ESPECIES`. |
| RN-03 | Edad: entero entre 0 y 30. |
| RN-04 | Peso: número finito entre 0.01 y 100 kg (ambos inclusive el máximo). |
| RN-05 | Nuevo ID = `max(inventario)+1` (o 1). |
| RN-06 | Actualizar/borrar/ficha clínica/exportar con selección cuando aplique. |
| RN-07 | Borrar exige confirmación. |
| RN-08 | Tratamiento: descripción obligatoria. Vacuna: nombre obligatorio. |
| RN-09 | Documento: nombre + ruta; foto: ruta en disco bajo `adjuntos/`. |
| RN-10 | Fichero > 5 MB → rechazo con mensaje. |

---

## 2. Requisitos no funcionales (RNF)

| ID | Categoría | Requisito | Criterio / evidencia |
| --- | --- | --- | --- |
| RNF-01 | Usabilidad | CRUD visible sin menús ocultos; foto junto al formulario; ficha clínica en pestañas. | `GestorAnimales` + `DialogoFichaClinica` |
| RNF-02 | Usabilidad | Mensajes en español correcto (ñ, tildes) comprensibles. | Textos UI / `ValueError` |
| RNF-03 | Fiabilidad | Datos inválidos no corrompen el inventario. | Validación previa |
| RNF-04 | Mantenibilidad | Separación: datos, validaciones, interfaz, exportación, arranque. | Paquetes bajo `tarea1/` |
| RNF-05 | Portabilidad | Python 3.8+; GUI con `tkinter`. Dependencias opcionales/documentadas: `fpdf2`, `Pillow`. | `requirements.txt` |
| RNF-06 | Rendimiento | Filtrar/refrescar tabla inmediato en inventarios pequeños/medios. | Dict en RAM |
| RNF-07 | Testabilidad | Pruebas automatizadas + informe en disco. | `ejecutar_tests.py` → `tests/resultados/` |
| RNF-08 | Integridad | Confirmación en borrados; límite de tamaño en adjuntos. | `askyesno`, 5 MB |
| RNF-09 | Limitación | Inventario de sesión **sin** persistencia al cerrar (adjuntos en disco sí permanecen). | Diseño / enunciado |
| RNF-10 | Documentación | Requisitos, CU, UML, manuales, pruebas y muestras. | `docs/`, `muestras/` |
| RNF-11 | Usabilidad tipográfica | Guía de estilos única (`Segoe UI` / Helvetica) en ttk y `tk.Text`. | `interfaz/estilos.py` |
| RNF-12 | Apertura de PDF | PDF ligeros (fuentes estándar) sin `/FitH` que ralentice visores. | `set_display_mode(100,"single")` |

---

## 3. Fuera de alcance (esta versión)

- Base de datos remota / multiusuario / autenticación.
- Persistencia automática del inventario al cerrar (JSON/SQLite serían evolución).
- Clases de dominio `Animal` / herencia (proyecto padre `animales_poo`).
- API HTTP.

Ver evoluciones en [manual_desarrollador.md](manual_desarrollador.md).
