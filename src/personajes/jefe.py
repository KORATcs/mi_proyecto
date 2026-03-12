from personajes.personaje import Personaje

class Jefe(Personaje):

    def __init__(self, nombre, vida):
        super().__init__(nombre)
        self._vida = vida
        self.ataque = 50 #todo jefe quita 2 (dos) corazones

    def atacar(self, Personaje):
        print(f"{self.nombre} ataca a {Personaje.nombre}")
        return Personaje.recibir_daño(self.ataque)