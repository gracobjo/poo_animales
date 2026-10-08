"""Pruebas de la capa FastAPI (opcionales si no hay dependencias)."""

import sys
import unittest
from pathlib import Path

RAIZ_PROYECTO = Path(__file__).resolve().parents[1]
if str(RAIZ_PROYECTO) not in sys.path:
    sys.path.insert(0, str(RAIZ_PROYECTO))

try:
    from fastapi.testclient import TestClient

    from src.api.app import app
    from src.api.store import inventario

    FASTAPI_DISPONIBLE = True
except ImportError:
    FASTAPI_DISPONIBLE = False
    TestClient = None  # type: ignore
    app = None  # type: ignore
    inventario = None  # type: ignore


@unittest.skipUnless(FASTAPI_DISPONIBLE, "Instala requirements.txt para la API")
class TestAPIAnimales(unittest.TestCase):
    """Cubre alta, polimorfismo HTTP y errores de dominio."""

    def setUp(self) -> None:
        self.client = TestClient(app)
        inventario.limpiar()

    def tearDown(self) -> None:
        inventario.limpiar()

    def test_raiz_enlaza_swagger(self) -> None:
        respuesta = self.client.get("/")
        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(respuesta.json()["swagger"], "/docs")

    def test_openapi_y_docs_existen(self) -> None:
        openapi = self.client.get("/openapi.json")
        self.assertEqual(openapi.status_code, 200)
        self.assertIn("paths", openapi.json())
        docs = self.client.get("/docs")
        self.assertEqual(docs.status_code, 200)

    def test_crear_perro_y_sonar(self) -> None:
        alta = self.client.post(
            "/animales/perros",
            json={
                "nombre": "Rex",
                "edad": 5,
                "peso": 12.0,
                "color": "marrón",
                "energia": 80,
            },
        )
        self.assertEqual(alta.status_code, 201)
        animal_id = alta.json()["id"]
        self.assertEqual(alta.json()["especie"], "perro")
        self.assertFalse(alta.json()["vacunado"])

        sonido = self.client.post(f"/animales/{animal_id}/sonido")
        self.assertEqual(sonido.status_code, 200)
        self.assertIn("Guau", sonido.json()["mensaje"])

    def test_polimorfismo_alimentar_gato_y_loro(self) -> None:
        gato = self.client.post(
            "/animales/gatos",
            json={
                "nombre": "Misi",
                "edad": 3,
                "peso": 4.5,
                "color": "blanco",
                "energia": 70,
            },
        ).json()
        loro = self.client.post(
            "/animales/loros",
            json={
                "nombre": "Kiko",
                "edad": 4,
                "peso": 0.4,
                "color": "verde",
                "energia": 50,
            },
        ).json()

        comida_gato = self.client.post(
            f"/animales/{gato['id']}/alimentar",
            json={"gramos": 100},
        )
        comida_loro = self.client.post(
            f"/animales/{loro['id']}/alimentar",
            json={"gramos": 100},
        )
        self.assertEqual(comida_gato.status_code, 200)
        self.assertEqual(comida_loro.status_code, 200)

        peso = self.client.get("/animales/resumen/peso-total")
        self.assertEqual(peso.status_code, 200)
        self.assertAlmostEqual(peso.json()["total_kg"], 5.1, places=2)
        self.assertEqual(peso.json()["cantidad"], 2)

    def test_peso_invalido_devuelve_400(self) -> None:
        respuesta = self.client.post(
            "/animales/perros",
            json={
                "nombre": "Rex",
                "edad": 5,
                "peso": -1,
                "color": "marrón",
            },
        )
        self.assertEqual(respuesta.status_code, 422)

    def test_jugar_sin_energia_devuelve_400(self) -> None:
        alta = self.client.post(
            "/animales/perros",
            json={
                "nombre": "Tobi",
                "edad": 2,
                "peso": 8.0,
                "color": "blanco",
                "energia": 10,
            },
        ).json()
        respuesta = self.client.post(
            f"/animales/{alta['id']}/acciones/jugar"
        )
        self.assertEqual(respuesta.status_code, 400)
        self.assertIn("Energía", respuesta.json()["detail"])

    def test_animal_inexistente_404(self) -> None:
        respuesta = self.client.get("/animales/999")
        self.assertEqual(respuesta.status_code, 404)

    def test_filtro_edad_minima(self) -> None:
        self.client.post(
            "/animales/perros",
            json={
                "nombre": "Rex",
                "edad": 5,
                "peso": 12.0,
                "color": "marrón",
            },
        )
        self.client.post(
            "/animales/gatos",
            json={
                "nombre": "Misi",
                "edad": 3,
                "peso": 4.5,
                "color": "blanco",
            },
        )
        respuesta = self.client.get("/animales", params={"edad_minima": 4})
        self.assertEqual(respuesta.status_code, 200)
        nombres = [item["nombre"] for item in respuesta.json()]
        self.assertEqual(nombres, ["Rex"])


if __name__ == "__main__":
    unittest.main()
