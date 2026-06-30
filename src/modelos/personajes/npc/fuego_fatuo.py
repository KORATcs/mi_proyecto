from src.modelos.personajes.npc.personajes_no_jugables import PersonajesNoJugables

class FuegoFatuo(PersonajesNoJugables):
    
    def __init__(self):
        super().__init__("Fuego Fatuo")
        # Ahora usamos estados en lugar de un simple True/False
        self.estado_mision = "desconocido" 
    
    def interactuar(self, personaje_jugador):
        """ Cambia el diálogo y la acción según el progreso de Hoku """
        
        if self.estado_mision == "desconocido":
            # Primer encuentro
            print(f"{self.nombre}: ¡Por favor, {personaje_jugador.nombre}! Ayúdame. Esta enredadera me atrapó.")
            print(f"{self.nombre}: Si logras quemarla con el fuego sagrado de la Cabra, te guiaré a la Grieta.")
            self.estado_mision = "esperando_rescate"
            
        elif self.estado_mision == "esperando_rescate":
            # Hoku vuelve a hablar pero verifica si ya tiene el poder
            if personaje_jugador.tiene_poder_fuego:
                print(f"{self.nombre}: ¡Tienes el poder del fuego! ¡Úsalo en la enredadera!")
                # Nota: Acá el jugador tendría que atacar la enredadera para romperla.
            else:
                print(f"{self.nombre}: Necesitas derrotar a la Cabra de Fuego para conseguir su poder...")
                
    def liberar_oficialmente(self):
        """ Esto se llama cuando la enredadera muere/se quema """
        self.estado_mision = "liberado"
        print(f"¡{self.nombre} ha sido liberado!")
        self.volar()
        
    def volar(self):
        print(f"{self.nombre} activa su modo de vuelo para guiar a Hoku a la Grieta.")