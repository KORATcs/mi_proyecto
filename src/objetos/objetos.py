from src.interactuable.interactuable import Interactuable

class Objetos(Interactuable):
    """Clase base para los objetos del juego, que pueden ser recolectados por Hoku para mejorar sus habilidades o aumentar su vida máxima"""
    
    def __init__(self, nombre):
        """Constructor de la clase Objetos, que recibe un nombre y lo asigna al objeto"""
        self.nombre = nombre
    
    def interactuar(self, jugador):
        """Metodo que permite a un objeto ser usado por el jugador, mostrando un mensaje de uso"""
        print(f"{jugador.nombre} usa {self.nombre}")