import pygame
from src.vistas.escenarios.escenario import Escenario
from src.vistas.plataformas.plataforma_grafica import PlataformaGrafica


# ==============================================================
# ESCENARIO 7 — izquierda -> 5 | derecha -> 8
# ==============================================================
class EscenarioSiete(Escenario):

    def __init__(self):
        super().__init__(1280, 720)

        self.cargar_fondo("src/assets/images/escenarios/escenario-7.png")

        self.salida_derecha   = 8
        self.salida_izquierda = 5
        self.salida_superior  = None
        self.salida_inferior  = None

        self.crear_plataformas()
        self.crear_enemigos()

    def crear_plataformas(self): pass
    def crear_enemigos(self): pass
