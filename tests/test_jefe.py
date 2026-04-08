import unittest
from src.personajes.jefes.jefe import Jefe
from src.personajes.jefes.cabra_de_fuego import CabraDeFuego
from src.personajes.protagonista.hoku import Hoku
"""TESTS PARA LA CLASE JEFE (y todas sus subclases correspondientes)"""

class TestJefe(unittest.TestCase):
    
    def setUp(self):
        """Creamos instancias de Jefe, CabraDeFuego y Hoku para usar en los tests"""
        self.jefe = Jefe("Jefe de Prueba", 0, "Habilidad de Prueba")
        self.cabra = CabraDeFuego()
        self.hoku = Hoku()
        
    
    def test_otorgar_recompensa(self):
        """Test para verificar que el metodo otorgar_recompensa funciona correctamente, otorgando la habilidad al personaje solo si el jefe ha sido derrotado"""
        self.jefe._vida = 0 #Simulamos que el jefe ha sido derrotado
        recompensa = self.jefe.otorgar_recompensa(self.hoku)
        self.assertEqual(recompensa, "Habilidad de Prueba")
        self.assertIn("Habilidad de Prueba", self.hoku.habilidades)
    
#============================ CABRA DE FUEGO ============================#

    def test_atacar_cabra_de_fuego(self):
        """Test para verificar que el ataque comun de la Cabra de Fuego funciona correctamente, quitando 2 corazones a Hoku"""
        self.cabra.atacar(self.hoku)
        self.assertEqual(self.hoku._vida, 2) #Hoku empieza con 4 de vida, el ataque comun de la cabra quita 2 corazones
    
    def test_atacar_embestida_cabra_de_fuego(self):
        """Test para verificar que el ataque de embestida de la Cabra de Fuego funciona correctamente, quitando 2 corazones a Hoku"""
        self.cabra.atacar_embestida(self.hoku)
        self.assertEqual(self.hoku._vida, 2) #Hoku empieza con 4 de vida, el ataque de embestida de la cabra quita 2 corazones
    
    def test_atacar_pisoton_cabra_de_fuego(self):
        """Test para verificar que el ataque de pisoton de la Cabra de Fuego funciona correctamente, quitando 3 corazones a Hoku"""
        self.cabra.atacar_pisoton(self.hoku)
        self.assertEqual(self.hoku._vida, 1) #Hoku empieza con 4 de vida, el ataque de pisoton de la cabra quita 3 corazones