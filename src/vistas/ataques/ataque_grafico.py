import pygame

class ZarpazoGrafico:
    def __init__(self, x, y, mirando_derecha, animaciones):
        self.animaciones = animaciones
        self.estado = "attack"
        self.frames = self.animaciones[self.estado]
        self.indice = 0
        self.tiempo = 0
        self.vel_anim = 1  # ms por frame
        self.golpeados = []

        self.image = self.frames[0]
        self.rect = self.image.get_rect()

        # 📍 Posición relativa a Hoku
        offset_x = 20 if mirando_derecha else -80
        self.rect.topleft = (x + offset_x, y)

        self.mirando_derecha = mirando_derecha
        self.activo = True

    def update(self, dt):
        self.tiempo += dt

        if self.tiempo >= self.vel_anim:
            self.tiempo = 0
            self.indice += 1

            if self.indice >= len(self.frames):
                self.activo = False
                return

            self.image = self.frames[self.indice]

    def dibujar(self, pantalla):
        img = self.image
        if not self.mirando_derecha:
            img = pygame.transform.flip(img, True, False)

        pantalla.blit(img, self.rect)