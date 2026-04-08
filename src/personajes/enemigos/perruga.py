from src.personajes.enemigos.enemigos import Enemigo
"""Clase Perruga, un enemigo común del juego. Es una oruga parecida a un perro que se comporta 
de manera agresiva hacia Hoku, detectándolo y atacándolo. Es un enemigo común que se encuentra en las primeras 
áreas del juego"""

class Perruga(Enemigo):

    def __init__(self):
        super().__init__("Perruga", 3, 1)
        self.posicion = 0
        self.direccion = 1  # 1 = derecha, -1 = izquierda
        self.limite_izq = 0
        self.limite_der = 10

    def moverse(self):
        """Metodo que permite a Perruga moverse de manera automática por el escenario, patrullando de un lado a otro"""
        self.posicion += self.direccion

        if self.posicion >= self.limite_der or self.posicion <= self.limite_izq:
            self.direccion *= -1  # cambia de dirección

        print(f"{self.nombre} patrulla en posición {self.posicion}")

    def ataque_especial(self, objetivo):
        """Metodo que permite a Perruga realizar un ataque especial desde abajo de la tierra,
        se esconde y va a la ubicacion actual de Hoku para atacarlo por sorpresa"""
        if self.estaVivo():
            print(f"{self.nombre} detecta a {objetivo.nombre}")
            print(f"{self.nombre} se esconde bajo tierra y ataca por sorpresa a {objetivo.nombre}")
            objetivo.recibir_danio(self.ataque * 2)
