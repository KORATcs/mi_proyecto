import pygame
from src.vistas.escenarios.escenario import Escenario
from src.vistas.escenarios.mapa_escenario import MAPA_ESCENARIO_5
from src.vistas.plataformas.plataforma_grafica import PlataformaGrafica



# ==============================================================
# ESCENARIO 5 — abajo -> 4 | izquierda -> 6 | derecha -> 7 | arriba -> 11
# ==============================================================
class EscenarioCinco(Escenario):

    def __init__(self):
        super().__init__(1280, 720)

        self.cargar_fondo("src/assets/images/escenarios/escenario-5.png")

        self.salida_derecha   = 7
        self.salida_izquierda = 6
        self.salida_superior  = 11
        self.salida_inferior  = 4

        self.crear_plataformas()
        self.crear_enemigos()

    def crear_plataformas(self):

        TAM_BLOQUE = 20

        for fila, linea in enumerate(MAPA_ESCENARIO_5):

            for columna, caracter in enumerate(linea):

                if caracter == "X":

                    x = columna * TAM_BLOQUE
                    y = fila * TAM_BLOQUE

                    plataforma = PlataformaGrafica(
                        x=x,
                        y=y,
                        ancho=TAM_BLOQUE,
                        alto=TAM_BLOQUE
                    )

                    self.plataformas.append(plataforma)
    def crear_enemigos(self): pass
