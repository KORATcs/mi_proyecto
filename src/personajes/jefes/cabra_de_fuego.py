from personajes.jefes.jefe import Jefe

class CabraDeFuego(Jefe):
    
    def __init__(self):
        """Constructor con atributos heredados: nombre y vida, mas sus atrivbu"""
        super().__init__("Cabra de Fuego", 25)
        self.ataque_embestida = 2 #embestida que va de un extremo a otro y choca contra la pared dejando caer bolas de fuego || quita 2 corazones
        self.ataque_pisoton = 3 #ataque de cerca con mucho poder, dejando caer todo el peso de su cuerpo en sus patas delanteras creando una pequeña explosion en el suelo || quita 3 corazones
