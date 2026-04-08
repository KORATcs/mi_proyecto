from src.personajes.personaje import Personaje
"""Clase Hoku, el protagonista del juego. Es un pequenio extraterrestre, hibrido, similar a un zorro del desierto,
que puede consumir habilidades de los jefes para avanzar por los mundos"""

class Hoku(Personaje):
    
    def __init__(self):
        super().__init__("Hoku")
        self.vida_maxima = 4 #puede incrementar su vida maxima 
        self._vida = self.vida_maxima #vida actual 
        self.ataque = 1 #hace 1 de danio 
        self.habilidades = [] #ataque que puede utilizarse cuando derrote el primer jefe (fuego)
        self.fragmentos = 0 #fragmentos que se van a ir recolectando para incrementar la vida maxima

    def saltar(self):
        print("Hoku salta")
    
    def curar(self):
        self._vida = self.vida_maxima 
        print("Hoku descansa en un templo Tsumi para recuperar su vida")

    def dash(self):
        print("Hoku hace un dash para esquivar ataques enemigos o atravesar ciertos obstáculos")

    def recolectar_fragmento(self, cantidad=1):
        """Metodo que permite a Hoku recolectar fragmentos para incrementar su vida maxima, verificando si se han recolectado 3 fragmentos o no"""
        self.fragmentos += cantidad

        while self.fragmentos >= 3:
            self.fragmentos -= 3
            self.vida_maxima += 1
            print("Vida máxima aumentada!")
    
    def desbloquear_habilidad(self, habilidad):
        """Metodo que desbloquea una habilidad a Hoku al derrotar a un jefe, verificando si la habilidad ya esta desbloqueada o no"""
        if habilidad not in self.habilidades:
            self.habilidades.append(habilidad)

    def lanzar_habilidad(self, habilidad, Enemigo):
        """Metodo que permite a Hoku lanzar una habilidad desbloqueada contra un enemigo, verificando si la habilidad esta desbloqueada o no"""
        if habilidad in self.habilidades:
            print(f"Hoku lanza {habilidad} a {Enemigo.nombre}")
            return Enemigo.recibir_danio(self.ataque)
        else:
            print(f"Hoku no ha desbloqueado la habilidad: {habilidad}")
    