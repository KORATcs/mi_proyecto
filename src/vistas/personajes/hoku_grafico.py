from src.vistas.personajes.personaje_grafico import PersonajeGrafico
import pygame

class HokuGrafico(PersonajeGrafico):
    def __init__(self, x, y, modelo_hoku):
        super().__init__(x, y, modelo_hoku)

        self.cargar_animacion("idle", "src/assets/images/personajes/hoku/hoku-estatico.png", 1, 200, 200)
        self.cargar_animacion("walk", "src/assets/images/personajes/hoku/hoku-walk.png", 3, 200, 200)
        self.cargar_animacion("attack", "src/assets/images/personajes/hoku/hoku-garras.png", 15, 200, 200)
        self.cargar_animacion("jump", "src/assets/images/personajes/hoku/hoku-jump.png", 8, 200, 200)
        self.cargar_animacion("death", "src/assets/images/personajes/hoku/hoku-death.png", 10, 200, 200)

        # 🎨 imagen base
        self.image = self.animaciones["idle"][0]

        # 📦 HITBOX (cuerpo real)
        self.rect = pygame.Rect(x, y, 80, 100)

        # ⚙️ OFFSETS del sprite respecto a la hitbox (LA CLAVE)
        self.offset_y = 20  # mueve arriba/abajo

        self.bloqueando_accion = False

        # físicas
        self.vel_y = 0
        self.gravedad = 0.8
        self.fuerza_salto = -20
        self.en_suelo = True
        
        self.tiempo_danio = 0
        self.cooldown_danio = 500

        self.mirando_derecha = True

    def update(self, dx, dy, esta_atacando, saltando, dt, limite_pantalla, enemigos):

        if dx > 0:
            self.mirando_derecha = True
        elif dx < 0:
            self.mirando_derecha = False

        self.tiempo_danio += dt

        # movimiento
        self.rect.x += dx

        for enemigo in enemigos:
            if self.rect.colliderect(enemigo.rect):
                if dx > 0:
                    self.rect.right = enemigo.rect.left
                elif dx < 0:
                    self.rect.left = enemigo.rect.right

        # salto
        if saltando and self.en_suelo:
            self.vel_y = self.fuerza_salto
            self.en_suelo = False

        # gravedad
        self.vel_y += self.gravedad
        self.rect.y += self.vel_y

        for enemigo in enemigos:
            if self.rect.colliderect(enemigo.rect):
                if self.vel_y > 0:
                    self.rect.bottom = enemigo.rect.top
                    self.vel_y = 0
                    self.en_suelo = True
                elif self.vel_y < 0:
                    self.rect.top = enemigo.rect.bottom
                    self.vel_y = 0

        if self.rect.bottom >= limite_pantalla.bottom:
            self.rect.bottom = limite_pantalla.bottom
            self.vel_y = 0
            self.en_suelo = True

        # animaciones
        if not self.modelo.estaVivo():
            self.cambiar_estado("death")
        else:
            if not self.en_suelo:
                self.cambiar_estado("jump")
            elif dx != 0:
                self.cambiar_estado("walk")
            else:
                self.cambiar_estado("idle")

        self.update_animacion(dt)

    def dibujar(self, pantalla):

        # 🔄 flip
        if self.mirando_derecha:
            imagen_final = self.image
        else:
            imagen_final = pygame.transform.flip(self.image, True, False)

        # 🎯 anclar SIEMPRE al mismo punto de la hitbox
        rect_imagen = imagen_final.get_rect(midbottom=self.rect.midbottom)

        # 🎯 aplicar offset SOLO vertical (para subir/bajar el cuerpo)
        rect_imagen.y += self.offset_y

        pantalla.blit(imagen_final, rect_imagen)

        # DEBUG || LO UTILIZO SOLO PARA VER EL HITBOX Y MEJORARLA SEGUN LO REQUIERE
       # pygame.draw.rect(pantalla, (0, 255, 0), self.rect, 2)