import pygame
from src.vistas.escenarios.escenario import Escenario
from src.vistas.plataformas.plataforma_grafica import PlataformaGrafica

# ==============================================================
# ESCENARIO 12 — abajo -> 11
# ==============================================================
class EscenarioDoce(Escenario):

    def __init__(self):
        super().__init__(1280, 720)

        self.cargar_fondo("src/assets/images/escenarios/escenario-12.png")

        self.salida_derecha   = None
        self.salida_izquierda = None
        self.salida_superior  = None
        self.salida_inferior  = 11

        self.crear_plataformas()
        self.crear_enemigos()

    def crear_plataformas(self): pass
    def crear_enemigos(self): pass