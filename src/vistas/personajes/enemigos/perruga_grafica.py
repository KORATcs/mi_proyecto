import pygame
import math
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
        # HITBOX
        # =========================
        rect_imagen = self.image.get_rect(topleft=(x, y))
        self.rect = pygame.Rect(0, 0, 80, 80)
        self.rect.center = rect_imagen.center

        # =========================
        # CONFIGURACIÓN DE VELOCIDAD DE FRAMES (Milisegundos)
        # =========================
        self.vel_animacion_patrulla = 180    
        self.vel_animacion_alerta = 90       
        self.velocidad_animacion = self.vel_animacion_patrulla 

        # =========================
        # CONFIGURACIÓN DE IA Y PATRULLA
        # =========================
        self.x_inicial = self.rect.x       
        self.rango_patrulla = 250          
        self.direccion_x = 1               

        self.velocidad_patrulla = 1.0      
        self.velocidad_persecucion = 1.8   
        self.radio_vision = 300            
        self.radio_ataque = 80    
        self.vel_animacion_ataque = 260 # Mayor número = Más lento pasa cada frame del mordisco.  

        # =========================
        # ESTADOS Y DAÑO
        # =========================
        self.recibiendo_danio = False
        self.tiempo_flash = 0
        self.duracion_flash = 100
        self.vida_anterior = self.modelo._vida

    def actualizar(self, jugador=None):
        # Detectar daño por vida del modelo
        if self.modelo._vida < self.vida_anterior:
            self.recibiendo_danio = True
            self.tiempo_flash = pygame.time.get_ticks()
        self.vida_anterior = self.modelo._vida

        if self.modelo.estaVivo():
            perseguiendo = False
            atacando = False
            
            # --- INTELIGENCIA ARTIFICIAL (CÁLCULO) ---
            if jugador is not None and jugador.modelo.estaVivo():
                distancia_x = jugador.rect.centerx - self.rect.centerx
                distancia_y = jugador.rect.centery - self.rect.centery
                distancia = math.sqrt(distancia_x**2 + distancia_y**2)
                
                if distancia <= self.radio_vision:
                    perseguiendo = True
                    self.velocidad_animacion = self.vel_animacion_alerta
                    
                    if distancia_x > 0:
                        self.mirando_derecha = True
                    else:
                        self.mirando_derecha = False
                    
                    if distancia <= self.radio_ataque:
                        atacando = True

            # --- MÁQUINA DE ESTADOS (COMPORTAMIENTO) ---
            if atacando:
                # 🔧 El ataque de Perruga se repite de manera continua (loop=True)
                self.cambiar_estado("attack", loop=True)
                self.velocidad_animacion = self.vel_animacion_ataque 
            elif perseguiendo:
                self.cambiar_estado("walk", loop=True)
                distancia_x = jugador.rect.centerx - self.rect.centerx
                if distancia_x > 0:
                    self.rect.x += self.velocidad_persecucion
                elif distancia_x < 0:
                    self.rect.x -= self.velocidad_persecucion
            else:
                self.cambiar_estado("walk", loop=True)
                self.velocidad_animacion = self.vel_animacion_patrulla
                self.rect.x += self.velocidad_patrulla * self.direccion_x

                if self.direccion_x == 1:
                    self.mirando_derecha = True
                else:
                    self.mirando_derecha = False

                if self.rect.x >= self.x_inicial + self.rango_patrulla:
                    self.direccion_x = -1
                elif self.rect.x <= self.x_inicial - self.rango_patrulla:
                    self.direccion_x = 1
        else:
            # 🔧 La muerte solo se ejecuta una vez (loop=False)
            self.cambiar_estado("death", loop=False)
            self.velocidad_animacion = 300 

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