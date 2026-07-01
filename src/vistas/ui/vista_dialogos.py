import pygame
import math

class VistaDialogos:
    def __init__(self):
        # =========================
        # CARGA DE ASSETS
        # =========================
        img_e_original = pygame.image.load("src/assets/images/HUD/boton-E.png").convert_alpha()
        # 🔧 NUEVO: Hacemos la imagen del botón E más pequeña (ej: 24x24 píxeles)
        self.img_boton_e = pygame.transform.scale(img_e_original, (50, 50))
        
        # 1. Cargamos el globo y lo AGRANDAMOS
        img_globo_orig = pygame.image.load("src/assets/images/HUD/globo-de-texto.png").convert_alpha()
        nuevo_ancho = int(img_globo_orig.get_width() * 3) 
        nuevo_alto = int(img_globo_orig.get_height() * 2.5)
        self.img_globo_texto = pygame.transform.scale(img_globo_orig, (nuevo_ancho, nuevo_alto))
        
        self.fuente_dialogo = pygame.font.SysFont(None, 24)
        
        # Variables de animación
        self.alpha_ui = 0 
        self.velocidad_fade = 15

    def actualizar(self, hoku_rect, npcs):
        """Calcula el fade in/out dependiendo de si Hoku está cerca de algún NPC"""
        hoku_cerca_de_alguien = False
        alguien_esta_hablando = False # 🔧 Nueva bandera

        for npc in npcs:
            area_interaccion = npc.rect.inflate(250, 250) # 🔧 (Radio más grande aquí)
            
            # Verificamos si el NPC puntualmente está en medio de una charla
            if hasattr(npc, 'modelo') and npc.modelo.mostrando_dialogo:
                alguien_esta_hablando = True

            if hoku_rect.colliderect(area_interaccion):
                hoku_cerca_de_alguien = True
                # 🔧 BORRAMOS el 'break' para que revise a todos los NPCs y el 'else' que te apagaba el diálogo
        
        # 🔧 MODIFICADO: La interfaz se mantiene visible (alpha_ui = 255) 
        # ya sea porque Hoku está cerca del botón, O porque el globo de texto está activo charlando.
        if hoku_cerca_de_alguien or alguien_esta_hablando:
            self.alpha_ui = min(255, self.alpha_ui + self.velocidad_fade)
        else:
            self.alpha_ui = max(0, self.alpha_ui - self.velocidad_fade)

    def dividir_texto(self, texto, fuente, max_ancho):
        """ 
        Divide un texto largo en una lista de líneas más cortas.
        Corta justo antes de superar el 'max_ancho' para que no sobresalga.
        """
        palabras = texto.split(' ')
        lineas = []
        linea_actual = ""

        for palabra in palabras:
            prueba_linea = linea_actual + palabra + " "
            ancho_prueba, _ = fuente.size(prueba_linea)
            
            if ancho_prueba <= max_ancho:
                linea_actual = prueba_linea
            else:
                if linea_actual:
                    lineas.append(linea_actual.strip())
                linea_actual = palabra + " "
        
        if linea_actual:
            lineas.append(linea_actual.strip())
            
        return lineas

    def dibujar(self, pantalla, hoku_rect, npcs):
        """Dibuja el botón o el globo de texto si Hoku está en el área"""
        if self.alpha_ui <= 0:
            return 

        self.img_boton_e.set_alpha(self.alpha_ui)
        self.img_globo_texto.set_alpha(self.alpha_ui)

        for npc in npcs:
            area_interaccion = npc.rect.inflate(250, 250)
            
            if hoku_rect.colliderect(area_interaccion):
                
                # ==============================================================
                # 1. ESTÁ HABLANDO -> Dibujar GLOBO (A la derecha) y TEXTO
                # ==============================================================
                if hasattr(npc.modelo, 'mostrando_dialogo') and npc.modelo.mostrando_dialogo:
                    
                    # 🔧 MODIFICADO: Ahora el globo se dibuja a la derecha del NPC (+20px)
                    pos_globo_x = npc.rect.right + 20
                    pos_globo_y = npc.rect.top - (self.img_globo_texto.get_height() // 3)
                    pantalla.blit(self.img_globo_texto, (pos_globo_x, pos_globo_y))

                    texto_actual = npc.modelo.dialogos_actuales[npc.modelo.indice_dialogo]
                    
                    # 🔧 MODIFICADO: Mayor margen interno (50px) para que quede impecable y centrado
                    max_ancho_texto = self.img_globo_texto.get_width() - 50 
                    
                    lineas_texto = self.dividir_texto(texto_actual, self.fuente_dialogo, max_ancho_texto)
                    
                    altura_linea = self.fuente_dialogo.get_linesize()
                    altura_total_texto = len(lineas_texto) * altura_linea
                    start_y = pos_globo_y + (self.img_globo_texto.get_height() // 2) - (altura_total_texto // 2)

                    for i, linea in enumerate(lineas_texto):
                        superficie_texto = self.fuente_dialogo.render(linea, True, (0, 0, 0)) # Texto negro
                        superficie_texto.set_alpha(self.alpha_ui)
                        
                        pos_texto_x = pos_globo_x + (self.img_globo_texto.get_width() // 2) - (superficie_texto.get_width() // 2)
                        pos_texto_y = start_y + (i * altura_linea)
                        
                        pantalla.blit(superficie_texto, (pos_texto_x, pos_texto_y))
                
                # ==============================================================
                # 2. NO ESTÁ HABLANDO -> Dibujar BOTÓN [E] (Pequeño y con Brillo)
                # ==============================================================
                else:
                    pos_boton_x = npc.rect.centerx - (self.img_boton_e.get_width() // 2)
                    pos_boton_y = npc.rect.top - self.img_boton_e.get_height() - 15

                    # 🔧 NUEVO: Efecto de Haz de Luz pulsante detras de la E
                    e_center_x = npc.rect.centerx
                    e_center_y = pos_boton_y + (self.img_boton_e.get_height() // 2)
                    
                    tiempo = pygame.time.get_ticks()
                    pulsacion = math.sin(tiempo * 0.005) * 5  # Controla la velocidad e intensidad
                    radio_luz = max(5, int(15 + pulsacion))   # Asegura que el radio no sea negativo

                    # Superficie transparente para el haz de luz
                    superficie_luz = pygame.Surface((radio_luz * 4, radio_luz * 4), pygame.SRCALPHA)
                    # Color celeste mágico brillante con el mismo alpha general del UI
                    alpha_haz = int((self.alpha_ui / 255) * 90) # Máxima opacidad de 90
                    color_haz = (100, 220, 255, alpha_haz) 
                    
                    pygame.draw.circle(superficie_luz, color_haz, (radio_luz, radio_luz), radio_luz)
                    pantalla.blit(superficie_luz, (e_center_x - radio_luz, e_center_y - radio_luz))

                    # Dibujamos el botón físico arriba del haz
                    pantalla.blit(self.img_boton_e, (pos_boton_x, pos_boton_y))