import pygame
import math
from src.vistas.personajes.personaje_grafico import PersonajeGrafico

class HibridoGrafico(PersonajeGrafico):

    def __init__(self, x, y, modelo_hibrido):
        super().__init__(x, y, modelo_hibrido)

        # =========================
        # ANIMACIONES
        # =========================
        self.cargar_animacion("attack", "src/assets/images/personajes/enemigos/hibrido/hibrido-attack.png", 5, 250, 250)
        self.cargar_animacion("death", "src/assets/images/personajes/enemigos/hibrido/hibrido-death.png", 6, 250, 250)
        self.cargar_animacion("walk", "src/assets/images/personajes/enemigos/hibrido/hibrido-walk.png", 3, 250, 250)

        # Usamos walk[0] como frame estático de guardia
        self.image = self.animaciones["walk"][0]

        # =========================
        # HITBOX
        # =========================
        rect_imagen = self.image.get_rect(topleft=(x, y))
        self.rect = pygame.Rect(0, 0, 80, 80)
        self.rect.center = rect_imagen.center

        # 🔧 GUARDAR PUESTO DE GUARDIA (Para volver si te pierde)
        self.x_origen = self.rect.x
        self.y_origen = self.rect.y

        # =========================
        # 🔧 VELOCIDAD DE FRAMES (Milisegundos) uwu
        # =========================
        self.vel_animacion_alerta = 100    # Velocidad de patitas al perseguir
        self.vel_animacion_ataque = 140    # Velocidad del zarpazo/ataque
        self.vel_animacion_muerte = 200    
        
        self.velocidad_animacion = self.vel_animacion_alerta

        # =========================
        # CONFIGURACIÓN DE IA
        # =========================
        self.velocidad_persecucion = 2.2   # Un poquito más rápido que Perruga
        self.velocidad_retorno = 1.5       # Velocidad a la que vuelve a su puesto
        self.radio_vision = 380            # Rango de guardia
        self.radio_ataque = 55             # Distancia para empezar a dar zarpazos

        # =========================
        # ESTADOS Y DAÑO
        # =========================
        self.recibiendo_danio = False
        self.tiempo_flash = 0
        self.duracion_flash = 0
        self.vida_anterior = self.modelo._vida

        self.vel_y = 0
        self.gravedad = 0.5

    def actualizar(self, jugador=None): # 🔧 Recibe a Hoku_vista
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
                    
                    if distancia_x > 0:
                        self.mirando_derecha = True
                    else:
                        self.mirando_derecha = False
                    
                    if distancia <= self.radio_ataque:
                        atacando = True

            # --- MÁQUINA DE ESTADOS COMPORTAMIENTO ---
            if atacando:
                # Cambia a modo ataque continuo (loop=True) tal cual Perruga
                self.cambiar_estado("attack", loop=True)
                self.velocidad_animacion = self.vel_animacion_ataque
                
            elif perseguiendo:
                # Persigue a Hoku en el eje X
                self.cambiar_estado("walk", loop=True)
                self.velocidad_animacion = self.vel_animacion_alerta
                
                distancia_x = jugador.rect.centerx - self.rect.centerx
                if distancia_x > 0:
                    self.rect.x += self.velocidad_persecucion
                elif distancia_x < 0:
                    self.rect.x -= self.velocidad_persecucion
                    
            else:
                # 🔧 LÓGICA DE RETORNO A SU PUESTO DE LA CÁRCEL
                distancia_a_origen = self.x_origen - self.rect.x
                
                if abs(distancia_a_origen) > self.velocidad_retorno:
                    # Si está lejos de su puesto, camina de vuelta
                    self.cambiar_estado("walk", loop=True)
                    self.velocidad_animacion = self.vel_animacion_alerta
                    
                    if distancia_a_origen > 0:
                        self.rect.x += self.velocidad_retorno
                        self.mirando_derecha = True
                    else:
                        self.rect.x -= self.velocidad_retorno
                        self.mirando_derecha = False
                else:
                    # Fijo en su puesto: Se queda quieto mirando al frente
                    self.rect.x = self.x_origen # Clavar posición exacta
                    self.cambiar_estado("walk", loop=True)
                    # Forzamos a que se quede congelado en el frame 0 (parado) cuando hace guardia
                    self.indice_frame = 0 
                    self.timer_animacion = 0

            self.modelo.moverse()
        else:
            self.cambiar_estado("death", loop=False)
            self.velocidad_animacion = self.vel_animacion_muerte
            #self.vel_y += self.gravedad
            #self.rect.y += self.vel_y

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