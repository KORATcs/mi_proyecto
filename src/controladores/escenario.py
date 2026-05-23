import pygame

from vistas.escenarios.escenario_1 import EscenarioUno


class GameController:

    def __init__(self):

        # Inicializar pygame
        pygame.init()

        # Configuración de pantalla
        self.ANCHO = 1280
        self.ALTO = 720
        self.FPS = 75

        # Crear ventana
        self.pantalla = pygame.display.set_mode(
            (self.ANCHO, self.ALTO)
        )

        # Título ventana
        pygame.display.set_caption("Mi Metroidvania")

        # Clock del juego
        self.clock = pygame.time.Clock()

        # Estado principal
        self.ejecutando = True

        # Escenario actual
        self.escenario_actual = EscenarioUno()

    # =========================
    # LOOP PRINCIPAL
    # =========================
    def ejecutar(self):

        while self.ejecutando:

            # Eventos
            self.eventos()

            # Actualizaciones
            self.actualizar()

            # Dibujado
            self.dibujar()

            # Actualizar pantalla
            pygame.display.flip()

            # Limitar FPS
            self.clock.tick(self.FPS)

        # Cerrar pygame
        pygame.quit()

    # =========================
    # EVENTOS
    # =========================
    def eventos(self):

        for evento in pygame.event.get():

            # Cerrar ventana
            if evento.type == pygame.QUIT:
                self.ejecutando = False

    # =========================
    # ACTUALIZACIONES
    # =========================
    def actualizar(self):

        # Actualizar escenario
        self.escenario_actual.actualizar()

        # Controlar cambios de mapa
        self.controlar_transiciones()

    # =========================
    # DIBUJADO
    # =========================
    def dibujar(self):

        # Limpiar pantalla
        self.pantalla.fill((0, 0, 0))

        # Dibujar escenario
        self.escenario_actual.dibujar(self.pantalla)

    # =========================
    # TRANSICIONES ENTRE MAPAS
    # =========================
    def controlar_transiciones(self):

        # Acá después vas a controlar:
        # - cambio de escenarios
        # - fade transitions
        # - posiciones del jugador
        # - pantallas de carga

        pass