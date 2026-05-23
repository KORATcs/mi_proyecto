import pygame
from src.vistas.escenarios.escenario import Escenario
from src.vistas.plataformas.plataforma_grafica import PlataformaGrafica



# ==============================================================
# ESCENARIO 9 — abajo -> 8 | izquierda -> 10
# ==============================================================
class EscenarioNueve(Escenario):

    def __init__(self):
        super().__init__(1280, 720)

        self.cargar_fondo("src/assets/images/escenarios/escenario-9.png")

        self.salida_derecha   = None
        self.salida_izquierda = 10
        self.salida_superior  = None
        self.salida_inferior  = 8

        self.crear_plataformas()
        self.crear_enemigos()

    def crear_plataformas(self): pass
    def crear_enemigos(self): pass
