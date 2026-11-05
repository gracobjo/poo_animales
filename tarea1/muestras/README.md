# Muestras para probar la importación

Archivos de ejemplo (no son datos clínicos reales) para ejercitar **Foto** y **Documentos** en la ficha clínica.

## Contenido

```text
muestras/
├── fotos/
│   ├── perro_labrador.png
│   ├── gato_atigrado.png
│   ├── loro_verde.png
│   ├── conejo_blanco.png
│   └── hamster_dorado.png
├── documentos/
│   ├── tratamiento_medico_ejemplo.pdf
│   ├── tratamiento_medico_ejemplo.docx
│   ├── hoja_vacunacion_ejemplo.pdf
│   ├── hoja_vacunacion_ejemplo.docx
│   └── consentimiento_adopcion_ejemplo.txt
├── generar_muestras.py
└── README.md
```

Las imágenes son **ilustraciones genéricas** generadas por script (no fotografías de animales reales). Los PDF/DOCX simulan informes de tratamientos y hojas de vacunación.

## Cómo usarlas en la app

1. Arranca el programa: `python app.py`
2. Selecciona un animal en la tabla (p. ej. Luna).
3. Pulsa **Ficha clínica / adjuntos**.
4. Pestaña **Foto** → *Elegir / importar foto...* → navega a `tarea1/muestras/fotos/` y elige un PNG.
5. Pestaña **Documentos** → *Importar documento...* → elige un PDF o DOCX de `tarea1/muestras/documentos/`.

Los archivos se **copian** a `tarea1/adjuntos/<id>/`; las muestras originales no se modifican.

## Regenerar las muestras

Si borras los ficheros o quieres volver a crearlos:

```bash
python tarea1/muestras/generar_muestras.py
```

Requisitos del generador: `Pillow` y `fpdf2` (ya listados en el `requirements.txt` del repo).
