import pygame
import math
import random
from src.vistas.personajes.personaje_grafico import PersonajeGrafico

from src.vistas.ataques.bola_fuego_cabra import BolaFuegoCabra
from src.vistas.ataques.bola_fuego_techo import BolaFuegoTecho


class CabraDeFuegoGrafica(PersonajeGrafico):

    def __init__(self, x, y, modelo_cabra_de_fuego):
        # Inicializamos al padre con los datos originales
        super().__init__(x, y, modelo_cabra_de_fuego)

        # =========================
        # ANIMACIONES
        # =========================
        self.cargar_animacion("death", "src/assets/images/personajes/jefes/cabraFuego/cabra-de-fuego-death.png", 18, 200, 200)
        self.cargar_animacion("walk", "src/assets/images/personajes/jefes/cabraFuego/cabra-de-fuego-walk.png", 2, 200, 200)
        self.cargar_animacion("desafiar", "src/assets/images/personajes/jefes/cabraFuego/cabra-de-fuego-desafiar.png", 4, 200, 200)
        self.cargar_animacion("attack", "src/assets/images/personajes/jefes/cabraFuego/CabradeFuego-Attack-Sheet.png", 5, 200, 200)
        
        try:
            self.cargar_animacion("attack", "src/assets/images/personajes/jefes/cabraFuego/CabradeFuego-Attack-Sheet.png", 5, 200, 200)
        except:
            self.cargar_animacion("attack", "src/assets/images/personajes/jefes/cabraFuego/cabra-de-fuego-desafiar.png", 4, 200, 200)

        self.image = self.animaciones["walk"][0]

        # =========================
        # HITBOX (FORZADO AL EXTREMO IZQUIERDO)
        # =========================
        # En vez de usar la 'x' variable del mapa, le clavamos 60 para que inicie a la izquierda uwu
        pos_x_inicial = 60 
        
        rect_imagen = self.image.get_rect(topleft=(pos_x_inicial, y))
        self.rect = pygame.Rect(0, 0, 110, 110)
        self.rect.center = rect_imagen.center

        # =========================
        # CONFIGURACIÓN DE VELOCIDADES DE FRAMES uwu
        # =========================
        self.vel_walk = 140
        self.vel_attack = 100
        self.vel_desafiar = 150
        self.vel_death = 200

        # =========================
        # MÁQUINA DE ESTADOS COMPLEJA (IA AUTÓNOMA)
        # =========================
        self.ia_estado = "ACERCARSE"
        self.timer_decision = 0
        self.cooldown_decision = 3000   
        self.timer_ataque_distancia = 0
        self.cooldown_ataque_distancia = 4000 

        self.velocidad_normal = 1.5
        self.velocidad_embestida = 7.0
        self.rango_cuerpo_a_cuerpo = 70
        
        self.proyectiles_pantalla = []

        # =========================
        # ESTADOS Y DAÑO
        # =========================
        self.recibiendo_danio = False
        self.tiempo_flash = 0
        self.duracion_flash = 0
        self.vida_anterior = self.modelo._vida

        self.vel_y = 0
        self.gravedad = 0.4

    def actualizar(self, jugador=None):
        if self.modelo._vida < self.vida_anterior:
            self.recibiendo_danio = True
            self.tiempo_flash = pygame.time.get_ticks()
        self.vida_anterior = self.modelo._vida

        for p in self.proyectiles_pantalla:
            p.actualizar()
        self.proyectiles_pantalla = [p for p in self.proyectiles_pantalla if p.activo]

        if self.modelo.estaVivo():
            if jugador is not None and jugador.modelo.estaVivo():
                
                distancia_x = jugador.rect.centerx - self.rect.centerx
                abs_distancia_x = abs(distancia_x)
                
                if self.ia_estado != "EMBESTIDA": 
                    self.mirando_derecha = distancia_x > 0

                self.timer_decision += 16
                self.timer_ataque_distancia += 16

                if self.timer_decision >= self.cooldown_decision and self.ia_estado not in ["PREPARANDO_EMBESTIDA", "EMBESTIDA"]:
                    self.timer_decision = 0
                    opciones = ["ACERCARSE", "ALEJARSE", "PREPARANDO_EMBESTIDA"]
                    self.ia_estado = random.choice(opciones)

                # --- EJECUCIÓN DE LA IA SEGÚN EL ESTADO ---
                if abs_distancia_x <= self.rango_cuerpo_a_cuerpo and self.ia_estado not in ["PREPARANDO_EMBESTIDA", "EMBESTIDA"]:
                    self.cambiar_estado("attack", loop=True)
                    self.velocidad_animacion = self.vel_attack
                    
                elif self.ia_estado == "ACERCARSE":
                    self.cambiar_estado("walk", loop=True)
                    self.velocidad_animacion = self.vel_walk
                    if distancia_x > 0: self.rect.x += self.velocidad_normal
                    else: self.rect.x -= self.velocidad_normal

                elif self.ia_estado == "ALEJARSE":
                    self.cambiar_estado("walk", loop=True)
                    self.velocidad_animacion = self.vel_walk
                    if distancia_x > 0: self.rect.x -= self.velocidad_normal
                    else: self.rect.x += self.velocidad_normal

                    if self.timer_ataque_distancia >= self.cooldown_ataque_distancia:
                        self.timer_ataque_distancia = 0
                        frente_x = self.rect.right if self.mirando_derecha else self.rect.left
                        frente_y = self.rect.top + 25

                        nuevo_fuego = BolaFuegoCabra(frente_x, frente_y, self.mirando_derecha)
                        self.proyectiles_pantalla.append(nuevo_fuego)

                elif self.ia_estado == "PREPARANDO_EMBESTIDA":
                    self.cambiar_estado("desafiar", loop=False)
                    self.velocidad_animacion = self.vel_desafiar
                    
                    if self.indice_frame >= len(self.animaciones["desafiar"]) - 1:
                        self.direccion_embestida = 1 if self.mirando_derecha else -1
                        self.ia_estado = "EMBESTIDA"

                # E) Embestida Veloz Ejecutándose
                elif self.ia_estado == "EMBESTIDA":
                    self.cambiar_estado("walk", loop=True) # Usa la caminata pero súper rápido
                    self.velocidad_animacion = 50 
                    self.rect.x += self.velocidad_embestida * self.direccion_embestida

                    # 🔧 CONTROL ESTIMADO PARA SPRITE DE 200x200 (Evita que el dibujo se hunda)
                    if self.rect.right > 1150:
                        self.rect.right = 1150  # Freno duro antes del borde real derecho
                    elif self.rect.left < 50:
                        self.rect.left = 50     # Freno duro antes del borde real izquierdo

                    # Detección de choque definitiva
                    if self.rect.right >= 1150 or self.rect.left <= 50:
                        # ¡CHOCÓ! Activa el cataclismo: lluvia de fuego del techo
                        self.ia_estado = "ACERCARSE" # Resetea estado a seguir a Hoku
                        self.timer_decision = 0
                        
                        # Generamos 5 bolas de fuego aleatorias desde el techo
                        for i in range(8):
                            x_drop = random.randint(100, 1180)
                            y_drop = -50 - (i * 40) # Desfasadas para que caigan escalonadas
                            lluvia_fuego = BolaFuegoTecho(x_drop, y_drop)
                            self.proyectiles_pantalla.append(lluvia_fuego)
            else:
                self.cambiar_estado("walk", loop=True)
        else:
            self.cambiar_estado("death", loop=False)
            self.velocidad_animacion = self.vel_death
            #self.vel_y += self.gravedad
            #self.rect.y += self.vel_y

        self.update_animacion(16)

    def dibujar(self, pantalla):
        rect_imagen = self.image.get_rect(center=self.rect.center)
        imagen_final = self.image.copy()

        # Dibujar los proyectiles activos de este jefe antes que a él mismo
        for p in self.proyectiles_pantalla:
            p.dibujar(pantalla)

        if self.recibiendo_danio:
            tiempo_actual = pygame.time.get_ticks()
            if tiempo_actual - self.tiempo_flash < self.duracion_flash:
                imagen_final.fill((255, 255, 255, 150), special_flags=pygame.BLEND_RGBA_ADD)
            else:
                self.recibiendo_danio = False

        if not self.mirando_derecha:
            imagen_final = pygame.transform.flip(imagen_final, True, False)

        # 🔧 CLAVAR EL DIBUJO DENTRO DE LA PANTALLA (Ancho estándar de 1280)
        if rect_imagen.right > 1260:
            rect_imagen.right = 1260
        if rect_imagen.left < 20:
            rect_imagen.left = 20

        pantalla.blit(imagen_final, rect_imagen)