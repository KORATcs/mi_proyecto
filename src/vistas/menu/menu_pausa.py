import pygame
import sys

class MenuPausa:
    def __init__(self, ancho, alto):
        self.ancho = ancho
        self.alto = alto
        
        # Banderas para avisarle al main.py qué decisión tomó el jugador
        self.continuar_juego = False
        self.retornar_al_menu = False
        self.cargar_checkpoint = False
        
        # Estado del sub-menú de confirmación
        self.mostrando_confirmacion = False
        self.indice_confirmacion = 1 # 0 = Sí, 1 = No
        
        # Filtro oscuro de fondo
        self.filtro_oscuro = pygame.Surface((self.ancho, self.alto))
        self.filtro_oscuro.set_alpha(180) 
        self.filtro_oscuro.fill((0, 0, 0)) 
        
        # Configuración del Título "PAUSA"
        self.fuente_titulo = pygame.font.SysFont(None, 100)
        self.texto_titulo = self.fuente_titulo.render("PAUSA", True, (255, 255, 255))
        self.rect_titulo = self.texto_titulo.get_rect(center=(self.ancho // 2, self.alto // 6))
        
        # Configuración de las Opciones
        self.fuente_opciones = pygame.font.SysFont(None, 48)
        self.fuente_advertencia = pygame.font.SysFont(None, 34)
        
        self.opciones = ["Continuar", "Cargar Último Punto de Control", "Salir al Menú", "Salir al Escritorio"]
        self.indice_seleccionado = 0 
        
        self.color_normal = (150, 150, 150)       
        self.color_seleccionado = (255, 255, 255) 
        self.color_advertencia = (255, 70, 70)

    def procesar_eventos(self, eventos):
        """Escucha las flechas y el Enter controlando si hay cuadro de diálogo activo"""
        for evento in eventos:
            if evento.type == pygame.KEYDOWN:
                if self.mostrando_confirmacion:
                    if evento.key in (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN):
                        self.indice_confirmacion = 0 if self.indice_confirmacion == 1 else 1
                    elif evento.key == pygame.K_RETURN:
                        if self.indice_confirmacion == 0: # SÍ
                            self.mostrando_confirmacion = False
                            self.cargar_checkpoint = True
                        else: # NO
                            self.mostrando_confirmacion = False
                    elif evento.key == pygame.K_ESCAPE:
                        self.mostrando_confirmacion = False
                else:
                    if evento.key == pygame.K_DOWN:
                        self.indice_seleccionado = (self.indice_seleccionado + 1) % len(self.opciones)
                    elif evento.key == pygame.K_UP:
                        self.indice_seleccionado = (self.indice_seleccionado - 1) % len(self.opciones)
                    elif evento.key == pygame.K_RETURN:
                        self.ejecutar_opcion()

    def ejecutar_opcion(self):
        opcion = self.opciones[self.indice_seleccionado]
        
        if opcion == "Continuar":
            self.continuar_juego = True
        elif opcion == "Cargar Último Punto de Control":
            self.mostrando_confirmacion = True
            self.indice_confirmacion = 1
        elif opcion == "Salir al Menú":
            self.retornar_al_menu = True
        elif opcion == "Salir al Escritorio":
            pygame.quit()
            sys.exit()

    def dibujar(self, pantalla):
        """Dibuja el filtro, el título y la lista de opciones centradas"""
        pantalla.blit(self.filtro_oscuro, (0, 0))
        pantalla.blit(self.texto_titulo, self.rect_titulo)
        
        pos_y_inicial = self.alto // 2 - 80
        for i, texto in enumerate(self.opciones):
            if i == self.indice_seleccionado:
                color = self.color_seleccionado
                texto_mostrar = f"> {texto} <" 
            else:
                color = self.color_normal
                texto_mostrar = texto
                
            superficie_texto = self.fuente_opciones.render(texto_mostrar, True, color)
            rect_texto = superficie_texto.get_rect(center=(self.ancho // 2, pos_y_inicial + (i * 60)))
            pantalla.blit(superficie_texto, rect_texto)

        # Cartel de advertencia de Checkpoint
        if self.mostrando_confirmacion:
            cuadro = pygame.Surface((620, 200))
            cuadro.fill((20, 20, 20))
            pygame.draw.rect(cuadro, self.color_advertencia, (0, 0, 620, 200), 3)
            
            txt1 = self.fuente_advertencia.render("¿ESTÁS SEGURO?", True, self.color_advertencia)
            txt2 = self.fuente_advertencia.render("Los datos de progreso no guardados se perderán por completo.", True, self.color_seleccionado)
            
            cuadro.blit(txt1, (310 - txt1.get_width()//2, 30))
            cuadro.blit(txt2, (310 - txt2.get_width()//2, 70))
            
            col_si = self.color_seleccionado if self.indice_confirmacion == 0 else self.color_normal
            col_no = self.color_seleccionado if self.indice_confirmacion == 1 else self.color_normal
            
            btn_si = self.fuente_opciones.render("> SÍ <" if self.indice_confirmacion == 0 else "SÍ", True, col_si)
            btn_no = self.fuente_opciones.render("> NO <" if self.indice_confirmacion == 1 else "NO", True, col_no)
            
            cuadro.blit(btn_si, (150 - btn_si.get_width()//2, 130))
            cuadro.blit(btn_no, (470 - btn_no.get_width()//2, 130))
            
            pantalla.blit(cuadro, (self.ancho // 2 - 310, self.alto // 2 - 100))