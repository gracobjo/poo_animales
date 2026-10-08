"""Aplicación FastAPI con documentación Swagger automática.

Arranque desde la raíz del proyecto::

    uvicorn src.api.app:app --reload

Swagger UI: http://127.0.0.1:8000/docs
OpenAPI JSON: http://127.0.0.1:8000/openapi.json

Esta capa es opcional. El curso de POO no depende de ella: los modelos
y servicios siguen siendo usables desde ``main.py`` sin instalar FastAPI.
"""

from typing import List, Optional

from fastapi import FastAPI, HTTPException, Query, status

from src.api.schemas import (
    AlimentarBody,
    AnimalCreate,
    AnimalResponse,
    HealthResponse,
    MensajeResponse,
    PesoTotalResponse,
)
from src.api.store import a_respuesta, inventario
from src.modelos.gato import Gato
from src.modelos.loro import Loro
from src.modelos.perro import Perro
from src.servicios.gestion_animales import (
    alimentar,
    animales_mayores_de,
    emitir_sonido,
    total_peso,
)

app = FastAPI(
    title="API Animales POO",
    description=(
        "Capa HTTP sobre el dominio de animales del curso de POO. "
        "Las clases ``Perro``, ``Gato`` y ``Loro`` siguen encapsulando "
        "las reglas; esta API solo las expone por REST. "
        "Documentación interactiva en **/docs** (Swagger UI)."
    ),
    version="1.0.0",
    contact={
        "name": "poo_animales",
        "url": "https://github.com/gracobjo/poo_animales",
    },
)


def _http_desde_value_error(error: ValueError) -> HTTPException:
    """Traduce un error de dominio a HTTP 400."""
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=str(error),
    )


def _animal_o_404(animal_id: int):
    animal = inventario.obtener(animal_id)
    if animal is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No existe el animal con id {animal_id}.",
        )
    return animal


@app.get(
    "/",
    response_model=HealthResponse,
    tags=["Sistema"],
    summary="Estado del servicio",
)
def raiz() -> HealthResponse:
    """Comprueba que la API está en marcha y enlaza a Swagger."""
    return HealthResponse(
        servicio="API Animales POO",
        swagger="/docs",
        mensaje=(
            "Núcleo POO intacto. Usa /docs para probar los endpoints."
        ),
    )


@app.get(
    "/animales",
    response_model=List[AnimalResponse],
    tags=["Animales"],
    summary="Listar animales",
)
def listar_animales(
    edad_minima: Optional[int] = Query(
        None,
        ge=0,
        description="Si se indica, solo animales con esa edad o más.",
    ),
) -> List[AnimalResponse]:
    """Lista el inventario. Opcionalmente filtra por edad (polimorfismo)."""
    try:
        if edad_minima is None:
            seleccion = inventario.listar()
            ids = inventario.listar_ids()
        else:
            pares = [
                (animal_id, inventario.obtener(animal_id))
                for animal_id in inventario.listar_ids()
            ]
            animales = [animal for _, animal in pares if animal is not None]
            filtrados = animales_mayores_de(animales, edad_minima)
            ids = [
                animal_id
                for animal_id, animal in pares
                if animal in filtrados
            ]
            seleccion = filtrados
    except ValueError as error:
        raise _http_desde_value_error(error) from error

    return [
        a_respuesta(animal_id, animal)
        for animal_id, animal in zip(ids, seleccion)
    ]


@app.get(
    "/animales/resumen/peso-total",
    response_model=PesoTotalResponse,
    tags=["Animales"],
    summary="Peso total del inventario",
)
def peso_total() -> PesoTotalResponse:
    """Suma los pesos con el servicio polimórfico ``total_peso``."""
    animales = inventario.listar()
    try:
        total = total_peso(animales)
    except ValueError as error:
        raise _http_desde_value_error(error) from error
    return PesoTotalResponse(total_kg=total, cantidad=len(animales))


@app.get(
    "/animales/{animal_id}",
    response_model=AnimalResponse,
    tags=["Animales"],
    summary="Obtener un animal por id",
)
def obtener_animal(animal_id: int) -> AnimalResponse:
    """Devuelve la ficha JSON de un animal concreto."""
    animal = _animal_o_404(animal_id)
    return a_respuesta(animal_id, animal)


@app.post(
    "/animales/perros",
    response_model=AnimalResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Alta"],
    summary="Crear un perro",
)
def crear_perro(datos: AnimalCreate) -> AnimalResponse:
    """Crea un ``Perro`` del dominio y lo guarda en memoria."""
    try:
        perro = Perro(
            datos.nombre,
            datos.edad,
            datos.peso,
            datos.color,
            energia=datos.energia,
        )
    except ValueError as error:
        raise _http_desde_value_error(error) from error
    animal_id = inventario.anadir(perro)
    return a_respuesta(animal_id, perro)


@app.post(
    "/animales/gatos",
    response_model=AnimalResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Alta"],
    summary="Crear un gato",
)
def crear_gato(datos: AnimalCreate) -> AnimalResponse:
    """Crea un ``Gato`` del dominio y lo guarda en memoria."""
    try:
        gato = Gato(
            datos.nombre,
            datos.edad,
            datos.peso,
            datos.color,
            energia=datos.energia,
        )
    except ValueError as error:
        raise _http_desde_value_error(error) from error
    animal_id = inventario.anadir(gato)
    return a_respuesta(animal_id, gato)


@app.post(
    "/animales/loros",
    response_model=AnimalResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Alta"],
    summary="Crear un loro",
)
def crear_loro(datos: AnimalCreate) -> AnimalResponse:
    """Crea un ``Loro`` del dominio y lo guarda en memoria."""
    try:
        loro = Loro(
            datos.nombre,
            datos.edad,
            datos.peso,
            datos.color,
            energia=datos.energia,
        )
    except ValueError as error:
        raise _http_desde_value_error(error) from error
    animal_id = inventario.anadir(loro)
    return a_respuesta(animal_id, loro)


@app.post(
    "/animales/{animal_id}/sonido",
    response_model=MensajeResponse,
    tags=["Comportamiento"],
    summary="Emitir sonido (polimorfismo)",
)
def sonar(animal_id: int) -> MensajeResponse:
    """Llama a ``emitir_sonido`` sin preguntar la especie."""
    animal = _animal_o_404(animal_id)
    try:
        mensaje = emitir_sonido(animal)
    except ValueError as error:
        raise _http_desde_value_error(error) from error
    return MensajeResponse(id=animal_id, mensaje=mensaje)


@app.post(
    "/animales/{animal_id}/alimentar",
    response_model=MensajeResponse,
    tags=["Comportamiento"],
    summary="Alimentar (polimorfismo)",
)
def dar_comida(animal_id: int, cuerpo: AlimentarBody) -> MensajeResponse:
    """Delega en ``alimentar`` → ``comer`` de la clase real."""
    animal = _animal_o_404(animal_id)
    try:
        mensaje = alimentar(animal, cuerpo.gramos)
    except ValueError as error:
        raise _http_desde_value_error(error) from error
    return MensajeResponse(id=animal_id, mensaje=mensaje)


@app.post(
    "/animales/{animal_id}/acciones/jugar",
    response_model=MensajeResponse,
    tags=["Comportamiento"],
    summary="Jugar (solo perro)",
)
def jugar(animal_id: int) -> MensajeResponse:
    """Ejecuta ``jugar`` si el animal es un perro."""
    animal = _animal_o_404(animal_id)
    if not isinstance(animal, Perro):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Solo un perro puede jugar con esta acción.",
        )
    try:
        mensaje = animal.jugar()
    except ValueError as error:
        raise _http_desde_value_error(error) from error
    return MensajeResponse(id=animal_id, mensaje=mensaje)


@app.post(
    "/animales/{animal_id}/acciones/cazar",
    response_model=MensajeResponse,
    tags=["Comportamiento"],
    summary="Cazar (solo gato)",
)
def cazar(animal_id: int) -> MensajeResponse:
    """Ejecuta ``cazar`` si el animal es un gato."""
    animal = _animal_o_404(animal_id)
    if not isinstance(animal, Gato):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Solo un gato puede cazar con esta acción.",
        )
    try:
        mensaje = animal.cazar()
    except ValueError as error:
        raise _http_desde_value_error(error) from error
    return MensajeResponse(id=animal_id, mensaje=mensaje)


@app.post(
    "/animales/{animal_id}/acciones/volar",
    response_model=MensajeResponse,
    tags=["Comportamiento"],
    summary="Volar (solo loro)",
)
def volar(animal_id: int) -> MensajeResponse:
    """Ejecuta ``volar`` si el animal es un loro."""
    animal = _animal_o_404(animal_id)
    if not isinstance(animal, Loro):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Solo un loro puede volar con esta acción.",
        )
    try:
        mensaje = animal.volar()
    except ValueError as error:
        raise _http_desde_value_error(error) from error
    return MensajeResponse(id=animal_id, mensaje=mensaje)


@app.delete(
    "/animales",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Sistema"],
    summary="Vaciar inventario (tests / demo)",
)
def vaciar_inventario() -> None:
    """Borra todos los animales en memoria."""
    inventario.limpiar()
