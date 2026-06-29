import pygame
import math
from src.vistas.personajes.personaje_grafico import PersonajeGrafico

class PerrugaGrafica(PersonajeGrafico):

    def __init__(self, x, y, modelo_perruga):
        super().__init__(x, y, modelo_perruga)

        # =========================
        # ANIMACIONES
        # =========================
        # Nota: Ajusté los frames a los números que me pasaste (2, 3, 5)
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
        # 🔧 CONFIGURACIÓN DE VELOCIDAD DE FRAMES (Milisegundos)
        # =========================
        # Cuanto MENOR sea el número, MÁS RÁPIDO pasarán los frames.
        self.vel_animacion_patrulla = 180    # Lento y pausado al patrullar
        self.vel_animacion_alerta = 90       # Rápido y frenético al perseguir o atacar
        
        # Asignamos la velocidad inicial
        self.velocidad_animacion = self.vel_animacion_patrulla 

        # =========================
        # CONFIGURACIÓN DE PATRULLA EN PÍXELES
        # =========================
        self.x_inicial = self.rect.x       
        self.rango_patrulla = 250          
        self.direccion_x = 1               

        self.velocidad_patrulla = 1.0      
        self.velocidad_persecucion = 1.8   
        self.radio_vision = 300            

        # =========================
        # ESTADOS Y DAÑO
        # =========================
        self.recibiendo_danio = False
        self.tiempo_flash = 0
        self.duracion_flash = 100
        self.vida_anterior = self.modelo._vida

        self.vel_y = 0
        self.gravedad = 0.5

    def actualizar(self, jugador=None):
        # Detectar daño por vida del modelo
        if self.modelo._vida < self.vida_anterior:
            self.recibiendo_danio = True
            self.tiempo_flash = pygame.time.get_ticks()
        self.vida_anterior = self.modelo._vida

        if self.modelo.estaVivo():
            self.cambiar_estado("walk")
            
            perseguiendo = False
            
            # --- INTELIGENCIA ARTIFICIAL(Argentina) (PERSECUCIÓN) ---
            if jugador is not None and jugador.modelo.estaVivo():
                distancia_x = jugador.rect.centerx - self.rect.centerx
                distancia_y = jugador.rect.centery - self.rect.centery
                distancia = math.sqrt(distancia_x**2 + distancia_y**2)
                
                if distancia <= self.radio_vision:
                    perseguiendo = True
                    
                    # Ajustamos la velocidad de la animación para que se vea más rápido
                    self.velocidad_animacion = self.vel_animacion_alerta
                    
                    if distancia_x > 0:
                        self.mirando_derecha = True
                        self.rect.x += self.velocidad_persecucion
                    elif distancia_x < 0:
                        self.mirando_derecha = False
                        self.rect.x -= self.velocidad_persecucion

            # --- PATRULLA NORMAL EN PÍXELES ---
            if not perseguiendo:
                # Volvemos a la velocidad de animación más lenta de patrulla
                self.velocidad_animacion = self.vel_animacion_patrulla

                # Mover en la dirección actual
                self.rect.x += self.velocidad_patrulla * self.direccion_x

                # Sincronizar SIEMPRE la mirada con la dirección del movimiento
                if self.direccion_x == 1:
                    self.mirando_derecha = True
                else:
                    self.mirando_derecha = False

                # Comprobar si se alejó mucho de su punto inicial
                if self.rect.x >= self.x_inicial + self.rango_patrulla:
                    self.direccion_x = -1
                    self.mirando_derecha = False
                elif self.rect.x <= self.x_inicial - self.rango_patrulla:
                    self.direccion_x = 1
                    self.mirando_derecha = True
        else:
            self.cambiar_estado("death")
            # Al morir, también puedes ajustar su velocidad si los 5 frames van muy lento/rápido
            self.velocidad_animacion = 300 
            
            self.rect.y += self.vel_y

        # Aquí es donde el PersonajeGrafico usa el valor que acabamos de modificar:
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