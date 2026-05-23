import pygame
from src.modelos.plataformas.plataformas_logica import Plataforma


class PlataformaGrafica:
    """
    Vista de una plataforma.
    Dibuja el rect de colisión (invisible en producción,
    visible en modo debug).
    """

    def __init__(self, x, y, ancho, alto, solida=True):

        # Modelo lógico
        self.modelo = Plataforma(x, y, ancho, alto, solida)

        # Rect de colisión (es lo que usa el jugador para chocar)
        self.rect = pygame.Rect(x, y, ancho, alto)

        # Debug: mostrar el rect en pantalla
        self.debug = True
        self.color_debug = (255, 0, 0)   # rojo para verlas bien

    def dibujar(self, pantalla):
        if self.debug:
            pygame.draw.rect(pantalla, self.color_debug, self.rect, 2)