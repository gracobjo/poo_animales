# Animales POO

Proyecto de ejemplo en Python para practicar los cuatro pilares de la programación orientada a objetos con un modelo sencillo de animales.

Repositorio: [https://github.com/gracobjo/poo_animales](https://github.com/gracobjo/poo_animales)

`Animal` es una clase abstracta. `Perro`, `Gato` y `Loro` la heredan, guardan su estado en atributos privados y exponen ese estado con propiedades validadas. Las funciones de `gestion_animales` trabajan con cualquier animal sin preguntar de qué especie es.

Solo usa la biblioteca estándar. Requiere Python 3.8 o superior.

## Documentación

| Documento | Para qué sirve |
| --- | --- |
| [Casos de uso](docs/casos_de_uso.md) | Qué puede hacer quien usa la biblioteca: registrar, alimentar, vacunar, cazar y consultar un grupo. Incluye flujos alternativos y errores. |
| [Manual de desarrollador](docs/manual_desarrollador.md) | Arquitectura, API, errores y pruebas. Incluye cómo crear las carpetas por primera vez y [cómo añadir una especie nueva](docs/manual_desarrollador.md#7-cómo-añadir-una-especie) (ejemplo paso a paso con el loro). |

## Conceptos implementados

### Abstracción

`Animal` hereda de `ABC` y no se puede instanciar. Declara los métodos abstractos `hacer_sonido()` y `tipo_alimentacion()`, y el método concreto `info_basica()`. La edad se guarda en `_edad` y se lee o modifica con la propiedad `edad`.

### Herencia

`Perro` y `Gato` reutilizan el constructor, la edad y la información básica de `Animal`. Cada uno implementa los métodos abstractos y añade su propio comportamiento:

- **Perro:** `ladrar`, `comer`, `jugar`, `descansar`, `vacunar`
- **Gato:** `maullar`, `ronronear`, `cazar`, `comer`, `dormir`
- **Loro:** `hablar`, `aprender`, `volar`, `comer`

### Encapsulamiento

El peso, el color y la energía usan doble guion bajo (`__peso`, `__color`, `__energia`). Desde fuera de la clase esos nombres no son visibles: Python aplica *name mangling*. Los getters y setters (`@property`) validan los datos y lanzan `ValueError` cuando no sirven. `vacunado`, `presas_cazadas` y `frase` son de solo lectura.

### Polimorfismo

`emitir_sonido`, `alimentar`, `listar_info`, `animales_mayores_de` y `total_peso` reciben un `Animal` o una secuencia de animales. La misma llamada produce el ladrido de un perro, el maullido de un gato o la frase de un loro según la clase real del objeto.

## Estructura del proyecto

```text
animales_poo/
├── main.py
├── README.md
├── .gitignore
├── docs/
│   ├── casos_de_uso.md
│   └── manual_desarrollador.md
├── ejemplos/
│   ├── __init__.py
│   └── demo_completa.py
├── src/
│   ├── __init__.py
│   ├── modelos/
│   │   ├── __init__.py
│   │   ├── animal.py
│   │   ├── perro.py
│   │   ├── gato.py
│   │   └── loro.py
│   ├── servicios/
│   │   ├── __init__.py
│   │   └── gestion_animales.py
│   └── utils/
│       ├── __init__.py
│       └── validadores.py
└── tests/
    ├── __init__.py
    ├── test_perro.py
    ├── test_gato.py
    └── test_loro.py
```

## Instrucciones de ejecución

Clonar y ejecutar desde la raíz del proyecto:

```bash
git clone https://github.com/gracobjo/poo_animales.git
cd poo_animales
python main.py
```

Para lanzar las pruebas unitarias:

```bash
python -m unittest discover -s tests -v
```

## Ejemplo de uso

```python
from src.modelos.gato import Gato
from src.modelos.loro import Loro
from src.modelos.perro import Perro
from src.servicios.gestion_animales import alimentar, emitir_sonido, total_peso

perro = Perro("Rex", 5, 12.0, "marrón")
gato = Gato("Misi", 3, 4.5, "blanco")
loro = Loro("Kiko", 4, 0.4, "verde")

print(emitir_sonido(perro))          # Rex dice: ¡Guau!
print(emitir_sonido(gato))           # Misi dice: ¡Miau!
print(emitir_sonido(loro))           # Kiko dice: ¡Aaah!
loro.aprender("Hola")
print(emitir_sonido(loro))           # Kiko dice: Hola
print(alimentar(perro, 200))
print(total_peso([perro, gato, loro]))

perro.jugar()
gato.cazar()
loro.volar()
```

Un peso negativo, una edad fuera de 0–30 o una segunda vacunación lanzan `ValueError`. Intentar `Animal("Fantasma", 1)` lanza `TypeError`, porque la clase es abstracta.

## Reglas de dominio

| Dato | Regla |
| --- | --- |
| Nombre | Texto no vacío; se recortan los espacios |
| Edad | Entero entre 0 y 30, inclusive |
| Peso | Número mayor que cero (kg) |
| Color | Texto no vacío |
| Energía | Número entre 0 y 100 |
| Comer | Cada 1000 g suman 1 kg y recuperan energía, sin pasar de 100 |
| Jugar (perro) | Consume 20 de energía |
| Descansar (perro) | Recupera 25 de energía |
| Cazar (gato) | Consume 25 de energía y suma una presa |
| Dormir (gato) | Recupera 40 de energía |
| Ronronear (gato) | Exige al menos 20 de energía y no la consume |
| Hablar (loro) | Repite la frase aprendida, o grazna si no hay ninguna |
| Aprender (loro) | Guarda una frase no vacía. `frase` es de solo lectura |
| Volar (loro) | Consume 30 de energía |
| Comer (loro) | Recupera 12 de energía, sin pasar de 100 |
