from personajes.personaje import Personaje

"""Clase padre de los ENEMIGOS. Esta clase es unicamente para todos los enemigos comunes y raros de todo el juego"""

class Enemigo(Personaje):

    def __init__(self, nombre, vida, ataque):
        super().__init__(nombre)
        self._vida = vida
        self.ataque = ataque

#DEBO CREAR ALMENOS ALGUNOS METODOS