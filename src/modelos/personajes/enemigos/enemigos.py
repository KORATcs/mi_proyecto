from src.modelos.personajes.personaje import Personaje
"""Clase padre de los ENEMIGOS. Esta clase es unicamente para todos los enemigos comunes y raros de todo el juego
Cada enemigo va a tener un nombre, una vida y un ataque basico. No van a tener habilidades especiales, 
ni van a otorgar habilidades a Hoku al ser derrotados"""

class Enemigo(Personaje):

    def __init__(self, nombre, vida, ataque):
        super().__init__(nombre)
        self._vida = vida
        self.ataque = ataque

    def detectar_objetivo(self, objetivo):
        """Metodo que permite a un enemigo detectar a Hoku y mostrar un mensaje de deteccion"""
        print(f"{self.nombre} detecta a {objetivo.nombre}")
        return True
    
    def comportarse(self, objetivo):
        """Metodo que permite a un enemigo comportarse de manera agresiva hacia Hoku, detectandolo y atacandolo si esta vivo"""
        if self.detectar_objetivo(objetivo):
            self.atacar(objetivo)

    def moverse(self):
        """Metodo que permite a un enemigo moverse por el escenario"""
        if self.estaVivo():
            print(f"{self.nombre} se mueve por el escenario")