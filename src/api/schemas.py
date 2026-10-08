"""Esquemas Pydantic para la API HTTP.

Estos modelos documentan el JSON de entrada/salida en Swagger.
No sustituyen a ``Perro`` / ``Gato`` / ``Loro``: la API los traduce
al dominio POO.
"""

from typing import Literal, Optional

from pydantic import BaseModel, Field


Especie = Literal["perro", "gato", "loro"]


class AnimalCreate(BaseModel):
    """Datos comunes para crear cualquier animal."""

    nombre: str = Field(..., min_length=1, example="Rex")
    edad: int = Field(..., ge=0, le=30, example=5)
    peso: float = Field(..., gt=0, example=12.0)
    color: str = Field(..., min_length=1, example="marrón")
    energia: float = Field(100, ge=0, le=100, example=80)


class AlimentarBody(BaseModel):
    """Cuerpo para alimentar a un animal."""

    gramos: float = Field(..., gt=0, example=200)


class MensajeResponse(BaseModel):
    """Respuesta con un mensaje de comportamiento."""

    id: int
    mensaje: str


class AnimalResponse(BaseModel):
    """Vista JSON de un animal almacenado."""

    id: int
    especie: Especie
    nombre: str
    edad: int
    peso: float
    color: str
    energia: float
    alimentacion: str
    vacunado: Optional[bool] = None
    presas_cazadas: Optional[int] = None
    frase: Optional[str] = None
    info_basica: str


class PesoTotalResponse(BaseModel):
    """Suma de pesos del inventario."""

    total_kg: float
    cantidad: int


class HealthResponse(BaseModel):
    """Estado del servicio."""

    servicio: str
    swagger: str
    mensaje: str
