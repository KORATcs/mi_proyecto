from personajes.personaje import Personaje

class Enemigo(Personaje):

    def __init__(self, nombre, vida):
        super().__init__(nombre)
        self._vida = vida
        self.ataque = 25 #todo enemigo normal quita 1 (un) corazon de vida

    def atacar(self, Personaje):
        print(f"{self.nombre} ataca a {Personaje.nombre}")
        return Personaje.recibir_daño(self.ataque)