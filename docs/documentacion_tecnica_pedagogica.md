# Documentación técnica y pedagógica

## Gestión de animales con Programación Orientada a Objetos (Python)

**Proyecto de referencia:** [gracobjo/poo_animales](https://github.com/gracobjo/poo_animales)  
**Enfoque didáctico:** migración de un diccionario Python a un modelo con clases (`Animal`, `Perro`, `Gato`)  
**Público:** estudiantes que aprenden POO y el proceso completo de desarrollo de software  
**Nivel:** especialización / refuerzo de fundamentos  

> Este documento es **autocontenido**: puedes estudiarlo sin abrir el código fuente.
> El repositorio sirve para practicar; aquí se explica *por qué* se diseñó así.

---

## Índice

1. [Introducción y objetivos](#1-introducción-y-objetivos)
2. [Análisis del problema inicial](#2-análisis-del-problema-inicial)
3. [Especificación de requisitos](#3-especificación-de-requisitos)
4. [Análisis del dominio](#4-análisis-del-dominio)
5. [Diseño de la solución](#5-diseño-de-la-solución)
6. [Etapas de codificación](#6-etapas-de-codificación-guía-paso-a-paso)
7. [Estrategia de pruebas](#7-estrategia-de-pruebas)
8. [Conceptos POO aplicados](#8-conceptos-poo-aplicados-con-ejemplos-del-proyecto)
9. [Guía para el estudiante](#9-guía-para-el-estudiante)
10. [Conclusiones](#10-conclusiones)

---

## 1. Introducción y objetivos

### 1.1 Propósito del documento

Este material acompaña el desarrollo de un sistema sencillo de **gestión de animales** (perros y gatos) en Python. No se limita a listar clases y métodos: describe el **ciclo completo** que un equipo (o un estudiante) debería seguir:

1. Entender el problema (datos sin comportamiento).
2. Definir qué debe hacer el sistema (requisitos).
3. Modelar el dominio (entidades y relaciones).
4. Diseñar módulos y responsabilidades.
5. Codificar en un orden sensato.
6. Probar (unitario, integración, casos límite).
7. Relacionar cada decisión con un pilar de la POO.

El hilo conductor es la migración desde un `dict` improvisado hasta un diseño con abstracción, herencia, encapsulamiento y polimorfismo.

### 1.2 Público objetivo

| Perfil | Qué busca en este documento |
| --- | --- |
| Estudiante de POO (primer contacto serio) | Ver *por qué* no basta un diccionario |
| Estudiante intermedio | Conectar teoría (pilares) con un repo real |
| Docente | Material de apoyo, tablas y checklist |

Se asume Python básico (variables, funciones, listas, diccionarios). No se asume experiencia previa en clases abstractas ni en tests.

### 1.3 Objetivos de aprendizaje

Al terminar, el estudiante debería ser capaz de:

1. Explicar los fallos de un modelo basado solo en diccionarios.
2. Redactar requisitos funcionales y no funcionales ligados a POO.
3. Identificar entidades, comportamientos y relaciones en un dominio pequeño.
4. Justificar una estructura de carpetas (`modelos`, `servicios`, `utils`, `tests`).
5. Describir el orden correcto de codificación (por qué no se empieza por `main.py`).
6. Diseñar pruebas unitarias y casos límite para validaciones y energía.
7. Señalar, en código concreto, dónde aparece cada pilar de la POO.
8. Proponer una especie nueva (p. ej. loro o caballo) sin romper los servicios.

### 1.4 Relación con el resto de la documentación del repo

| Documento | Enfoque |
| --- | --- |
| **Este documento** | Proceso completo: análisis → diseño → código → pruebas → pedagogía |
| [Tutorial de especialización](tutorial_especializacion.md) | Curso con ejercicios y solucionario |
| [Casos de uso](casos_de_uso.md) | Flujos del cuidador (CU) |
| [Manual de desarrollador](manual_desarrollador.md) | API y cómo extender |

---

## 2. Análisis del problema inicial

### 2.1 Escenario de partida: el diccionario

Muchos proyectos empiezan “rápido” así:

```python
perro_dict = {
    "nombre": "Rocky",
    "raza": "Labrador",
    "peso": 25.5,
    "color": "Dorado",
    "edad": 3,
    "vacunado": True,
}
```

El diccionario **guarda datos**. Eso basta para imprimir una ficha o guardar un JSON. El problema aparece en cuanto el dominio tiene **reglas** y **acciones**:

- El peso no puede ser negativo.
- Vacunar dos veces no debería ser posible (o debería controlarse).
- Un gato no “juega” igual que un perro; un perro no “caza” igual que un gato.
- Una lista mixta de animales debería poder “sonar” sin un `if` eterno por tipo.

### 2.2 Problemas detectados en el enfoque inicial

#### Falta de validación de datos

```python
perro_dict["peso"] = -10   # Python lo permite
perro_dict["edad"] = 200   # también
```

Nadie obliga a comprobar el valor *antes* de guardarlo. La validación, si existe, se copia en muchas funciones y se olvida en otras.

#### Ausencia de comportamiento

El diccionario no sabe ladrar, comer ni jugar. El comportamiento vive en funciones externas:

```python
def ladrar(animal):
    return f"{animal['nombre']} dice: ¡Guau!"
```

Cuando aparece el gato, esa función (y muchas más) crecen con `if animal["tipo"] == ...`.

#### Falta de protección de datos

Cualquiera con acceso al diccionario puede hacer:

```python
perro_dict["vacunado"] = False   # “desvacunar” sin pasar por vacunar()
```

No hay frontera entre *leer* y *cambiar con sentido*.

#### Escalabilidad limitada

| Cambio solicitado | Coste con `dict` + `if` |
| --- | --- |
| Añadir un gato | Nuevas claves + ramas en muchas funciones |
| Añadir un loro | Más ramas; riesgo de olvidar una |
| Cambiar la regla de energía al comer | Buscar y editar todos los sitios que tocan `"energia"` |
| Impedir pesos ilegales | Validar en *cada* escritura (o no validar) |

### 2.3 Justificación de por qué se necesita POO

La POO no es “más código por snobismo”. En este dominio aporta:

1. **Contrato** (`Animal`): todo animal sabe hacer sonido y declarar alimentación.
2. **Reutilización** (herencia): nombre, edad e información básica en un solo sitio.
3. **Protección** (encapsulamiento): el peso y la vacunación no se manipulan a ciegas.
4. **Extensión limpia** (polimorfismo): `emitir_sonido(animal)` no pregunta la especie.

> **Tabla comparativa 1 — Diccionario frente a clases**

| Aspecto | Enfoque `dict` | Enfoque POO (este proyecto) |
| --- | --- | --- |
| Datos | Claves de un diccionario | Atributos / propiedades |
| Comportamiento | Funciones sueltas + `if` | Métodos de cada clase |
| Validación | Manual y fácil de olvidar | Setters + validadores |
| Nuevo tipo | Abrir N funciones | Crear una clase |
| Estado ilegal | Fácil de crear | Rechazado con `ValueError` / `TypeError` |
| Ideal para | JSON, configs, registros planos | Dominio con reglas y variantes |

---

## 3. Especificación de requisitos

### 3.1 Requisitos funcionales

El sistema debe permitir:

| ID | Requisito | Ejemplo en el proyecto |
| --- | --- | --- |
| RF-01 | Crear un perro con nombre, edad, peso, color y energía | `Perro("Rocky", 3, 25.5, "Dorado")` |
| RF-02 | Crear un gato con los mismos datos básicos | `Gato("Misi", 2, 4.0, "blanco")` |
| RF-03 | Consultar una ficha básica | `info_basica()`, `str(animal)` |
| RF-04 | Emitir el sonido característico | `hacer_sonido()` / `ladrar()` / `maullar()` |
| RF-05 | Indicar el tipo de alimentación | `tipo_alimentacion()` |
| RF-06 | Alimentar (sube peso y recupera energía) | `comer(gramos)` / `alimentar(...)` |
| RF-07 | Acciones de perro: jugar, descansar, vacunar | métodos en `Perro` |
| RF-08 | Acciones de gato: ronronear, cazar, dormir | métodos en `Gato` |
| RF-09 | Operar sobre un grupo sin saber la especie | `emitir_sonido`, `listar_info`, `total_peso`, … |
| RF-10 | Filtrar por edad mínima | `animales_mayores_de(animales, n)` |

> En el repositorio actual también existe `Loro` (aprender frase, volar). Para el aprendizaje inicial basta dominar **Perro** y **Gato**; el loro demuestra que el diseño escala.

### 3.2 Requisitos no funcionales (los 4 pilares + robustez)

#### Abstracción

- Debe existir una clase base que **no se pueda instanciar**.
- Esa clase define el contrato mínimo (`hacer_sonido`, `tipo_alimentacion`) y lo común (`nombre`, `edad`, `info_basica`).

#### Herencia

- `Perro` y `Gato` reutilizan el constructor y la lógica común de `Animal`.
- Cada uno añade solo lo específico de su especie.

#### Encapsulamiento

- Peso, color, energía (y vacunación / presas) no se manipulan como campos públicos libres.
- El acceso pasa por `@property` con validación.
- Algunos datos son de **solo lectura** (`vacunado`, `presas_cazadas`).

#### Polimorfismo

- Funciones de servicio reciben un `Animal` (o una secuencia) y delegan en métodos del objeto.
- Añadir una especie no debe obligar a reescribir esas funciones.

#### Robustez

- Datos inválidos → `ValueError` (y el estado no queda a medias).
- Intentar crear `Animal(...)` → `TypeError`.
- Mensajes de error comprensibles (incluyen el nombre del campo).

> **Tabla comparativa 2 — Requisitos no funcionales y evidencia**

| Pilar / calidad | Cómo se exige | Evidencia en el diseño |
| --- | --- | --- |
| Abstracción | Clase base abstracta | `Animal(ABC)` + `@abstractmethod` |
| Herencia | Subclases concretas | `Perro(Animal)`, `Gato(Animal)` |
| Encapsulamiento | Privados + properties | `__peso`, `@property`, solo lectura |
| Polimorfismo | Servicios genéricos | `emitir_sonido(animal)` |
| Robustez | Errores explícitos | `ValueError` / `TypeError` |

---

## 4. Análisis del dominio

### 4.1 Entidades (sustantivos)

| Entidad | Descripción | Atributos principales |
| --- | --- | --- |
| Animal | Concepto genérico (no existe “solo”) | nombre, edad |
| Perro | Animal doméstico canino | peso, color, energía, vacunado |
| Gato | Animal doméstico felino | peso, color, energía, presas_cazadas |
| Grupo de animales | Colección para operaciones | lista / secuencia |
| Validador | Regla reutilizable sobre números | (no es entidad de negocio; es utilidad) |

### 4.2 Comportamientos (verbos)

| Quién | Verbos |
| --- | --- |
| Cualquier animal | hacer sonido, declarar alimentación, informar ficha |
| Perro | ladrar, comer, jugar, descansar, vacunar |
| Gato | maullar, ronronear, cazar, comer, dormir |
| Servicio de gestión | emitir sonido, alimentar, listar, filtrar por edad, sumar pesos |
| Validador | validar positivo, validar rango |

### 4.3 Relaciones (diagrama conceptual en texto)

```text
                    ┌──────────────┐
                    │   Animal     │  <<abstracto>>
                    │--------------│
                    │ nombre       │
                    │ edad         │
                    │--------------│
                    │ hacer_sonido │
                    │ tipo_alim.   │
                    │ info_basica  │
                    └──────┬───────┘
                           │
            ┌──────────────┴──────────────┐
            │                             │
            ▼                             ▼
     ┌─────────────┐               ┌─────────────┐
     │    Perro    │               │    Gato     │
     │-------------│               │-------------│
     │ peso        │               │ peso        │
     │ color       │               │ color       │
     │ energia     │               │ energia     │
     │ vacunado    │               │ presas      │
     │-------------│               │-------------│
     │ ladrar      │               │ maullar     │
     │ comer       │               │ ronronear   │
     │ jugar       │               │ cazar       │
     │ descansar   │               │ comer       │
     │ vacunar     │               │ dormir      │
     └─────────────┘               └─────────────┘

     ┌────────────────────┐
     │ gestion_animales   │  usa ──► Animal (y subclases)
     │ emitir_sonido      │
     │ alimentar          │
     │ listar_info        │
     │ animales_mayores_de│
     │ total_peso         │
     └────────────────────┘

     ┌────────────────────┐
     │ validadores        │  usa ──► Perro, Gato, Animal (edad)
     └────────────────────┘
```

**Lectura del diagrama:**

- `Perro` **es un** `Animal` (herencia).
- `Gato` **es un** `Animal`.
- Los servicios **usan** animales sin conocer la clase concreta (polimorfismo).
- Los validadores **apoyan** a modelos (no son animales).

---

## 5. Diseño de la solución

### 5.1 Justificación de la estructura de carpetas

```text
poo_animales/
├── main.py                 # Arranque (delgado)
├── ejemplos/
│   └── demo_completa.py    # Demostración / prueba de integración manual
├── src/
│   ├── modelos/            # Qué es un animal (dominio)
│   ├── servicios/          # Qué se hace con varios animales
│   └── utils/              # Validaciones reutilizables
├── tests/                  # Pruebas unitarias
└── docs/                   # Documentación (este archivo y otras guías)
```

Separar **modelos** y **servicios** evita una clase “dios” que lo haga todo. Separar **utils** evita copiar `if valor <= 0` en diez sitios. Separar **tests** deja claro que las pruebas no son el producto, pero garantizan el producto.

### 5.2 Responsabilidad de cada módulo

| Módulo | Responsabilidad | No debe |
| --- | --- | --- |
| `animal.py` | Contrato + datos comunes | Conocer perros o gatos en concreto |
| `perro.py` / `gato.py` | Estado y comportamiento de la especie | Contener lógica de listados de grupo |
| `gestion_animales.py` | Operaciones polimórficas de grupo | Tener `if isinstance(..., Perro)` |
| `validadores.py` | Reglas numéricas genéricas | Conocer nombres de animales |
| `demo_completa.py` | Mostrar el sistema de punta a punta | Definir reglas de dominio nuevas |
| `test_*.py` | Fijar el comportamiento esperado | Depender del orden de otros tests |
| `main.py` | Llamar a la demo | Contener lógica de negocio |

### 5.3 Diagrama de clases (ASCII)

```text
                         <<abstract>>
                     +------------------+
                     |      Animal      |
                     +------------------+
                     | +nombre: str    |
                     | #_edad: int      |
                     +------------------+
                     | +edad            |
                     | +info_basica()   |
                     | +hacer_sonido()* |
                     | +tipo_alimentacion()* |
                     +---------+--------+
                               |
               +---------------+---------------+
               |                               |
               v                               v
    +-------------------+           +-------------------+
    |       Perro       |           |        Gato       |
    +-------------------+           +-------------------+
    | -__peso           |           | -__peso           |
    | -__color          |           | -__color          |
    | -__energia        |           | -__energia        |
    | -__vacunado       |           | -__presas_cazadas |
    +-------------------+           +-------------------+
    | +ladrar()         |           | +maullar()        |
    | +comer(gramos)    |           | +ronronear()      |
    | +jugar()          |           | +cazar()          |
    | +descansar()      |           | +comer(gramos)    |
    | +vacunar()        |           | +dormir()         |
    +-------------------+           +-------------------+

    +------------------------------------------+
    |         gestion_animales (módulo)        |
    +------------------------------------------+
    | emitir_sonido(animal: Animal)            |
    | alimentar(animal, gramos)                |
    | listar_info(animales)                    |
    | animales_mayores_de(animales, edad_min)  |
    | total_peso(animales)                     |
    +------------------------------------------+
              | usa
              v
           Animal
```

### 5.4 Flujo de dependencias entre módulos

```text
main.py
   └── ejemplos/demo_completa.py
            ├── modelos/perro.py ──┐
            ├── modelos/gato.py  ──┼──► modelos/animal.py ──► utils/validadores.py
            └── servicios/gestion_animales.py ──► animal.py

tests/test_perro.py ──► perro.py ──► animal.py
tests/test_gato.py  ──► gato.py  ──► animal.py
```

**Regla de dependencia:** las capas de arriba conocen a las de abajo; **nunca al revés**. `animal.py` no importa la demo. `validadores.py` no importa `Perro`.

---

## 6. Etapas de codificación (guía paso a paso)

### Por qué NO se empieza por `main.py`

`main.py` es la **fachada**. Si empiezas por él, tiendes a meter reglas de negocio en el script de arranque (“ya que estoy aquí, valido el peso…”). Eso produce código difícil de probar y de reutilizar.

El orden correcto construye **de dentro hacia fuera**: reglas y modelos primero, orquestación al final.

### Paso 1 — Preparar el entorno (andamiaje)

1. Crear la estructura de carpetas (`src/modelos`, `src/servicios`, `src/utils`, `tests`, `ejemplos`).
2. Añadir `__init__.py` en cada paquete.
3. Dejar archivos vacíos listos para rellenar (script PowerShell del manual, si aplica).
4. Fijar Python 3.8+ y un `.gitignore` básico.

**Por qué primero:** sin paquetes claros, los imports se improvisan y el diseño se ensucia.

### Paso 2 — Los cimientos (clase abstracta `Animal`)

1. Definir `Animal(ABC)`.
2. Validar `nombre` y `edad`.
3. Declarar `hacer_sonido` y `tipo_alimentacion` como abstractos.
4. Implementar `info_basica`.

**Por qué ahora:** fija el contrato. Todo lo demás *encaja* en ese marco.

```python
from abc import ABC, abstractmethod

class Animal(ABC):
    def __init__(self, nombre: str, edad: int) -> None:
        self.nombre = ...  # validado
        self.edad = edad   # property 0–30

    def info_basica(self) -> str:
        return (
            f"{self.nombre} es un {self.__class__.__name__} "
            f"de {self.edad} años."
        )

    @abstractmethod
    def hacer_sonido(self) -> str:
        ...

    @abstractmethod
    def tipo_alimentacion(self) -> str:
        ...
```

### Paso 3 — Las entidades concretas (`Perro` y `Gato`)

1. `class Perro(Animal)` / `class Gato(Animal)`.
2. `super().__init__(nombre, edad)` al inicio.
3. Atributos privados (`__peso`, `__energia`, …) + `@property`.
4. Implementar abstractos (`hacer_sonido` → `ladrar` / `maullar`).
5. Métodos propios (`jugar`, `vacunar`, `cazar`, …).
6. Validar **antes** de mutar el estado.

**Por qué ahora:** ya existe el molde; puedes concentrarte en el comportamiento de cada especie.

### Paso 4 — La lógica de negocio (servicios polimórficos)

1. Escribir `emitir_sonido`, `alimentar`, `listar_info`, etc.
2. Anotar parámetros como `Animal` o secuencias de `Animal`.
3. **Prohibido** (como regla de diseño): ramificar por especie dentro del servicio.

```python
def emitir_sonido(animal: Animal) -> str:
    return animal.hacer_sonido()
```

**Por qué después de los modelos:** el servicio necesita objetos que ya cumplan el contrato.

### Paso 5 — Utilidades y punto de entrada

1. Centralizar `validar_positivo` y `validar_rango` (pueden adelantarse al paso 2–3; lo importante es no duplicarlas).
2. Escribir tests unitarios en paralelo o justo después de cada clase.
3. Montar `demo_completa.py` (integración narrativa).
4. Dejar `main.py` en una o dos líneas: importar y ejecutar la demo.

```python
# main.py — delgado a propósito
from ejemplos.demo_completa import main

if __name__ == "__main__":
    main()
```

> **Tabla comparativa 3 — Orden de desarrollo**

| Orden incorrecto (típico) | Orden recomendado | Riesgo del incorrecto |
| --- | --- | --- |
| 1. `main.py` con toda la lógica | 1. Estructura de paquetes | Código imposible de testear |
| 2. Diccionarios globales | 2. `Animal` abstracto | Sin contrato claro |
| 3. `if tipo == ...` | 3. `Perro` / `Gato` | Explosión de condicionales |
| 4. Tests “si sobra tiempo” | 4. Servicios + tests | Regresiones silenciosas |
| 5. Refactor heroico al final | 5. Demo + `main` delgado | Refactor caro y con miedo |

---

## 7. Estrategia de pruebas

### 7.1 Pruebas unitarias

**Objetivo:** verificar *una clase* (o un método) de forma aislada.

| Archivo | Qué cubre |
| --- | --- |
| `tests/test_perro.py` | Sonido, comer, jugar, descansar, vacunar, setters, abstractos cumplidos |
| `tests/test_gato.py` | Sonido, ronronear, cazar, dormir, comer, setters, solo lectura de presas |

Patrón recomendado:

```python
class TestPerro(unittest.TestCase):
    def setUp(self) -> None:
        self.perro = Perro("Rex", 4, 12.0, "marrón", energia=60)

    def test_jugar_sin_energia_no_cambia_el_estado(self) -> None:
        cansado = Perro("Tobi", 2, 8.0, "blanco", energia=10)
        with self.assertRaises(ValueError):
            cansado.jugar()
        self.assertEqual(cansado.energia, 10)
```

**Ideas de casos de prueba (perro):**

| Caso | Esperado |
| --- | --- |
| `ladrar()` | Texto con el nombre y “Guau” |
| `comer(500)` | Peso +0.5; energía +15 (tope 100) |
| `comer(0)` | `ValueError`; peso y energía iguales |
| `jugar()` con energía 60 | Energía 40 |
| `jugar()` con energía 10 | `ValueError`; energía 10 |
| `vacunar()` dos veces | Segunda → `ValueError` |
| `peso = -1` | `ValueError`; peso anterior intacto |
| `isinstance(perro, Animal)` | `True` |

**Ideas de casos de prueba (gato):**

| Caso | Esperado |
| --- | --- |
| `maullar()` | Texto con “Miau” |
| `ronronear()` con energía baja | `ValueError` |
| `cazar()` OK | Energía −25; `presas_cazadas` +1 |
| `cazar()` sin energía | Error; presas siguen en 0 |
| `presas_cazadas = 5` | `AttributeError` (solo lectura) |

Ejecución:

```bash
python -m unittest discover -s tests -v
```

### 7.2 Pruebas de integración

**Objetivo:** comprobar que las piezas **encajan** cuando se usan juntas.

En este proyecto, `ejemplos/demo_completa.py` actúa como prueba de integración *narrativa*:

1. Crea instancias de varias especies.
2. Ejecuta comportamientos propios.
3. Muestra encapsulamiento (setters que fallan, atributos privados).
4. Intenta instanciar `Animal` (debe fallar).
5. Recorre un grupo con `emitir_sonido`, `listar_info`, `alimentar`, `total_peso`.

No sustituye a los unitarios, pero detecta fallos de cableado (imports, firmas, mensajes).

### 7.3 Casos límite (edge cases)

| Situación extrema | Comportamiento esperado | Dónde se controla |
| --- | --- | --- |
| Peso 0 o negativo | `ValueError` | `validar_positivo` / setter |
| Edad −1 o 31 | `ValueError` | property `edad` |
| Energía 101 | `ValueError` | `validar_rango` |
| `True` como número | `ValueError` | validadores (excluyen `bool`) |
| Comer con tope de energía | Energía queda en 100, no 115 | `min(ENERGIA_MAXIMA, …)` |
| Jugar / cazar sin energía | Error; estado intacto | guardas al inicio del método |
| Vacunar dos veces | Error | flag `__vacunado` |
| Secuencia = string en `listar_info` | `ValueError` | `_como_lista` |
| `Animal("x", 1)` | `TypeError` | `ABC` |

**Principio de oro:** *validar antes de modificar*. Si el método lanza, el objeto debe quedar como estaba.

---

## 8. Conceptos POO aplicados (con ejemplos del proyecto)

### 8.1 Abstracción

**Definición breve:** ocultar detalles y exponer solo lo esencial; definir *qué* debe poder hacerse, no *cómo* lo hace cada variante.

**En el proyecto:** `Animal` declara el contrato y prohíbe instancias incompletas.

```python
@abstractmethod
def hacer_sonido(self) -> str:
    ...
```

**Beneficio:** el resto del código programa contra `Animal`, no contra una lista interminable de tipos.

### 8.2 Herencia

**Definición breve:** una clase reutiliza y especializa otra.

**En el proyecto:** `Perro` y `Gato` heredan nombre, edad e `info_basica`.

```python
class Perro(Animal):
    def __init__(self, nombre, edad, peso, color, energia=100):
        super().__init__(nombre, edad)
        ...
```

**Beneficio:** un cambio en la regla de edad (0–30) se hace una sola vez en `Animal`.

### 8.3 Encapsulamiento

**Definición breve:** el estado interno se protege; el exterior usa una interfaz controlada.

**En el proyecto:** `__peso` + property; `vacunado` sin setter.

```python
@property
def peso(self) -> float:
    return self.__peso

@peso.setter
def peso(self, valor: float) -> None:
    self.__peso = validar_positivo(valor, "peso")
```

**Beneficio:** imposible “columpiarse” con `peso = -5` sin un error explícito.

### 8.4 Polimorfismo

**Definición breve:** la misma operación se comporta distinto según el objeto real.

**En el proyecto:**

```python
for animal in [perro, gato]:
    print(emitir_sonido(animal))
# Rocky dice: ¡Guau!
# Misi dice: ¡Miau!
```

**Beneficio:** añadir un `Loro` no obliga a reescribir el bucle ni el servicio.

### 8.5 Mapa pilar → archivo → beneficio

| Pilar | Archivo clave | Beneficio tangible |
| --- | --- | --- |
| Abstracción | `animal.py` | Contrato único |
| Herencia | `perro.py`, `gato.py` | Menos duplicación |
| Encapsulamiento | properties + `validadores.py` | Datos coherentes |
| Polimorfismo | `gestion_animales.py` | Extensión barata |

---

## 9. Guía para el estudiante

### 9.1 Checklist de tareas (en orden)

Usa esta lista como plan de trabajo del proyecto (o de un ejercicio equivalente):

- [ ] **Entender el problema:** escribir un `perro_dict` y listar 4 debilidades
- [ ] **Requisitos:** anotar RF (qué hace) y RNF (pilares + errores)
- [ ] **Dominio:** tabla de sustantivos y verbos
- [ ] **Diseño:** boceto ASCII de clases + carpetas
- [ ] **Andamiaje:** crear paquetes y `__init__.py`
- [ ] **Código:** `validadores.py` → `animal.py` → `perro.py` → `gato.py`
- [ ] **Servicios:** `gestion_animales.py` sin `isinstance` por especie
- [ ] **Tests unitarios:** al menos sonido, comer, un fallo de energía, un setter inválido
- [ ] **Demo + main:** recorrido completo sin lógica nueva en `main.py`
- [ ] **Autoevaluación:** responder las preguntas de la sección 9.3
- [ ] **(Plus)** Añadir otra especie siguiendo el manual, sin tocar los servicios

### 9.2 Errores comunes a evitar

| Error | Por qué duele | Alternativa |
| --- | --- | --- |
| Empezar por `main.py` lleno de lógica | Impide testear | Modelos primero |
| Usar `if tipo == "perro"` en servicios | Rompe el polimorfismo | Llamar a métodos del objeto |
| Asignar `self.__peso = valor` sin validar | Estado corrupto | Pasar por el setter |
| Mutar y *después* validar | Objeto a medias si falla | Validar → luego mutar |
| Tests que comparten el mismo objeto mutable | Falsos positivos/negativos | `setUp` crea instancia nueva |
| Olvidar implementar un abstracto | `TypeError` al instanciar | Checklist de contrato |
| Tratar un `str` como lista de animales | Itera caracteres | Rechazar strings en el servicio |

### 9.3 Preguntas de autoevaluación

1. ¿Qué ocurre si ejecutas `Animal("Luna", 2)` y por qué?
2. ¿Dónde vive la regla “peso > 0” en el diseño final?
3. ¿Por qué `vacunado` no tiene setter?
4. ¿Qué ventaja tiene `emitir_sonido(animal)` frente a un `if` por especie?
5. ¿Por qué `_como_lista` rechaza un texto?
6. Si añades un `Caballo`, ¿qué archivos tocas y cuáles no?
7. Explica con un ejemplo la diferencia entre prueba unitaria y la demo.
8. Un gato con energía 10 intenta `cazar()`. ¿Qué pasa con `presas_cazadas`?

*(Respuestas orientativas: ver también el [solucionario del tutorial](tutorial_especializacion.md#solucionario-completo).)*

**Respuestas breves:**

1. `TypeError`: faltan métodos abstractos.  
2. En el setter de `peso` / `validar_positivo`.  
3. Solo debe cambiar con `vacunar()`.  
4. Extender no obliga a editar el servicio.  
5. Un `str` es iterable por caracteres.  
6. Tocas modelo + tests + demo + docs; no `gestion_animales` ni (salvo lo común) `Animal`.  
7. Unitario = un método aislado; demo = flujo completo.  
8. `ValueError` y `presas_cazadas` sigue en 0.

### 9.4 Recursos adicionales recomendados

| Recurso | Para qué |
| --- | --- |
| [Repositorio](https://github.com/gracobjo/poo_animales) | Código y demos |
| [Tutorial de especialización](tutorial_especializacion.md) | Ejercicios + solucionario |
| [Manual de desarrollador](manual_desarrollador.md) | API y extensión (loro) |
| [Casos de uso](casos_de_uso.md) | Visión funcional |
| Documentación oficial `abc` (Python) | Clases abstractas |
| Documentación `unittest` | Estilo de tests del repo |

---

## 10. Conclusiones

### 10.1 Resumen de lo aprendido

Has recorrido el camino completo:

**problema (`dict`) → requisitos → dominio → diseño → código ordenado → pruebas → pilares POO.**

El resultado no es solo “tener clases”, sino un sistema donde:

- las reglas de negocio están localizadas,
- los errores son explícitos,
- y añadir una especie no dinamita el resto.

### 10.2 Beneficios de la migración diccionario → POO

| Antes (`dict`) | Después (POO) |
| --- | --- |
| Datos sin contrato | `Animal` define el contrato |
| Validación opcional | Validación en la frontera (properties) |
| Comportamiento disperso | Métodos junto al estado |
| Extensión por `if` | Extensión por nuevas clases |
| Difícil de testear con rigor | Tests unitarios por especie + demo |

### 10.3 Posibles mejoras futuras del proyecto

Ideas razonables para continuar aprendiendo (sin reescribir todo):

1. **Nueva especie** (`Caballo`, `Pez`) siguiendo el checklist del manual.
2. **Persistencia:** guardar/cargar animales en JSON (el `dict` vuelve en la *frontera*; las clases siguen en el núcleo).
3. **Capa de aplicación:** un pequeño menú CLI o notebook didáctico.
4. **Más tests de integración automatizados** (además de la demo narrativa).
5. **(Avanzado)** introducir un patrón *Strategy* para la recuperación de energía al comer, o un *Factory* para crear animales desde un registro de configuración — solo cuando el diseño lo pida de verdad.

---

## Apéndice A — Mini glosario

| Término | Significado en este proyecto |
| --- | --- |
| Clase abstracta | Plantilla no instanciable (`Animal`) |
| Método abstracto | Obligación de las subclases |
| Property | Getter/setter con aspecto de atributo |
| Name mangling | `__peso` → `_Perro__peso` fuera de la clase |
| Duck typing | “Si tiene `comer`, se puede alimentar” |
| Caso límite | Entrada extrema (0, negativo, tope, vacío) |

## Apéndice B — Comandos esenciales

```bash
git clone https://github.com/gracobjo/poo_animales.git
cd poo_animales
python main.py
python -m unittest discover -s tests -v
```

---

*Documento alineado con el repositorio [gracobjo/poo_animales](https://github.com/gracobjo/poo_animales).  
Pensado como material de estudio independiente para cursos de especialización en POO.*
