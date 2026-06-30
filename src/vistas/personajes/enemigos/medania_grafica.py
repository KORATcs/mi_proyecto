import pygame
import math
from src.vistas.personajes.personaje_grafico import PersonajeGrafico

class MedaniaGrafica(PersonajeGrafico):

    def __init__(self, x, y, modelo_medania):
        super().__init__(x, y, modelo_medania)

        # =========================
        # ANIMACIONES
        # =========================
        self.cargar_animacion("idle", "src/assets/images/personajes/enemigos/medania/medania-idle.png", 2, 200, 200)
        self.cargar_animacion("attack", "src/assets/images/personajes/enemigos/medania/medania-attack.png", 8, 200, 200)
        self.cargar_animacion("death", "src/assets/images/personajes/enemigos/medania/medania-death.png", 6, 200, 200)

        self.image = self.animaciones["idle"][0]

        # =========================
        # HITBOX Fijo de la Vista
        # =========================
        rect_imagen = self.image.get_rect(topleft=(x, y))
        self.rect = pygame.Rect(0, 0, 90, 90)
        self.rect.center = rect_imagen.center

        # Guardar las coordenadas asignadas fijas
        self.pos_x_fija = self.rect.x
        self.pos_y_fija = self.rect.y

        # =========================
        # 🔧 CONFIGURACIÓN DE VELOCIDAD DE FRAMES (Milisegundos)
        # =========================
        # Modifica estos números a tu gusto para acelerar o ralentizar los sprites uwu
        self.vel_animacion_idle = 400      # Tranquilo cuando no te ve
        self.vel_animacion_ataque = 250    # Más rápido y frenético cuando te escupe/ataca
        self.vel_animacion_muerte = 250    # Velocidad de su desaparición

        self.velocidad_animacion = self.vel_animacion_idle

        # =========================
        # RANGO DE DETECCIÓN / ATAQUE
        # =========================
        self.radio_vision = 150            # Distancia en píxeles a la que te detecta

        # =========================
        # ESTADOS Y DAÑO
        # =========================
        self.recibiendo_danio = False
        self.tiempo_flash = 0
        self.duracion_flash = 0
        self.vida_anterior = self.modelo._vida

        self.vel_y = 0
        self.gravedad = 0.5

    def actualizar(self, jugador=None): # 🔧 Agregamos jugador=None para recibir a Hoku
        # Detectar daño por vida del modelo
        if self.modelo._vida < self.vida_anterior:
            self.recibiendo_danio = True
            self.tiempo_flash = pygame.time.get_ticks()
        self.vida_anterior = self.modelo._vida

        if self.modelo.estaVivo():
            # Forzar su posición fija
            self.rect.x = self.pos_x_fija
            self.rect.y = self.pos_y_fija
            
            detectado = False

            # --- INTELIGENCIA ARTIFICIAL (DETECCIÓN) ---
            if jugador is not None and jugador.modelo.estaVivo():
                distancia_x = jugador.rect.centerx - self.rect.centerx
                distancia_y = jugador.rect.centery - self.rect.centery
                distancia = math.sqrt(distancia_x**2 + distancia_y**2)

                # ¿Entró en el campo de visión?
                if distancia <= self.radio_vision:
                    detectado = True
                    
                    # Girar para mirar siempre a Hoku mientras lo ataca
                    if distancia_x > 0:
                        self.mirando_derecha = True
                    else:
                        self.mirando_derecha = False

            # --- MÁQUINA DE ESTADOS ---
            if detectado:
                # Cambia a animación de ataque continuo gracias al loop=True de la clase padre
                self.cambiar_estado("attack", loop=True)
                self.velocidad_animacion = self.vel_animacion_ataque
            else:
                # Si Hoku no está, se queda flotando/respirando en paz
                self.cambiar_estado("idle", loop=True)
                self.velocidad_animacion = self.vel_animacion_idle

            self.modelo.moverse()
        else:
            # Al morir, no repite el bucle (loop=False) y cae por gravedad
            self.cambiar_estado("death", loop=False)
            self.velocidad_animacion = self.vel_animacion_muerte
            
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