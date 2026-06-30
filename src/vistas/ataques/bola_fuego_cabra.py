import pygame
from src.vistas.personajes.personaje_grafico import PersonajeGrafico

class BolaFuegoCabra(PersonajeGrafico):
    """ Bola de fuego horizontal con fase de carga y fase de lanzamiento """
    def __init__(self, x, y, hacia_derecha):
        super().__init__(x, y, None)

        # =========================
        # 🔧 CARGAR AMBAS ANIMACIONES
        # =========================
        # Fase 1: Crecer (Se queda quieta en la frente)
        self.cargar_animacion("crecer", "src/assets/images/personajes/ataques/bola-de-fuego-hit1.png", 5, 100, 100)
        # Fase 2: Avance (Sale disparada)
        self.cargar_animacion("volar", "src/assets/images/personajes/ataques/bola-de-fuego-avance-hit.png", 4, 100, 100)
        
        # Estado inicial
        self.estado_actual = "crecer"
        self.image = self.animaciones["crecer"][0]

        # =========================
        # HITBOX Y SETEO INICIAL
        # =========================
        self.rect = self.image.get_rect(center=(x, y))
        
        # Guardamos la velocidad pero NO la usamos hasta que termine de crecer
        self.velocidad_disparo = 5.5 * (1 if hacia_derecha else -1)
        self.mirando_derecha = hacia_derecha
        self.activo = True
        
        self.velocidad_animacion = 90  # Tiempo para los frames de carga

    def actualizar(self):
        # --- MÁQUINA DE ESTADOS DEL PROYECTIL ---
        
        if self.estado_actual == "crecer":
            # 1. Se queda quieta cargando en la frente de la cabra
            # Avanzamos la animación SIN bucle (loop=False) para detectar el final
            self.cambiar_estado("crecer", loop=False)
            
            # Verificamos si llegó al último frame del crecimiento
            if self.indice_frame >= len(self.animaciones["crecer"]) - 1:
                # ¡Terminó de crecer! Cambiamos al estado volar
                self.estado_actual = "volar"
                self.velocidad_animacion = 70 # Podemos hacer que vuele con frames más rápidos
                
        elif self.estado_actual == "volar":
            # 2. Ya creció, ahora se mueve y cicla su sprite en bucle (loop=True)
            self.cambiar_estado("volar", loop=True)
            self.rect.x += self.velocidad_disparo
            
            # Si sale de la pantalla se destruye de forma automática
            if self.rect.x > 1300 or self.rect.x < -100:
                self.activo = False

        # Actualiza los frames de la clase padre según el estado configurado
        self.update_animacion(16)

    def dibujar(self, pantalla):
        img = self.image
        if not self.mirando_derecha:
            img = pygame.transform.flip(img, True, False)
            
        pantalla.blit(img, self.rect)