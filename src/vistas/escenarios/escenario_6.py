import pygame
from src.vistas.escenarios.escenario import Escenario
from src.vistas.escenarios.mapa_escenario import MAPA_ESCENARIO_6
from src.vistas.plataformas.plataforma_grafica import PlataformaGrafica

# Importaciones del modelo y vista de la Cabra de Fuego
from src.modelos.personajes.jefes.cabra_de_fuego import CabraDeFuego
from src.vistas.personajes.jefes.cabra_de_fuego_grafica import CabraDeFuegoGrafica

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
        TAM_BLOQUE = 20
        for fila, linea in enumerate(MAPA_ESCENARIO_6):
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
        # Generar al Jefe Cabra de Fuego en el centro de la habitación
        cabra_jefe = CabraDeFuegoGrafica(
            800,
            450,
            CabraDeFuego()
        )
        self.enemigos.append(cabra_jefe)