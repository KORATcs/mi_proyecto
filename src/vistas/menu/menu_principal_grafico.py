import pygame
import sys

class MenuPrincipalGrafico:
    def __init__(self, ancho, alto):
        """Clase para representar el menú principal del juego"""
        self.ancho = ancho
        self.alto = alto
        
        # Banderas para avisarle al main.py qué queremos hacer
        self.iniciar_juego = False
        self.cargar_partida = False
        
        # Estado del sub-menú de confirmación
        self.mostrando_confirmacion = False
        self.indice_confirmacion = 1 # 0 = Sí, 1 = No (por defecto en "No" por seguridad)
        
        # =========================
        # CARGA DE IMÁGENES ESTÁTICAS
        # =========================
        self.img_fondo = pygame.image.load("src/assets/images/escenarios/escenario-menu.png").convert()
        self.img_titulo = pygame.image.load("src/assets/images/HUD/titulo-hoku-menu-principal.png").convert_alpha()
        ancho_t = int(self.img_titulo.get_width() * 1.2) 
        alto_t = int(self.img_titulo.get_height() * 1.2)
        self.img_titulo = pygame.transform.scale(self.img_titulo, (ancho_t, alto_t))

        # =========================
        # ANIMACIÓN: HOKU DURMIENDO
        # =========================
        self.frames_durmiendo = []
        ruta_spritesheet = "src/assets/images/HUD/hoku-menu-Sheet.png"
        spritesheet = pygame.image.load(ruta_spritesheet).convert_alpha()
        
        CANTIDAD_FRAMES = 4
        ANCHO_ORIGINAL = spritesheet.get_width() // CANTIDAD_FRAMES
        ALTO_ORIGINAL = spritesheet.get_height()
        
        ANCHO_FINAL = ANCHO_ORIGINAL * 2 
        ALTO_FINAL = ALTO_ORIGINAL * 2
        
        for i in range(CANTIDAD_FRAMES):
            origen_x = i * ANCHO_ORIGINAL
            origen_y = 0
            rect_recorte = pygame.Rect(origen_x, origen_y, ANCHO_ORIGINAL, ALTO_ORIGINAL)
            frame = spritesheet.subsurface(rect_recorte)
            frame_escalado = pygame.transform.scale(frame, (ANCHO_FINAL, ALTO_FINAL))
            self.frames_durmiendo.append(frame_escalado)
        
        self.indice_frame = 0
        self.tiempo_animacion = 0
        self.velocidad_animacion = 200 

        # =========================
        # TEXTOS Y OPCIONES
        # =========================
        self.fuente_opciones = pygame.font.SysFont(None, 48)
        self.fuente_advertencia = pygame.font.SysFont(None, 36)
        
        # Estas opciones se reconfiguran dinámicamente desde el main.py
        self.opciones = ["Nueva Partida", "Salir al Escritorio"]
        self.indice_seleccionado = 0
        
        # Colores
        self.color_normal = (150, 150, 150)
        self.color_seleccionado = (255, 255, 255)
        self.color_advertencia = (255, 70, 70)

    def actualizar_opciones_disponibles(self, tiene_guardado):
        """Reconfigura la lista de opciones según la base de datos"""
        if tiene_guardado:
            self.opciones = ["Continuar", "Nueva Partida", "Salir al Escritorio"]
        else:
            self.opciones = ["Nueva Partida", "Salir al Escritorio"]
            
        # Corregimos límites si cambiamos de menú
        if self.indice_seleccionado >= len(self.opciones):
            self.indice_seleccionado = 0

    def procesar_eventos(self, eventos):
        """Lee las teclas para moverse por el menú o la confirmación"""
        for evento in eventos:
            if evento.type == pygame.KEYDOWN:
                if self.mostrando_confirmacion:
                    # Controles pantalla de confirmación
                    if evento.key in (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN):
                        self.indice_confirmacion = 0 if self.indice_confirmacion == 1 else 1
                    elif evento.key == pygame.K_RETURN:
                        if self.indice_confirmacion == 0:  # Eligió SÍ
                            self.mostrando_confirmacion = False
                            self.iniciar_juego = True
                        else:  # Eligió NO
                            self.mostrando_confirmacion = False
                    elif evento.key == pygame.K_ESCAPE:
                        self.mostrando_confirmacion = False
                else:
                    # Controles menú normal
                    if evento.key == pygame.K_DOWN:
                        self.indice_seleccionado = (self.indice_seleccionado + 1) % len(self.opciones)
                    elif evento.key == pygame.K_UP:
                        self.indice_seleccionado = (self.indice_seleccionado - 1) % len(self.opciones)
                    elif evento.key == pygame.K_RETURN:
                        self.ejecutar_opcion()

    def ejecutar_opcion(self):
        opcion = self.opciones[self.indice_seleccionado]
        
        if opcion == "Continuar":
            self.cargar_partida = True
        elif opcion == "Nueva Partida":
            # Si el menú tiene la opción "Continuar", significa que hay datos que sobreescribir
            if "Continuar" in self.opciones:
                self.mostrando_confirmacion = True
                self.indice_confirmacion = 1 # Enfocamos "No" por seguridad
            else:
                self.iniciar_juego = True 
        elif opcion == "Salir al Escritorio":
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
        
        # 3. Dibujar a Hoku durmiendo
        if len(self.frames_durmiendo) > 0:
            frame_actual = self.frames_durmiendo[self.indice_frame]
            pantalla.blit(frame_actual, (750, 355))
            
        # 4. Dibujar las opciones normales
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

        # 5. Dibujar caja de confirmación flotante si se requiere
        if self.mostrando_confirmacion:
            # Fondo del cuadro
            cuadro = pygame.Surface((600, 200))
            cuadro.fill((20, 20, 20))
            pygame.draw.rect(cuadro, self.color_advertencia, (0, 0, 600, 200), 3)
            
            # Textos de advertencia
            txt1 = self.fuente_advertencia.render("¿ESTÁS SEGURO?", True, self.color_advertencia)
            txt2 = self.fuente_advertencia.render("Tus datos guardados serán sobreescritos.", True, self.color_seleccionado)
            
            cuadro.blit(txt1, (300 - txt1.get_width()//2, 30))
            cuadro.blit(txt2, (300 - txt2.get_width()//2, 70))
            
            # Opciones SÍ / NO
            col_si = self.color_seleccionado if self.indice_confirmacion == 0 else self.color_normal
            col_no = self.color_seleccionado if self.indice_confirmacion == 1 else self.color_normal
            
            btn_si = self.fuente_opciones.render("> SÍ <" if self.indice_confirmacion == 0 else "SÍ", True, col_si)
            btn_no = self.fuente_opciones.render("> NO <" if self.indice_confirmacion == 1 else "NO", True, col_no)
            
            cuadro.blit(btn_si, (150 - btn_si.get_width()//2, 130))
            cuadro.blit(btn_no, (450 - btn_no.get_width()//2, 130))
            
            # Estampar cuadro en el centro de la pantalla
            pantalla.blit(cuadro, (self.ancho // 2 - 300, self.alto // 2 - 100))