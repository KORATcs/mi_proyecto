import pygame
from src.vistas.escenarios.escenario import Escenario
from src.vistas.escenarios.mapa_escenario import MAPA_ESCENARIO_9
from src.vistas.plataformas.plataforma_grafica import PlataformaGrafica

# Importaciones del modelo y vista de Hibrido
from src.modelos.personajes.enemigos.hibrido import Hibrido
from src.vistas.personajes.enemigos.hibrido_grafico import HibridoGrafico

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

    def crear_plataformas(self):
        TAM_BLOQUE = 20
        for fila, linea in enumerate(MAPA_ESCENARIO_9):
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
            500,
            400,
            Hibrido()
        )
        self.enemigos.append(hibrido)