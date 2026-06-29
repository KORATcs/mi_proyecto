import pygame
from src.vistas.personajes.personaje_grafico import PersonajeGrafico

class HibridoGrafico(PersonajeGrafico):

    def __init__(self, x, y, modelo_hibrido):
        super().__init__(x, y, modelo_hibrido)

        # =========================
        # ANIMACIONES
        # =========================
        self.cargar_animacion("attack", "src/assets/images/personajes/enemigos/hibrido/hibrido-attack.png", 5, 150, 150)
        self.cargar_animacion("death", "src/assets/images/personajes/enemigos/hibrido/hibrido-death.png", 6, 150, 150)
        self.cargar_animacion("walk", "src/assets/images/personajes/enemigos/hibrido/hibrido-walk.png", 3, 150, 150)

        self.image = self.animaciones["walk"][0]

        # =========================
        # HITBOX
        # =========================
        rect_imagen = self.image.get_rect(topleft=(x, y))
        self.rect = pygame.Rect(0, 0, 80, 80)
        self.rect.center = rect_imagen.center

        # =========================
        # ESTADOS Y DAÑO
        # =========================
        self.recibiendo_danio = False
        self.tiempo_flash = 0
        self.duracion_flash = 100
        self.vida_anterior = self.modelo._vida

        self.vel_y = 0
        self.gravedad = 0.5

    def actualizar(self):
        if self.modelo._vida < self.vida_anterior:
            self.recibiendo_danio = True
            self.tiempo_flash = pygame.time.get_ticks()
        self.vida_anterior = self.modelo._vida

        if self.modelo.estaVivo():
            # Por ahora, como su modelo es agresivo básico, usa walk como estado por defecto
            self.cambiar_estado("walk")
            self.modelo.moverse()
            
            # Aquí podrías añadir lógica de persecución en píxeles cambiando self.rect.x
        else:
            self.cambiar_estado("death")
            self.vel_y += self.gravedad
            self.rect.y += self.vel_y

        self.update_animacion(16)

    def dibujar(self, pantalla):
        rect_imagen = self.image.get_rect(center=self.rect.center)
        imagen_final = self.image.copy()

        if self.recibiendo_danio:
            tiempo_actual = pygame.time.get_ticks()
            if tiempo_actual - self.tiempo_flash < self.duracion_flash:
                imagen_final.fill((255, 255, 255, 120), special_flags=pygame.BLEND_RGBA_ADD)
            else:
                self.recibiendo_danio = False

        if not self.mirando_derecha:
            imagen_final = pygame.transform.flip(imagen_final, True, False)

        pantalla.blit(imagen_final, rect_imagen)