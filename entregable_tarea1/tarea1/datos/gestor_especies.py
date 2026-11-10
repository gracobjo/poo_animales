"""Catálogo de especies nativas y personalizadas (persistencia JSON).

Las nativas viven en ``constantes.ESPECIES`` / clases POO.
Las personalizadas se guardan en ``especies_personalizadas.json``.
"""

from __future__ import annotations

import json
import tempfile
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

from datos.constantes import ESPECIES as ESPECIES_NATIVAS

RUTA_POR_DEFECTO = Path(__file__).resolve().parent / "especies_personalizadas.json"

_catalogo_global: Optional["CatalogoEspecies"] = None


def normalizar_nombre(nombre: str) -> str:
    """Clave de comparación: sin espacios extremos y en minúsculas."""
    return str(nombre or "").strip().casefold()


def get_catalogo(ruta: Optional[Path] = None) -> "CatalogoEspecies":
    """Singleton del catálogo (ruta por defecto del proyecto)."""
    global _catalogo_global
    if ruta is not None:
        return CatalogoEspecies(ruta)
    if _catalogo_global is None:
        _catalogo_global = CatalogoEspecies(RUTA_POR_DEFECTO)
    return _catalogo_global


def reiniciar_catalogo_global() -> None:
    """Útil en tests: olvida el singleton."""
    global _catalogo_global
    _catalogo_global = None


class CatalogoEspecies:
    """Lee/escribe especies personalizadas y consulta el catálogo completo."""

    def __init__(self, ruta: Path | str) -> None:
        self.ruta = Path(ruta)
        self._personalizadas: List[Dict[str, Any]] = []
        self.cargar()

    # --- Persistencia ---

    def cargar(self) -> None:
        """Carga el JSON; si no existe, crea ``[]``. JSON corrupto → lista vacía en memoria."""
        if not self.ruta.is_file():
            self._personalizadas = []
            self._guardar_seguro([])
            return
        try:
            texto = self.ruta.read_text(encoding="utf-8")
            datos = json.loads(texto) if texto.strip() else []
        except (OSError, json.JSONDecodeError, UnicodeError):
            # No sobrescribir el archivo corrupto: se conserva en disco.
            self._personalizadas = []
            return
        if not isinstance(datos, list):
            self._personalizadas = []
            return
        limpios: List[Dict[str, Any]] = []
        for item in datos:
            if not isinstance(item, dict):
                continue
            try:
                limpios.append(self._normalizar_registro(item, exigir_completo=True))
            except ValueError:
                continue
        self._personalizadas = limpios

    def _guardar_seguro(self, registros: List[Dict[str, Any]]) -> None:
        """Escritura atómica (temp + replace)."""
        self.ruta.parent.mkdir(parents=True, exist_ok=True)
        contenido = json.dumps(registros, ensure_ascii=False, indent=2) + "\n"
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            delete=False,
            dir=str(self.ruta.parent),
            prefix=".especies_",
            suffix=".tmp",
        ) as tmp:
            tmp.write(contenido)
            tmp_path = Path(tmp.name)
        tmp_path.replace(self.ruta)

    def _persistir(self) -> None:
        self._guardar_seguro(self._personalizadas)

    @staticmethod
    def _normalizar_registro(
        datos: Dict[str, Any], *, exigir_completo: bool = True
    ) -> Dict[str, Any]:
        nombre = str(datos.get("nombre", "")).strip()
        sonido = str(datos.get("sonido", "")).strip()
        alimentacion = str(datos.get("alimentacion", "")).strip()
        cuidados = str(datos.get("cuidados", "")).strip()
        activa = bool(datos.get("activa", True))
        if exigir_completo:
            if not nombre:
                raise ValueError("El nombre de la especie es obligatorio.")
            if not sonido:
                raise ValueError("La descripción del sonido es obligatoria.")
            if not alimentacion:
                raise ValueError("El tipo de alimentación es obligatorio.")
            if not cuidados:
                raise ValueError("Los cuidados específicos son obligatorios.")
        return {
            "nombre": nombre,
            "sonido": sonido,
            "alimentacion": alimentacion,
            "cuidados": cuidados,
            "activa": activa,
        }

    # --- Consultas ---

    def nativas(self) -> tuple[str, ...]:
        return ESPECIES_NATIVAS

    def es_nativa(self, nombre: str) -> bool:
        clave = normalizar_nombre(nombre)
        return any(normalizar_nombre(n) == clave for n in ESPECIES_NATIVAS)

    def personalizadas(self) -> List[Dict[str, Any]]:
        return [dict(item) for item in self._personalizadas]

    def _buscar_indice(self, nombre: str) -> int:
        clave = normalizar_nombre(nombre)
        for indice, item in enumerate(self._personalizadas):
            if normalizar_nombre(item["nombre"]) == clave:
                return indice
        return -1

    def obtener_personalizada(
        self, nombre: str, *, solo_activas: bool = False
    ) -> Optional[Dict[str, Any]]:
        indice = self._buscar_indice(nombre)
        if indice < 0:
            return None
        item = self._personalizadas[indice]
        if solo_activas and not item.get("activa", True):
            return None
        return dict(item)

    def nombres_activos_para_alta(self) -> tuple[str, ...]:
        """Nativas + personalizadas activas (desplegable de alta/edición)."""
        extras = [
            item["nombre"]
            for item in self._personalizadas
            if item.get("activa", True)
        ]
        return ESPECIES_NATIVAS + tuple(extras)

    def nombres_para_filtro(self) -> tuple[str, ...]:
        """Nativas + todas las personalizadas (también inactivas)."""
        extras = [item["nombre"] for item in self._personalizadas]
        return ESPECIES_NATIVAS + tuple(extras)

    def nombres_conocidos(self) -> tuple[str, ...]:
        return self.nombres_para_filtro()

    def especie_permitida_en_alta(self, nombre: str) -> bool:
        clave = normalizar_nombre(nombre)
        for candidata in self.nombres_activos_para_alta():
            if normalizar_nombre(candidata) == clave:
                return True
        return False

    def especie_conocida(self, nombre: str) -> bool:
        clave = normalizar_nombre(nombre)
        for candidata in self.nombres_conocidos():
            if normalizar_nombre(candidata) == clave:
                return True
        return False

    # --- Mutaciones ---

    def anadir(self, datos: Dict[str, Any]) -> Dict[str, Any]:
        registro = self._normalizar_registro(datos, exigir_completo=True)
        if self.es_nativa(registro["nombre"]):
            raise ValueError(
                f"'{registro['nombre']}' es una especie nativa y no se puede "
                "volver a crear."
            )
        if self._buscar_indice(registro["nombre"]) >= 0:
            raise ValueError(
                f"Ya existe una especie personalizada llamada "
                f"'{registro['nombre']}'."
            )
        registro["activa"] = True
        self._personalizadas.append(registro)
        self._persistir()
        return dict(registro)

    def actualizar(self, nombre_actual: str, datos: Dict[str, Any]) -> Dict[str, Any]:
        indice = self._buscar_indice(nombre_actual)
        if indice < 0:
            raise ValueError(
                f"No hay especie personalizada llamada '{nombre_actual}'."
            )
        if self.es_nativa(nombre_actual):
            raise ValueError("Las especies nativas no se pueden modificar.")

        nuevo = self._normalizar_registro(
            {**self._personalizadas[indice], **datos},
            exigir_completo=True,
        )
        # Conservar estado activa salvo que venga explícito
        if "activa" in datos:
            nuevo["activa"] = bool(datos["activa"])
        else:
            nuevo["activa"] = bool(self._personalizadas[indice].get("activa", True))

        if self.es_nativa(nuevo["nombre"]):
            raise ValueError(
                f"No se puede renombrar a '{nuevo['nombre']}' "
                "(coincide con una especie nativa)."
            )
        otro = self._buscar_indice(nuevo["nombre"])
        if otro >= 0 and otro != indice:
            raise ValueError(
                f"Ya existe una especie personalizada llamada '{nuevo['nombre']}'."
            )

        self._personalizadas[indice] = nuevo
        self._persistir()
        return dict(nuevo)

    def desactivar(self, nombre: str) -> Dict[str, Any]:
        if self.es_nativa(nombre):
            raise ValueError("Las especies nativas no se pueden desactivar.")
        indice = self._buscar_indice(nombre)
        if indice < 0:
            raise ValueError(f"No hay especie personalizada llamada '{nombre}'.")
        self._personalizadas[indice]["activa"] = False
        self._persistir()
        return dict(self._personalizadas[indice])

    def activar(self, nombre: str) -> Dict[str, Any]:
        if self.es_nativa(nombre):
            raise ValueError("Las especies nativas no requieren activación.")
        indice = self._buscar_indice(nombre)
        if indice < 0:
            raise ValueError(f"No hay especie personalizada llamada '{nombre}'.")
        self._personalizadas[indice]["activa"] = True
        self._persistir()
        return dict(self._personalizadas[indice])

    def eliminar(
        self,
        nombre: str,
        *,
        especies_en_uso: Optional[Iterable[str]] = None,
    ) -> None:
        if self.es_nativa(nombre):
            raise ValueError("Las especies nativas no se pueden eliminar.")
        indice = self._buscar_indice(nombre)
        if indice < 0:
            raise ValueError(f"No hay especie personalizada llamada '{nombre}'.")
        clave = normalizar_nombre(nombre)
        usadas = {
            normalizar_nombre(e)
            for e in (especies_en_uso or [])
        }
        if clave in usadas:
            raise ValueError(
                f"No se puede eliminar '{nombre}': hay animales registrados "
                "con esa especie. Puedes desactivarla para impedir nuevas altas."
            )
        del self._personalizadas[indice]
        self._persistir()


def especies_usadas_en_inventario(inventario: Dict[int, Dict[str, Any]]) -> List[str]:
    """Nombres de especie presentes en el inventario."""
    return [str(reg.get("especie", "")) for reg in inventario.values()]
