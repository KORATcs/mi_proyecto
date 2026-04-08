from src.personajes.enemigos.enemigos import Enemigo
"""Clase Bichiluz, un enemigo común del juego. Es un pequenio ser luminoso que flota por el escenario sin atacar a Hoku, 
pero puede ser molesto si se acerca demasiado"""

class Bichiluz(Enemigo):
    
    def __init__(self):
        super().__init__("Bichiluz", 3, 1)

    def comportarse(self, objetivo):
        """Metodo que permite a Bichiluz comportarse de manera pasiva hacia Hoku, 
        flotando tranquilamente por el escenario sin atacarlo ni detectarlo"""
        print(f"{self.nombre} flota tranquilamente")

    def moverse(self):
        """Metodo que permite a Bichiluz moverse por el escenario de manera tranquila, 
        sin atacar a Hoku ni detectarlo"""
        if self.estaVivo():
            print(f"{self.nombre} flota en el mismo lugar por el escenario")