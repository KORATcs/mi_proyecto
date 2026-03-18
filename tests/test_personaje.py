import unittest
from src.personajes.personaje import Personaje

class TestPersonaje(unittest.TestCase):

    def setUp(self):
        """Prepara el SET DE DATOS con el que haremos las pruebas"""
        self.personaje = Personaje("Hoku")
        self.personaje2 = Personaje("Ala Mayor")

    def test_recibir_danio(self): 
        """PROBAR que el metodo "recibir_danio()" me reste correctamente la vida"""
        self.personaje.recibir_danio(50)

        self.assertEqual(self.personaje._vida, 50)

    def test_recibir_danio_extremo(self):
        """PROBAR que el metodo "recibir_danio()" deje la vida en 0 si recibe daño extremo (mas del total de su vida disponible)"""
        self.personaje.recibir_danio(150)
        self.assertEqual(self.personaje._vida, 0)

    def test_recibir_danio_negativo(self):
        """PRUEBA que el metodo "recibir_danio()" no permita recibir danio negativo"""
        pass 

    def test_atacar(self):
        """PRUEBA que el metodo "atacar" reduce la vida del enemigo"""
        self.personaje.atacar(self.personaje2)
        self.assertEqual(self.personaje2._vida, 50)


    def test_esta_vivo(self): 
        """PROBAR que el metodo "esta_vivo()" muestre la vida correcta si esta vivo"""
        self.personaje._vida = 100

        self.assertEqual(self.personaje.estaVivo(), True)

    def test_esta_no_vivo(self):
        """PROBAR que el metodo "esta_vivo()" muestre False si el personaje tiene 0 de vida"""
        self.personaje._vida = 0
        self.assertEqual(self.personaje.estaVivo(), False)
