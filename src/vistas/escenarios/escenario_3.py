import pygame
from src.vistas.escenarios.escenario import Escenario
from src.vistas.escenarios.mapa_escenario import MAPA_ESCENARIO_3
from src.vistas.plataformas.plataforma_grafica import PlataformaGrafica

# Importaciones del modelo y vista de Perruga
from src.modelos.personajes.enemigos.perruga import Perruga
from src.vistas.personajes.enemigos.perruga_grafica import PerrugaGrafica

# ==============================================================
# ESCENARIO 3 — izquierda -> 2 | arriba -> 4
# ==============================================================
class EscenarioTres(Escenario):

    def __init__(self):
        super().__init__(1280, 720)

        self.cargar_fondo("src/assets/images/escenarios/escenario-3.png")

        self.salida_derecha   = None
        self.salida_izquierda = 2
        self.salida_superior  = 4
        self.salida_inferior  = None

        self.crear_plataformas()
        self.crear_enemigos()

    def crear_plataformas(self):
        TAM_BLOQUE = 20
        for fila, linea in enumerate(MAPA_ESCENARIO_3):
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
        # Generar un solo Perruga (Ajusta x=600, y=500 según tus plataformas)
        perruga = PerrugaGrafica(
            600,
            500,
            Perruga()
        )
        self.enemigos.append(perruga)