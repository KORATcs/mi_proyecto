import pygame

from src.modelos.plataformas.plataformas_logica import Plataforma

class PlataformaGrafica:

    def __init__(self, x, y, ancho, alto, solida=True):

        self.modelo = Plataforma(
            x,
            y,
            ancho,
            alto,
            solida
        )

        self.rect = pygame.Rect(
            x,
            y,
            ancho,
            alto
        )

        self.debug = True

        self.color_debug = (255, 0, 0)

    def dibujar(self, pantalla): pass

        # if self.debug:#

           # pygame.draw.rect(
           #     pantalla,
           #     self.color_debug,
           #     self.rect,
           #     2
           # )