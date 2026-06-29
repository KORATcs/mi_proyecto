import pygame
from src.vistas.personajes.personaje_grafico import PersonajeGrafico


class HokuGrafico(PersonajeGrafico):

    def __init__(self, x, y, modelo_hoku):
        super().__init__(x, y, modelo_hoku)

        self.cargar_animacion("idle",   "src/assets/images/personajes/hoku/hoku-estatico.png", 1,  200, 200)
        self.cargar_animacion("walk",   "src/assets/images/personajes/hoku/hoku-walk.png",     3,  200, 200)
        self.cargar_animacion("attack", "src/assets/images/personajes/hoku/hoku-garras.png",   15, 200, 200)
        self.cargar_animacion("jump",   "src/assets/images/personajes/hoku/hoku-jump.png",     8,  200, 200)
        self.cargar_animacion("death",  "src/assets/images/personajes/hoku/hoku-death.png",    10, 200, 200)

        self.image = self.animaciones["idle"][0]

        # HITBOX
        self.rect = pygame.Rect(x, y, 80, 100)
    
        self.offset_y = 20

        self.bloqueando_accion = False

        # Físicas
        self.vel_y          = 0
        self.gravedad       = 0.8
        self.fuerza_salto   = -20
        self.en_suelo       = True

        self.tiempo_danio   = 0
        self.cooldown_danio = 9999999

        self.mirando_derecha = True

        # Cambiar a False cuando quieras volver a la física normal
        self.modo_flotante = False

    # ==================================================
    # UPDATE
    # ==================================================
    def update(self, dx, dy, esta_atacando, saltando, dt,
               limite_pantalla, enemigos, escenario=None):

        if dx > 0:
            self.mirando_derecha = True
        elif dx < 0:
            self.mirando_derecha = False

        self.tiempo_danio += dt

        tiene_salida_derecha   = escenario and escenario.salida_derecha   is not None
        tiene_salida_izquierda = escenario and escenario.salida_izquierda is not None
        tiene_salida_superior  = escenario and escenario.salida_superior  is not None
        tiene_salida_inferior  = escenario and escenario.salida_inferior  is not None

        plataformas = escenario.plataformas if escenario else []

        if self.modo_flotante:
            # ── MODO FLOTANTE ──────────────────────────────
            self.rect.x += dx
            self.rect.y += dy

        else:
            # ── MODO NORMAL ────────────────────────────────

            # Movimiento horizontal
            self.rect.x += dx

            # Colisión horizontal con enemigos
            for enemigo in enemigos:
                if self.rect.colliderect(enemigo.rect):
                    if dx > 0:
                        self.rect.right = enemigo.rect.left
                    elif dx < 0:
                        self.rect.left  = enemigo.rect.right

            # Colisión horizontal con plataformas
            for plataforma in plataformas:

                # usar hitbox si existe
                colision_rect = (
                    plataforma.hitbox
                    if hasattr(plataforma, "hitbox")
                    else plataforma.rect
                )

                if (
                    plataforma.modelo.solida
                    and self.rect.colliderect(colision_rect)
                ):

                    # evitar empuje raro al subir
                    diferencia_y = abs(
                        self.rect.bottom - colision_rect.top
                    )

                    if diferencia_y < 25:
                        continue

                    if dx > 0:

                        self.rect.right = colision_rect.left

                    elif dx < 0:

                        self.rect.left = colision_rect.right

            # Salto
            if saltando and self.en_suelo:
                self.vel_y    = self.fuerza_salto
                self.en_suelo = False

            # Gravedad
            self.vel_y  += self.gravedad
            self.rect.y += self.vel_y

            # Colisión vertical con enemigos
            for enemigo in enemigos:
                if self.rect.colliderect(enemigo.rect):
                    if self.vel_y > 0:
                        self.rect.bottom = enemigo.rect.top
                        self.vel_y       = 0
                        self.en_suelo    = True
                    elif self.vel_y < 0:
                        self.rect.top  = enemigo.rect.bottom
                        self.vel_y     = 0

            # Colisión vertical con plataformas
            for plataforma in plataformas:

                colision_rect = (
                    plataforma.hitbox
                    if hasattr(plataforma, "hitbox")
                    else plataforma.rect
                )

                if (
                    plataforma.modelo.solida
                    and self.rect.colliderect(colision_rect)
                ):

                    # cayendo
                    if self.vel_y > 0:

                        self.rect.bottom = colision_rect.top

                        self.vel_y = 0

                        self.en_suelo = True

                    # golpeando abajo
                    elif self.vel_y < 0:

                        self.rect.top = colision_rect.bottom

                        self.vel_y = 0

            # Límite inferior
            if not tiene_salida_inferior:
                if self.rect.bottom >= limite_pantalla.bottom:
                    self.rect.bottom = limite_pantalla.bottom
                    self.vel_y       = 0
                    self.en_suelo    = True

            # Límite superior
            if not tiene_salida_superior:
                if self.rect.top < limite_pantalla.top:
                    self.rect.top = limite_pantalla.top
                    self.vel_y    = 0

        # Límites horizontales (ambos modos)
        if not tiene_salida_derecha:
            if self.rect.right > limite_pantalla.right:
                self.rect.right = limite_pantalla.right

        if not tiene_salida_izquierda:
            if self.rect.left < limite_pantalla.left:
                self.rect.left = limite_pantalla.left

        # Animaciones
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

    # ==================================================
    # DIBUJAR
    # ==================================================
    def dibujar(self, pantalla):

        if self.mirando_derecha:
            imagen_final = self.image
        else:
            imagen_final = pygame.transform.flip(self.image, True, False)

        rect_imagen = imagen_final.get_rect(midbottom=self.rect.midbottom)
        rect_imagen.y += self.offset_y

        pantalla.blit(imagen_final, rect_imagen)
        # print(self.rect.y, self.rect.bottom)

        # DEBUG hitbox
        # pygame.draw.rect(pantalla, (0, 255, 0), self.rect, 2)