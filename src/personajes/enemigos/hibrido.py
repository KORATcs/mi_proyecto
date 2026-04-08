from src.personajes.enemigos.enemigos import Enemigo
"""Clase Hibrido, un enemigo común del juego. Es un pequenio ser híbrido que se comporta de manera agresiva hacia Hoku, 
detectándolo y atacándolo si está vivo. Es más violento que el resto de los enemigos comunes, 
pero no es tan complejo de vencer"""

class Hibrido(Enemigo):
        
    def __init__(self):
        super().__init__("Hibrido", 5, 1)
    
    def ataque_especial(self, objetivo):
        """Metodo que permite a Hibrido realizar un ataque especial hacia Hoku, 
        atacándolo con una fuerza mayor a su ataque básico"""
        if self.estaVivo():
            print(f"{self.nombre} realiza un ataque especial hacia {objetivo.nombre}")
            objetivo.recibir_danio(self.ataque * 2)