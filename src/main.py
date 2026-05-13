import pygame
import sys

# =========================
# MODELOS
# =========================
from src.modelos.personajes.protagonista.hoku import Hoku
from src.modelos.personajes.enemigos.bichiluz import Bichiluz

# =========================
# VISTAS
# =========================
from src.vistas.personajes.hoku_grafico import HokuGrafico
from src.vistas.personajes.bichiluz_grafico import BichiluzGrafico

from src.vistas.ataques.ataque_grafico import ZarpazoGrafico

from src.vistas.ui.hud import HUD

# =========================
# ESCENARIOS
# =========================
from src.vistas.escenarios.escenario_uno import EscenarioUno

# =========================
# CONTROLADORES
# =========================
from src.controladores.controlador_hoku import ControladorHoku
from src.controladores.controlador_bichiluz import ControladorBichiluz


class GameController:

    def __init__(self):

        # =========================
        # INICIALIZAR PYGAME
        # =========================
        pygame.init()

        # =========================
        # CONFIGURACIÓN GENERAL
        # =========================
        self.ANCHO = 1280
        self.ALTO = 720
        self.FPS = 75

        self.NEGRO = (0, 0, 0)

        # =========================
        # VENTANA
        # =========================
        self.pantalla = pygame.display.set_mode(
            (self.ANCHO, self.ALTO)
        )

        pygame.display.set_caption("Hoku")

        # =========================
        # CLOCK
        # =========================
        self.clock = pygame.time.Clock()

        # =========================
        # ESTADO PRINCIPAL
        # =========================
        self.ejecutando = True

        # =========================
        # LÍMITES PANTALLA
        # =========================
        self.limite_pantalla = pygame.Rect(
            0,
            0,
            self.ANCHO,
            self.ALTO
        )

        # =========================
        # ESCENARIO ACTUAL
        # =========================
        self.escenario_actual = EscenarioUno()

        # =========================
        # MODELOS
        # =========================
        self.hoku_logico = Hoku()

        self.bichiluz_logico = Bichiluz()

        # =========================
        # VISTAS PERSONAJES
        # =========================
        self.hoku_vista = HokuGrafico(
            100,
            100,
            self.hoku_logico
        )

        self.bichiluz_vista = BichiluzGrafico(
            500,
            300,
            self.bichiluz_logico
        )

        # =========================
        # HUD
        # =========================
        self.hud_hoku = HUD(
            self.hoku_logico,
            20,
            20
        )

        self.hud_bichiluz = HUD(
            self.bichiluz_logico,
            20,
            70
        )

        # =========================
        # CONTROLADORES
        # =========================
        self.controlador_hoku = ControladorHoku()

        self.controlador_bichiluz = ControladorBichiluz()

        # =========================
        # LISTAS ESCALABLES
        # =========================
        self.enemigos = []

        self.enemigos.append(
            self.bichiluz_vista
        )

        self.ataques = []

    # ==================================================
    # LOOP PRINCIPAL
    # ==================================================
    def ejecutar(self):

        while self.ejecutando:

            self.dt = self.clock.tick(self.FPS)

            self.eventos()

            self.actualizar()

            self.dibujar()

            pygame.display.flip()

        pygame.quit()
        sys.exit()

    # ==================================================
    # EVENTOS
    # ==================================================
    def eventos(self):

        self.eventos_actuales = pygame.event.get()

        for evento in self.eventos_actuales:

            # CERRAR JUEGO
            if evento.type == pygame.QUIT:
                self.ejecutando = False

            # ATAQUE MANUAL
            if evento.type == pygame.KEYDOWN:

                if evento.key == pygame.K_SPACE:

                    if self.hoku_vista.rect.colliderect(
                        self.bichiluz_vista.rect
                    ):

                        self.hoku_logico.atacar(
                            self.bichiluz_logico
                        )

        # INPUT PERSONAJES
        self.controlador_hoku.procesar_eventos(
            self.eventos_actuales
        )

        #self.controlador_bichiluz.procesar_eventos(
        #    self.eventos_actuales
        #)

    # ==================================================
    # UPDATE
    # ==================================================
    def actualizar(self):

        # =========================
        # ESCENARIO
        # =========================
        self.escenario_actual.actualizar()

        # =========================
        # MOVIMIENTO HOKU
        # =========================
        dx, dy = self.controlador_hoku.obtener_movimiento()

        esta_atacando = (
            self.controlador_hoku.atacando
        )

        saltando = (
            self.controlador_hoku.saltando
        )

        # =========================
        # MOVIMIENTO BICHILUZ
        # =========================
        bichi1, bichi2 = (
            self.controlador_bichiluz.obtener_movimiento()
        )

        # NORMALIZAR DIAGONAL
        if bichi1 != 0 and bichi2 != 0:

            bichi1 *= 0.7
            bichi2 *= 0.7

        # VELOCIDAD
        VELOCIDAD = 5

        dx *= VELOCIDAD
        dy *= VELOCIDAD

        bichi1 *= VELOCIDAD
        bichi2 *= VELOCIDAD

        # =========================
        # CREAR ATAQUE
        # =========================
        if (
            esta_atacando
            and not self.hoku_vista.bloqueando_accion
        ):

            offset = (
                40
                if self.hoku_vista.mirando_derecha
                else -40
            )

            nuevo_ataque = ZarpazoGrafico(
                self.hoku_vista.rect.x + offset,
                self.hoku_vista.rect.y,
                self.hoku_vista.mirando_derecha,
                self.hoku_vista.animaciones
            )

            self.ataques.append(
                nuevo_ataque
            )

        # =========================
        # UPDATE HOKU
        # =========================
        self.hoku_vista.update(
            dx,
            dy,
            esta_atacando,
            saltando,
            self.dt,
            self.limite_pantalla,
            self.enemigos
        )

        # =========================
        # UPDATE ENEMIGOS
        # =========================
        for enemigo in self.enemigos:

            enemigo.update(
                bichi1,
                bichi2,
                self.dt,
                self.limite_pantalla
            )

        # =========================
        # DAÑO POR CONTACTO
        # =========================
        for enemigo in self.enemigos:

            if self.hoku_vista.rect.colliderect(
                enemigo.rect
            ):

                if (
                    self.hoku_vista.tiempo_danio
                    >= self.hoku_vista.cooldown_danio
                ):

                    enemigo.modelo.atacar(
                        self.hoku_logico
                    )

                    self.hoku_vista.tiempo_danio = 0

        # =========================
        # UPDATE ATAQUES
        # =========================
        for ataque in self.ataques:

            ataque.update(self.dt)

            for enemigo in self.enemigos:

                if (
                    ataque.rect.colliderect(
                        enemigo.rect
                    )

                    and enemigo.modelo
                    not in ataque.golpeados
                ):

                    self.hoku_logico.atacar(
                        enemigo.modelo
                    )

                    ataque.golpeados.append(
                        enemigo.modelo
                    )

        # =========================
        # LIMPIAR ATAQUES
        # =========================
        self.ataques = [

            ataque

            for ataque in self.ataques

            if ataque.activo
        ]

        # =========================
        # TRANSICIONES
        # =========================
        self.controlar_transiciones()

    # ==================================================
    # DIBUJAR
    # ==================================================
    def dibujar(self):

        # LIMPIAR PANTALLA
        self.pantalla.fill(self.NEGRO)

        # =========================
        # ESCENARIO
        # =========================
        self.escenario_actual.dibujar(
            self.pantalla
        )

        # =========================
        # ENEMIGOS
        # =========================
        for enemigo in self.enemigos:

            enemigo.dibujar(
                self.pantalla
            )

        # =========================
        # JUGADOR
        # =========================
        self.hoku_vista.dibujar(
            self.pantalla
        )

        # =========================
        # ATAQUES
        # =========================
        for ataque in self.ataques:

            ataque.dibujar(
                self.pantalla
            )

        # =========================
        # HUD
        # =========================
        self.hud_hoku.dibujar(
            self.pantalla
        )

        self.hud_bichiluz.dibujar(
            self.pantalla
        )

    # ==================================================
    # TRANSICIONES ENTRE ESCENARIOS
    # ==================================================
    def controlar_transiciones(self):

        # EJEMPLO FUTURO:
        #
        # if self.hoku_vista.rect.right >= self.ANCHO:
        #
        #     if self.escenario_actual.salida_derecha:
        #
        #         self.escenario_actual = (
        #             self.escenario_actual.salida_derecha
        #         )
        #
        #         self.hoku_vista.rect.left = 0

        pass


# ======================================================
# MAIN
# ======================================================
def main():

    juego = GameController()

    juego.ejecutar()


if __name__ == "__main__":
    main()
