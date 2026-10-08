# Plantilla maestra: diseño y estructura de proyectos Python (POO)

Documento **vivo**: cópialo al inicio de cada proyecto nuevo, rellena el
diseño **antes** de programar y usa la estructura como base de carpetas.

Está pensada para el nivel **Estándar / Mediano** (la opción más versátil
para aprender y escalar). Incluye criterios para saber cuándo *no* usarla.

**Proyecto de referencia (ejemplo relleno):**
[gracobjo/poo_animales](https://github.com/gracobjo/poo_animales)

---

## Cómo usarla en la práctica

1. Copia este archivo a tu nuevo repo (o a una carpeta de plantillas).
2. Rellena la **Fase 2** a mano (sustituye la columna “Tu proyecto”).
3. Crea las carpetas de la **Fase 1** (script PowerShell al final).
4. Programa siguiendo el orden de la **Fase 3**.
5. Cierra con el checklist de la **Fase 4**.

---

## Fase 0: Evaluación del alcance

Marca con ✅ el nivel. Confirma que esta plantilla encaja.

| Nivel | Qué es | ¿Usar esta plantilla? |
| --- | --- | --- |
| 1 | Script / aprendizaje puro (1–3 archivos, sin tests) | **No.** Un solo `.py` basta. |
| 2 | Proyecto estándar / educativo / librería (≈4–20 archivos, lógica clara, tests) | **✅ Sí. Esta plantilla.** |
| 3 | App empresarial / DDD (varios equipos, BD complejas, microservicios) | **No.** Arquitectura por dominios: Domain / Application / Infrastructure. |
| 4 | Proyecto gobernado por un framework (Django, FastAPI “full”, Flask app factory) | **Parcial.** Respeta la estructura del framework; reutiliza solo Fase 2 y 4. |

> **Este repo (`poo_animales`)** es Nivel 2. La API FastAPI en `src/api/` es
> una ampliación opcional (hacia Nivel 4 ligero), no el núcleo didáctico.

---

## Fase 1: Estructura de carpetas (Src Layout)

Estructura **estándar** recomendada para proyectos Python medianos.
Sustituye `nombre_del_proyecto` y `[entidad]` / `[gestion]` por tu dominio.

```text
nombre_del_proyecto/
│
├── .gitignore                 # venv, __pycache__, .env, .idea, …
├── README.md                  # Qué es, cómo ejecutar, mapa de docs
├── requirements.txt           # Dependencias externas (vacío o mínimo al inicio)
├── main.py                    # Punto de entrada delgado
│
├── src/                       # Código fuente (paquete raíz)
│   ├── __init__.py
│   │
│   ├── modelos/               # Entidades y estado (“las cosas”)
│   │   ├── __init__.py
│   │   ├── base.py            # Clases abstractas / ABC (opcional el nombre)
│   │   └── [entidad].py       # Clases concretas (usuario.py, producto.py, …)
│   │
│   ├── servicios/             # Lógica que orquesta modelos (polimorfismo)
│   │   ├── __init__.py
│   │   └── [gestion].py       # ej. gestion_inventario.py
│   │
│   └── utils/                 # Herramientas transversales
│       ├── __init__.py
│       └── validadores.py
│
├── tests/                     # Pruebas unitarias
│   ├── __init__.py
│   └── test_[entidad].py
│
└── ejemplos/                  # Demos de flujo completo
    ├── __init__.py
    └── demo_flujo_principal.py
```

### Ampliaciones opcionales (cuando hagan falta)

| Necesidad | Dónde |
| --- | --- |
| Documentación larga | `docs/` (casos de uso, tutorial, plantillas) |
| API HTTP + Swagger | `src/api/` (FastAPI) — ver evolución en Fase 5 |
| Persistencia | `src/repositorios/` o `src/infraestructura/` |

### Nota sobre nombres en el proyecto Animales

En [poo_animales](https://github.com/gracobjo/poo_animales) la clase abstracta
está en `src/modelos/animal.py` (no en `base.py`). **Ambos son válidos:**

- `base.py` / `entidad_base.py` → plantilla genérica.
- `animal.py` → el nombre refleja el dominio (más claro en un curso de animales).

Lo importante es: **una clase ABC + concretas en `modelos/`**, no el nombre del archivo.

---

## Fase 2: Plantilla de diseño OOP

**No escribas código** hasta tener esta tabla clara.
Sustituye la columna *Tu proyecto*. La de Animales es el ejemplo ya resuelto.

| Elemento de diseño | Tu proyecto (rellenar) | Ejemplo — Proyecto Animales |
| --- | --- | --- |
| **Objetivo del sistema** | ¿Qué problema resuelve? | Gestionar estado y comportamiento de mascotas (perros, gatos, loros) con reglas claras. |
| **Entidades (clases)** | ¿Cuáles son abstractas? ¿Cuáles concretas? | Abstracta: `Animal`. Concretas: `Perro`, `Gato`, `Loro`. |
| **Atributos (estado)** | ¿Qué datos? ¿Cuáles privados / sensibles? | Público: `nombre`. Protegido/privado: `_edad`, `__peso`, `__energia`, `__vacunado` / `__presas_cazadas` / `__frase`. |
| **Métodos (comportamiento)** | ¿Qué hace cada entidad por sí misma? | Comunes: `hacer_sonido()`, `tipo_alimentacion()`, `info_basica()`, `comer()`. Perro: `ladrar`, `jugar`, `descansar`, `vacunar`. Gato: `maullar`, `ronronear`, `cazar`, `dormir`. Loro: `hablar`, `aprender`, `volar`. |
| **Relaciones** | ¿Herencia (*es un*)? ¿Composición (*tiene un*)? | `Perro` / `Gato` / `Loro` *es un* `Animal` (herencia). El inventario de la API *tiene* animales (colección). |
| **Reglas de negocio** | Validaciones en setters o métodos | Peso > 0. Edad 0–30. Energía 0–100. No vacunar dos veces. No cazar/jugar/volar sin energía. |
| **Servicios polimórficos** | ¿Qué operaciones reciben la clase base? | `emitir_sonido`, `alimentar`, `listar_info`, `animales_mayores_de`, `total_peso`. |
| **Fuera de alcance (v1)** | ¿Qué NO harás aún? | BD real, auth, UI gráfica (salvo demo consola / API opcional). |

### Mini-reglas al rellenar

1. Si un sustantivo no tiene comportamiento propio, quizá sea un **atributo**, no una clase.
2. Si un verbo necesita saber el tipo concreto con muchos `if`, candida a **método polimórfico** en la jerarquía.
3. Toda regla “nunca debe pasar X” → **setter**, constructor o método que valide **antes** de mutar.

---

## Fase 3: Flujo de trabajo de codificación (orden obligatorio)

Este orden evita imports circulares y bases flojas.

| Paso | Nombre | Qué haces | Por qué en este orden |
| --- | --- | --- | --- |
| 1 | **Andamiaje** | Carpetas, `__init__.py`, `.gitignore`, `venv` | Sin paquete claro, los imports se improvisan. |
| 2 | **Cimientos (abstracción)** | Clase base + `@abstractmethod` | Fija el contrato del dominio. |
| 3 | **Ladrillos (concretas)** | Herencia, `__`, `@property`, `ValueError` | Cada especie/entidad cumple el contrato. |
| 4 | **Cerebro (servicios)** | Funciones sobre la clase base | Aquí brilla el polimorfismo. |
| 5 | **Seguridad (tests)** | `test_[entidad].py` — feliz + error | Congela las reglas de negocio. |
| 6 | **Escaparate** | `ejemplos/demo_….py` + `main.py` delgado | Demuestra el flujo; no mete reglas nuevas. |

### Comandos útiles (Windows / PowerShell)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
# Crear árbol: ver script Crear-Archivo al final de este documento
python main.py
python -m unittest discover -s tests -v
```

### Qué no hacer

| Anti-patrón | Problema |
| --- | --- |
| Empezar por un `main.py` gordo | Lógica imposible de testear |
| Meter `if tipo == "perro"` en servicios | Rompes el polimorfismo |
| Validar *después* de asignar | Objeto a medias si falla |
| Saltar los tests “para luego” | Regresiones y miedo a refactorizar |

---

## Fase 4: Checklist de calidad POO (autoevaluación)

Antes de dar el proyecto por cerrado:

### Abstracción

- [ ] Hay al menos una clase `ABC` que **no** se puede instanciar.
- [ ] Los `@abstractmethod` cubren lo que *toda* subclase debe saber hacer.
- [ ] Intentar `ClaseBase(...)` lanza `TypeError` (lo has comprobado).

### Encapsulamiento

- [ ] Datos críticos con `_` o `__` (y acceso vía `@property` cuando haga falta).
- [ ] Los setters validan y lanzan `ValueError` (o similar).
- [ ] Datos de solo lectura (`vacunado`, contadores, etc.) **sin** setter público.

### Herencia

- [ ] Las hijas llaman a `super().__init__(...)` cuando corresponde.
- [ ] Las hijas aportan comportamiento o estado propio (no solo renombrar).
- [ ] Lo común vive en la base; lo específico, en la hija.

### Polimorfismo

- [ ] Existe ≥ 1 función en `servicios/` tipada con la **clase base**.
- [ ] Esa función **no** ramifica con `isinstance` por cada hija (salvo casos excepcionales y documentados).
- [ ] Añadir una hija nueva no obliga a reescribir ese servicio.

### Ingeniería básica

- [ ] `main.py` es delgado.
- [ ] Hay tests de caso feliz y de error para reglas críticas.
- [ ] README explica cómo ejecutar demo y tests.

---

## Fase 5: Escalabilidad (si el proyecto crece)

| Si necesitas… | Cómo evolucionar `src/` |
| --- | --- |
| Base de datos | `src/repositorios/` o `src/infraestructura/`. Los modelos siguen siendo dominio; el repositorio persiste. |
| API web | `src/api/` o `src/interfaces/api/` (FastAPI/Flask). `main` / `uvicorn` arrancan el servidor. En Animales: ver [api_swagger.md](api_swagger.md). |
| Lógica muy compleja | Migrar hacia DDD: `dominio/` (reglas puras) + `aplicacion/` (casos de uso) + `infraestructura/`. |
| Muchas utilidades | Partir `utils/` en submódulos: `utils/fechas.py`, `utils/archivos.py`, … |
| Muchos documentos | Carpeta `docs/` con mapa en el README (como este repo). |

### Del Nivel 2 hacia API (ejemplo Animales)

```text
src/
├── modelos/      ← sin cambios (núcleo POO)
├── servicios/    ← sin cambios
├── utils/        ← sin cambios
└── api/          ← NUEVO: FastAPI + schemas + store en memoria
```

Swagger documenta la **capa HTTP**, no sustituye el diseño OOP de la Fase 2.

---

## Consejo final

> La estructura no es un fin en sí mismo: gestiona complejidad.  
> **3 archivos** → esta plantilla es exceso (*over-engineering*).  
> **30 archivos en un solo `main.py`** → caos.  
> **Esta plantilla** → equilibrio para la mayoría de proyectos de aprendizaje y profesionales pequeños.

---

## Anexo A — Script PowerShell: crear el andamiaje

Ejecutar en la **carpeta padre** del proyecto. Cambia `nombre_del_proyecto`.

```powershell
function Crear-Archivo($ruta) {
    $carpeta = Split-Path $ruta -Parent
    if ($carpeta -and -not (Test-Path $carpeta)) {
        New-Item -ItemType Directory -Force -Path $carpeta | Out-Null
    }
    New-Item -ItemType File -Force -Path $ruta | Out-Null
}

$p = "nombre_del_proyecto"   # <-- cambia esto

Crear-Archivo "$p\src\modelos\base.py"
Crear-Archivo "$p\src\modelos\__init__.py"
Crear-Archivo "$p\src\servicios\gestion.py"
Crear-Archivo "$p\src\servicios\__init__.py"
Crear-Archivo "$p\src\utils\validadores.py"
Crear-Archivo "$p\src\utils\__init__.py"
Crear-Archivo "$p\src\__init__.py"
Crear-Archivo "$p\tests\test_ejemplo.py"
Crear-Archivo "$p\tests\__init__.py"
Crear-Archivo "$p\ejemplos\demo_flujo_principal.py"
Crear-Archivo "$p\ejemplos\__init__.py"
Crear-Archivo "$p\main.py"
Crear-Archivo "$p\README.md"
Crear-Archivo "$p\requirements.txt"
Crear-Archivo "$p\.gitignore"
Crear-Archivo "$p\docs\PLANTILLA_DISENO.md"

Write-Host "Andamiaje creado. Revisa con: cd $p; tree /F" -ForegroundColor Green
```

Comprobar:

```powershell
cd nombre_del_proyecto
tree /F
```

> `New-Item -Force` deja el archivo **vacío** si ya existía. Úsalo solo al crear la estructura la primera vez.

---

## Anexo B — Correspondencia con `poo_animales`

| Pieza de la plantilla | En este repositorio |
| --- | --- |
| `modelos/base.py` | `src/modelos/animal.py` |
| Entidades concretas | `perro.py`, `gato.py`, `loro.py` |
| Servicios | `src/servicios/gestion_animales.py` |
| Utils | `src/utils/validadores.py` |
| Tests | `tests/test_perro.py`, `test_gato.py`, `test_loro.py`, `test_api.py` |
| Demo | `ejemplos/demo_completa.py` + `main.py` |
| Docs del proceso | [documentacion_tecnica_pedagogica.md](documentacion_tecnica_pedagogica.md) |
| Curso con ejercicios | [tutorial_especializacion.md](tutorial_especializacion.md) |
| API opcional | [api_swagger.md](api_swagger.md) |

---

## Anexo C — Plantilla en blanco (para imprimir / copiar rápido)

```text
PROYECTO: _______________________________  FECHA: __________

Nivel (Fase 0): [ ]1  [x]2  [ ]3  [ ]4

Objetivo:
___________________________________________________________

Entidades abstractas:
___________________________________________________________

Entidades concretas:
___________________________________________________________

Atributos públicos / privados:
___________________________________________________________

Métodos por entidad:
___________________________________________________________

Relaciones (herencia / composición):
___________________________________________________________

Reglas de negocio (validaciones):
___________________________________________________________

Servicios polimórficos previstos:
___________________________________________________________

Fuera de alcance v1:
___________________________________________________________
```

---

*Plantilla alineada con el enfoque del repositorio poo_animales.
Adáptala; no la sigas como dogma si tu alcance es Nivel 1 o Nivel 3.*
