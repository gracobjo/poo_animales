"""Almacén en memoria de animales para la API.

La demo de consola no necesita persistencia. La API sí necesita un sitio
donde guardar las instancias entre peticiones HTTP. Este módulo no
sustituye al dominio: solo guarda referencias a objetos ``Animal``.
"""

from typing import Dict, List, Optional

from src.modelos.animal import Animal
from src.modelos.gato import Gato
from src.modelos.loro import Loro
from src.modelos.perro import Perro
from src.api.schemas import AnimalResponse, Especie


class InventarioAnimales:
    """Inventario simple con identificadores enteros correlativos."""

    def __init__(self) -> None:
        self._animales: Dict[int, Animal] = {}
        self._siguiente_id = 1

    def limpiar(self) -> None:
        """Vacía el inventario (útil en tests)."""
        self._animales.clear()
        self._siguiente_id = 1

    def anadir(self, animal: Animal) -> int:
        """Guarda un animal y devuelve su id."""
        animal_id = self._siguiente_id
        self._animales[animal_id] = animal
        self._siguiente_id += 1
        return animal_id

    def obtener(self, animal_id: int) -> Optional[Animal]:
        """Devuelve el animal o ``None`` si no existe."""
        return self._animales.get(animal_id)

    def listar(self) -> List[Animal]:
        """Devuelve todos los animales en orden de id."""
        return [self._animales[clave] for clave in sorted(self._animales)]

    def listar_ids(self) -> List[int]:
        """Devuelve los ids ordenados."""
        return sorted(self._animales)


def especie_de(animal: Animal) -> Especie:
    """Traduce la clase concreta a una etiqueta JSON."""
    if isinstance(animal, Perro):
        return "perro"
    if isinstance(animal, Gato):
        return "gato"
    if isinstance(animal, Loro):
        return "loro"
    raise ValueError(
        f"Especie no soportada por la API: {type(animal).__name__}"
    )


def a_respuesta(animal_id: int, animal: Animal) -> AnimalResponse:
    """Convierte un objeto del dominio en el schema de salida."""
    especie = especie_de(animal)
    datos = {
        "id": animal_id,
        "especie": especie,
        "nombre": animal.nombre,
        "edad": animal.edad,
        "peso": animal.peso,
        "color": animal.color,
        "energia": animal.energia,
        "alimentacion": animal.tipo_alimentacion(),
        "info_basica": animal.info_basica(),
        "vacunado": None,
        "presas_cazadas": None,
        "frase": None,
    }
    if isinstance(animal, Perro):
        datos["vacunado"] = animal.vacunado
    if isinstance(animal, Gato):
        datos["presas_cazadas"] = animal.presas_cazadas
    if isinstance(animal, Loro):
        datos["frase"] = animal.frase
    return AnimalResponse(**datos)


inventario = InventarioAnimales()
