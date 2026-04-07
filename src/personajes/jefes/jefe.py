from personajes.personaje import Personaje

"""Clase Padre de todas las subclases de los Jefes. Cada nivel/realidad va a tener un jefe unico oblgiatorio
Cada uno de ellos, va a tener un nombre, vida y ataques especiales unicos y diferentes. Lo unico basico es su 
golpe comun que quita siempre 2 corazones"""

class Jefe(Personaje):

    def __init__(self, nombre, vida):
        super().__init__(nombre)
        self._vida = vida
        self.ataque = 2 #todo jefe quita 2 (dos) corazones con su ataque inicial

#DEBO CREAR ALMENOS ALGUNOS METODOS