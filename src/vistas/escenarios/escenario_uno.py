import pygame

from src.vistas.escenarios.escenario import Escenario


class EscenarioUno(Escenario):

    def __init__(self):

        super().__init__(1280, 720)

        # Fondo del escenario
        self.fondo = pygame.image.load("src/assets/images/escenarios/primer_escenario.png").convert()

        # Conexiones
        self.salida_derecha = None

        # Crear contenido del mapa
        self.crear_plataformas()
        self.crear_enemigos()

    # =========================
    # PLATAFORMAS
    # =========================
    def crear_plataformas(self):

        pass

    # =========================
    # ENEMIGOS
    # =========================
    def crear_enemigos(self):

        pass