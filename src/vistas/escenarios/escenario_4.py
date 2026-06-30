import pygame
from src.vistas.escenarios.escenario import Escenario
from src.vistas.escenarios.mapa_escenario import MAPA_ESCENARIO_4
from src.vistas.plataformas.plataforma_grafica import PlataformaGrafica

# Importaciones del modelo y vista de Medania
from src.modelos.personajes.enemigos.medania import Medania
from src.vistas.personajes.enemigos.medania_grafica import MedaniaGrafica

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

    def crear_plataformas(self):
        TAM_BLOQUE = 20
        for fila, linea in enumerate(MAPA_ESCENARIO_4):
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
        # Generar al estático Medania (Ajusta la posición en su cueva)
        medania = MedaniaGrafica(
            1120,
            5,
            Medania()
        )
        self.enemigos.append(medania)