import pygame

from src.vistas.plataformas.plataforma_grafica import (
    PlataformaGrafica
)


class PlataformaMovil(PlataformaGrafica):

    def __init__(self, x, y, ancho, alto):

        super().__init__(x, y, ancho, alto)

        # =========================
        # MOVIMIENTO
        # =========================
        self.velocidad = 1

        self.direccion = 1

        self.limite_superior = y - 120

        self.limite_inferior = y + 120

        # =========================
        # IMAGEN
        # =========================
        self.image = pygame.image.load(
            "src/assets/images/objetos/plataforma_movil.png"
        ).convert_alpha()

        self.image = pygame.transform.scale(
            self.image,
            (ancho, alto)
        )

        # =========================
        # HITBOX MÁS CHICA
        # =========================
        self.hitbox = pygame.Rect(
            x + 40,
            y + 40,
            ancho - 60,
            alto - 80
        )

    # ==================================================
    # UPDATE
    # ==================================================
    def update(self):

        movimiento = (
            self.velocidad * self.direccion
        )

        self.rect.y += movimiento

        self.hitbox.y += movimiento

        if self.rect.y <= self.limite_superior:

            self.direccion = 1

        elif self.rect.y >= self.limite_inferior:

            self.direccion = -1

    # ==================================================
    # DIBUJAR
    # ==================================================
    def dibujar(self, pantalla):

        pantalla.blit(
            self.image,
            self.rect
        )

        #==========================================
        #Dibuja la HITBOX de la plataforma
        #=========================================
        #if self.debug:

        #    # imagen
        #    pygame.draw.rect(
        #        pantalla,
        #        (255, 0, 0),
        #        self.rect,
        #        2
        #    )

            # hitbox
        #    pygame.draw.rect(
        #        pantalla,
        #        (0, 255, 0),
        #        self.hitbox,
        #        2
        #   )