# Tarea 1 — Análisis y defensa del proyecto

**Programa ejecutable:** `app.py` (`datos/`, `validaciones/`, `interfaz/`, `exportacion/`)  
**Documentación formal:** carpeta [`docs/`](docs/README.md) (requisitos RF/RNF, CU, UML, manuales, pruebas)  
**Defensa oral / narrada:** este Markdown/PDF + `../gestion_animales_tkinter.ipynb`  
**Enunciado oficial:** `Enunciado_oficial_Tarea_1.pdf`  
**Fecha de entrega (enunciado):** 12 de noviembre de 2026  

Este documento sirve para **explicar y defender** el trabajo ante el tribunal: qué hace, cómo está organizado, qué del temario se aplica y cómo responder a cambios de refactorización.

**Arranque (entrega):** `cd tarea1` → `python app.py` (o `python main.py`)  
**Extras respecto al enunciado mínimo:** ficha clínica, foto/documentos (importar/pegar, máx. 5 MB), exportación PDF, ficha POO en la GUI, **especies personalizadas** (JSON + `EspeciePersonalizada`), tests con informe en disco.

**Cuaderno ≠ programa.** El `.ipynb` es un guion didáctico (CRUD + ficha POO con scrollbars + demo de `EspeciePersonalizada`). La ventana completa (foto, clínica, PDF, *Gestionar especies*, estilos) solo sale de `tarea1/app.py`. Ver tabla en [README.md](README.md#cuaderno-vs-programa-apppy--mainpy).

---

## 1. Relación con el enunciado

| Requisito del enunciado | Cómo se cumple en el proyecto |
| --- | --- |
| Temática libre | Refugio / inventario de animales (perro, gato, loro) |
| Al menos un diccionario complejo | `animales`: ID → ficha con varios campos |
| Funcionalidades CRUD | Crear, leer, actualizar y borrar |
| Interfaz con `tkinter` | Clase `GestorAnimales` + widgets `tk` / `ttk` |
| Presentación con posibles cambios | Ver sección 8 (preguntas de refactorización) |

**Dato clave para defender:** los datos viven en un **diccionario en memoria**. No hay base de datos. Es deliberado: el objetivo es practicar **Tkinter** y estructuras del lenguaje, no persistencia.

---

## 2. Idea general del proyecto

Aplicación de escritorio CRUD sobre un inventario de animales, ampliada con ficha clínica, adjuntos y PDF.

| Operación | Método de lógica | Método de interfaz |
| --- | --- | --- |
| Create | `crear_animal()` | `_crear()` |
| Read | `leer_animal()` | `_seleccionar()` / `_actualizar_tabla()` |
| Update | `actualizar_animal()` | `_actualizar()` |
| Delete | `borrar_animal()` | `_borrar()` |
| Clínica / adjuntos | `adjuntos.py` + listas en el `dict` | `DialogoFichaClinica` |
| Exportar | `exportar_fichas_pdf()` | `_exportar_pdf()` |

Frase de apertura recomendada en la defensa:

> Es una aplicación CRUD con Tkinter sobre un diccionario: separamos datos, validación e interfaz; además hay ficha clínica, pegado de adjuntos (límite 5 MB) y exportación a PDF.

---

## 3. Mapa con el temario (Tema 2 y Tema 3)

### 3.1 Tema 2 — POO y estructuras

El enunciado exige **diccionario + CRUD + Tkinter**. La ficha vive en un `dict`; además hay una **capa POO** paralela para demostrar el Tema 2 sin romper el enunciado.

| Idea del Tema 2 | En este proyecto |
| --- | --- |
| Diccionarios | Inventario `dict[int, dict]`; ID = identidad |
| Herencia + ABC | `AnimalRefugio` (abstracta) → `Perro`, `Gato`, `Conejo`, `Loro`, `Hamster` en `datos/modelos.py` |
| Getters / setters | `@property` + `@xxx.setter` (nombre, edad, peso, color, observaciones) |
| Decoradores | `@abstractmethod`, `@property`, `@classmethod`, y propio `@cuenta_usos` en `datos/decoradores.py` |
| Polimorfismo | `hacer_sonido()` / `tipo_alimentacion()` / `cuidados_especificos()`; la GUI muestra `generar_ficha()` sin `if` por especie |
| Puente dict ↔ objeto | `datos/adaptador_poo.py` (`registro_a_animal`, `animal_a_campos`) |
| Ficha en Tkinter | Panel «Información del animal seleccionado»: dict → adaptador → objeto → `generar_ficha()`; scrollbars en comportamiento / alimentación / cuidados |
| Especies dinámicas | Nativas (clases fijas) + personalizadas (`EspeciePersonalizada` + `especies_personalizadas.json`) vía *Gestionar especies* |
| Validación procedural | `validar_datos()` sigue siendo la puerta del CRUD (coherente con los setters) |

**Frase de defensa:** *«El CRUD trabaja con diccionarios, como pide el enunciado; la herencia y las properties son una capa didáctica conectada por un adaptador.»*

### 3.2 Tema 3 — Interfaces gráficas aplicadas

| Lección Tema 3 | Uso en el cuaderno |
| --- | --- |
| Gestores de geometría | `pack()` en bloques principales; `grid()` dentro de `LabelFrame` |
| Variables de control | `StringVar` enlazadas a `Entry` / `Combobox` |
| Frame / LabelFrame | Formulario, filtros y zona de tabla |
| Button / Entry | Acciones CRUD y campos de texto |
| Eventos genéricos | `bind("<KeyRelease>")`, `<<ComboboxSelected>>`, `<<TreeviewSelect>>` |
| Cajas de diálogo | `showerror`, `showinfo`, `askyesno` |
| Widgets TTK | Controles `ttk` homogéneos |
| Combobox | Especie del formulario y filtro |
| Text | Observaciones multilínea |
| Treeview | Tabla con columnas e `iid` = ID |

---

## 4. Sección 1 — Datos iniciales

```python
ESPECIES = ("Perro", "Gato", "Loro")

animales = {
    1: {"nombre": "Luna", "especie": "Perro", "edad": 4, "peso": 18.5, ...},
    2: {...},
}
```

**Qué hace**

- `ESPECIES` alimenta el `Combobox` del formulario y el filtro.
- `animales` usa un **ID numérico** como clave y un diccionario como valor.

**¿Por qué un diccionario y no una lista?**

| Criterio | Diccionario por ID | Lista |
| --- | --- | --- |
| Acceso por ID | `animales[3]` en O(1) | Hay que buscar el elemento |
| Actualizar / borrar | Directo con la clave | Recorrer o conocer el índice |
| Similitud con BD | El ID actúa como clave primaria | Índice frágil si se reordena |

**Pregunta típica:** *¿Y si quiero añadir otro loro?*  
→ Añadir una entrada con el siguiente ID libre (o usar `crear_animal`).

---

## 5. Sección 2 — Funciones CRUD puras

Corazón lógico del proyecto, **separado de la interfaz**.

### `validar_datos(datos)`

1. Limpia espacios con `.strip()`.
2. Obliga nombre, especie (de `ESPECIES`) y color.
3. Edad: entero entre 0 y 30 (rechaza `bool`).
4. Peso: `float` finito entre `PESO_MIN_KG` (0.01) y `PESO_MAX_KG` (100) kg.
5. Si falla → `ValueError` con mensaje claro.
6. Si va bien → diccionario limpio y normalizado.

### `crear_animal` / `leer_animal` / `actualizar_animal` / `borrar_animal`

- Reciben el inventario como **argumento** (no dependen de una global oculta).
- `leer_animal` usa `.copy()` para no modificar el registro original por accidente.
- `crear_animal` calcula `max(inventario, default=0) + 1` → ID único.
- `borrar_animal` usa `.pop()` y devuelve el registro eliminado.

**Punto fuerte:** estas funciones se pueden probar sin abrir ninguna ventana (separación de responsabilidades).

---

## 6. Sección 3 — Prueba rápida

Usa `inventario_prueba = {}` independiente:

**Crear → Leer → Actualizar (edad 2→3) → Borrar (quedan 0)**

Es una mini prueba manual. En un proyecto real se usaría `unittest` o `pytest`; aquí basta para verificar el flujo antes de la GUI.

---

## 7. Sección 4 — Interfaz gráfica (`GestorAnimales`)

### 7.1 Variables de control

```python
self.nombre_var = tk.StringVar()
self.especie_var = tk.StringVar(value=ESPECIES[0])
```

Enlazan widgets y datos: al escribir en un `Entry`, la variable se actualiza; al hacer `set()`, el campo se rellena.

### 7.2 Layout (`_crear_controles`)

Tres bloques verticales con `pack()`:

1. Formulario (`LabelFrame` “Datos del animal”) → `grid()` interno.
2. Filtros (`LabelFrame` “Buscar y filtrar”).
3. Tabla (`Treeview` + scrollbars).

**Regla de oro:** no mezclar `pack()` y `grid()` en el **mismo** contenedor. Aquí el padre usa `pack` y cada `LabelFrame` interno usa `grid`.

### 7.3 Treeview

- Columnas: id, nombre, especie, edad, peso, color, observaciones.
- `show="headings"` → sin columna fantasma del árbol.
- `selectmode="browse"` → una sola fila seleccionable.
- `iid=str(animal_id)` → el ID viaja con la fila.

### 7.4 Eventos (`bind`)

| Evento | Efecto |
| --- | --- |
| `<KeyRelease>` en búsqueda | Refresco en tiempo real |
| `<<ComboboxSelected>>` | Filtro por especie |
| `<<TreeviewSelect>>` | Carga la fila en el formulario |

### 7.5 Acciones `_crear` / `_actualizar` / `_borrar`

Patrón común:

```python
try:
    ...  # operación CRUD
except ValueError as error:
    messagebox.showerror("...", str(error))
    return
```

El borrado pide confirmación con `askyesno`.

### 7.6 `_actualizar_tabla`

Borra filas (`get_children` + `delete`) y reinserta aplicando:

- Filtro de texto en el nombre (`.casefold()`, parcial).
- Filtro de especie o “Todas”.
- Barra de estado: total / visibles.

---

## 8. Sección 5 — Ejecución

```python
raiz = tk.Tk()
aplicacion = GestorAnimales(raiz, animales)
raiz.mainloop()
```

Crea la ventana, pasa el inventario y arranca el bucle de eventos.

---

## 9. Preguntas de refactorización (y respuestas)

### 1. ¿Cómo añadirías la especie “Conejo”?

Añadir `"Conejo"` a la tupla `ESPECIES`. Combobox y filtro la leen de ahí; no hace falta reescribir la GUI.

### 2. ¿Cómo guardar datos entre sesiones?

De menor a mayor complejidad:

1. **JSON** al cerrar / abrir (`dump` / `load`; adaptar IDs si llegan como string).
2. **CSV** (más plano; se pierde anidamiento).
3. **SQLite** (tabla `animales` con `PRIMARY KEY`; las firmas CRUD apenas cambian).

### 3. ¿Cómo separarías el código en archivos?

Ya está hecho en `tarea1/`:

| Carpeta / archivo | Contenido |
| --- | --- |
| `datos/constantes.py` + `inventario.py` | `ESPECIES`, inventario inicial, CRUD |
| `validaciones/reglas.py` | `validar_datos` |
| `interfaz/gestor.py` | `GestorAnimales` |
| `app.py` / `main.py` | Arranque (`Tk` + `mainloop`) |

Ejecución: `python app.py` desde `tarea1/`.

### 4. ¿Cómo añadirías el campo “chip” (sí/no)?

1. Añadirlo a cada registro.  
2. Validarlo en `validar_datos`.  
3. `ttk.Checkbutton` + `BooleanVar`.  
4. Incluirlo en columnas del `Treeview`.  
5. Actualizar `_seleccionar` y `_datos_del_formulario`.

### 5. ¿Por qué el CRUD no usa solo clases?

El enunciado pide **diccionarios**. Por eso el inventario sigue siendo `dict`. Las clases (`AnimalRefugio` y subclases) existen en `datos/modelos.py` con herencia, `@property` y decoradores; el adaptador las construye cuando hace falta (p. ej. resumen polimórfico en la GUI).

### 6. ¿Qué pasa si dos animales tienen el mismo nombre?

No hay conflicto: el identificador único es el **ID**, no el nombre.

### 7. ¿Cómo harías estadísticas?

Botón que abra un `Toplevel` con totales por especie (`Counter`), medias de edad/peso y, opcionalmente, un `Canvas` o matplotlib.

### 8. ¿Por qué `_actualizar_tabla` borra y reinserta todo?

Con filtros, muchas filas dejan de ser visibles. Reconstruir la vista es simple y seguro. En inventarios pequeños el coste es imperceptible. A gran escala: `tabla.item(iid, values=...)`.

### 9. ¿Y si el peso se escribe con coma?

Normalizar en el formulario, por ejemplo:

```python
texto_peso = self.peso_var.get().replace(",", ".")
```

### 10. ¿Confirmación antes de salir?

```python
raiz.protocol("WM_DELETE_WINDOW", self._confirmar_salida)
```

y en `_confirmar_salida` un `askyesno`.

---

## 10. Consejos para la defensa oral

1. Empieza por lo general (CRUD + separación datos/GUI).  
2. Nombra principios: validación con excepciones, variables de control, gestores de geometría.  
3. Si piden un cambio en vivo: lee el código, di el plan en voz alta, luego edita.  
4. Si no está implementado: “lo haría así…” y describe el enfoque.  
5. Domina `pack` / `grid` / `place` (aquí no se usa `place`).

---

## 11. Checklist rápido antes de presentar

- [ ] Ejecutar `python app.py`: CRUD, filtros, ficha clínica, pegar/importar ≤ 5 MB, foto, exportar PDF.  
- [ ] Ejecutar `python ejecutar_tests.py` y abrir `tests/resultados/ultimo_informe.txt`.  
- [ ] (Opcional) `python probar_crud.py` para mostrar el CRUD sin GUI.  
- [ ] Provocar un error de validación y mostrar el `messagebox`.  
- [ ] Señalar módulos clave y diagramas en [docs/uml.md](docs/uml.md) / [docs/requisitos.md](docs/requisitos.md).  
- [ ] Tener respuesta lista para “añadir especie” y “guardar en JSON”.  
- [ ] Relacionar al menos 5 widgets con lecciones del Tema 3.  
- [ ] Usar el cuaderno solo como guion de defensa / documentación (no como sustituto de `app.py`).  
- [ ] Si alguien ejecuta el notebook: aclarar que la GUI completa es `python app.py`.  
- [ ] Conocer [docs/pruebas.md](docs/pruebas.md) y [docs/manual_usuario.md](docs/manual_usuario.md).

---

## 12. Archivos de esta carpeta

| Archivo / carpeta | Contenido |
| --- | --- |
| `app.py` / `main.py` | Programa: arranque de la GUI |
| `datos/`, `validaciones/`, `interfaz/` | Módulos del programa |
| `probar_crud.py` | Prueba CRUD sin ventana |
| `ejecutar_tests.py` | Batería unittest + informe en `tests/resultados/` |
| `docs/pruebas.md` | Cómo ejecutar tests y dónde se guarda el resultado |
| `muestras/` | Fotos y PDF/DOCX de ejemplo para probar importación |
| `Enunciado_oficial_Tarea_1.pdf` | PDF del profesor |
| `Analisis_defensa_gestion_animales.md` | Esta guía (Markdown) |
| `Tarea_1.pdf` | Esta guía en PDF |
| `README.md` | Índice de la carpeta |
| `../gestion_animales_tkinter.ipynb` | Defensa / documentación narrada |
| `docs/` | Requisitos (RF/RNF), CU, UML, manuales, pruebas |
| `exportacion/` | PDF de fichas |
| `adjuntos/` | Fotos/documentos importados por animal |
