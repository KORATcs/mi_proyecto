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
    # ACTUALIZAR
    # =========================
    def actualizar(self):

        for enemigo in self.enemigos:
            enemigo.actualizar()

    # =========================
    # DIBUJAR
    # =========================
    def dibujar(self, pantalla):

        # Dibujar fondo
        pantalla.blit(self.fondo, (0, 0))

        # Dibujar plataformas
        for plataforma in self.plataformas:
            plataforma.dibujar(pantalla)

        # Dibujar enemigos
        for enemigo in self.enemigos:
            enemigo.dibujar(pantalla)

    # =========================
    # CREACIÓN DE ELEMENTOS
    # =========================
    def crear_plataformas(self):
        pass

    def crear_enemigos(self):
        pass