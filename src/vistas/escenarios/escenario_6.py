import pygame
from src.vistas.escenarios.escenario import Escenario
from src.vistas.plataformas.plataforma_grafica import PlataformaGrafica


# ==============================================================
# ESCENARIO 6 — derecha -> 5
# ==============================================================
class EscenarioSeis(Escenario):

    def __init__(self):
        super().__init__(1280, 720)

        self.cargar_fondo("src/assets/images/escenarios/escenario-6.png")

        self.salida_derecha   = 5
        self.salida_izquierda = None
        self.salida_superior  = None
        self.salida_inferior  = None

        self.crear_plataformas()
        self.crear_enemigos()

    def crear_plataformas(self):
        # SUELO — franja horizontal en toda la pantalla
        suelo = PlataformaGrafica(
            x=0, y=600,
            ancho=1280, alto=90    # llega hasta y=720 (borde inferior)
        )
        
        self.plataformas.append(suelo)

    def crear_enemigos(self): pass
