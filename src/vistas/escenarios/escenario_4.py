import pygame
from src.vistas.escenarios.escenario import Escenario
from src.vistas.plataformas.plataforma_grafica import PlataformaGrafica


# ==============================================================
# ESCENARIO 4 — abajo -> 3 | arriba -> 5
# ==============================================================
class EscenarioCuatro(Escenario):

    def __init__(self):
        super().__init__(1280, 720)

        self.cargar_fondo("src/assets/images/escenarios/escenario-4.png")

        self.salida_derecha   = None
        self.salida_izquierda = None
        self.salida_superior  = 5
        self.salida_inferior  = 3

        self.crear_plataformas()
        self.crear_enemigos()

    def crear_plataformas(self): pass
    def crear_enemigos(self): pass

