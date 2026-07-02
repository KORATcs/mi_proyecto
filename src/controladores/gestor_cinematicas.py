import pygame

class GestorCinematicas:
    def __init__(self, pantalla):
        self.pantalla = pantalla
        self.reproduciendo = False
        self.frames = []          # Guardará tuplas: (superficie_imagen, fps_de_este_frame)
        self.indice_actual = 0
        self.timer = 0
        self.callback_final = None

    def cargar_desde_spritesheet(self, configuracion_tiras, callback):
        """
        Carga múltiples spritesheets con tamaños y velocidades (FPS) independientes.
        """
        self.frames = []
        
        if isinstance(configuracion_tiras, dict):
            lista_tiras = [configuracion_tiras]
        else:
            lista_tiras = configuracion_tiras

        try:
            for tira in lista_tiras:
                ruta = tira["ruta"]
                columnas = tira["columnas"]
                filas = tira["filas"]
                # Si no especificamos "fps" en la tira, por defecto usa 12
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
                        
                        # Guardamos el cuadro JUNTO con los FPS que le corresponden
                        self.frames.append((cuadro_escalado, fps_tira))
            
            self.indice_actual = 0
            self.timer = 0
            self.reproduciendo = True
            self.callback_final = callback
            print(f"¡Cinemática híbrida cargada! Total de frames: {len(self.frames)}")
            
        except Exception as e:
            print(f"Error al procesar las tiras de velocidad variable: {e}")
            self.reproduciendo = False

    def actualizar(self, dt):
        if not self.reproduciendo: 
            return

        self.timer += dt
        
        # Obtenemos los FPS específicos del cuadro que se está mostrando ahora
        _, fps_actual = self.frames[self.indice_actual]
        intervalo = 1000 // fps_actual

        if self.timer >= intervalo:
            self.timer = 0
            self.indice_actual += 1
            
            if self.indice_actual >= len(self.frames):
                self.reproduciendo = False
                if self.callback_final:
                    self.callback_final()

    def dibujar(self):
        if self.reproduciendo:
            # Dibujamos solo la superficie (el primer elemento de la tupla)
            self.pantalla.blit(self.frames[self.indice_actual][0], (0, 0))