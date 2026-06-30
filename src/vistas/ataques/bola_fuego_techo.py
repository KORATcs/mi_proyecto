import pygame
from src.vistas.personajes.personaje_grafico import PersonajeGrafico

class BolaFuegoTecho(PersonajeGrafico):
    """ Meteorito/Fuego vertical que cae del cielo e impacta en el suelo con iluminación circular """
    def __init__(self, x, y):
        super().__init__(x, y, None)

        # =========================
        # 🔧 CARGAR ANIMACIONES
        # =========================
        self.ancho_sprite = 100
        self.alto_sprite = 100
        
        # Fase 1: Caída libre
        self.cargar_animacion("caer", "src/assets/images/personajes/ataques/bola-de-fuego-avance-hit.png", 4, self.ancho_sprite, self.alto_sprite)
        # Fase 2: Impacto/Explosión
        self.cargar_animacion("impacto", "src/assets/images/personajes/ataques/bola-de-fuego-hit1.png", 5, self.ancho_sprite, self.alto_sprite)
        
        self.estado_actual = "caer"
        self.image = self.animaciones["caer"][0]

        # 🔧 CARGAR Y ESCALAR EL RESPLANDOR CIRCULAR (Para eliminar el cuadrado)
        # Asegurate de tener esta imagen: src/assets/images/personajes/ataques/resplandor.png
        # Debe ser una esfera suave y brillante con bordes difuminados y transparencia.
        # He puesto un respaldo generado por código que crea una esfera suave.
        try:
            self.imagen_resplandor = pygame.image.load("src/assets/images/personajes/ataques/resplandor.png").convert_alpha()
            # Escalar el resplandor para hacerlo más pequeño que el sprite (e.g., 70% del sprite)
            self.imagen_resplandor = pygame.transform.scale(self.imagen_resplandor, (70, 70))
        except:
            # Respaldo visual: un resplandor circular suave generado por código (Mejor que un cuadrado uwu)
            # Esto crea un degradado circular de fuego incandescente a transparente.
            resplandor_generado = pygame.Surface((70, 70), pygame.SRCALPHA)
            for r in range(35, 0, -1):
                # Crear un degradado suave de amarillo/naranja a transparente
                # El alfa (transparencia) aumenta hacia el centro para un efecto suave
                alfa = int((35 - r) / 35 * 180) # Más brillante en el centro
                pygame.draw.circle(resplandor_generado, (255, 200, 50, alfa), (35, 35), r)
            self.imagen_resplandor = resplandor_generado

        # =========================
        # HITBOX Y FÍSICAS
        # =========================
        self.rect = self.image.get_rect(topleft=(x, y))
        
        self.velocidad_caida = 4.5       
        self.velocidad_animacion = 80    
        self.limite_suelo = 630          # Ajustá este número para que coincida con tu suelo
        
        self.activo = True
        self.hacer_destello = False

    def actualizar(self):
        # --- MÁQUINA DE ESTADOS DEL METEORITO ---
        
        if self.estado_actual == "caer":
            # 1. Descenso normal
            self.cambiar_estado("caer", loop=True)
            self.rect.y += self.velocidad_caida
            
            # Si cruza la línea del suelo, frena y empieza a explotar
            if self.rect.y >= self.limite_suelo:
                self.rect.y = self.limite_suelo # Clavarla en el piso
                self.estado_actual = "impacto"
                self.velocidad_animacion = 60   # Explosión un poquito más rápida
                
        elif self.estado_actual == "impacto":
            # 2. Fase de impacto en el suelo (loop=False para saber cuándo termina)
            self.cambiar_estado("impacto", loop=False)
            
            # Activamos el efecto visual de iluminación circular en los frames finales de la explosión
            if self.indice_frame >= len(self.animaciones["impacto"]) - 3:
                self.hacer_destello = True
            
            # Cuando la animación de explosión llega al último frame, se elimina el objeto
            if self.indice_frame >= len(self.animaciones["impacto"]) - 1:
                self.activo = False

        # Actualiza los frames automáticos de la clase padre
        self.update_animacion(16)

    def dibujar(self, pantalla):
        # Rotamos la imagen SOLO en la fase de caída.
        if self.estado_actual == "caer":
            imagen_final = pygame.transform.rotate(self.image, -90)
            rect_imagen = imagen_final.get_rect(center=self.rect.center)
        else:
            # En impacto, usamos el sprite normal (derecho)
            imagen_final = self.image.copy()
            
            # 🔧 EFECTO DE ILUMINACIÓN/DESTELLO (CON CÍRCULO SUAVE, NO CUADRADO)
            if self.hacer_destello:
                # Centramos el resplandor circular sobre el sprite de impacto
                # (El resplandor es circular y ya está escalado a 70x70)
                rect_resplandor = self.imagen_resplandor.get_rect(center=imagen_final.get_rect().center)
                # Superponemos con BLEND_RGBA_ADD para el efecto de resplandor aditivo
                imagen_final.blit(self.imagen_resplandor, rect_resplandor, special_flags=pygame.BLEND_RGBA_ADD)

            rect_imagen = imagen_final.get_rect(center=self.rect.center)

        pantalla.blit(imagen_final, rect_imagen)