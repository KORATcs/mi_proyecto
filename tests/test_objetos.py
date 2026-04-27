import unittest
from src.modelos.objetos.objetos import Objetos
from src.modelos.objetos.palancas import Palancas
from src.modelos.objetos.puertas import Puertas
from src.modelos.personajes.protagonista.hoku import Hoku

class TestObjetos(unittest.TestCase):

    def setUp(self):
        """Configuración inicial para las pruebas de objetos e interactuables"""
        self.hoku = Hoku()
        self.objeto_generico = Objetos("Item Misterioso")
        self.palanca = Palancas()
        self.puerta = Puertas()

    def test_nombres_objetos(self):
        """Verifica que los objetos tengan los nombres correctos al crearse"""
        self.assertEqual(self.objeto_generico.nombre, "Item Misterioso")
        self.assertEqual(self.palanca.nombre, "palanca")
        self.assertEqual(self.puerta.nombre, "puerta")

    def test_interaccionar_objeto_generico(self):
        """Verifica que un objeto genérico pueda interactuar sin errores"""
        try:
            self.objeto_generico.interactuar(self.hoku)
        except Exception as e:
            self.fail(f"interactuar() en Objetos lanzó una excepción: {e}")

    def test_interaccionar_palanca(self):
        """Verifica que la palanca ejecute su interacción"""
        try:
            self.palanca.interactuar(self.hoku)
        except Exception as e:
            self.fail(f"interactuar() en Palancas lanzó una excepción: {e}")

    def test_interaccionar_puerta(self):
        """Verifica que la puerta ejecute su interacción"""
        try:
            self.puerta.interactuar(self.hoku)
        except Exception as e:
            self.fail(f"interactuar() en Puertas lanzó una excepción: {e}")

    def test_interactuable_base_error(self):
        """
        Verifica que la clase base Interactuable lance error 
        si no se sobrescribe (asegura el contrato de la interfaz)
        """
        from src.modelos.interactuable.interactuable import Interactuable
        interactuable_puro = Interactuable()
        with self.assertRaises(NotImplementedError):
            interactuable_puro.interactuar(self.hoku)
