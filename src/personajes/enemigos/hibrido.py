from personajes.enemigos.enemigos import Enemigo


class Hibrido(Enemigo):
        
    def __init__(self):
        super().__init__("Hibrido", 5, 1)