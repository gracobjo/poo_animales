"""Constantes del dominio del refugio."""

# Especies nativas con clase POO propia. El catálogo completo (nativas +
# personalizadas) lo gestiona ``datos.gestor_especies``.
ESPECIES = ("Perro", "Gato", "Conejo", "Loro", "Hámster")
ESPECIES_NATIVAS = ESPECIES

# Peso en kg: mayor que 0 y hasta un máximo realista para mascotas del refugio.
PESO_MIN_KG = 0.01
PESO_MAX_KG = 100.0
