"""Demostración de abstracción, herencia, encapsulamiento y polimorfismo."""

from src.modelos.animal import Animal
from src.modelos.gato import Gato
from src.modelos.perro import Perro
from src.servicios.gestion_animales import (
    alimentar,
    animales_mayores_de,
    emitir_sonido,
    listar_info,
    total_peso,
)


def _titulo(texto: str) -> None:
    """Imprime un separador para distinguir cada parte de la demo."""
    print("\n" + "=" * 62)
    print(texto)
    print("=" * 62)


def _crear_animales() -> tuple:
    """Crea un perro y un gato con datos válidos.

    Returns:
        La pareja ``(perro, gato)`` lista para el resto de la demo.
    """
    _titulo("1. Herencia: crear un Perro y un Gato")
    perro = Perro("Rex", 5, 12.0, "marrón", energia=80)
    gato = Gato("Misi", 3, 4.5, "blanco", energia=70)
    print(perro)
    print(gato)
    print(perro.info_basica())
    print(gato.info_basica())
    return perro, gato


def _mostrar_comportamiento(perro: Perro, gato: Gato) -> None:
    """Ejecuta los métodos propios de cada especie."""
    _titulo("2. Comportamiento específico de cada clase")
    print(perro.ladrar())
    print(perro.comer(250))
    print(perro.jugar())
    print(perro.descansar())
    print(perro.vacunar())
    try:
        perro.vacunar()
    except ValueError as error:
        print(f"No se puede vacunar otra vez: {error}")

    print(gato.maullar())
    print(gato.ronronear())
    print(gato.comer(100))
    print(gato.cazar())
    print(gato.dormir())


def _mostrar_encapsulamiento(perro: Perro, gato: Gato) -> None:
    """Muestra getters, setters y el bloqueo de los atributos privados."""
    _titulo("3. Encapsulamiento: propiedades y atributos privados")
    print(f"Peso de {perro.nombre} leído con el getter: {perro.peso} kg")
    perro.peso = 13.2
    print(f"Peso actualizado con el setter: {perro.peso} kg")
    perro.color = "  negro  "
    print(f"Color normalizado por el setter: '{perro.color}'")

    try:
        perro.peso = -1
    except ValueError as error:
        print(f"Setter rechazado: {error}")

    try:
        gato.energia = 150
    except ValueError as error:
        print(f"Setter rechazado: {error}")

    # Fuera de la clase, __peso no existe: Python renombró el atributo.
    try:
        print(perro.__peso)  # type: ignore[attr-defined]
    except AttributeError as error:
        print(f"Acceso directo a __peso bloqueado: {error}")

    try:
        perro.vacunado = False  # type: ignore[misc]
    except AttributeError as error:
        print(f"'vacunado' es de solo lectura: {error}")

    try:
        gato.presas_cazadas = 10  # type: ignore[misc]
    except AttributeError as error:
        print(f"'presas_cazadas' es de solo lectura: {error}")


def _mostrar_abstraccion() -> None:
    """Intenta instanciar la clase abstracta para mostrar que no se puede."""
    _titulo("4. Abstracción: Animal no se puede instanciar")
    try:
        Animal("Fantasma", 1)  # type: ignore[abstract]
        print("Esto no debería imprimirse.")
    except TypeError as error:
        print("TypeError esperado al instanciar la clase abstracta:")
        print(f"  {error}")


def _mostrar_polimorfismo(animales: list) -> None:
    """Recorre perros y gatos usando solo la interfaz de Animal."""
    _titulo("5. Polimorfismo: la misma llamada, distinto resultado")
    for animal in animales:
        print(
            f"{animal.nombre}: sonido -> {emitir_sonido(animal)} | "
            f"alimentación -> {animal.tipo_alimentacion()}"
        )


def _usar_servicios(animales: list) -> None:
    """Usa las funciones que aceptan cualquier secuencia de animales."""
    _titulo("6. Servicios polimórficos")
    print("Información básica:")
    for linea in listar_info(animales):
        print(f"  - {linea}")

    print(f"Peso total del grupo: {total_peso(animales):.2f} kg")
    print(alimentar(animales[0], 500))
    print(alimentar(animales[1], 200))
    print(f"Peso total después de comer: {total_peso(animales):.2f} kg")

    mayores = animales_mayores_de(animales, 4)
    nombres = ", ".join(animal.nombre for animal in mayores) or "ninguno"
    print(f"Animales de 4 años o más: {nombres}")

    try:
        alimentar(animales[0], -20)
    except ValueError as error:
        print(f"Ración inválida rechazada: {error}")


def main() -> None:
    """Ejecuta la demostración completa de principio a fin."""
    print("DEMO DE POO: ANIMALES")
    perro, gato = _crear_animales()
    _mostrar_comportamiento(perro, gato)
    _mostrar_encapsulamiento(perro, gato)
    _mostrar_abstraccion()
    animales = [perro, gato]
    _mostrar_polimorfismo(animales)
    _usar_servicios(animales)
    _titulo("Fin de la demostración")


if __name__ == "__main__":
    main()
