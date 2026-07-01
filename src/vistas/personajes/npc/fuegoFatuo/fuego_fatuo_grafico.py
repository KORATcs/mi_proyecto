import pygame
import math
from src.vistas.personajes.personaje_grafico import PersonajeGrafico

class FuegoFatuoGrafico(PersonajeGrafico):

    def __init__(self, x, y, modelo_fuego_fatuo):
        # El modelo puede ser None si es puramente visual, o tener su propia lógica
        super().__init__(x, y, modelo_fuego_fatuo)

        # =========================
        # ANIMACIÓN
        # =========================
        self.cargar_animacion("idle", "src/assets/images/personajes/npc/fuegoFatuo/fuego-fatuo-idle.png", 4, 140, 140)
        
        self.estado_actual = "idle"
        self.image = self.animaciones["idle"][0]

        # =========================
        # HITBOX Y POSICIÓN
        # =========================
        rect_imagen = self.image.get_rect(topleft=(x, y))
        self.rect = pygame.Rect(0, 0, 50, 50)
        self.rect.center = rect_imagen.center

        # =========================
        # LÓGICA DE COMPORTAMIENTO Y VUELO
        # =========================
        self.estado_npc = "encerrado"  # Puede ser "encerrado" o "guiando"
        self.velocidad_animacion = 120 # Animación fluida
        self.mirando_derecha = True

        # Guardamos su Y inicial para que la oscilación (flotar) tenga un ancla
        self.pos_y_base = self.rect.y

    def liberar(self):
        """ Llama a este método cuando Hoku interactúe con su jaula/cristal """
        self.estado_npc = "guiando"

    def actualizar(self, jugador=None):
        # Siempre usa su animación de fuego titilando
        self.cambiar_estado("idle", loop=True)

        if self.estado_npc == "encerrado":
            # --- FASE 1: ENCERRADO Y FLOTANDO ---
            # Efecto de flotar suavemente en su lugar (arriba y abajo) usando el tiempo de Pygame
            tiempo = pygame.time.get_ticks() / 250
            self.rect.y = self.pos_y_base + int(math.sin(tiempo) * 5)

        elif self.estado_npc == "guiando" and jugador is not None:
            # --- FASE 2: LIBERADO Y SIGUIENDO A HOKU ---
            # Queremos que se posicione un poco arriba y atrás de Hoku
            offset_x = -40 if jugador.mirando_derecha else 40
            offset_y = -50
            
            objetivo_x = jugador.rect.centerx + offset_x
            objetivo_y = jugador.rect.centery + offset_y

            # Calculamos la distancia hacia ese punto objetivo
            distancia_x = objetivo_x - self.rect.centerx
            distancia_y = objetivo_y - self.rect.centery

            # Acercamiento suave (Interpolación lineal / Lerp)
            # Se mueve solo un 5% de la distancia por frame..
            self.rect.x += distancia_x * 0.05
            self.rect.y += distancia_y * 0.05

            # Actualizar hacia dónde mira para que siga la dirección del movimiento
            if distancia_x > 1:
                self.mirando_derecha = True
            elif distancia_x < -1:
                self.mirando_derecha = False

            # Le agregamos la pequeña oscilación extra mientras vuela
            tiempo = pygame.time.get_ticks() / 200
            self.rect.y += int(math.sin(tiempo) * 3)

        # Hacemos correr los frames de la clase padre
        self.update_animacion(16)

    def dibujar(self, pantalla):
        # Voltear la imagen si está flotando hacia la izquierda
        imagen_final = self.image.copy()
        if not self.mirando_derecha:
            imagen_final = pygame.transform.flip(imagen_final, True, False)

        rect_imagen = imagen_final.get_rect(center=self.rect.center)
        
        # Opcional: Si querés que el fuego fatuo también brille e ilumine, descomentá esto:
        # brillo = pygame.Surface(imagen_final.get_size(), pygame.SRCALPHA)
        # brillo.fill((100, 255, 255, 60)) # Un brillo celeste suave
        # imagen_final.blit(brillo, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)

        pantalla.blit(imagen_final, rect_imagen)