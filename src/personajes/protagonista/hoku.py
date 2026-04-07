from personajes.personaje import Personaje

class Hoku(Personaje):
    
    def __init__(self):
        super().__init__("Hoku")
        self._vida = 4 #tiene 4 corazones
        self.ataque = 1 #hace 1 de daño 
        self.ataque_especial_desbloqueado = False #ataque que puede utilizarse cuando derrote el primer jefe (fuego)



