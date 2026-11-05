# Manual de usuario — Refugio Animal

## 1. ¿Qué es?

Aplicación de escritorio para el inventario de un refugio (perros, gatos y loros): alta/consulta/edición/borrado, búsqueda, ficha clínica (tratamientos, vacunas), documentos, foto y exportación a PDF.

**Importante**

- El **inventario** vive en memoria: al cerrar la app se pierden altas/cambios de esa sesión (vuelve el ejemplo).
- Los **archivos** (fotos/documentos) sí se guardan en `tarea1/adjuntos/<id>/` y permanecen en disco.

---

## 2. Requisitos para usar la app

| Necesitas | Para qué |
| --- | --- |
| Python 3.8+ con Tkinter | Interfaz |
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

O desde la raíz del repo: `python tarea1/app.py`.

Ventana: **Refugio Animal - Gestión de animales**.

---

## 4. Pantalla principal

| Zona | Función |
| --- | --- |
| **Datos del animal** | Formulario de ficha básica |
| **Foto** (derecha) | Miniatura del animal seleccionado |
| **Crear / Actualizar / Borrar / Limpiar** | CRUD |
| **Exportar PDF** | Generar fichas en PDF |
| **Ficha clínica / adjuntos** | Tratamientos, vacunas, docs, foto |
| **Buscar y filtrar** | Nombre y especie |
| **Tabla** | Listado visible |
| **Barra de estado** | Totales y mensajes |

---

## 5. Operaciones

### 5.1 Consultar y seleccionar

Haz clic en una fila: se rellenan el formulario y la foto (si hay).

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

### 5.7 Ficha clínica / adjuntos

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

### 5.8 Carpeta de muestras

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
| Especie | Perro / Gato / Loro |
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
| Perdí altas al cerrar | Normal: inventario sin persistencia; los adjuntos en `adjuntos/` sí quedan |
| PDF tarda en abrirse | Vuelve a exportar con la versión actual (sin `/FitH`) |
| No veo ñ / tildes en botones | Reinicia la app tras actualizar el código |

---

## 8. Cerrar

Cierra la ventana. No hay «Guardar inventario»: la sesión termina.
