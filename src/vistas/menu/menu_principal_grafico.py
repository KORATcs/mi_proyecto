import pygame
import sys

class MenuPrincipalGrafico:
    def __init__(self, ancho, alto):
        self.ancho = ancho
        self.alto = alto
        
        # Bandera para avisarle al main.py que queremos jugar
        self.iniciar_juego = False
        
        # =========================
        # CARGA DE IMÁGENES ESTÁTICAS
        # =========================
        self.img_fondo = pygame.image.load("src/assets/images/escenarios/escenario-menu.png").convert()
        self.img_titulo = pygame.image.load("src/assets/images/HUD/titulo-hoku-menu-principal.png").convert_alpha()
        # Multiplicá por 1.5 para agrandar un poco, o por 2 para que sea el doble
        ancho_t = int(self.img_titulo.get_width() * 1.2) 
        alto_t = int(self.img_titulo.get_height() * 1.2)
        
        # 3. Lo reescalamos y lo guardamos en self.img_titulo
        self.img_titulo = pygame.transform.scale(self.img_titulo, (ancho_t, alto_t))
        # =========================
        # ANIMACIÓN: HOKU DURMIENDO
        # =========================
        self.frames_durmiendo = []
        
        # 1. RUTA DE TU SPRITESHEET
        ruta_spritesheet = "src/assets/images/HUD/hoku-menu-Sheet.png"
        spritesheet = pygame.image.load(ruta_spritesheet).convert_alpha()
        
        # 2. TAMAÑO ORIGINAL Y CANTIDAD DE FRAMES
        CANTIDAD_FRAMES = 4
        ANCHO_ORIGINAL = spritesheet.get_width() // CANTIDAD_FRAMES
        ALTO_ORIGINAL = spritesheet.get_height()
        
        # 👇 3. ¡NUEVO TAMAÑO! 👇
        # Poné acá el ancho y alto final que quieras que tenga Hoku.
        # Por ejemplo, si querés duplicar su tamaño poné:
        ANCHO_FINAL = ANCHO_ORIGINAL * 2 
        ALTO_FINAL = ALTO_ORIGINAL * 2
        
        for i in range(CANTIDAD_FRAMES):
            origen_x = i * ANCHO_ORIGINAL
            origen_y = 0
            rect_recorte = pygame.Rect(origen_x, origen_y, ANCHO_ORIGINAL, ALTO_ORIGINAL)
            
            # Recortamos el frame original
            frame = spritesheet.subsurface(rect_recorte)
            
            # 👇 ¡AGRANDAMOS EL FRAME! 👇
            # Esta línea toma el recorte y lo escala al nuevo tamaño.
            frame_escalado = pygame.transform.scale(frame, (ANCHO_FINAL, ALTO_FINAL))
            
            self.frames_durmiendo.append(frame_escalado)
        
        self.indice_frame = 0
        self.tiempo_animacion = 0
        self.velocidad_animacion = 200 # Milisegundos por frame

        # =========================
        # TEXTOS Y OPCIONES
        # =========================
        self.fuente_opciones = pygame.font.SysFont(None, 48)
        self.opciones = ["Nueva Partida", "Cargar Partida", "Salir"]
        self.indice_seleccionado = 0
        
        # Colores
        self.color_normal = (150, 150, 150)
        self.color_seleccionado = (255, 255, 255)

    def procesar_eventos(self, eventos):
        """Lee las teclas para moverse por el menú"""
        for evento in eventos:
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_DOWN:
                    self.indice_seleccionado = (self.indice_seleccionado + 1) % len(self.opciones)
                elif evento.key == pygame.K_UP:
                    self.indice_seleccionado = (self.indice_seleccionado - 1) % len(self.opciones)
                elif evento.key == pygame.K_RETURN:
                    self.ejecutar_opcion()

    def ejecutar_opcion(self):
        opcion = self.opciones[self.indice_seleccionado]
        if opcion == "Nueva Partida":
            self.iniciar_juego = True 
        elif opcion == "Cargar Partida":
            print("Función Cargar Partida (Próximamente)")
        elif opcion == "Salir":
            pygame.quit()
            sys.exit()

    def actualizar(self, dt):
        """Avanza la animación de Hoku durmiendo"""
        if len(self.frames_durmiendo) > 0:
            self.tiempo_animacion += dt
            if self.tiempo_animacion >= self.velocidad_animacion:
                self.tiempo_animacion = 0
                self.indice_frame = (self.indice_frame + 1) % len(self.frames_durmiendo)

    def dibujar(self, pantalla):
        # 1. Dibujar el fondo
        pantalla.blit(self.img_fondo, (0, 0))
        
        # 2. Dibujar el título
        pantalla.blit(self.img_titulo, (90, 50)) 
        
        # 3. Dibujar a Hoku durmiendo (más grande)
        if len(self.frames_durmiendo) > 0:
            frame_actual = self.frames_durmiendo[self.indice_frame]
            
            pantalla.blit(frame_actual, (750, 355))
            
        # 4. Dibujar las opciones
        margen_izquierdo = 100
        pos_y = 350
        for i, texto in enumerate(self.opciones):
            if i == self.indice_seleccionado:
                color = self.color_seleccionado
                texto_mostrar = f"> {texto}" 
            else:
                color = self.color_normal
                texto_mostrar = texto
            superficie_texto = self.fuente_opciones.render(texto_mostrar, True, color)
            pantalla.blit(superficie_texto, (margen_izquierdo, pos_y + (i * 60)))