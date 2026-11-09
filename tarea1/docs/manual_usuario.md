# Manual de usuario — Refugio Animal

## 1. ¿Qué es?

Aplicación de escritorio para el inventario de un refugio (especies nativas y personalizadas): alta/consulta/edición/borrado, búsqueda, ficha clínica (tratamientos, vacunas), documentos, foto y exportación a PDF.

**Importante**

- El **inventario de animales** se guarda en `tarea1/datos/inventario.json` (sobrevive al cerrar la app).
- Las **especies personalizadas** se guardan en `tarea1/datos/especies_personalizadas.json`.
- Los **archivos** (fotos/documentos) van en `tarea1/adjuntos/<id>/`.

---

## 2. Requisitos para usar la app

| Necesitas | Para qué |
| --- | --- |
| Python 3.14+ con Tkinter | Interfaz |
| `fpdf2` | Exportar PDF (`pip install fpdf2`) |
| `Pillow` (recomendado) | Pegar imágenes / vista previa JPG |

```bash
pip install fpdf2 Pillow
```

---

## 3. Cómo abrir el programa

```bash
cd tarea1
python app.py
```

También vale `python main.py` (llama a `app.py`).  
Desde la raíz del repo: `python tarea1/app.py`.

Ventana: **Refugio Animal - Gestión de animales**.

> **No confundir con el cuaderno.**  
> `gestion_animales_tkinter.ipynb` abre una **demo didáctica** (CRUD + ficha POO + especies personalizadas en celdas).  
> La interfaz completa de la entrega es la de `app.py` / `main.py` (foto, clínica, PDF, *Gestionar especies*, estilos).  
> Detalle de diferencias: [../README.md](../README.md#cuaderno-vs-programa-apppy--mainpy).

---

## 4. Pantalla principal

| Zona | Función |
| --- | --- |
| **Logo / título** | Cabecera con `refugio.png` o `refugio.jpg` (si está en `tarea1/` o la raíz del repo) |
| **Datos del animal** | Formulario de ficha básica |
| **Foto** (derecha) | Miniatura del animal seleccionado |
| **Crear / Actualizar / Borrar / Limpiar** | CRUD |
| **Exportar PDF** | Generar fichas en PDF |
| **Ficha clínica / adjuntos** | Tratamientos, vacunas, docs, foto |
| **Gestionar especies** | Alta/edición/desactivación de especies personalizadas (JSON) |
| **Buscar y filtrar** | Nombre y especie |
| **Información del animal seleccionado** | Ficha POO: datos, sonido, alimentación y cuidados (polimorfismo). *Comportamiento*, *Alimentación* y *Cuidados* tienen barra de desplazamiento si el texto es largo |
| **Tabla** | Listado visible |
| **Barra de estado** | Totales y mensajes |

---

## 5. Operaciones

### 5.1 Consultar y seleccionar

Haz clic en una fila: se rellenan el formulario y la foto (si hay), y el panel **Información del animal seleccionado** muestra la ficha generada por la capa POO (`generar_ficha()`). Si los textos de comportamiento, alimentación o cuidados son extensos (p. ej. una especie personalizada), usa la barra vertical de cada bloque.

### 5.2 Buscar / filtrar

Escribe parte del nombre y/o elige especie (**Todas** = sin filtro de especie).

### 5.3 Crear

**Limpiar** → rellenar → **Crear**. Si hay error de validación, no se guarda nada.

### 5.4 Actualizar / borrar

Selecciona fila → **Actualizar** o **Borrar** (borrar pide confirmación).

### 5.5 Limpiar

Vacía formulario, quita selección y panel de foto. No borra animales.

### 5.6 Exportar PDF

| Situación | Resultado |
| --- | --- |
| Hay fila seleccionada | Solo esa ficha |
| No hay selección | Pregunta si exportar **todas las visibles** |

El PDF incluye datos, clínica, documentación listada y **foto** si existe.  
Dependencia: `fpdf2`.

### 5.7 Gestionar especies

**Gestionar especies** abre una ventana para:

- consultar las **nativas** (Perro, Gato, …; no editables);
- **añadir / editar** especies personalizadas (nombre, sonido, alimentación, cuidados);
- **desactivar** (no aparecen en altas nuevas; los animales ya registrados se siguen viendo);
- **eliminar** solo si ningún animal del inventario la usa.

Las personalizadas se guardan en `datos/especies_personalizadas.json` y aparecen en el desplegable de especie sin reiniciar la app.

### 5.8 Ficha clínica / adjuntos

1. Selecciona un animal.  
2. **Ficha clínica / adjuntos**.  
3. Pestañas:

| Pestaña | Acciones |
| --- | --- |
| Tratamientos | Añadir / eliminar (fecha, descripción, veterinario) |
| Vacunaciones | Añadir / eliminar (fecha, vacuna, próxima) |
| Documentos | Importar, **Pegar** (Ctrl+V), abrir, eliminar |
| Foto | Importar, **Pegar** (Ctrl+V), quitar |

#### Cómo pegar bien (Windows)

1. En el **Explorador**, clic derecho en el archivo → **Copiar**.  
2. En Documentos o Foto → **Pegar** o **Ctrl+V**.  
3. También: captura / «Copiar imagen»; o texto del editor (se guarda como `.txt` en Documentos).

**Límite: 5 MB** por archivo.

### 5.9 Carpeta de muestras

Para practicar sin salir del proyecto:

| Ruta | Contenido |
| --- | --- |
| `tarea1/muestras/fotos/` | PNG de ejemplo |
| `tarea1/muestras/documentos/` | PDF, DOCX y TXT de tratamientos/vacunas |

Guía: [../muestras/README.md](../muestras/README.md).

---

## 6. Reglas de los campos

| Campo | Regla |
| --- | --- |
| Nombre, color | Obligatorios |
| Especie | Nativas o personalizadas activas (desplegable) |
| Edad | Entero 0–30 |
| Peso | Entre 0.01 y 100 kg (vale `3,8`) |
| Observaciones | Opcional |
| Adjuntos | Máximo 5 MB |

---

## 7. Problemas frecuentes

| Situación | Qué hacer |
| --- | --- |
| «Selecciona un animal…» | Marca una fila en la tabla |
| Pegar dice que no hay nada | Copia el **archivo** en el Explorador (no solo el nombre en el IDE) |
| Archivo demasiado grande | Usa uno ≤ 5 MB |
| Perdí el `inventario.json` | Se regenera el ejemplo al arrancar; las altas previas solo vuelven si restauras el archivo |
| PDF tarda en abrirse | Vuelve a exportar con la versión actual (sin `/FitH`) |
| No veo ñ / tildes en botones | Reinicia la app tras actualizar el código |

---

## 8. Cerrar

Cierra la ventana. El inventario y las especies personalizadas ya están guardados en sus JSON; no hace falta un botón «Guardar» aparte.
