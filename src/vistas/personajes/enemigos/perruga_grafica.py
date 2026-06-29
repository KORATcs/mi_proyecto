import pygame
from src.vistas.personajes.personaje_grafico import PersonajeGrafico

class PerrugaGrafica(PersonajeGrafico):

    def __init__(self, x, y, modelo_perruga):
        super().__init__(x, y, modelo_perruga)

        # =========================
        # ANIMACIONES
        # =========================
        self.cargar_animacion("walk", "src/assets/images/personajes/enemigos/perruga/perruga-walk.png", 2, 150, 150)
        self.cargar_animacion("attack", "src/assets/images/personajes/enemigos/perruga/perruga-attack.png", 3, 150, 150)
        self.cargar_animacion("death", "src/assets/images/personajes/enemigos/perruga/perruga-death.png", 5, 150, 150)

        self.image = self.animaciones["walk"][0]

        # =========================
        # HITBOX (Controlada por la Vista)
        # =========================
        rect_imagen = self.image.get_rect(topleft=(x, y))
        self.rect = pygame.Rect(0, 0, 80, 80)
        self.rect.center = rect_imagen.center

        # =========================
        # ESTADOS Y DAÑO
        # =========================
        self.recibiendo_danio = False
        self.tiempo_flash = 0
        self.duracion_flash = 100
        self.vida_anterior = self.modelo._vida

        self.vel_y = 0
        self.gravedad = 0.5

        # Velocidad de caminata en píxeles de la vista
        self.velocidad_patrulla = 2 

    def actualizar(self):
        # Detectar daño por vida del modelo
        if self.modelo._vida < self.vida_anterior:
            self.recibiendo_danio = True
            self.tiempo_flash = pygame.time.get_ticks()
        self.vida_anterior = self.modelo._vida

        if self.modelo.estaVivo():
            self.cambiar_estado("walk")
            
            # Ejecuta la lógica matemática de su patrulla
            self.modelo.moverse() 

            # Sincronizar la dirección del sprite con el modelo lógico (1 o -1)
            if getattr(self.modelo, 'direccion', 1) == 1:
                self.mirando_derecha = True
                self.rect.x += self.velocidad_patrulla
            else:
                self.mirando_derecha = False
                self.rect.x -= self.velocidad_patrulla
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
                imagen_final.fill((255, 255, 255, 120), special_flags=pygame.BLEND_RGBA_ADD)
            else:
                self.recibiendo_danio = False

        if not self.mirando_derecha:
            imagen_final = pygame.transform.flip(imagen_final, True, False)

        pantalla.blit(imagen_final, rect_imagen)