import pygame

class ControladorHoku:
    def __init__(self):
        self.atacando = False
        self.saltando = False

    def procesar_eventos(self, eventos):
        """Eventos puntuales (click, teclas presionadas una vez)"""
        self.atacando = False
        self.saltando = False

        for evento in eventos:
            """Detecta eventos puntuales como ataques o saltos"""
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1:
                    self.atacando = True

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    self.saltando = True

    def obtener_movimiento(self):
        """Movimiento continuo (teclas mantenidas)"""
        teclas = pygame.key.get_pressed()

        dx, dy = 0, 0

        if teclas[pygame.K_w]:
            dy -= 1
        if teclas[pygame.K_s]:
            dy += 1
        if teclas[pygame.K_a]:
            dx -= 1
        if teclas[pygame.K_d]:
            dx += 1

        return dx, dy

    def salto(self):
        """Detecta salto"""
        teclas = pygame.key.get_pressed()
        return teclas[pygame.K_SPACE]