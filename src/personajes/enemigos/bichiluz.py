from personajes.enemigos.enemigos import Enemigo


class Bichiluz(Enemigo):
    
    def __init__(self):
        super().__init__("Bichiluz", 3, 1)