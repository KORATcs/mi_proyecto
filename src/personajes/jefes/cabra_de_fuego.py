from src.personajes.jefes.jefe import Jefe
"""Clase Cabra de Fuego, el primer jefe del juego. Es una cabra gigante hecha de fuego que ataca a Hoku con embestidas y pisotones, 
y al ser derrotada le otorga la habilidad de Bola de Fuego, un ataque a distancia que quita 1 corazón"""

class CabraDeFuego(Jefe):

    def __init__(self):
        super().__init__("Cabra de Fuego", 1, "Bola de Fuego")
        self.ataque_embestida = 2 #embestida que va de un extremo a otro y choca contra la pared dejando caer bolas de fuego || quita 2 corazones
        self.ataque_pisoton = 3 #ataque de cerca con mucho poder, dejando caer todo el peso de su cuerpo en sus patas delanteras creando una pequenia explosion en el suelo || quita 3 corazones
        self.bolas_de_fuego = 1 #bolas de fuego que caen al suelo al usar su ataque de embestida, pueden ser esquivadas por Hoku, pero si lo alcanzan le quitan 1 corazon cada una

    def atacar(self, Enemigo):
        print(f"{self.nombre} ataca a {Enemigo.nombre} dando un golpe con sus cuernos en llamas")
        Enemigo.recibir_danio(self.ataque)
    
    def atacar_embestida(self, Enemigo):
        print(f"{self.nombre} embiste a {Enemigo.nombre} con su cuerpo en llamas, chocando contra la pared y dejando caer bolas de fuego")
        Enemigo.recibir_danio(self.ataque_embestida)

    def atacar_pisoton(self, Enemigo):
        print(f"{self.nombre} ataca a {Enemigo.nombre} con un pisoton")
        Enemigo.recibir_danio(self.ataque_pisoton)

        