from personajes.enemigos.enemigos import Enemigo


class Perruga(Enemigo):

    def __init__(self):
        super().__init__("Perruga", 3, 1)