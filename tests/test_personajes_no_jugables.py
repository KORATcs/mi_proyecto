import unittest
from src.modelos.personajes.npc.personajes_no_jugables import PersonajesNoJugables
from src.modelos.personajes.npc.fuego_fatuo import FuegoFatuo
from src.modelos.personajes.protagonista.hoku import Hoku

class TestNPC(unittest.TestCase):

    def setUp(self):
        """Configuración inicial para las pruebas de NPCs"""
        self.hoku = Hoku()
        self.npc_generico = PersonajesNoJugables("Guía del Bosque")
        self.fuego_fatuo = FuegoFatuo()

    def test_herencia_personaje(self):
        """Verifica que el NPC herede correctamente los atributos de Personaje"""
        self.assertEqual(self.npc_generico.nombre, "Guía del Bosque")
        self.assertTrue(hasattr(self.npc_generico, 'estaVivo'))

    def test_inicializacion_fuego_fatuo(self):
        """Verifica que Fuego Fatuo se inicialice con el nombre correcto"""
        self.assertEqual(self.fuego_fatuo.nombre, "Fuego Fatuo")

    def test_interactuar_npc(self):
        """Verifica que el NPC pueda interactuar con Hoku sin errores"""
        try:
            self.npc_generico.interactuar(self.hoku)
        except Exception as e:
            self.fail(f"interactuar() en NPC lanzó una excepción: {e}")

    def test_interactuar_fuego_fatuo(self):
        """Verifica que la subclase Fuego Fatuo también pueda interactuar"""
        try:
            self.fuego_fatuo.interactuar(self.hoku)
        except Exception as e:
            self.fail(f"interactuar() en FuegoFatuo lanzó una excepción: {e}")

    def test_volar_fuego_fatuo(self):
        """Verifica que el método volar se ejecute correctamente"""
        try:
            self.fuego_fatuo.volar()
        except Exception as e:
            self.fail(f"volar() lanzó una excepción: {e}")
