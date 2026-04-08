import pygame

class PersonajeGrafico:
    def __init__(self, x, y, ancho, alto, color):
        # El rect maneja la posición y las colisiones
        self.rect = pygame.Rect(x, y, ancho, alto)
        self.color = color
        self.color_ojos_base = (255, 255, 255) # Blanco
        self.color_pupila = (0, 0, 0)         # Negro
        
    def mover(self, dx, dy, limite_pantalla):
        """Mueve el personaje y lo mantiene dentro de la pantalla"""
        self.rect.x += dx
        self.rect.y += dy
        self.rect.clamp_ip(limite_pantalla)

    def colisiona_con(self, otro_personaje):
        """Verifica si colisiona con otro objeto PersonajeGrafico"""
        return self.rect.colliderect(otro_personaje.rect)

    def dibujar(self, pantalla):
        """Dibuja el gatito completo en la pantalla"""
        cx, cy = self.rect.center
        
        # 1. Orejas (ajustadas a los costados)
        # Izquierda
        pygame.draw.polygon(pantalla, self.color, [
            (cx - 30, cy - 10), (cx - 35, cy - 35), (cx - 10, cy - 25)
        ])
        # Derecha
        pygame.draw.polygon(pantalla, self.color, [
            (cx + 30, cy - 10), (cx + 35, cy - 35), (cx + 10, cy - 25)
        ])

        # 2. Cabeza
        pygame.draw.circle(pantalla, self.color, (cx, cy), 30)

        # 3. Ojos nwn
        # Bases blancas
        pygame.draw.circle(pantalla, self.color_ojos_base, (cx - 12, cy - 5), 10)
        pygame.draw.circle(pantalla, self.color_ojos_base, (cx + 12, cy - 5), 10)
        # Pupilotas negras
        pygame.draw.circle(pantalla, self.color_pupila, (cx - 12, cy - 5), 7)
        pygame.draw.circle(pantalla, self.color_pupila, (cx + 12, cy - 5), 7)
        # Brillos
        pygame.draw.circle(pantalla, self.color_ojos_base, (cx - 15, cy - 8), 2)
        pygame.draw.circle(pantalla, self.color_ojos_base, (cx + 9, cy - 8), 2)

        # 4. Naricita
        pygame.draw.polygon(pantalla, (255, 100, 100), [(cx, cy + 5), (cx - 3, cy + 2), (cx + 3, cy + 2)])