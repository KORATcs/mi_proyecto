from personajes.enemigos.enemigos import Enemigo


class Medaña(Enemigo):
    
    def __init__(self):
     super().__init__("Medaña", 4, 1)