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

        # 🔧 CAMBIO: Ahora guardamos dinámicamente si el estado actual loopea o no
        self.animacion_loop = True 

    def cargar_animacion(self, nombre, ruta, frames, w, h):
        sprite_sheet = pygame.image.load(ruta).convert_alpha()
        lista_frames = []
        ancho_frame = sprite_sheet.get_width() // frames
        alto_frame = sprite_sheet.get_height()

        for i in range(frames):
            frame = sprite_sheet.subsurface((i * ancho_frame, 0, ancho_frame, alto_frame))
            frame = pygame.transform.scale(frame, (w, h))
            lista_frames.append(frame)

        self.animaciones[nombre] = lista_frames

    # 🔧 CAMBIO: Agregamos el parámetro opcional 'loop'
    def cambiar_estado(self, nuevo_estado, loop=True):
        if self.estado_actual != nuevo_estado:
            self.estado_actual = nuevo_estado
            self.indice_frame = 0
            self.timer_animacion = 0
            self.animacion_loop = loop # Guardamos la preferencia del loop

    def update_animacion(self, dt):
        if self.estado_actual not in self.animaciones:
            return

        self.timer_animacion += dt

        if self.timer_animacion >= self.velocidad_animacion:
            self.timer_animacion = 0
            frames = self.animaciones[self.estado_actual]

            # 🔧 CAMBIO: Ahora usamos la variable dinámica en vez del set hardcodeado
            if not self.animacion_loop:
                # NO loop (One-shot como la muerte o saltos)
                if self.indice_frame < len(frames) - 1:
                    self.indice_frame += 1
            else:
                # LOOP (Caminata, idles, ataques de enemigos)
                self.indice_frame = (self.indice_frame + 1) % len(frames)

            self.image = frames[self.indice_frame]

    # ... (Los métodos mover y dibujar se quedan exactamente igual) ...

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