import unittest
from src.modelos.personajes.enemigos.enemigos import Enemigo
from src.modelos.personajes.enemigos.bichiluz import Bichiluz
from src.modelos.personajes.enemigos.hibrido import Hibrido
from src.modelos.personajes.enemigos.medania import Medania
from src.modelos.personajes.enemigos.perruga import Perruga
"""TESTS PARA LA CLASE ENEMIGO (y todas sus subclases correspondientes)"""

class TestEnemigo(unittest.TestCase):

    def setUp(self):
        """CONFIGURACION INICIAL PARA LAS PRUEBAS"""
        self.enemigo = Enemigo("Catnap", 3, 1) #ENEMIGO DE PRUEBA 1
        self.enemigo2 = Enemigo("Whiskas", 3, 1) #ENEMIGO DE PRUEBA 2
        self.enemigo3 = Bichiluz() #ENEMIGO DE PRUEBA 3
        self.enemigo4 = Hibrido() #ENEMIGO DE PRUEBA 4
        self.enemigo5 = Medania() #ENEMIGO DE PRUEBA 5
        self.enemigo6 = Perruga() #ENEMIGO DE PRUEBA 6

    def test_detectar_objetivo(self):
        """TEST PARA EL METODO DETECTAR_ENEMIGO"""
        objetivo = self.enemigo2
        resultado = self.enemigo.detectar_objetivo(objetivo)
        self.assertTrue(resultado)
    
    def test_comportarse(self):
        """TEST PARA EL METODO COMPORTARSE"""
        objetivo = self.enemigo2
        self.enemigo.comportarse(objetivo)
        self.assertEqual(self.enemigo2._vida, 2)
    
    def test_moverse(self):
        """TEST PARA EL METODO MOVERSE"""
        self.enemigo.moverse()
        self.assertTrue(True) #NO HAY UN RESULTADO ESPECIFICO PARA ESTE METODO, SOLO SE VERIFICA QUE SE EJECUTE SIN ERRORES

    def test_comportarse_bichiluz(self):
        """TEST PARA EL METODO COMPORTARSE DE BICHILUZ"""
        objetivo = self.enemigo2
        self.enemigo3.comportarse(objetivo)
        self.assertEqual(self.enemigo2._vida, 3) #BICHILUZ NO ATACA, POR LO QUE LA VIDA DE HOKU NO DEBERIA CAMBIAR

    def test_moverse_bichiluz(self):
        """TEST PARA EL METODO MOVERSE DE BICHILUZ"""
        self.enemigo3.moverse()
        self.assertTrue(True) #NO HAY UN RESULTADO ESPECIFICO PARA ESTE METODO, SOLO SE VERIFICA QUE SE EJECUTE SIN ERRORES

    def test_ataque_especial_hibrido(self):
        """TEST PARA EL METODO ATAQUE_ESPECIAL DE HIBRIDO"""
        objetivo = self.enemigo2
        self.enemigo4.ataque_especial(objetivo)
        self.assertEqual(self.enemigo2._vida, 1) #EL ATAQUE ESPECIAL DE HIBRIDO DEBERIA CAUSAR EL DOBLE DE DAÑO QUE SU ATAQUE BASICO

    def test_moverse_medania(self):
        """TEST PARA EL METODO MOVERSE DE MEDANIA"""
        self.enemigo5.moverse()
        self.assertTrue(True) #NO HAY UN RESULTADO ESPECIFICO PARA ESTE METODO, SOLO SE VERIFICA QUE SE EJECUTE SIN ERRORES     
    
    def test_moverse_perruga(self):
        """TEST PARA EL METODO MOVERSE DE PERRUGA"""
        self.enemigo6.moverse()
        self.assertTrue(True) #NO HAY UN RESULTADO ESPECIFICO PARA ESTE METODO, SOLO SE VERIFICA QUE SE EJECUTE SIN ERRORES 
    
    def test_ataque_especial_perruga(self):
        """TEST PARA EL METODO ATAQUE_ESPECIAL DE PERRUGA"""
        objetivo = self.enemigo2
        self.enemigo6.ataque_especial(objetivo)
        self.assertEqual(self.enemigo2._vida, 1)
    
    def test_ataque_especial_extremo_perruga(self):
        """TEST PARA EL METODO ATAQUE_ESPECIAL DE PERRUGA. Como el danio es mayor a la vida actual, el enemigo
        que recibio el danio deberia tener 0 de vida, no un numero negativo"""
        self.enemigo2._vida = 1
        objetivo = self.enemigo2
        self.enemigo6.ataque_especial(objetivo)
        self.assertEqual(self.enemigo2._vida, 0)