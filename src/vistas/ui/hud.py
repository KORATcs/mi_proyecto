import pygame

class HUD:
    def __init__(self, personaje, x, y, ancho=200, alto=20, color=(200, 0, 0)):
        self.personaje = personaje  # modelo lógico
        self.x = x
        self.y = y
        self.ancho = ancho
        self.alto = alto
        self.color = color

        self.borde_color = (255, 255, 255)
        self.fondo_color = (60, 60, 60)

        # fuente
        self.fuente = pygame.font.SysFont("Arial", 18)

    def dibujar(self, pantalla):
        # 🧠 obtener vida
        vida_max = self.personaje._vida
        vida_actual = vida_max
        

        # 🛡️ evitar división por cero
        if vida_max <= 0:
            proporcion = 0
        else:
            proporcion = max(0, vida_actual / vida_max)

        # 📦 fondo barra
        pygame.draw.rect(
            pantalla,
            self.fondo_color,
            (self.x, self.y, self.ancho, self.alto)
        )

        # ❤️ barra de vida
        pygame.draw.rect(
            pantalla,
            self.color,
            (self.x, self.y, self.ancho * proporcion, self.alto)
        )

        # 🧱 borde
        pygame.draw.rect(
            pantalla,
            self.borde_color,
            (self.x, self.y, self.ancho, self.alto),
            2
        )

        # 📝 texto
        texto = f"HP: {vida_actual}/{vida_max}  ATK: {self.personaje.ataque}"
        superficie_texto = self.fuente.render(texto, True, (255, 255, 255))

        pantalla.blit(superficie_texto, (self.x, self.y + self.alto + 5))