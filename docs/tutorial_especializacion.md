# Tutorial de especialización: POO con animales

Curso práctico basado en el repositorio
[gracobjo/poo_animales](https://github.com/gracobjo/poo_animales).

**Nivel:** especialización (se asume Python básico: variables, funciones,
listas y diccionarios).  
**Duración orientativa:** 6–8 horas (teoría + ejercicios guiados).  
**Requisito:** Python 3.8 o superior. Solo biblioteca estándar.

## Qué vas a aprender

Al terminar este tutorial serás capaz de:

1. Explicar por qué un `dict` no basta cuando hay reglas de dominio y
   comportamiento distinto por tipo.
2. Identificar y aplicar los cuatro pilares: abstracción, herencia,
   encapsulamiento y polimorfismo.
3. Leer y usar el código real del repositorio (`Animal`, `Perro`, `Gato`,
   `Loro`, servicios y tests).
4. Añadir una especie nueva sin tocar los servicios polimórficos.
5. Contrastar, con el mismo problema, la solución con diccionarios y la
   solución orientada a objetos.

## Materiales del curso

| Recurso | Uso en el curso |
| --- | --- |
| [Repositorio](https://github.com/gracobjo/poo_animales) | Código fuente |
| [README](../README.md) | Visión general y reglas de dominio |
| [Casos de uso](casos_de_uso.md) | Qué puede hacer el cuidador |
| [Manual de desarrollador](manual_desarrollador.md) | API y guía para añadir especies |
| Este tutorial | Recorrido pedagógico paso a paso |

---

## Unidad 0. Preparación del entorno

### 0.1 Clonar el proyecto

```bash
git clone https://github.com/gracobjo/poo_animales.git
cd poo_animales
python --version
```

### 0.2 Ejecutar la demo y las pruebas

```bash
python main.py
python -m unittest discover -s tests -v
```

**Ejercicio guiado 0.** Anota en una hoja:

- Cuántos animales crea la demo.
- Qué ocurre si intentas vacunar al perro dos veces.
- Qué mensaje sale al intentar `Animal("Fantasma", 1)`.

Comprueba tus notas con la salida de `python main.py`.

---

## Unidad 1. El mismo problema, primero con diccionarios

Antes de POO, muchas veces modelamos un animal así:

```python
perro = {
    "tipo": "perro",
    "nombre": "Rex",
    "edad": 5,
    "peso": 12.0,
    "color": "marrón",
    "energia": 80,
    "vacunado": False,
}

gato = {
    "tipo": "gato",
    "nombre": "Misi",
    "edad": 3,
    "peso": 4.5,
    "color": "blanco",
    "energia": 70,
    "presas_cazadas": 0,
}
```

### 1.1 Comportamiento con `if` por tipo

```python
def hacer_sonido(animal: dict) -> str:
    if animal["tipo"] == "perro":
        return f"{animal['nombre']} dice: ¡Guau!"
    if animal["tipo"] == "gato":
        return f"{animal['nombre']} dice: ¡Miau!"
    if animal["tipo"] == "loro":
        frase = animal.get("frase", "")
        if frase:
            return f"{animal['nombre']} dice: {frase}"
        return f"{animal['nombre']} dice: ¡Aaah!"
    raise ValueError("Tipo de animal desconocido.")


def comer(animal: dict, gramos: float) -> None:
    if gramos <= 0:
        raise ValueError("'gramos' debe ser mayor que cero.")
    animal["peso"] += gramos / 1000
    if animal["tipo"] == "perro":
        animal["energia"] = min(100, animal["energia"] + 15)
    elif animal["tipo"] == "gato":
        animal["energia"] = min(100, animal["energia"] + 10)
    elif animal["tipo"] == "loro":
        animal["energia"] = min(100, animal["energia"] + 12)
    else:
        raise ValueError("Tipo de animal desconocido.")
```

Cada especie nueva obliga a abrir **todas** las funciones y añadir otra
rama. Si alguien escribe `"Perro"` en lugar de `"perro"`, el código falla
en silencio o en un sitio lejano. Si alguien hace
`perro["peso"] = -5`, el diccionario lo acepta: no hay validación.

### 1.2 Problemas típicos del enfoque con `dict`

| Problema | Ejemplo |
| --- | --- |
| Claves opacas | `"energia"` frente a `"energía"`; un typo no se detecta al escribir |
| Sin contrato | Nada obliga a que un “loro” tenga `frase` |
| Validación dispersa | Hay que recordar validar en cada función |
| Crecimiento frágil | Un animal nuevo = cambiar N funciones con `if` |
| Estado mutable sin control | `animal["vacunado"] = True` desde cualquier sitio |
| Comportamiento mezclado con datos | El `dict` solo guarda datos; la lógica vive fuera |

### Ejercicio guiado 1 (dict)

Copia este fragmento en un archivo temporal `sandbox_dict.py` y ejecútalo:

```python
animales = [
    {"tipo": "perro", "nombre": "Rex", "edad": 5, "peso": 12.0, "energia": 80},
    {"tipo": "gato", "nombre": "Misi", "edad": 3, "peso": 4.5, "energia": 70},
]

def total_peso(grupo):
    return sum(a["peso"] for a in grupo)

# 1) Imprime el peso total.
print(total_peso(animales))

# 2) Rompe el modelo a propósito:
animales[0]["peso"] = -10
print(total_peso(animales))  # ¿tiene sentido un peso negativo?

# 3) Añade un loro solo en la lista, sin tocar hacer_sonido.
#    ¿Qué pasa si llamas hacer_sonido al loro sin haber añadido la rama?
```

**Pregunta de reflexión:** ¿dónde pondrías la regla “el peso debe ser
mayor que cero” para que nadie pueda saltársela?

Guarda esa respuesta: en POO la respuesta es el *setter* de la propiedad
`peso`.

---

## Unidad 2. Abstracción: el contrato `Animal`

En el repositorio, `src/modelos/animal.py` define *qué* es un animal, no
*cómo* suena cada especie.

```python
from abc import ABC, abstractmethod

class Animal(ABC):
    def __init__(self, nombre: str, edad: int) -> None:
        self.nombre = ...   # validado
        self.edad = edad    # property con rango 0–30

    def info_basica(self) -> str:
        return f"{self.nombre} es un {self.__class__.__name__} de {self.edad} años."

    @abstractmethod
    def hacer_sonido(self) -> str:
        ...

    @abstractmethod
    def tipo_alimentacion(self) -> str:
        ...
```

- `ABC` + `@abstractmethod` = no se puede crear un `Animal` “genérico”.
- `info_basica()` es concreto: todas las especies lo heredan.
- `hacer_sonido()` y `tipo_alimentacion()` son el **contrato**: cada
  subclase debe implementarlos.

### Ejercicio guiado 2

Desde la raíz del proyecto, abre un intérprete:

```bash
python
```

```python
from src.modelos.animal import Animal
from src.modelos.perro import Perro

try:
    Animal("Fantasma", 1)
except TypeError as e:
    print("Abstracción:", e)

rex = Perro("Rex", 5, 12.0, "marrón")
print(rex.info_basica())
print(isinstance(rex, Animal))
```

**Esperado:**

- `TypeError` al instanciar `Animal`.
- `Rex es un Perro de 5 años.`
- `True` en `isinstance`.

**Comparación con dict:** con un diccionario no hay forma de *impedir*
crear un animal incompleto. Con `ABC`, Python lo impide en tiempo de
ejecución.

---

## Unidad 3. Herencia: `Perro`, `Gato` y `Loro`

Cada especie reutiliza nombre, edad e `info_basica()`, e implementa lo
suyo.

| Clase | Archivo | Métodos propios | Alimentación |
| --- | --- | --- | --- |
| `Perro` | `src/modelos/perro.py` | `ladrar`, `comer`, `jugar`, `descansar`, `vacunar` | omnívoro |
| `Gato` | `src/modelos/gato.py` | `maullar`, `ronronear`, `cazar`, `comer`, `dormir` | carnívoro |
| `Loro` | `src/modelos/loro.py` | `hablar`, `aprender`, `volar`, `comer` | granívoro |

Patrón del constructor (ejemplo del loro):

```python
def __init__(self, nombre, edad, peso, color, energia=100):
    super().__init__(nombre, edad)  # valida en la base
    self.__frase = ""
    self.peso = peso                # pasa por el setter
    self.color = color
    self.energia = energia
```

### Ejercicio guiado 3

```python
from src.modelos.gato import Gato
from src.modelos.loro import Loro
from src.modelos.perro import Perro

perro = Perro("Rex", 5, 12.0, "marrón", energia=80)
gato = Gato("Misi", 3, 4.5, "blanco", energia=70)
loro = Loro("Kiko", 4, 0.4, "verde", energia=50)

print(perro.ladrar())
print(gato.maullar())
print(loro.hablar())          # aún sin frase → graznido
print(loro.aprender("Hola"))
print(loro.hablar())          # ahora repite la frase

print(perro.tipo_alimentacion())
print(gato.tipo_alimentacion())
print(loro.tipo_alimentacion())
```

**Tarea:** sin mirar el código, predice la energía de `Rex` después de
`perro.jugar()` (parte de 80; jugar cuesta 20). Compruébalo.

**Comparación con dict:** en el enfoque con diccionarios, “aprender una
frase” sería otra función suelta y otra clave opcional. Aquí el método
vive *dentro* del loro y solo el loro sabe cómo actualizar `__frase`.

---

## Unidad 4. Encapsulamiento: propiedades y validación

Los atributos con doble guion bajo (`__peso`, `__energia`, `__frase`) no
son accesibles como `objeto.__peso` desde fuera. Python los renombra
(*name mangling*). El acceso correcto es la `@property`.

```python
@property
def peso(self) -> float:
    return self.__peso

@peso.setter
def peso(self, valor: float) -> None:
    self.__peso = validar_positivo(valor, "peso")
```

Algunas propiedades son de **solo lectura**: `vacunado`, `presas_cazadas`,
`frase`. Solo cambian con `vacunar()`, `cazar()` o `aprender()`.

Los validadores reutilizables están en `src/utils/validadores.py`:

- `validar_positivo(valor, nombre_campo)`
- `validar_rango(valor, minimo, maximo, nombre_campo)`

### Ejercicio guiado 4

```python
from src.modelos.perro import Perro

rex = Perro("Rex", 5, 12.0, "marrón")

# Lectura y escritura controlada
print(rex.peso)
rex.peso = 13.5
print(rex.peso)

# Rechazo: el estado no cambia
try:
    rex.peso = -1
except ValueError as e:
    print("Rechazado:", e)
print("Peso intacto:", rex.peso)

# Name mangling
try:
    print(rex.__peso)
except AttributeError as e:
    print("Privado:", e)

# Solo lectura
rex.vacunar()
try:
    rex.vacunado = False
except AttributeError as e:
    print("Solo lectura:", e)
```

**Comparación con dict:**

```python
# Con dict, esto “funciona” y corrompe los datos:
animal = {"peso": 12.0}
animal["peso"] = -1          # nadie lo detiene
animal["vacunado"] = False   # cualquiera puede mentir
```

Con clases, la regla vive **junto al dato**. Quien usa el objeto no
puede saltársela sin provocar un error explícito.

---

## Unidad 5. Polimorfismo: una llamada, muchos comportamientos

Los servicios de `src/servicios/gestion_animales.py` no preguntan la
especie:

```python
def emitir_sonido(animal: Animal) -> str:
    return animal.hacer_sonido()

def alimentar(animal: Animal, gramos: float) -> str:
    return animal.comer(gramos)
```

La misma función produce ladrido, maullido o frase según la clase real.
Eso es polimorfismo.

### Ejercicio guiado 5

```python
from src.modelos.gato import Gato
from src.modelos.loro import Loro
from src.modelos.perro import Perro
from src.servicios.gestion_animales import (
    alimentar,
    animales_mayores_de,
    emitir_sonido,
    listar_info,
    total_peso,
)

animales = [
    Perro("Rex", 5, 12.0, "marrón"),
    Gato("Misi", 3, 4.5, "blanco"),
    Loro("Kiko", 4, 0.4, "verde"),
]

for a in animales:
    print(emitir_sonido(a), "|", a.tipo_alimentacion())

print(listar_info(animales))
print("Peso total:", total_peso(animales))
print("Mayores de 4:", [a.nombre for a in animales_mayores_de(animales, 4)])

for a in animales:
    print(alimentar(a, 100))
```

**Observación clave:** no hay `if isinstance(a, Perro)` en el bucle. Si
mañana añades un `Caballo` con `hacer_sonido` y `comer`, este mismo
código sigue funcionando.

### Comparación directa: dict vs POO en polimorfismo

```python
# --- Con dict: hay que ramificar ---
def emitir_sonido_dict(animal: dict) -> str:
    if animal["tipo"] == "perro":
        return f"{animal['nombre']} dice: ¡Guau!"
    if animal["tipo"] == "gato":
        return f"{animal['nombre']} dice: ¡Miau!"
    # ... cada especie nueva abre esta función


# --- Con POO: una sola línea ---
def emitir_sonido_poo(animal) -> str:
    return animal.hacer_sonido()
```

| Criterio | `dict` + `if` | Clases + polimorfismo |
| --- | --- | --- |
| Añadir especie | Editar muchas funciones | Crear una clase nueva |
| Validación | Manual y repetida | Centralizada en propiedades |
| Autocompletado / IDE | Claves como strings | Métodos y atributos tipados |
| Estado ilegal | Fácil de crear | Rechazado con `ValueError` |
| Contrato | Informal (documentación) | Formal (`ABC` + abstractos) |
| Ideal para | Datos planos, JSON, configs | Dominio con reglas y comportamiento |

**Cuándo sí usar un `dict`:** lecturas de JSON, configuración, tablas
temporales, o cuando el dato es solo un registro sin comportamiento.  
**Cuándo preferir clases:** cuando el dato tiene reglas, acciones y
variantes (perro / gato / loro).

---

## Unidad 6. Recorrido del proyecto real

### Mapa mental

```text
Cuidador / demo / tests
        │
        ▼
┌───────────────────┐
│  servicios/       │  emitir_sonido, alimentar, listar_info...
│  gestion_animales │  (polimorfismo)
└─────────┬─────────┘
          │
          ▼
┌───────────────────┐
│  modelos/         │  Animal ← Perro, Gato, Loro
│  (herencia +      │
│   encapsulamiento)│
└─────────┬─────────┘
          │
          ▼
┌───────────────────┐
│  utils/           │  validar_positivo, validar_rango
│  validadores      │
└───────────────────┘
```

### Ejercicio guiado 6 — leer código con propósito

Abre cada archivo y responde (una frase por archivo):

1. `animal.py` — ¿Qué métodos son abstractos y por qué?
2. `perro.py` — ¿Qué ocurre si llamas `vacunar()` dos veces?
3. `gato.py` — ¿`ronronear()` consume energía? ¿Por qué?
4. `loro.py` — ¿Quién puede cambiar `frase`?
5. `gestion_animales.py` — ¿Por qué `_como_lista` rechaza un `str`?
6. `validadores.py` — ¿Por qué se rechaza un `bool` aunque sea
   subclase de `int`?

Contrasta tus respuestas con los [casos de uso](casos_de_uso.md) y el
[manual](manual_desarrollador.md).

---

## Unidad 7. Ejemplo guiado completo: del dict al objeto

Vamos a traducir un escenario concreto.

### 7.1 Versión con diccionarios (frágil)

```python
def jugar_perro(animal: dict) -> None:
    if animal["tipo"] != "perro":
        raise ValueError("Solo los perros juegan así.")
    if animal["energia"] < 20:
        raise ValueError("Energía insuficiente.")
    animal["energia"] -= 20


rex = {"tipo": "perro", "nombre": "Rex", "energia": 15}
# Alguien, por error, salta la función:
rex["energia"] = 100   # trampa: no pasó por jugar_perro
jugar_perro(rex)
```

### 7.2 Versión con el repositorio (robusta)

```python
from src.modelos.perro import Perro

rex = Perro("Rex", 5, 12.0, "marrón", energia=15)
try:
    rex.jugar()
except ValueError as e:
    print(e)              # Energía insuficiente...
print(rex.energia)        # sigue en 15

rex.descansar()           # +25 → 40
print(rex.jugar())        # ahora sí; energía 20
```

No hay forma limpia de “hacer trampa” bajando la energía a mano sin
pasar por la propiedad (y esa propiedad solo acepta 0–100, no evita
jugar con poca energía: eso lo controla `jugar()`).

### Ejercicio guiado 7

1. Crea un gato con energía 10.
2. Intenta `cazar()`. Debe fallar y dejar `presas_cazadas` en 0.
3. Llama a `dormir()` y vuelve a `cazar()`.
4. Comprueba `presas_cazadas == 1`.

Solución esperada (no mires hasta intentarlo):

```python
from src.modelos.gato import Gato

misi = Gato("Misi", 3, 4.5, "blanco", energia=10)
try:
    misi.cazar()
except ValueError:
    pass
assert misi.presas_cazadas == 0
misi.dormir()
misi.cazar()
assert misi.presas_cazadas == 1
```

---

## Unidad 8. Añadir una especie (práctica de especialización)

Sigue la guía detallada del
[manual, sección 7](manual_desarrollador.md#7-cómo-añadir-una-especie).
Aquí va el resumen pedagógico.

### Ejercicio guiado 8 — diseñar un `Caballo` (en papel o en código)

Sin implementar todavía (o implementándolo si tienes tiempo), responde:

1. ¿Qué devuelve `hacer_sonido()`? (ej. `"{nombre} dice: ¡Hiii!"`)
2. ¿`tipo_alimentacion()`? (ej. `"herbívoro"`)
3. ¿Qué método propio tiene? (ej. `galopar`, coste 35 de energía)
4. ¿Necesita `comer(gramos)`? Si sí, ¿cuánta energía recupera?
5. ¿Hay algún dato de solo lectura? (ej. `carreras_ganadas`)

**Checklist mínimo** (igual que el loro):

- [ ] `class Caballo(Animal)` en `src/modelos/caballo.py`
- [ ] `super().__init__(nombre, edad)` al inicio
- [ ] Métodos abstractos implementados
- [ ] Propiedades validadas
- [ ] Export en `__init__.py`
- [ ] `tests/test_caballo.py`
- [ ] Una línea en la demo
- [ ] Tests en verde: `python -m unittest discover -s tests -v`

**Lo que no tocas:** `animal.py` (salvo datos comunes a todos) ni
`gestion_animales.py`.

---

## Unidad 9. Tabla resumen dict vs POO (para el examen / memoria)

| Pregunta | Respuesta con `dict` | Respuesta con POO (este repo) |
| --- | --- | --- |
| ¿Dónde viven los datos? | Claves del diccionario | Atributos / propiedades |
| ¿Dónde vive el comportamiento? | Funciones externas con `if` | Métodos de cada clase |
| ¿Cómo se valida? | A mano, si te acuerdas | Setters + validadores |
| ¿Cómo se añade un tipo? | Nuevas ramas en muchas funciones | Nueva clase |
| ¿Se puede crear un tipo incompleto? | Sí | No (abstractos / constructor) |
| ¿Quién controla `vacunado` / `frase`? | Cualquiera con la clave | Solo el método adecuado |
| ¿Una lista mixta cómo suena? | `if` por `"tipo"` | `animal.hacer_sonido()` |
| ¿Tests? | Comprueban funciones y claves | Comprueban objetos y contratos |

### Mini-reto final

Escribe en 10 líneas (como máximo) por qué, en este dominio de animales
con energía, vacunas y frases, las clases son más adecuadas que una
lista de diccionarios. Usa al menos dos pilares de POO en tu respuesta.

---

## Unidad 10. Autoevaluación

Marca lo que ya sabes hacer sin mirar apuntes:

- [ ] Explicar por qué `Animal(...)` lanza `TypeError`
- [ ] Crear un `Perro`, un `Gato` y un `Loro` válidos
- [ ] Provocar y capturar un `ValueError` de un setter
- [ ] Usar `emitir_sonido` y `total_peso` con una lista mixta
- [ ] Decir qué archivo no hay que modificar al añadir una especie
- [ ] Contrastar el mismo caso (`comer` / peso negativo) en dict y en POO
- [ ] Ejecutar la demo y la batería de tests del repositorio

Si marcas menos de 5, repite las unidades 2, 4 y 5.  
Si marcas 7, estás listo para el ejercicio del `Caballo` (unidad 8).

---

## Solucionario breve de los ejercicios guiados

| Ej. | Idea de la solución |
| --- | --- |
| 0 | 3 animales; segunda vacuna → `ValueError`; `Animal` → `TypeError` |
| 1 | El peso negativo se acepta en el dict; el loro sin rama falla o hay que ampliar `hacer_sonido` |
| 2 | Abstracción vía `ABC`; `Perro` sí es `Animal` |
| 3 | Tras jugar: energía 60; alimentaciones distintas por especie |
| 4 | Setter rechaza; `__peso` no existe fuera; `vacunado` sin setter |
| 5 | Tres sonidos distintos con el mismo `emitir_sonido` |
| 7 | Cazar falla con energía 10; tras dormir, una presa |
| 8 | Nueva clase + export + tests; servicios intactos |

---

## Próximos pasos (ampliación del curso)

1. Leer todos los [casos de uso](casos_de_uso.md) y mapear cada CU a un
   método del código.
2. Seguir el
   [manual para añadir especies](manual_desarrollador.md#7-cómo-añadir-una-especie)
   e implementar `Caballo`.
3. Añadir un test de integración que cree las tres especies, las
   alimente y compruebe `total_peso`.
4. (Avanzado) Serializar un `Perro` a `dict` para JSON y volver a crear
   el objeto: verás que el `dict` sirve en la frontera del sistema, y la
   clase en el núcleo del dominio.

---

## Referencias del repositorio

- Código: [https://github.com/gracobjo/poo_animales](https://github.com/gracobjo/poo_animales)
- Demo: `python main.py`
- Tests: `python -m unittest discover -s tests -v`
- Documentación técnica: [manual de desarrollador](manual_desarrollador.md)
- Escenarios funcionales: [casos de uso](casos_de_uso.md)
