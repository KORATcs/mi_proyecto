from src.modelos.objetos.objetos import Objetos

class Palancas(Objetos):
    
    def __init__(self):
        super().__init__("palanca")
    
    def interactuar(self, jugador):
        """Metodo que permite a Hoku activar las palancas para abrir puertas o activar mecanismos, 
        mostrando un mensaje de activación"""
        print(f"{jugador.nombre} activa la {self.nombre} para abrir una puerta o activar un mecanismo")