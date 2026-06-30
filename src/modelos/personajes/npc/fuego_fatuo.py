# src/modelos/personajes/npc/fuego_fatuo.py

from src.modelos.personajes.npc.personajes_no_jugables import PersonajesNoJugables

class FuegoFatuo(PersonajesNoJugables):
    
    def __init__(self):
        super().__init__("Fuego Fatuo")
        self.dialogos_actuales = [] # Lista de textos a mostrar
        self.indice_dialogo = 0     # En qué texto vamos
        self.mostrando_dialogo = False
        self.siguiendo_hoku = False
    
    def interactuar(self, jugador_logico, enemigos_vivos):
        # 1. Si ya estamos hablando, avanzamos al siguiente globo
        if self.mostrando_dialogo:
            self.indice_dialogo += 1
            
            # Si llegamos al final del diálogo, cerramos la charla
            if self.indice_dialogo >= len(self.dialogos_actuales):
                self.mostrando_dialogo = False
                
                # Si el diálogo que acaba de terminar era el de victoria, ¡lo empezamos a seguir!
                if jugador_logico.cabra_derrotada and not self.siguiendo_hoku and enemigos_vivos == 0:
                    self.siguiendo_hoku = True
            return

        # 2. Si NO estábamos hablando, iniciamos la charla desde cero
        self.indice_dialogo = 0
        self.mostrando_dialogo = True

        if enemigos_vivos > 0:
            self.dialogos_actuales = ["..."]
        
        elif self.siguiendo_hoku:
            self.dialogos_actuales = ["¡Vamos, la grieta está cerca!"]
        
        elif not jugador_logico.cabra_derrotada:
            self.dialogos_actuales = [
                "¡Oh! Me has salvado de ese monstruo...",
                "Pero sigo paralizado por el miedo.",
                "Esa Cabra de Fuego me aterra. Mátala y te ayudaré."
            ]
        else:
            self.dialogos_actuales = [
                "¿La derrotaste? ¡Eres increíble!",
                "Te seguiré hasta la salida, vamos."
            ]