import unittest
from src.modelos.personajes.personaje import Personaje
from src.modelos.personajes.protagonista.hoku import Hoku
from excepciones.excepciones import DanioInvalidoError, PersonajeMuertoError, ObjetivoMuertoError, HabilidadNoDesbloqueadaError, JefeNoDerrotadoError
"""TESTS PARA LA CLASE PERSONAJE (y su subclase Hoku)"""

class TestPersonaje(unittest.TestCase):

    def setUp(self):
        """CONFIGURACION INICIAL PARA LAS PRUEBAS"""
        self.personaje = Personaje("Hoku") #PERSONAJE DE PRUEBA 1
        self.personaje._vida = 4
        self.personaje.ataque = 1

        self.personaje2 = Personaje("Bichiluz") #PERSONAJE DE PRUEBA 2
        self.personaje2._vida = 3
        self.personaje2.ataque = 1

        self.Hoku = Hoku() #INSTANCIA DE HOKU PARA PROBAR SU HERENCIA DE PERSONAJE

    def test_mostrar_estado_vivo(self):
        """PROBAR que el metodo "mostrar_estado()" muestre el estado del personaje correctamente si esta vivo"""
        self.personaje.mostrar_estado()
        self.assertEqual(self.personaje.nombre, "Hoku")
        self.assertEqual(self.personaje._vida, 4)
        self.assertEqual(self.personaje.ataque, 1)

    def test_mostrar_estado_muerto(self):
        """PROBAR que el metodo "mostrar_estado()" muestre el estado del personaje correctamente si esta muerto"""
        self.personaje._vida = 0
        self.personaje.mostrar_estado()
        self.assertEqual(self.personaje.nombre, "Hoku")
        self.assertEqual(self.personaje._vida, 0)
        self.assertEqual(self.personaje.ataque, 1)

    def test_esta_vivo(self):
       """PROBAR que el metodo "esta_vivo()" muestre que este vivo"""
       self.personaje._vida = 4
       self.assertEqual(self.personaje.estaVivo(), True)
    
    def test_esta_muerto(self):
        """PROBAR que el metodo "esta_vivo()" muestre que este muerto"""
        self.personaje._vida = 0
        self.assertEqual(self.personaje.estaVivo(), False)

    def test_atacar(self):
       """PRUEBA que el metodo "atacar" reduce la vida del enemigo"""
       self.personaje.atacar(self.personaje2)
       self.assertEqual(self.personaje2._vida, 2)

    def test_atacar_enemigo_muerto(self):
        """Antes esperaba un print, ahora verifica que lance la excepción"""
        self.personaje2._vida = 0
        # Verificamos que se lance la excepción correcta
        with self.assertRaises(ObjetivoMuertoError):
            self.personaje.atacar(self.personaje2)

    def test_atacar_danio_extremo(self):
        """PROBAR que el metodo "atacar" deje la vida del enemigo en 0 si el ataque es mayor a la vida actual del enemigo"""
        self.personaje.ataque = 5
        self.personaje.atacar(self.personaje2)
        self.assertEqual(self.personaje2._vida, 0)

    def test_recibir_danio(self):
        """PROBAR que el metodo "recibir_danio()" reste la vida del personaje correctamente"""
        self.personaje.recibir_danio(2)
        self.assertEqual(self.personaje._vida, 2)

    def test_recibir_danio_extremo(self):
       """PROBAR que el metodo "recibir_danio()" deje la vida en 0 si recibe danio extremo (mas del total de su vida disponible)"""
       self.personaje.recibir_danio(10)
       self.assertEqual(self.personaje._vida, 0)

    def test_recibir_danio_negativo(self):
        """Nuevo test para validar la nueva regla de daño"""
        with self.assertRaises(DanioInvalidoError):
            self.personaje.recibir_danio(-10)

#=================================== HOKU TESTS ===================================#

    def test_saltar(self):
        """PROBAR que el metodo "saltar()" muestre el mensaje correcto"""
        self.Hoku.saltar()
    
    def test_curar(self):
        """PROBAR que el metodo "curar()" restaure la vida de Hoku a su vida maxima"""
        self.Hoku._vida = 2
        self.Hoku.curar()
        self.assertEqual(self.Hoku._vida, self.Hoku.vida_maxima)

    def test_curar_ya_estando_lleno(self):
        """Validar que curar no sobrepase la vida maxima"""
        self.Hoku._vida = self.Hoku.vida_maxima
        self.Hoku.curar()
        self.assertEqual(self.Hoku._vida, self.Hoku.vida_maxima)

    def test_dash(self):
        """PROBAR que el metodo "dash()" muestre el mensaje correcto"""
        self.Hoku.dash()

    def test_recolectar_fragmento(self):
        """PROBAR que el metodo "recolectar_fragmento()" incremente la cantidad de fragmentos y la vida maxima de Hoku correctamente"""
        self.Hoku.vida_maxima = 4
        self.Hoku._vida = 4
        self.Hoku.recolectar_fragmento(3)
        self.assertEqual(self.Hoku.fragmentos, 0)
        self.assertEqual(self.Hoku.vida_maxima, 5)
    
    def test_recolectar_fragmentos_incompletos(self):
        """PROBAR que el metodo "recolectar_fragmento()" incremente la cantidad de fragmentos pero no la vida maxima si no se han recolectado 3 fragmentos"""
        self.Hoku.vida_maxima = 4
        self.Hoku._vida = 4
        self.Hoku.recolectar_fragmento(2)
        self.assertEqual(self.Hoku.fragmentos, 2)
        self.assertEqual(self.Hoku.vida_maxima, 4)
    
    def test_recolectar_fragmentos_maximos(self):
        """PROBAR que el metodo "recolectar_fragmento()" incremente la vida maxima correctamente si se recolectan multiples de 3 fragmentos"""
        self.Hoku.vida_maxima = 4
        self.Hoku._vida = 4
        self.Hoku.recolectar_fragmento(6)
        self.assertEqual(self.Hoku.fragmentos, 0)
        self.assertEqual(self.Hoku.vida_maxima, 6)
    
    def test_desbloquear_habilidad(self):
        """PROBAR que el metodo "desbloquear_habilidad()" agregue una habilidad a la lista de habilidades de Hoku si no esta desbloqueada"""
        self.Hoku.habilidades = []
        self.Hoku.desbloquear_habilidad("Bola de Fuego")
        self.assertIn("Bola de Fuego", self.Hoku.habilidades)
    
    def test_desbloquear_habilidad_repetida(self):
        """PROBAR que el metodo "desbloquear_habilidad()" no agregue una habilidad a la lista de habilidades de Hoku si ya esta desbloqueada"""
        self.Hoku.habilidades = ["Bola de Fuego"]
        self.Hoku.desbloquear_habilidad("Bola de Fuego")
        self.assertEqual(self.Hoku.habilidades.count("Bola de Fuego"), 1)
    
    def test_lanzar_habilidad_desbloqueada(self):
        """PROBAR que el metodo "lanzar_habilidad()" reduzca la vida del enemigo si la habilidad esta desbloqueada"""
        self.Hoku.habilidades = ["Bola de Fuego"]
        self.Hoku.lanzar_habilidad("Bola de Fuego", self.personaje2)
        self.assertEqual(self.personaje2._vida, 2)
    
    def test_lanzar_habilidad_no_desbloqueada(self):
        """Antes verificaba que la vida no cambiara, ahora verifica el error"""
        self.Hoku.habilidades = []
        with self.assertRaises(HabilidadNoDesbloqueadaError):
            self.Hoku.lanzar_habilidad("Bola de Fuego", self.personaje2)
    
    def test_lanzar_habilidad_enemigo_muerto(self):
        """PROBAR que el metodo "lanzar_habilidad()" muestre el mensaje correcto si el enemigo esta muerto"""
        self.Hoku.habilidades = ["Bola de Fuego"]
        self.personaje2._vida = 0
        self.Hoku.lanzar_habilidad("Bola de Fuego", self.personaje2)
        self.assertEqual(self.personaje2._vida, 0)
    
    def test_lanzar_habilidad_danio_extremo(self):
        """PROBAR que el metodo "lanzar_habilidad()" deje la vida del enemigo en 0 si el ataque es mayor a la vida actual del enemigo"""
        self.Hoku.habilidades = ["Bola de Fuego"]
        self.Hoku.ataque = 5
        self.Hoku.lanzar_habilidad("Bola de Fuego", self.personaje2)
        self.assertEqual(self.personaje2._vida, 0)

