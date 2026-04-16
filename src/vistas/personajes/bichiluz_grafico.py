import pygame
from src.vistas.personajes.personaje_grafico import PersonajeGrafico

class BichiluzGrafico(PersonajeGrafico):
    def __init__(self, x, y, modelo_bichiluz):
        super().__init__(x, y, modelo_bichiluz)

        self.cargar_animacion("idle", "src/assets/images/personajes/enemigos/bichiluz/bichiluz-idle.png", 2, 150, 150)
        self.cargar_animacion("death", "src/assets/images/personajes/enemigos/bichiluz/bichiluz-death.png", 1, 150, 150)

        # 🧠 IMPORTANTE: primero definimos imagen base
        self.image = self.animaciones["idle"][0]

        # 🎨 rect SOLO para calcular centro visual inicial
        rect_imagen = self.image.get_rect(topleft=(x, y))

        # 📦 hitbox más chica (colisiones)
        self.rect = pygame.Rect(0, 0, 80, 80)

        # 🎯 centramos hitbox respecto al sprite
        self.rect.center = rect_imagen.center

    def actualizar(self, dx, dy, dt, limite_pantalla):
        
        # movimiento
        self.rect.x += dx
        self.rect.y += dy

        # límites de pantalla
        if self.rect.left < limite_pantalla.left:
            self.rect.left = limite_pantalla.left
        if self.rect.right > limite_pantalla.right:
            self.rect.right = limite_pantalla.right
        if self.rect.top < limite_pantalla.top:
            self.rect.top = limite_pantalla.top
        if self.rect.bottom > limite_pantalla.bottom:
            self.rect.bottom = limite_pantalla.bottom

        # animación
        if self.modelo.estaVivo():
            self.cambiar_estado("idle")
        else:
            self.cambiar_estado("death")

        self.update_animacion(dt)

    def dibujar(self, pantalla):
        # SIEMPRE centrar sprite respecto a hitbox
        rect_imagen = self.image.get_rect(center=self.rect.center)
        pantalla.blit(self.image, rect_imagen)

        # DEBUG || LO UTILIZO SOLO PARA VER EL HITBOX Y MEJORARLA SEGUN LO REQUIERE
        #pygame.draw.rect(pantalla, (255, 0, 0), self.rect, 2)