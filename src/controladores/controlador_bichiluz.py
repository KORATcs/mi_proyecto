import pygame
"""CLASE MOMENTANEA PARA QUE BICHILUZ PUEDA MOVERSE Y ATACAR"""
class ControladorBichiluz:
    def __init__(self):
        self.atacar = False

    def obtener_movimiento(self):
        """Movimiento continuo (teclas mantenidas)"""
        teclas = pygame.key.get_pressed()

        bichi1, bichi2 = 0, 0

        if teclas[pygame.K_UP]:
            bichi2 -= 1
        if teclas[pygame.K_DOWN]:
            bichi2 += 1
        if teclas[pygame.K_LEFT]:
            bichi1 -= 1
        if teclas[pygame.K_RIGHT]:
            bichi1 += 1

        return bichi1, bichi2
