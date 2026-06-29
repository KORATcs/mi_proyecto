import pygame


class Escenario:

    def __init__(self, ancho, alto):

        # Tamaño lógico del escenario
        self.ancho = ancho
        self.alto = alto

        # Fondo
        self.fondo = None

        # Entidades
        self.plataformas = []
        self.enemigos = []
        self.objetos = []

        # Conexiones metroidvania
        self.salida_derecha = None
        self.salida_izquierda = None
        self.salida_superior = None
        self.salida_inferior = None

    # =========================
    # CARGAR FONDO
    # =========================
    def cargar_fondo(self, ruta):
        """
        Carga la imagen y la escala UNA SOLA VEZ al tamaño
        lógico del escenario (ancho x alto).
        Llamar esto en el __init__ de cada escenario hijo
        en lugar de pygame.image.load directo.
        """
        imagen = pygame.image.load(ruta).convert()
        self.fondo = pygame.transform.scale(imagen, (self.ancho, self.alto))

    # =========================
    # ACTUALIZAR
    # =========================
    def actualizar(self):

        for enemigo in self.enemigos:
            enemigo.actualizar()
        
        for plataforma in self.plataformas:
            if hasattr(plataforma, "update"):
                plataforma.update()

    # =========================
    # DIBUJAR
    # =========================
    def dibujar(self, pantalla):

        pantalla.blit(self.fondo, (0, 0))

        for plataforma in self.plataformas:
            plataforma.dibujar(pantalla)

        for enemigo in self.enemigos:
            enemigo.dibujar(pantalla)

    # =========================
    # CREACIÓN DE ELEMENTOS
    # =========================
    def crear_plataformas(self):
        pass

    def crear_enemigos(self):
        pass

    # =========================
    # DETECCIÓN DE SALIDA
    # =========================
    def detectar_salida(self, jugador_rect):

        if jugador_rect.left >= self.ancho and self.salida_derecha is not None:
            return ("derecha", self.salida_derecha)

        if jugador_rect.right <= 0 and self.salida_izquierda is not None:
            return ("izquierda", self.salida_izquierda)

        if jugador_rect.bottom <= 0 and self.salida_superior is not None:
            return ("superior", self.salida_superior)

        if jugador_rect.top >= self.alto and self.salida_inferior is not None:
            return ("inferior", self.salida_inferior)

        return (None, None)

    