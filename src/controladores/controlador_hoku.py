import pygame

class ControladorHoku:
    def __init__(self):
        self.atacando = False
        self.saltando = False
        self.interactuando = False # 🔧 NUEVO ESTADO

    def procesar_eventos(self, eventos):
        """Eventos puntuales (click, teclas presionadas una vez)"""
        self.atacando = False
        self.saltando = False
        self.interactuando = False # 🔧 REINICIAMOS EN CADA FRAME

        for evento in eventos:
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1:
                    self.atacando = True

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    self.saltando = True
                
                # 🔧 NUEVO EVENTO: Detectar la tecla E para interactuar
                if evento.key == pygame.K_e: 
                    self.interactuando = True

    def obtener_movimiento(self):
        """Movimiento continuo (teclas mantenidas)"""
        teclas = pygame.key.get_pressed()

        dx, dy = 0, 0
        velocidad = 15
        velocidad_2 = 15

        if teclas[pygame.K_w]:
            dy -= velocidad_2
        if teclas[pygame.K_s]:
            dy += velocidad_2
        if teclas[pygame.K_a]:
            dx -= velocidad
        if teclas[pygame.K_d]:
            dx += velocidad

        return dx, dy

    def salto(self):
        """Detecta salto"""
        teclas = pygame.key.get_pressed()
        return teclas[pygame.K_SPACE]