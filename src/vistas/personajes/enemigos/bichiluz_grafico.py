import pygame
import math

from src.vistas.personajes.personaje_grafico import PersonajeGrafico

class BichiluzGrafico(PersonajeGrafico):
    
    def __init__(self, x, y, modelo_bichiluz):

        super().__init__(x, y, modelo_bichiluz)

        # =========================
        # ANIMACIONES
        # =========================
        self.cargar_animacion("idle", "src/assets/images/personajes/enemigos/bichiluz/bichiluz-idle.png", 2,150,150)
        self.cargar_animacion("death", "src/assets/images/personajes/enemigos/bichiluz/bichiluz-death.png",1,150,150)

        self.image = self.animaciones["idle"][0]

        # =========================
        # HITBOX
        # =========================
        rect_imagen = self.image.get_rect(
            topleft=(x, y)
        )

        self.rect = pygame.Rect(
            0,
            0,
            80,
            80
        )

        self.rect.center = rect_imagen.center

        # =========================
        # FLOTACIÓN
        # =========================
        self.pos_y_inicial = self.rect.y

        self.tiempo = 0

        self.amplitud = 8

        self.velocidad_flotacion = 0.05

        # =========================
        # FLASH BLANCO
        # =========================
        self.recibiendo_danio = False

        self.tiempo_flash = 0

        self.duracion_flash = 0

        self.vida_anterior = self.modelo._vida

        # =========================
        # MUERTE
        # =========================
        self.vel_y = 0

        self.gravedad = 0.5

        self.en_suelo = False

    # ==================================================
    # ACTUALIZAR
    # ==================================================
    def actualizar(self):

        # =========================
        # DETECTAR DAÑO
        # =========================
        if self.modelo._vida < self.vida_anterior:

            self.recibiendo_danio = True

            self.tiempo_flash = pygame.time.get_ticks()

        self.vida_anterior = self.modelo._vida

        # =========================
        # VIVO
        # =========================
        if self.modelo.estaVivo():

            self.cambiar_estado("idle")

            # flotación
            self.tiempo += self.velocidad_flotacion
            
             #esto hace que el personaje tenga un pequeño movimiento de arriba a abajo
            offset = math.sin(
                self.tiempo
            ) * self.amplitud

            self.rect.y = (
                self.pos_y_inicial + offset
            )

        # =========================
        # MUERTO
        # =========================
        else:

            self.cambiar_estado("death")

            self.vel_y += self.gravedad

            self.rect.y += self.vel_y

        self.update_animacion(16)

    # ==================================================
    # DIBUJAR
    # ==================================================
    def dibujar(self, pantalla):

        rect_imagen = self.image.get_rect(
            center=self.rect.center
        )

        imagen_final = self.image.copy()

        # =========================
        # FLASH BLANCO
        # =========================
        if self.recibiendo_danio:

            tiempo_actual = pygame.time.get_ticks()

            if (
                tiempo_actual - self.tiempo_flash
                < self.duracion_flash
            ):

                imagen_final.fill(
                    (255, 255, 255, 120),
                    special_flags=pygame.BLEND_RGBA_ADD
                )

            else:

                self.recibiendo_danio = False

        pantalla.blit(
            imagen_final,
            rect_imagen
        )

        # DEBUG HITBOX
        # pygame.draw.rect(
        #     pantalla,
        #     (255, 0, 0),
        #     self.rect,
        #     2
        # )