import pygame

class TemploTsumi:
    def __init__(self, x, y, id_escenario):

        self.id_escenario = id_escenario

        # 1. Cargamos el spritesheet
        spritesheet = pygame.image.load("src/assets/images/objetos/templo-tsumi.png").convert_alpha()
        
        # Pygame que mida la imagen completa
        ancho_total, alto_total = spritesheet.get_size()
        
        # ==========================================
        # CONFIGURACIÓN 
        # ==========================================
        cantidad_frames = 5
        
        ancho_frame = ancho_total // cantidad_frames
        alto_frame = alto_total  
        # ==========================================

        self.frames = []
        
        # 2. Cortamos la imagen en fila
        for i in range(cantidad_frames):
            # Ahora es imposible que se salga de los bordes
            pedacito = spritesheet.subsurface((i * ancho_frame, 0, ancho_frame, alto_frame))
            
            # Lo agrandamos un poco para que se vea bien en el mapa (ajustá el 200, 240 a gusto)
            pedacito_agrandado = pygame.transform.scale(pedacito, (600, 600))
            self.frames.append(pedacito_agrandado)
            
        self.rect = self.frames[0].get_rect(topleft=(x, y))
        
        # 3. Variables para animar fácil
        self.indice_frame = 0
        self.tiempo_anim = 0
        
        self.fuente_ui = pygame.font.SysFont(None, 30)
        self.distancia_interaccion = 300

    def actualizar(self, dt):
        """Suma el tiempo y cambia al siguiente frame de la lista"""
        self.tiempo_anim += dt
        if self.tiempo_anim > 150: # 150 milisegundos de velocidad
            self.tiempo_anim = 0
            # Este truquito hace que vuelva a 0 cuando llega al final
            self.indice_frame = (self.indice_frame + 1) % len(self.frames) 

    def verificar_cercania(self, hoku_rect):
        centro_templo = pygame.Vector2(self.rect.center)
        centro_hoku = pygame.Vector2(hoku_rect.center)
        return centro_templo.distance_to(centro_hoku) <= self.distancia_interaccion

    def interactuar(self, game_controller):
        hoku_logico = game_controller.hoku_logico
        hoku_vista = game_controller.hoku_vista
        
        if game_controller.estado_juego == "JUGANDO":
            game_controller.estado_juego = "REZANDO"
            
            if hasattr(hoku_vista, "cambiar_animacion"):
                hoku_vista.cambiar_animacion("rezar")
            hoku_vista.bloqueando_accion = True 
            
            hoku_logico.vida = hoku_logico.vida_maxima 
            id_escenario = self.id_escenario 
            
            # Solo curamos a Hoku y guardamos la partida, nada de enemigos.
            game_controller.bd.guardar_partida(
                escenario_id=id_escenario, pos_x=hoku_vista.rect.x,
                pos_y=hoku_vista.rect.y, vida_maxima=hoku_logico.vida_maxima
            )
            
        elif game_controller.estado_juego == "REZANDO":
            game_controller.estado_juego = "JUGANDO"
            hoku_vista.bloqueando_accion = False
            if hasattr(hoku_vista, "cambiar_animacion"):
                hoku_vista.cambiar_animacion("quieto")

    def dibujar(self, pantalla, hoku_rect, estado_juego):
        # Dibujamos el frame que toca ahora mismo
        pantalla.blit(self.frames[self.indice_frame], self.rect.topleft)
        
        if self.verificar_cercania(hoku_rect):
            texto = "[E] REZAR" if estado_juego == "JUGANDO" else "[E] SALIR"
            superficie_texto = self.fuente_ui.render(texto, True, (255, 255, 0)) 
            rect_texto = superficie_texto.get_rect(center=(self.rect.centerx, self.rect.top - 30))
            pantalla.blit(superficie_texto, rect_texto)