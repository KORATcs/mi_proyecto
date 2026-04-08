from src.personajes.enemigos.enemigos import Enemigo
"""Clase Medania/Medaña, un enemigo común del juego. Es una pequenia arania que se comporta de manera tímida, 
pero puede atacar a Hoku si se siente amenazada. Es un enemigo común que se encuentra en las primeras áreas del juego"""

class Medania(Enemigo):
    
    def __init__(self):
     super().__init__("Medania", 4, 1)
    
    def moverse(self):
        """Metodo que permite a Medania quedarse en su cueva/rincon de manera tímida, 
        evitando acercarse a Hoku y atacándolo solo si se siente amenazada (solo si Hoku entra en su "radio de detección")"""
        if self.estaVivo():
            print(f"{self.nombre} se mantiene de manera tímida en la cueva o en su rincon")
