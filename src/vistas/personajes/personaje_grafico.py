import pygame

class PersonajeGrafico:
    def __init__(self, x, y, modelo):
        """Clase base para gráficos de personajes"""
        self.modelo = modelo

        self.animaciones = {}
        self.estado_actual = "idle"
        self.indice_frame = 0

        self.image = None
        self.rect = None

        self.mirando_derecha = True

        self.timer_animacion = 0
        self.velocidad_animacion = 120

        # Estados que NO se repiten (one-shot)
        self.estados_no_loop = {"attack", "jump", "death"}

    def cargar_animacion(self, nombre, ruta, frames, w, h):
        sprite_sheet = pygame.image.load(ruta).convert_alpha()

        lista_frames = []

        ancho_frame = sprite_sheet.get_width() // frames
        alto_frame = sprite_sheet.get_height()

        for i in range(frames):
            frame = sprite_sheet.subsurface((i * ancho_frame, 0, ancho_frame, alto_frame))

            # 🔥 ACÁ está la magia
            frame = pygame.transform.scale(frame, (w, h))

            lista_frames.append(frame)

        self.animaciones[nombre] = lista_frames

    def cambiar_estado(self, nuevo_estado):
        if self.estado_actual != nuevo_estado:
            self.estado_actual = nuevo_estado
            self.indice_frame = 0
            self.timer_animacion = 0

    def update_animacion(self, dt):
        if self.estado_actual not in self.animaciones:
            return

        self.timer_animacion += dt

        if self.timer_animacion >= self.velocidad_animacion:
            self.timer_animacion = 0

            frames = self.animaciones[self.estado_actual]

            if self.estado_actual in self.estados_no_loop:
                # NO loop
                if self.indice_frame < len(frames) - 1:
                    self.indice_frame += 1
            else:
                # LOOP
                self.indice_frame = (self.indice_frame + 1) % len(frames)

            self.image = frames[self.indice_frame]

    def mover(self, dx, dy, limite_pantalla):
        if dx > 0:
            self.mirando_derecha = True
        elif dx < 0:
            self.mirando_derecha = False

        self.rect.x += dx
        self.rect.y += dy
        self.rect.clamp_ip(limite_pantalla)

    def dibujar(self, pantalla):
        img = self.image
        if not self.mirando_derecha:
            img = pygame.transform.flip(img, True, False)

        pantalla.blit(img, self.rect)