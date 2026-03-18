from personajes.personaje import Personaje

class Hoku(Personaje):
    
    def __init__(self):
        super().__init__("Hoku")
        self._vida = 100 #tiene 4 corazones (cada corazon son 25 puntos de vida - lo mismo que golpea un enemigo normal)
        self.ataque = 50
        self.ataque_especial_desbloqueado = False #ataque que puede utilizarse cuando derrote el primer jefe

    def recibir_danio(self, daño):
        return super().recibir_danio(daño)
    
    def atacar(self, Enemigo):
        return super().atacar(Enemigo)