from src.modelos.personajes.npc.personajes_no_jugables import PersonajesNoJugables

class FuegoFatuo(PersonajesNoJugables):
    
    def __init__(self):
        super().__init__("Fuego Fatuo")
    
    def volar(self):
        """Metodo que permite a Fuego Fatuo volar por el escenario, mostrando un mensaje de vuelo"""
        print(f"{self.nombre} vuela por el escenario")