# API HTTP y Swagger

Capa **opcional** sobre el dominio POO. El curso de clases (`Animal`,
`Perro`, `Gato`, `Loro`) no depende de ella. Sirve para exponer el mismo
comportamiento por REST y documentarlo con **Swagger UI**.

Repositorio: [gracobjo/poo_animales](https://github.com/gracobjo/poo_animales)

## Arquitectura

```text
Cliente / Swagger UI
        │  HTTP JSON
        ▼
┌───────────────────┐
│  src/api/app.py   │  FastAPI (rutas + OpenAPI)
│  schemas.py       │  Contratos JSON (Pydantic)
│  store.py         │  Inventario en memoria
└─────────┬─────────┘
          │ usa
          ▼
┌───────────────────┐
│  modelos +        │  Núcleo POO (sin cambios)
│  gestion_animales │
└───────────────────┘
```

Swagger documenta la **API**. Las reglas de peso, energía y vacunación
siguen viviendo en las clases.

## Instalación

Desde la raíz del proyecto (hace falta red la primera vez):

```bash
pip install -r requirements.txt
```

El núcleo POO (`python main.py` y los tests de modelos) sigue funcionando
**sin** estas dependencias.

## Arranque

```bash
uvicorn src.api.app:app --reload
```

| URL | Qué es |
| --- | --- |
| http://127.0.0.1:8000/ | Estado del servicio |
| http://127.0.0.1:8000/docs | **Swagger UI** (probar endpoints) |
| http://127.0.0.1:8000/redoc | ReDoc (otra vista OpenAPI) |
| http://127.0.0.1:8000/openapi.json | Especificación OpenAPI |

## Endpoints principales

| Método | Ruta | Descripción |
| --- | --- | --- |
| `GET` | `/` | Salud + enlace a `/docs` |
| `GET` | `/animales` | Listar (`?edad_minima=` opcional) |
| `GET` | `/animales/{id}` | Ficha de un animal |
| `GET` | `/animales/resumen/peso-total` | Suma de pesos |
| `POST` | `/animales/perros` | Alta de perro |
| `POST` | `/animales/gatos` | Alta de gato |
| `POST` | `/animales/loros` | Alta de loro |
| `POST` | `/animales/{id}/sonido` | `emitir_sonido` (polimorfismo) |
| `POST` | `/animales/{id}/alimentar` | Body `{"gramos": 200}` |
| `POST` | `/animales/{id}/acciones/jugar` | Solo perro |
| `POST` | `/animales/{id}/acciones/cazar` | Solo gato |
| `POST` | `/animales/{id}/acciones/volar` | Solo loro |
| `DELETE` | `/animales` | Vaciar inventario (demo/tests) |

### Ejemplo con curl

```bash
curl -X POST http://127.0.0.1:8000/animales/perros ^
  -H "Content-Type: application/json" ^
  -d "{\"nombre\":\"Rex\",\"edad\":5,\"peso\":12,\"color\":\"marron\",\"energia\":80}"

curl -X POST http://127.0.0.1:8000/animales/1/sonido
```

En bash (Linux/macOS), usa `\` en lugar de `^`.

## Errores

| Situación | HTTP |
| --- | --- |
| JSON inválido / peso ≤ 0 en el schema | 422 |
| Regla de dominio (`ValueError`, p. ej. jugar sin energía) | 400 |
| Id inexistente | 404 |

## Pruebas

```bash
python -m unittest tests.test_api -v
```

Si FastAPI no está instalado, esos tests se **omiten** (`skip`) y el resto
de la batería POO sigue en verde.

## Relación con el aprendizaje de POO

| Capa | Pregunta que responde |
| --- | --- |
| Modelos | ¿Qué es un animal y qué reglas tiene? |
| Servicios | ¿Cómo opero un grupo sin `if` por especie? |
| API + Swagger | ¿Cómo expongo eso a otros sistemas / alumnos por HTTP? |

No sustituye el [tutorial](tutorial_especializacion.md) ni la
[documentación técnica-pedagógica](documentacion_tecnica_pedagogica.md):
es una ampliación de presentación.
