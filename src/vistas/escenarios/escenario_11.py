import pygame
from src.vistas.escenarios.escenario import Escenario
from src.vistas.plataformas.plataforma_grafica import PlataformaGrafica



# ==============================================================
# ESCENARIO 11 — abajo -> 5 | arriba -> 12
# ==============================================================
class EscenarioOnce(Escenario):

    def __init__(self):
        super().__init__(1280, 720)

        self.cargar_fondo("src/assets/images/escenarios/escenario-11.png")

        self.salida_derecha   = None
        self.salida_izquierda = None
        self.salida_superior  = 12
        self.salida_inferior  = 5

        self.crear_plataformas()
        self.crear_enemigos()

    def crear_plataformas(self): pass
    def crear_enemigos(self): pass

