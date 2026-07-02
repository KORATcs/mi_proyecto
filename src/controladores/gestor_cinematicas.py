import pygame

class GestorCinematicas:
    def __init__(self, pantalla):
        self.pantalla = pantalla
        self.reproduciendo = False
        self.frames = []          # Guardará tuplas: (superficie_imagen, fps_de_este_frame)
        self.indice_actual = 0
        self.timer = 0
        self.callback_final = None

        # Variables para el texto elegante (Interludios)
        self.modo_texto = False
        self.texto_actual = ""     # Guardará la frase personalizada
        self.texto_alpha = 0
        self.texto_fase = "fade_in" # "fade_in", "espera", "fade_out"
        self.texto_timer = 0
        self.velocidad_fade = 0.2    # Qué tan rápido aparece/desaparece el texto

    def cargar_desde_spritesheet(self, configuracion_tiras, callback, texto_interludio=None):
        """
        Carga múltiples spritesheets. Opcionalmente recibe un 'texto_interludio' 
        que se mostrará con fade-in al terminar los frames visuales.
        """
        self.frames = []
        
        # Resetear variables de texto e inyectar el nuevo si existe
        self.modo_texto = False
        self.texto_actual = texto_interludio
        self.texto_alpha = 0
        self.texto_fase = "fade_in"
        self.texto_timer = 0

        if isinstance(configuracion_tiras, dict):
            lista_tiras = [configuracion_tiras]
        else:
            lista_tiras = configuracion_tiras

        try:
            for tira in lista_tiras:
                ruta = tira["ruta"]
                columnas = tira["columnas"]
                filas = tira["filas"]
                fps_tira = tira.get("fps", 12) 
                
                spritesheet = pygame.image.load(ruta).convert()
                
                ancho_cuadro = spritesheet.get_width() // columnas
                alto_cuadro = spritesheet.get_height() // filas
                
                for fila in range(filas):
                    for columna in range(columnas):
                        rect_recorte = pygame.Rect(columna * ancho_cuadro, fila * alto_cuadro, ancho_cuadro, alto_cuadro)
                        
                        superficie_cuadro = pygame.Surface((ancho_cuadro, alto_cuadro))
                        superficie_cuadro.blit(spritesheet, (0, 0), rect_recorte)
                        
                        cuadro_escalado = pygame.transform.scale(superficie_cuadro, self.pantalla.get_size())
                        
                        self.frames.append((cuadro_escalado, fps_tira))
            
            self.indice_actual = 0
            self.timer = 0
            self.reproduciendo = True
            self.callback_final = callback
            
        except Exception as e:
            print(f"Error al procesar las tiras en el gestor: {e}")
            self.reproduciendo = False

    def mostrar_solo_texto(self, texto, callback):
        """
        Muestra una pantalla negra con texto elegante directamente sin animaciones previas.
        Ideal para interludios intermedios y los créditos finales.
        """
        self.frames = []
        self.indice_actual = 0
        self.timer = 0
        self.texto_actual = texto
        self.texto_alpha = 0
        self.texto_fase = "fade_in"
        self.texto_timer = 0
        self.modo_texto = True
        self.reproduciendo = True
        self.callback_final = callback

    def actualizar(self, dt):
        if not self.reproduciendo: 
            return

        # Lógica del texto elegante (Fade-in / Espera / Fade-out)
        if self.modo_texto:
            if self.texto_fase == "fade_in":
                self.texto_alpha += self.velocidad_fade * dt
                if self.texto_alpha >= 255:
                    self.texto_alpha = 255
                    self.texto_fase = "espera"
                    self.texto_timer = 0

            elif self.texto_fase == "espera":
                self.texto_timer += dt
                # Se queda 3.5 segundos visible en pantalla para que dé tiempo a leer
                if self.texto_timer >= 3500: 
                    self.texto_fase = "fade_out"

            elif self.texto_fase == "fade_out":
                self.texto_alpha -= self.velocidad_fade * dt
                if self.texto_alpha <= 0:
                    self.texto_alpha = 0
                    self.reproduciendo = False
                    self.modo_texto = False
                    if self.callback_final:
                        self.callback_final()
            return

        # Lógica de animación normal por frames de imagen
        self.timer += dt
        _, fps_actual = self.frames[self.indice_actual]
        intervalo = 1000 // fps_actual

        if self.timer >= intervalo:
            self.timer = 0
            self.indice_actual += 1
            
            if self.indice_actual >= len(self.frames):
                if self.texto_actual:
                    self.modo_texto = True
                else:
                    self.reproduciendo = False
                    if self.callback_final:
                        self.callback_final()

    def dibujar(self):
        if not self.reproduciendo:
            return

        # Renderizar pantalla de texto elegante
        if self.modo_texto and self.texto_actual:
            self.pantalla.fill((0, 0, 0)) # Fondo negro poético
            fuente = pygame.font.SysFont("Georgia", 32, italic=True)
            
            lineas = self.texto_actual.split("\n")
            alto_fuente = fuente.get_linesize()
            alto_total_bloque = len(lineas) * alto_fuente
            y_centro_base = (self.pantalla.get_height() - alto_total_bloque) // 2

            for i, linea in enumerate(lineas):
                texto_superficie = fuente.render(linea, True, (255, 255, 255))
                ancho_t, alto_t = texto_superficie.get_size()
                
                superficie_transparente = pygame.Surface((ancho_t, alto_t), pygame.SRCALPHA)
                superficie_transparente.blit(texto_superficie, (0, 0))
                superficie_transparente.set_alpha(int(self.texto_alpha))
                
                x_centro = (self.pantalla.get_width() - ancho_t) // 2
                y_centro = y_centro_base + (i * alto_fuente)
                
                self.pantalla.blit(superficie_transparente, (x_centro, y_centro))
            
        elif len(self.frames) > 0:
            # Dibujar cuadro de animación normal
            self.pantalla.blit(self.frames[self.indice_actual][0], (0, 0))