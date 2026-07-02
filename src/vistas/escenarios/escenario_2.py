import pygame
from src.vistas.escenarios.escenario import Escenario
from src.vistas.escenarios.mapa_escenario import MAPA_ESCENARIO_2
from src.vistas.plataformas.plataforma_grafica import PlataformaGrafica
from src.vistas.objetos.templo_tsumi import TemploTsumi

# ==============================================================
# ESCENARIO 2 — izquierda -> 1 | derecha -> 3
# ==============================================================
class EscenarioDos(Escenario):

    def __init__(self):
        super().__init__(1280, 720)

        self.cargar_fondo("src/assets/images/escenarios/escenario-2.png")

        self.salida_derecha   = 3
        self.salida_izquierda = 1
        self.salida_superior  = None
        self.salida_inferior  = None

        self.crear_plataformas()
        self.crear_enemigos()
        self.templo = TemploTsumi(x=355, y=120, id_escenario=2)

    def crear_plataformas(self):
        TAM_BLOQUE = 20

        for fila, linea in enumerate(MAPA_ESCENARIO_2):

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

    def crear_enemigos(self): 
        pass