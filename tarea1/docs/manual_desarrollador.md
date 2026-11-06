# Manual de desarrollador — Refugio Animal

Guía para **mantener y evolucionar** el código ante cambios de enunciado o sugerencias del tribunal. Cada sección indica **qué tocar**, **en qué orden** y **qué verificar**.

Docs relacionados: [requisitos](requisitos.md) · [casos de uso](casos_de_uso.md) · [UML](uml.md) · [usuario](manual_usuario.md) · [pruebas](pruebas.md).

---

## 1. Visión general

CRUD Tkinter sobre diccionarios, con ficha clínica, adjuntos, portapapeles, PDF y tests.

| Capa | Ubicación | Responsabilidad |
| --- | --- | --- |
| Arranque | `app.py`, `main.py` | `Tk`, inventario, `mainloop` |
| Presentación | `interfaz/` | GUI, estilos, ficha clínica, portapapeles, miniatura |
| Dominio | `datos/` | CRUD, persistencia JSON del inventario, ficha clínica, adjuntos, **modelos POO**, **catálogo de especies** |
| Reglas | `validaciones/reglas.py` | `validar_datos` (+ listas clínicas) |
| Exportación | `exportacion/pdf_fichas.py` | PDF por animal |
| Pruebas | `tests/`, `ejecutar_tests.py` | unittest + informes |
| Muestras | `muestras/` | Fotos/PDF/DOCX de demo |

El cuaderno `../gestion_animales_tkinter.ipynb` es **defensa/documentación**, no el ejecutable.

La GUI del cuaderno **no coincide** con `app.py` / `main.py`: es una versión reducida (CRUD + panel POO) para explicar el flujo en celdas. La interfaz de entrega (`interfaz/gestor.py`) añade foto, ficha clínica, PDF, estilos y el mismo panel POO. Tabla comparativa: [../README.md](../README.md#cuaderno-vs-programa-apppy--mainpy).

**Principio de defensa:** la lógica vive fuera de Tkinter. Si el tribunal pide un cambio de regla, casi siempre se responde en `validaciones/` o `datos/`; si pide un cambio visual, en `interfaz/`.

---

## 2. Entorno

```bash
pip install fpdf2 Pillow
cd tarea1
python app.py
# o: python main.py
python ejecutar_tests.py
```

| Paquete | Uso |
| --- | --- |
| stdlib | `tkinter`, `unittest`, `ctypes` (CF_HDROP) |
| `fpdf2` | PDF |
| `Pillow` | Miniaturas JPG, pegar imagen, embeber foto en PDF |

`app.py` inserta `tarea1` en `sys.path` para imports locales.

---

## 3. Estructura del proyecto

```text
tarea1/
├── app.py / main.py / ejecutar_tests.py / probar_crud.py
├── datos/
│   ├── constantes.py      # ESPECIES, PESO_MIN_KG, PESO_MAX_KG
│   ├── inventario.py              # CRUD + animales_iniciales
│   ├── persistencia_inventario.py # inventario.json (separado del catálogo)
│   ├── ficha.py                   # Normalización clínica
│   ├── adjuntos.py                # Copia/pegar bytes, límite 5 MB
│   ├── modelos.py                 # AnimalRefugio ABC + subclases (@property)
│   ├── decoradores.py             # @cuenta_usos (decorador propio)
│   ├── adaptador_poo.py           # dict ↔ objeto + resumen polimórfico
│   ├── gestor_especies.py         # Catálogo + especies_personalizadas.json
│   └── recursos.py                # Logo
├── validaciones/reglas.py
├── interfaz/
│   ├── gestor.py          # Ventana principal + panel foto
│   ├── ficha_clinica.py   # Diálogo pestañas
│   ├── estilos.py         # ttk.Style / tipografía
│   ├── vista_foto.py      # Miniatura Tk/Pillow
│   └── portapapeles.py    # CF_HDROP + Tk clipboard + ImageGrab
├── exportacion/pdf_fichas.py
├── adjuntos/<id>/fotos|documentos/
├── muestras/{fotos,documentos}/
├── tests/ + tests/resultados/
└── docs/
```

---

## 4. Modelo de datos

```python
{
  id: {
    "nombre", "especie", "edad", "peso", "color", "observaciones",
    "foto": "ruta o ''",
    "tratamientos": [{"fecha","descripcion","veterinario"}, ...],
    "vacunaciones": [{"fecha","vacuna","proxima"}, ...],
    "documentos": [{"nombre","ruta","fecha"}, ...],
  }
}
```

- Claves internas en ASCII (`descripcion`, `proxima`); textos de UI en español con ñ/tildes.
- `actualizar_animal` **preserva** campos clínicos si el formulario principal no los envía.
- `borrar_animal` elimina también `adjuntos/<id>/`.

---

## 5. Mapa de impacto (qué capa tocar)

Usa esta tabla en defensa: *«según el tipo de cambio, se modifica esta capa»*.

| Tipo de petición | Capa principal | Archivos típicos |
| --- | --- | --- |
| Nuevo valor de lista (especie, etc.) | Constantes | `datos/constantes.py` |
| Cambiar rango/regla (edad, peso…) | Validación (+ etiqueta UI) | `validaciones/reglas.py`, a veces `constantes.py`, etiqueta en `gestor.py` |
| Nuevo campo del animal | Dominio → validación → UI → PDF → tests → docs | Ver §7.1 |
| Nuevo botón / panel / filtro | Solo presentación | `interfaz/gestor.py` (o nuevo módulo) |
| Ficha clínica / adjuntos | Dominio clínico + diálogo | `ficha.py`, `adjuntos.py`, `ficha_clinica.py` |
| PDF distinto | Exportación | `exportacion/pdf_fichas.py` |
| Aspecto (fuentes, colores) | Estilos | `interfaz/estilos.py` |
| Datos de demostración | Inventario / muestras | `inventario.py`, `muestras/` |
| Nueva prueba | Tests | `tests/test_*.py` |

**Orden canónico de un cambio de dominio:**

1. Constantes (si aplica)  
2. `validar_datos` / normalizadores  
3. CRUD / inventario (si el campo se guarda o se inicializa)  
4. Formulario / Treeview / ficha clínica  
5. PDF (si debe salir impreso)  
6. Tests  
7. Docs (RF/RN, manual usuario, UML, este manual)

---

## 6. Cómo actualizar la interfaz

### 6.1 Layout actual (`GestorAnimales._crear_controles`)

El padre usa `pack()`; cada `LabelFrame` interno usa `grid()`. **No mezclar** `pack` y `grid` en el mismo contenedor.

Bloques:

1. Título / subtítulo  
2. Zona datos: formulario (izq.) + foto (der.)  
3. Botones de acción (Añadir, Actualizar, Borrar, Limpiar, Ficha clínica, Exportar PDF…)  
4. Filtros (texto + especie)  
5. `Treeview` + scrollbars  
6. Barra de estado (`estado_var`)

### 6.2 Añadir un widget al formulario

1. Crear `tk.StringVar` (u otra) en `__init__`.  
2. En `_crear_controles`: `Label` + `Entry`/`Combobox`/`Checkbutton` con `grid(row=…, column=…)`.  
3. En `_datos_del_formulario`: leer la variable y meterla en el `dict`.  
4. En `_cargar_seleccion` / `_limpiar_formulario`: `set()` / vaciar.  
5. Si el valor debe verse en la tabla: columna en `_crear_controles` (Treeview) + `_actualizar_tabla`.  
6. Si es dato de negocio: pasar por `validar_datos` (nunca confiar solo en la UI).

### 6.3 Añadir un botón

En la fila de botones de `gestor.py`:

```python
ttk.Button(marco, text="…", command=self._mi_accion).pack(side="left", padx=4)
```

Implementar `_mi_accion` con el patrón:

```python
try:
    ...
except ValueError as error:
    messagebox.showerror("Error", str(error))
    return
self._actualizar_tabla()
self.estado_var.set("…")
```

### 6.4 Nuevo diálogo (ventana secundaria)

Preferible **módulo nuevo** en `interfaz/` (como `ficha_clinica.py`):

- Recibe `parent`, `inventario`, `animal_id` (o el registro).  
- Usa `Toplevel` + `grab_set` si debe ser modal.  
- Al guardar, escribe en el inventario y deja que `gestor` refresque la tabla/foto.

### 6.5 Tipografía y tema

Todo el look & feel centralizado en `interfaz/estilos.py` (`aplicar_tema`, `configurar_texto`). Evitar fuentes distintas repartidas por widgets.

### 6.6 Checklist rápido de UI

- [ ] Widget enlazado a `StringVar` (o similar)  
- [ ] Lectura en `_datos_del_formulario`  
- [ ] Carga/limpieza coherentes  
- [ ] Validación en dominio si el dato persiste  
- [ ] Treeview / PDF / estado si el usuario debe ver el resultado  
- [ ] Test GUI con `Tk()` + `withdraw()` y mocks de `messagebox` / `filedialog`

---

## 7. Catálogo de alteraciones (defensa)

Casos que el tribunal suele pedir. Para cada uno: **dónde** y **qué no olvidar**.

### 7.1 Nuevo campo en la ficha (ej. `sexo`, `chip`, `estado_adopcion`)

| Paso | Archivo |
| --- | --- |
| Validar / normalizar | `validaciones/reglas.py` (`validar_datos`) |
| Iniciales / CRUD si hace falta default | `datos/inventario.py` |
| Formulario + variables + tabla | `interfaz/gestor.py` |
| PDF | `exportacion/pdf_fichas.py` |
| Tests | `tests/test_validaciones.py`, `test_datos.py`, `test_interfaz.py` |
| Docs | `requisitos.md` (RF/RN), `manual_usuario.md`, `uml.md`, casos de uso |

Si el campo es solo clínico (no va en el formulario principal): `ficha.py` + `ficha_clinica.py` (+ PDF).

### 7.2 Nueva especie

1. Añadir el literal en `ESPECIES` (`datos/constantes.py`).  
2. El `Combobox` y el filtro leen `ESPECIES` → la UI se actualiza sola.  
3. Opcional: un animal de ejemplo en `animales_iniciales()`.  
4. Test: crear/validar con esa especie.  
5. Actualizar subtítulo de la ventana si aún dice «perros, gatos y loros».

### 7.3 Cambiar rangos (edad, peso, tamaño de adjunto)

| Constante / regla | Dónde |
| --- | --- |
| Edad 0–30 | `validaciones/reglas.py` + etiqueta «Edad (0-30)» en `gestor.py` |
| Peso | `PESO_MIN_KG` / `PESO_MAX_KG` en `constantes.py` + mensaje en `reglas.py` + etiqueta en `gestor.py` |
| Límite 5 MB | `datos/adjuntos.py` (+ mensaje en ficha clínica / tests) |

Siempre: actualizar `test_validaciones` (y RN en `requisitos.md`).

### 7.4 Campo obligatorio ↔ opcional

Solo `validaciones/reglas.py` (quitar o añadir el `if not …`). Ajustar manual de usuario y tests negativos/positivos.

### 7.5 Renombrar etiqueta o mensaje de error

- Textos de pantalla: `gestor.py`, `ficha_clinica.py`, `estilos` (títulos).  
- Mensajes de negocio: `raise ValueError("…")` en `reglas.py` / `inventario.py` / `adjuntos.py`.  
- La GUI ya muestra `str(error)` → no hace falta duplicar el texto en el botón.

### 7.6 Nueva columna en la tabla

En `gestor.py`:

1. `columns=` del `Treeview` y `heading` / `column`.  
2. Tupla de valores en `_actualizar_tabla`.  
3. Si la columna es filtrable, extender `_actualizar_tabla` (hoy: nombre parcial + especie).

### 7.7 Nuevo filtro (por color, por rango de edad, etc.)

1. Widget en el `LabelFrame` de filtros.  
2. Lógica dentro de `_actualizar_tabla` (mantener filtros composables).  
3. Test de interfaz que deje N animales y compruebe filas visibles.

### 7.8 Nuevo botón de negocio (estadísticas, adoptar, archivar…)

1. Función pura en `datos/` o `validaciones/` si transforma el inventario.  
2. Botón + handler en `gestor.py`.  
3. Si necesita gráficos: `Toplevel` nuevo; no hinchar el constructor principal.  
4. Tests unitarios de la función pura + smoke GUI opcional.

### 7.9 Persistencia en disco (JSON)

Ya hay **dos** archivos JSON, a propósito separados:

| Pieza | Dónde |
| --- | --- |
| Catálogo de especies | `datos/especies_personalizadas.json` vía `gestor_especies.py` |
| Inventario de animales | `datos/inventario.json` vía `persistencia_inventario.py` |
| Carga al arrancar | `app.py` → `cargar_inventario()` |
| Guardado tras CRUD / clínica | `GestorAnimales._persistir_inventario()` |
| Tests de GUI | `persistir=False` para no tocar el JSON real |
| Claves `str`→`int` | En el loader |
| Rutas de foto/documentos | Relativas a `adjuntos/` |

Escritura atómica (temporal + `replace`). No meter I/O dentro de `validar_datos`.

### 7.10 Capa POO (ya incorporada) y cómo ampliarla

**Qué hay hoy**

| Concepto | Dónde |
| --- | --- |
| ABC + herencia | `datos/modelos.py` → `AnimalRefugio` ← `Perro`/`Gato`/`Conejo`/`Loro`/`Hamster` |
| Getters / setters | `@property` + `@nombre.setter`, `@edad.setter`, … |
| Decoradores stdlib | `@abstractmethod`, `@classmethod`, `@property` |
| Decorador propio | `@cuenta_usos` en `datos/decoradores.py` (usado en `info_basica`) |
| Adaptador | `registro_a_animal` / `animal_a_campos` / `resumen_polimorfico` |
| Ficha POO | `cuidados_especificos()` + `generar_ficha()` en `AnimalRefugio` |
| Especies personalizadas | `EspeciePersonalizada` + `gestor_especies.py` + `especies_personalizadas.json` |
| Uso en GUI | Panel ficha POO; botón *Gestionar especies* (`dialogo_especies.py`); combos refrescan el catálogo |
| Textos largos en ficha | `Text` + scrollbar en *Comportamiento*, *Alimentación* y *Cuidados* (`gestor.py`) |
| Logo del refugio | `datos/recursos.py` → `refugio.png` / `.jpg` en cabecera Tkinter y PDF (`pdf_fichas.py`) |
| Tests | `tests/test_modelos_poo.py`, `tests/test_gestor_especies.py`, ficha/especies en `tests/test_interfaz.py` |

**Nueva especie con clase**

1. Literal en `ESPECIES`.  
2. Subclase en `modelos.py` + entrada en `CLASES_POR_ESPECIE`.  
3. Test de sonido / adaptador.  
4. Docs UML / RF-03.

**El CRUD no cambia:** sigue validando con `validar_datos` y guardando `dict`. Los setters de la clase refuerzan las mismas reglas cuando se usa el adaptador.

### 7.10b Sustituir del todo el inventario por objetos

Si el tribunal pidiera *solo* clases (sin dict):

1. Inventario `Dict[int, AnimalRefugio]` (o lista).  
2. Serializar clínica en atributos o composición (`FichaClinica`).  
3. Adaptar GUI/PDF a getters.  
4. Hoy **no** es el diseño principal porque el enunciado pide diccionarios.

### 7.11 Cambios en ficha clínica (tratamiento, vacuna, documento, foto)

| Elemento | Archivos |
| --- | --- |
| Forma del registro clínico | `datos/ficha.py` |
| Copiar/pegar/límite tamaño | `datos/adjuntos.py` |
| UI pestañas | `interfaz/ficha_clinica.py` |
| Miniatura principal | `vista_foto.py` + panel en `gestor.py` |
| Pegar desde Explorador | `portapapeles.py` |
| Tests | `test_ficha_clinica.py`, `test_portapapeles.py` |

### 7.12 Exportación PDF

| Petición | Dónde |
| --- | --- |
| Más campos / otra maquetación | `exportacion/pdf_fichas.py` |
| Solo selección vs todos los visibles | Handler en `gestor.py` (ya distingue) |
| Fuente / zoom inicial | Helvetica + `set_display_mode` en el mismo módulo |
| Dependencia ausente | Import **perezoso** de `fpdf` (evitar romper el arranque GUI) |

### 7.13 Internacionalización / textos

No hay i18n: literales en español en UI y `ValueError`. Para un cambio puntual, buscar el string. Para varios idiomas: capa de mensajes (dict) usada por reglas y GUI.

### 7.14 Datos de demostración y muestras

| Qué | Dónde |
| --- | --- |
| Animales al arrancar | `cargar_inventario()`; si no hay JSON, siembra `animales_iniciales()` |
| Ficheros de ejemplo | `muestras/` + `muestras/generar_muestras.py` |
| Adjuntos de sesión | `adjuntos/<id>/` (generados en runtime; no versionar basura) |

### 7.15 Arranque, título, tamaño de ventana

- Título / `geometry` / `minsize`: `__init__` de `GestorAnimales`.  
- Inventario inyectado: `app.py` / `main.py` (`cargar_inventario()` → `GestorAnimales`).  
- Para demos: se puede pasar otro `dict` y `persistir=False` sin tocar la clase.

### 7.16 Tests y regresión tras un cambio del tribunal

```bash
python ejecutar_tests.py
# → tests/resultados/ultimo_informe.txt
```

| Cambio | Tests mínimos |
| --- | --- |
| Regla nueva | `test_validaciones` (caso ok + caso error) |
| CRUD | `test_datos` |
| Widget / flujo | `test_interfaz` |
| Clínica / 5 MB | `test_ficha_clinica` |
| PDF | `test_exportacion_pdf` |
| Portapapeles | `test_portapapeles` |
| Herencia / properties | `test_modelos_poo` |

### 7.17 Documentación que debe ir al día

Tras un cambio aceptado en defensa:

1. `docs/requisitos.md` (RF / RN)  
2. `docs/manual_usuario.md` (si el usuario lo nota)  
3. `docs/casos_de_uso.md` / `uml.md` si cambia el flujo o el modelo  
4. Este manual si aparece un **tipo nuevo** de extensión  
5. `Analisis_defensa_gestion_animales.md` si la pregunta típica de oral cambia

---

## 8. Interfaz — detalles técnicos útiles en oral

### Tipografía

`aplicar_tema` + `configurar_texto`: evita Courier en `tk.Text`.

### Portapapeles

Orden en `leer_portapapeles()`:

1. `CF_HDROP` (archivos del Explorador) con ctypes tipado.  
2. Imagen (`ImageGrab`).  
3. Texto Tkinter (`clipboard_get`) → ruta de fichero o contenido `.txt`.

No usar `ctypes.wstring_at` sin `GlobalLock` tipado (provocaba access violation).

### Foto

- Formulario: `cargar_miniatura` en panel derecho.  
- PDF: miniatura JPEG embebida; `set_display_mode(100, "single")` evita `/FitH` lento.

### Tests GUI

`Tk()` + `withdraw()`, mock de `messagebox` / `filedialog`. Sin `mainloop`.

---

## 9. Estilo de código

- Type hints y docstrings breves.  
- Dominio → `ValueError` con mensaje para la GUI.  
- Validaciones **sin** depender de Tkinter.  
- Textos visibles al usuario en español correcto.  
- Evitar ciclos de import: listas y límites en `constantes.py`.

---

## 10. Frases útiles ante el tribunal

- *«La validación está centralizada en `validar_datos`; la interfaz solo captura y muestra errores.»*  
- *«Para una especie nueva solo tocamos `ESPECIES`; el combobox y el filtro se alimentan de esa tupla.»*  
- *«Un campo nuevo atraviesa constantes/reglas → inventario → gestor → PDF → tests → docs.»*  
- *«Los adjuntos y el límite de 5 MB viven en `datos/adjuntos.py`, no en el diálogo.»*  
- *«El PDF es un módulo aparte: si falla `fpdf2`, la GUI puede seguir abriendo.»*  
- *«Herencia y `@property` están en `modelos.py`; el CRUD sigue en diccionarios vía el adaptador.»*

---

## 11. Checklist de entrega / defensa

- [ ] `python app.py` (o `main.py`)  
- [ ] CRUD + filtros + ficha clínica + pegar/importar ≤ 5 MB  
- [ ] Exportar PDF con foto  
- [ ] `python ejecutar_tests.py` OK  
- [ ] Docs y UML alineados con el código  
- [ ] Saber localizar en 30 s: especies, peso/edad, formulario, Treeview, PDF, tests  
