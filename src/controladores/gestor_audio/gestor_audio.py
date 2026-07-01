import pygame

class GestorAudio:
    def __init__(self):
        # Inicializamos el mixer de Pygame
        pygame.mixer.init()
        
        # Diccionario para almacenar los efectos de sonido (SFX) cortos
        self.efectos = {}
        
        # Opcional: Podés cargar los efectos de sonido acá para tenerlos listos
        # self.cargar_efecto("golpe", "src/assets/audio/sfx/golpe.wav")

    # ==========================================
    # LÓGICA PARA MÚSICA DE FONDO (Streaming)
    # ==========================================
    def reproducir_musica(self, ruta_archivo, volumen=1.0):
        """Carga y reproduce una canción de fondo en bucle infinito"""
        try:
            pygame.mixer.music.load(ruta_archivo)
            pygame.mixer.music.set_volume(volumen)
            pygame.mixer.music.play(-1) # -1 significa loop infinito
        except pygame.error as e:
            print(f"Error al cargar la música {ruta_archivo}: {e}")

    def detener_musica(self, tiempo_fade=1000):
        """Detiene la música actual con un efecto de desaparición suave"""
        pygame.mixer.music.fadeout(tiempo_fade)

    def pausar_musica(self):
        pygame.mixer.music.pause()

    def reanudar_musica(self):
        pygame.mixer.music.unpause()

    # ==========================================
    # LÓGICA PARA EFECTOS DE SONIDO (SFX en canales)
    # ==========================================
    def cargar_efecto(self, nombre, ruta_archivo):
        """Carga un sonido corto en memoria para reproducirlo al instante"""
        try:
            self.efectos[nombre] = pygame.mixer.Sound(ruta_archivo)
        except pygame.error as e:
            print(f"Error al cargar el sonido {ruta_archivo}: {e}")

    def reproducir_efecto(self, nombre, volumen=1.0):
        """Reproduce un sonido cargado previamente sin interrumpir la música"""
        if nombre in self.efectos:
            self.efectos[nombre].set_volume(volumen)
            self.efectos[nombre].play()