import pygame
from src.vistas.personajes.personaje_grafico import PersonajeGrafico

class CabraDeFuegoGrafica(PersonajeGrafico):

    def __init__(self, x, y, modelo_cabra_de_fuego):
        super().__init__(x, y, modelo_cabra_de_fuego)

        # =========================
        # ANIMACIONES
        # =========================
        self.cargar_animacion("death", "src/assets/images/personajes/jefes/cabraFuego/cabra-de-fuego-death.png", 18, 150, 150)
        self.cargar_animacion("walk", "src/assets/images/personajes/jefes/cabraFuego/cabra-de-fuego-walk.png", 2, 150, 150)
        self.cargar_animacion("desafiar", "src/assets/images/personajes/jefes/cabraFuego/cabra-de-fuego-desafiar.png", 4, 150, 150)

        self.image = self.animaciones["walk"][0]

        # =========================
        # HITBOX
        # =========================
        rect_imagen = self.image.get_rect(topleft=(x, y))
        self.rect = pygame.Rect(0, 0, 110, 110)
        self.rect.center = rect_imagen.center

        # =========================
        # ESTADOS Y DAÑO
        # =========================
        self.recibiendo_danio = False
        self.tiempo_flash = 0
        self.duracion_flash = 80
        self.vida_anterior = self.modelo._vida

        self.vel_y = 0
        self.gravedad = 0.4

    def actualizar(self):
        if self.modelo._vida < self.vida_anterior:
            self.recibiendo_danio = True
            self.tiempo_flash = pygame.time.get_ticks()
        self.vida_anterior = self.modelo._vida

        if self.modelo.estaVivo():
            # Estado base por defecto mientras no se use una máquina de estados compleja
            self.cambiar_estado("walk")
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
                imagen_final.fill((255, 255, 255, 150), special_flags=pygame.BLEND_RGBA_ADD)
            else:
                self.recibiendo_danio = False

        if not self.mirando_derecha:
            imagen_final = pygame.transform.flip(imagen_final, True, False)

        pantalla.blit(imagen_final, rect_imagen)