from src.objetos.objetos import Objetos

class Puertas(Objetos):
    
    def __init__(self):
        super().__init__("puerta")
    
    def interactuar(self, jugador):
        """Metodo que permite a Hoku abrir las puertas para avanzar por el nivel, mostrando un mensaje de apertura"""
        print(f"{jugador.nombre} abre la {self.nombre} para avanzar por el nivel")