import pygame
from src.vistas.escenarios.escenario import Escenario
from src.vistas.escenarios.mapa_escenario import MAPA_ESCENARIO_10
from src.vistas.plataformas.plataforma_grafica import PlataformaGrafica

# Importaciones del modelo y vista de Hibrido
from src.modelos.personajes.enemigos.hibrido import Hibrido
from src.vistas.personajes.enemigos.hibrido_grafico import HibridoGrafico

# ==============================================================
# ESCENARIO 10 — derecha -> 9
# ==============================================================
class EscenarioDiez(Escenario):

    def __init__(self):
        super().__init__(1280, 720)

        self.cargar_fondo("src/assets/images/escenarios/escenario-10.png")

        self.salida_derecha   = 9
        self.salida_izquierda = None
        self.salida_superior  = None
        self.salida_inferior  = None

        self.crear_plataformas()
        self.crear_enemigos()

    def crear_plataformas(self):

        TAM_BLOQUE = 20

        for fila, linea in enumerate(MAPA_ESCENARIO_10):

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
        # Generar un solo Híbrido patrullero
        hibrido = HibridoGrafico(
            600,
            400,
            Hibrido()
        )
        self.enemigos.append(hibrido)

