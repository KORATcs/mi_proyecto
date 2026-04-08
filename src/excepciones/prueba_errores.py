from modelos.personajes.personaje import Personaje
from src.excepciones.excepciones import DanioInvalidoError

# Instancia
hoku = Personaje("Hoku")

# --- PRUEBA MANUAL ---
print("Ejecutando prueba de daño...")
# Aquí llamas manualmente a la excepción para ver si VS Code la reconoce

try:
    # Simulamos que algo salió mal y lanzamos tu excepción
    raise DanioInvalidoError("Prueba de error de daño")
except DanioInvalidoError as e:
    print(f"La excepción funciona correctamente: {e}")