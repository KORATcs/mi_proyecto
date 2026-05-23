import pygame
from src.vistas.escenarios.escenario import Escenario
from src.vistas.plataformas.plataforma_grafica import PlataformaGrafica


# ==============================================================
# ESCENARIO 8 — izquierda -> 7 | arriba -> 9
# ==============================================================
class EscenarioOcho(Escenario):

    def __init__(self):
        super().__init__(1280, 720)

        self.cargar_fondo("src/assets/images/escenarios/escenario-8.png")

        self.salida_derecha   = None
        self.salida_izquierda = 7
        self.salida_superior  = 9
        self.salida_inferior  = None

        self.crear_plataformas()
        self.crear_enemigos()

    def crear_plataformas(self): pass
    def crear_enemigos(self): pass

