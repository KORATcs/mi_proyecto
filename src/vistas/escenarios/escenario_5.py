import pygame

from src.vistas.escenarios.escenario import Escenario


from src.vistas.escenarios.mapa_escenario import (
    MAPA_ESCENARIO_5,
    TAM_BLOQUE
)

from src.vistas.plataformas.plataforma_grafica import (
    PlataformaGrafica
)

from src.vistas.plataformas.plataforma_movil import (
    PlataformaMovil
)


class EscenarioCinco(Escenario):

    def __init__(self):

        super().__init__(1280, 720)

        self.cargar_fondo(
            "src/assets/images/escenarios/escenario-5.png"
        )

        self.salida_derecha   = 7
        self.salida_izquierda = 6
        self.salida_superior  = 11
        self.salida_inferior  = 4

        self.crear_plataformas()

        self.crear_enemigos()

    def crear_plataformas(self):

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

                    self.plataformas.append(
                        plataforma
                    )

        plataforma_flotante = PlataformaMovil(
            x=900,
            y=200,
            ancho=200,
            alto=200
        )

        self.plataformas.append(
            plataforma_flotante
        )

    def actualizar(self, jugador=None):
        super().actualizar(jugador)

        for plataforma in self.plataformas:

            if hasattr(plataforma, "update"):

                plataforma.update()

    def crear_enemigos(self): pass