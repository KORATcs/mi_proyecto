import pygame

class HUD:
    def __init__(self, personaje, x, y):
        self.personaje = personaje  # Modelo lógico de Hoku
        self.x = x
        self.y = y

        # Carga de imágenes de los corazones
        try:
            self.img_corazon_lleno = pygame.image.load("src/assets/images/HUD/corazon-Sheet.png").convert_alpha()
            self.img_corazon_vacio = pygame.image.load("src/assets/images/HUD/corazon-vacio.png").convert_alpha()
            
            self.img_corazon_lleno = pygame.transform.scale(self.img_corazon_lleno, (60, 60))
            self.img_corazon_vacio = pygame.transform.scale(self.img_corazon_vacio, (60, 60))
        except Exception as e:
            print(f"[HUD ERROR]: No se pudieron cargar las imágenes de los corazones: {e}")
            self.img_corazon_lleno = None
            self.img_corazon_vacio = None

        self.fuente = pygame.font.SysFont("Arial", 18, bold=True)

    def dibujar(self, pantalla):
        # Accedemos directamente a las variables reales de tu Hoku lúdico
        vida_actual = int(getattr(self.personaje, "_vida", 4))
        vida_max = int(getattr(self.personaje, "vida_maxima", 4))
        ataque_actual = getattr(self.personaje, "ataque", 1)

        # DIBUJAR LOS CORAZONES
        espaciado = 65  
        for i in range(vida_max):
            pos_x = self.x + (i * espaciado)
            pos_y = self.y
            
            if i < vida_actual:
                if self.img_corazon_lleno:
                    pantalla.blit(self.img_corazon_lleno, (pos_x, pos_y))
                else:
                    pygame.draw.rect(pantalla, (0, 255, 0), (pos_x, pos_y, 50, 50))
            else:
                if self.img_corazon_vacio:
                    pantalla.blit(self.img_corazon_vacio, (pos_x, pos_y))
                else:
                    pygame.draw.rect(pantalla, (255, 0, 0), (pos_x, pos_y, 50, 50), 2)
