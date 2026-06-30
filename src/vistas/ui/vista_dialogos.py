import pygame

class VistaDialogos:
    def __init__(self):
        # =========================
        # CARGA DE ASSETS
        # =========================
        self.img_boton_e = pygame.image.load("src/assets/images/HUD/boton-E.png").convert_alpha()
        
        # 1. Cargamos el globo y lo AGRANDAMOS
        # Puedes cambiar el '1.5' por 2.0 (doble) o 1.2 (un poco más) según lo necesites.
        img_globo_orig = pygame.image.load("src/assets/images/HUD/globo-de-texto.png").convert_alpha()
        nuevo_ancho = int(img_globo_orig.get_width() * 2.5) 
        nuevo_alto = int(img_globo_orig.get_height() * 2)
        self.img_globo_texto = pygame.transform.scale(img_globo_orig, (nuevo_ancho, nuevo_alto))
        
        self.fuente_dialogo = pygame.font.SysFont(None, 24)
        
        # Variables de animación
        self.alpha_ui = 0 
        self.velocidad_fade = 15

    def actualizar(self, hoku_rect, npcs):
        """Calcula el fade in/out dependiendo de si Hoku está cerca de algún NPC"""
        hoku_cerca_de_alguien = False

        for npc in npcs:
            area_interaccion = npc.rect.inflate(150, 150)
            
            if hoku_rect.colliderect(area_interaccion):
                hoku_cerca_de_alguien = True
                break
            else:
                if hasattr(npc, 'modelo') and npc.modelo.mostrando_dialogo:
                    npc.modelo.mostrando_dialogo = False

        # Aplicamos la animación de fade
        if hoku_cerca_de_alguien:
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
            # Probamos cómo quedaría la línea si le sumamos la palabra nueva
            prueba_linea = linea_actual + palabra + " "
            ancho_prueba, _ = fuente.size(prueba_linea)
            
            if ancho_prueba <= max_ancho:
                # Si entra bien en el globo, la sumamos a la línea
                linea_actual = prueba_linea
            else:
                # Si se pasa del borde, guardamos la línea y empezamos una nueva
                if linea_actual:
                    lineas.append(linea_actual.strip())
                linea_actual = palabra + " "
        
        # Añadimos la última línea que quedó pendiente
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
            area_interaccion = npc.rect.inflate(150, 150)
            
            if hoku_rect.colliderect(area_interaccion):
                
                # 1. ESTÁ HABLANDO -> Dibujar GLOBO y TEXTO AJUSTADO
                if hasattr(npc.modelo, 'mostrando_dialogo') and npc.modelo.mostrando_dialogo:
                    
                    pos_globo_x = npc.rect.centerx - (self.img_globo_texto.get_width() // 2)
                    pos_globo_y = npc.rect.top - self.img_globo_texto.get_height() - 10
                    pantalla.blit(self.img_globo_texto, (pos_globo_x, pos_globo_y))

                    texto_actual = npc.modelo.dialogos_actuales[npc.modelo.indice_dialogo]
                    
                    # 2. Calcular márgenes (dejamos 40px de respiro adentro del globo)
                    max_ancho_texto = self.img_globo_texto.get_width() - 40 
                    
                    # 3. Dividir el texto en múltiples líneas
                    lineas_texto = self.dividir_texto(texto_actual, self.fuente_dialogo, max_ancho_texto)
                    
                    # 4. Calcular la altura total para centrar todo el bloque de texto
                    altura_linea = self.fuente_dialogo.get_linesize()
                    altura_total_texto = len(lineas_texto) * altura_linea
                    start_y = pos_globo_y + (self.img_globo_texto.get_height() // 2) - (altura_total_texto // 2)

                    # 5. Dibujar línea por línea
                    for i, linea in enumerate(lineas_texto):
                        superficie_texto = self.fuente_dialogo.render(linea, True, (0, 0, 0)) # Texto negro
                        superficie_texto.set_alpha(self.alpha_ui)
                        
                        pos_texto_x = pos_globo_x + (self.img_globo_texto.get_width() // 2) - (superficie_texto.get_width() // 2)
                        pos_texto_y = start_y + (i * altura_linea)
                        
                        pantalla.blit(superficie_texto, (pos_texto_x, pos_texto_y))
                
                # 2. NO ESTÁ HABLANDO -> Dibujar BOTÓN [E]
                else:
                    pos_boton_x = npc.rect.centerx - (self.img_boton_e.get_width() // 2)
                    pos_boton_y = npc.rect.top - self.img_boton_e.get_height() - 10
                    pantalla.blit(self.img_boton_e, (pos_boton_x, pos_boton_y))