import pygame
import random

# 🛠️ MODO DEPURACIÓN: Cambialo a True para ver las cajas de colisión en pantalla y calibrarlas
VER_HITBOXES = False  # Cambiar a False para desactivar la visualización de hitboxes

# ==================================================
# CLASE AUXILIAR: PROCESADOR AUTOMÁTICO DE ANIMACIONES
# ==================================================
class AnimadorSpritesheet:
    def __init__(self, ruta, columnas, filas, fps, ancho_destino=None, alto_destino=None):
        self.frames = []
        self.indice = 0
        self.timer = 0
        self.fps = fps
        self.tiempo_por_frame = 1000 / fps  

        try:
            self.sheet = pygame.image.load(ruta).convert_alpha()
            ancho_original_frame = self.sheet.get_width() // columnas
            alto_original_frame = self.sheet.get_height() // filas
            
            for f in range(filas):
                for c in range(columnas):
                    rect_recorte = pygame.Rect(
                        c * ancho_original_frame, 
                        f * alto_original_frame, 
                        ancho_original_frame, 
                        alto_original_frame
                    )
                    frame_recortado = self.sheet.subsurface(rect_recorte)
                    
                    if ancho_destino and alto_destino:
                        frame_recortado = pygame.transform.scale(frame_recortado, (ancho_destino, alto_destino))
                    
                    self.frames.append(frame_recortado)
        except Exception as e:
            print(f"[ERROR MINIJUEGO]: No se pudo cargar la ruta: {ruta}. Motivo: {e}")
            self.frames = []

    def actualizar(self, dt):
        if not self.frames:
            return
        self.timer += dt
        if self.timer >= self.tiempo_por_frame:
            self.timer -= self.tiempo_por_frame
            self.indice = (self.indice + 1) % len(self.frames)

    def obtener_frame_actual(self):
        if not self.frames:
            return None
        return self.frames[self.indice]


# ==================================================
# PERSONAJE: FUEGO FATUO (MOVIMIENTO LIBRE)
# ==================================================
class PersonajeMinijuego:
    def __init__(self, x, y, ancho_pantalla, alto_pantalla):
        self.x = x
        self.y = y
        
        self.ancho = 150  
        self.alto = 150
        self.velocidad = 0.55  
        
        # AJUSTE DE HITBOX: Cuántos píxeles recortar de la colisión (Negativo = Achicar)
        self.hitbox_ajuste_ancho = -60
        self.hitbox_ajuste_alto = -60
        
        self.ancho_pantalla = ancho_pantalla
        self.alto_pantalla = alto_pantalla
        
        self.animacion = AnimadorSpritesheet(
            ruta="src/assets/images/minijuego/fuego-fatuo-minijuego-Sheet.png", 
            columnas=4,   
            filas=1,      
            fps=10,       
            ancho_destino=self.ancho, 
            alto_destino=self.alto
        )

    def obtener_hitbox(self):
        # Creamos el rectángulo exterior de la imagen completa
        rect_completo = pygame.Rect(self.x, self.y, self.ancho, self.alto)
        # .inflate achica la caja manteniendo el centro perfecto del personaje
        return rect_completo.inflate(self.hitbox_ajuste_ancho, self.hitbox_ajuste_alto)

    def mover(self, izquierda, derecha, arriba, abajo, dt):
        if izquierda and self.x > 0:
            self.x -= self.velocidad * dt
        if derecha and self.x + self.ancho < self.ancho_pantalla:
            self.x += self.velocidad * dt
        if arriba and self.y > 0:
            self.y -= self.velocidad * dt
        if abajo and self.y + self.alto < self.alto_pantalla:
            self.y += self.velocidad * dt
            
        self.animacion.actualizar(dt)

    def dibujar(self, pantalla):
        img = self.animacion.obtener_frame_actual()
        if img:
            pantalla.blit(img, (self.x, self.y))
        else:
            pygame.draw.rect(pantalla, (0, 200, 255), (self.x, self.y, self.ancho, self.alto))
            
        # Si el modo debug está activo, dibuja el contorno de la hitbox real en VERDE
        if VER_HITBOXES:
            pygame.draw.rect(pantalla, (0, 255, 0), self.obtener_hitbox(), 2)


# ==================================================
# OBSTÁCULOS: ROCAS (GRANDES Y PEQUEÑAS)
# ==================================================
class ObstaculoMinijuego:
    def __init__(self, x, y, ancho_pantalla, alto_pantalla, es_grande=False):
        self.x = x
        self.y = y
        self.es_grande = es_grande
        self.ancho_pantalla = ancho_pantalla
        self.alto_pantalla = alto_pantalla
        
        if es_grande:
            self.ancho = 200  
            self.alto = 200
            self.velocidad = 0.38  
            
            # AJUSTE DE HITBOX ROCA GIGANTE
            self.hitbox_ajuste_ancho = -90  
            self.hitbox_ajuste_alto = -90
            
            self.animacion = AnimadorSpritesheet(
                ruta="src/assets/images/minijuego/roca-gigante-Sheet.png", 
                columnas=6,  
                filas=1,     
                fps=8,       
                ancho_destino=self.ancho,
                alto_destino=self.alto
            )
        else:
            self.ancho = 100  
            self.alto = 100
            self.velocidad = 0.61  
            
            # AJUSTE DE HITBOX ROCA CHICA/FUEGO
            self.hitbox_ajuste_ancho = -40
            self.hitbox_ajuste_alto = -40
            
            self.animacion = AnimadorSpritesheet(
                ruta="src/assets/images/minijuego/fuego-minijuego-Sheet.png",  
                columnas=2,  
                filas=1,     
                fps=12,      
                ancho_destino=self.ancho,
                alto_destino=self.alto
            )

    def obtener_hitbox(self):
        rect_completo = pygame.Rect(self.x, self.y, self.ancho, self.alto)
        return rect_completo.inflate(self.hitbox_ajuste_ancho, self.hitbox_ajuste_alto)
            
    def mover(self, dt):
        self.y += self.velocidad * dt
        self.animacion.actualizar(dt)
        
        if self.y > self.alto_pantalla:
            self.y = -self.alto
            self.x = random.randint(0, self.ancho_pantalla - self.ancho)

    def dibujar(self, pantalla):
        img = self.animacion.obtener_frame_actual()
        if img:
            pantalla.blit(img, (self.x, self.y))
        else:
            color = (130, 40, 40) if self.es_grande else (240, 70, 70)
            pygame.draw.rect(pantalla, color, (self.x, self.y, self.ancho, self.alto))
            
        # Si el modo debug está activo, dibuja la hitbox real del obstáculo en ROJO
        if VER_HITBOXES:
            pygame.draw.rect(pantalla, (255, 0, 0), self.obtener_hitbox(), 2)


# ==================================================
# MANAGER GENERAL DEL MINIJUEGO
# ==================================================
class MinijuegoGrieta:
    def __init__(self, pantalla):
        self.pantalla = pantalla
        self.ancho = pantalla.get_width()   
        self.alto = pantalla.get_height()   
        
        self.animacion_fondo = AnimadorSpritesheet(
            ruta="src/assets/images/minijuego/fondo-minijuego-Sheet.png", 
            columnas=10,  
            filas=1,
            fps=15,      
            ancho_destino=self.ancho, 
            alto_destino=self.alto    
        )
        
        self.reiniciar()

    def reiniciar(self):
        self.jugador = PersonajeMinijuego(self.ancho // 2 - 75, self.alto - 200, self.ancho, self.alto)
        self.obstaculos = []
        
        for _ in range(5): 
            x_random = random.randint(0, self.ancho - 100)
            y_random = random.randint(-600, -50)
            self.obstaculos.append(ObstaculoMinijuego(x_random, y_random, self.ancho, self.alto, es_grande=False))
            
        for _ in range(3): 
            x_random = random.randint(0, self.ancho - 200)
            y_random = random.randint(-900, -200)
            self.obstaculos.append(ObstaculoMinijuego(x_random, y_random, self.ancho, self.alto, es_grande=True))
            
        self.metros_escalados = 0
        self.meta_metros = 3500  
        self.activo = True

    def actualizar(self, dt, callback_victoria):
        if not self.activo:
            return

        self.animacion_fondo.actualizar(dt)

        teclas = pygame.key.get_pressed()
        izquierda = teclas[pygame.K_LEFT] or teclas[pygame.K_a]
        derecha = teclas[pygame.K_RIGHT] or teclas[pygame.K_d]
        arriba = teclas[pygame.K_UP] or teclas[pygame.K_w]
        abajo = teclas[pygame.K_DOWN] or teclas[pygame.K_s]
        
        self.jugador.mover(izquierda, derecha, arriba, abajo, dt)
        
        # 🚨 CAMBIO CLAVE: Ahora obtenemos la hitbox calibrada en lugar del área total de la imagen
        rect_jugador = self.jugador.obtener_hitbox()
        
        for obs in self.obstaculos:
            obs.mover(dt)
            # 🚨 CAMBIO CLAVE: Obtenemos la hitbox calibrada de la roca
            rect_obs = obs.obtener_hitbox()
            
            if rect_jugador.colliderect(rect_obs):
                print("[Minijuego]: ¡Fuego Fatuo golpeado! Reiniciando el ascenso...")
                self.reiniciar()
                return

        self.metros_escalados += 0.22 * dt
        if self.metros_escalados >= self.meta_metros:
            self.activo = False
            callback_victoria()

    def dibujar(self):
        img_fondo = self.animacion_fondo.obtener_frame_actual()
        if img_fondo:
            self.pantalla.blit(img_fondo, (0, 0))
        else:
            self.pantalla.fill((18, 12, 22)) 
        
        for obs in self.obstaculos:
            obs.dibujar(self.pantalla)

        self.jugador.dibujar(self.pantalla)

        fuente = pygame.font.SysFont("Arial", 26, bold=True)
        texto = fuente.render(f"Escapando hacia el cielo: {int(self.metros_escalados)} / {self.meta_metros}m", True, (255, 255, 255))
        self.pantalla.blit(texto, (40, 30))