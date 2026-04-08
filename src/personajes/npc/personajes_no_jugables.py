from src. interactuable.interactuable import Interactuable
from src. personajes.personaje import Personaje
"""Clase PersonajesNoJugables, es una clase padre para todos los personajes no jugables del juego, estos pueden ser buenos 
o malos (pero nunca enemigos o jefes) Esta clase hereda de Personaje y puede tener atributos y métodos específicos para 
los personajes no jugables, como comportamientos de ataque, patrones de movimiento, habilidades especiales, entre otros"""

class PersonajesNoJugables(Personaje, Interactuable):
    
    def __init__(self, nombre):
        """Constructor de la clase PersonajesNoJugables, que recibe un nombre y lo asigna al personaje no jugable"""
        super().__init__(nombre)

    def interactuar(self, Personaje):
        """Metodo que permite a un personaje no jugable interactuar con el jugador, mostrando un mensaje de interacción"""
        print(f"{self.nombre} interactua con {Personaje.nombre}")