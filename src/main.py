import pygame
import sys

# =========================
# MODELOS
# =========================
from src.modelos.personajes.protagonista.hoku import Hoku

# =========================
# VISTAS
# =========================
from src.vistas.personajes.hoku.hoku_grafico import HokuGrafico
from src.vistas.ataques.zarpazo_grafico import ZarpazoGrafico
from src.vistas.ui.hud import HUD
from src.vistas.ui.vista_dialogos import VistaDialogos # 🔧 NUEVO: Importamos la vista de diálogos

# =========================
# CONTROLADORES
# =========================
from src.controladores.controlador_hoku import ControladorHoku
from src.controladores.gestor_escenarios import GestorEscenarios


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
        self.FPS = 100

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
        # GESTOR DE ESCENARIOS
        # =========================
        self.gestor_escenarios = GestorEscenarios()

        self.gestor_escenarios.cargar_escenario(1)

        # =========================
        # MODELO HOKU
        # =========================
        self.hoku_logico = Hoku()

        # =========================
        # VISTA HOKU
        # =========================
        self.hoku_vista = HokuGrafico(
            600,
            100,
            self.hoku_logico
        )

        # =========================
        # HUD Y DIÁLOGOS
        # =========================
        self.hud_hoku = HUD(
            self.hoku_logico,
            20,
            20
        )
        
        # NUEVO: Instanciamos la vista visual de los diálogos
        self.vista_dialogos = VistaDialogos()

        # =========================
        # CONTROLADOR
        # =========================
        self.controlador_hoku = ControladorHoku()

        # =========================
        # ATAQUES
        # =========================
        self.ataques = []

        # =========================
        # ACOMPAÑANTES GLOBALES
        # =========================
        self.acompanantes = [] # Lista que guarda a los NPCs que te siguen entre pantallas

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

            if evento.type == pygame.QUIT:

                self.ejecutando = False

        self.controlador_hoku.procesar_eventos(
            self.eventos_actuales
        )

    # ==================================================
    # UPDATE
    # ==================================================
    def actualizar(self):

        # =========================
        # ESCENARIO ACTUAL
        # =========================
        escenario_actual = (
            self.gestor_escenarios.escenario_actual
        )

        # ==============================================================
        # LÓGICA DE ACOMPAÑANTES
        # ==============================================================
        # 🔧 1. Reclutamos al Fuego Fatuo usando TU variable 'siguiendo_hoku'
        for npc in escenario_actual.npcs[:]: # El [:] evita bugs al borrar elementos de la lista en vivo
            if hasattr(npc, 'modelo') and getattr(npc.modelo, 'siguiendo_hoku', False):
                escenario_actual.npcs.remove(npc)  # Lo quitamos del mapa estático
                self.acompanantes.append(npc)      # ¡Se vuelve un compañero de viaje!

        # 2. Movimiento suave e inercia fantasmagórica (Lerp)
        for ac in self.acompanantes:

            if hasattr(ac, 'update'):
                ac.update(self.dt) # O ac.update() si no usa delta time
            elif hasattr(ac, 'actualizar'):
                ac.actualizar()

            # Calculamos la posición detrás de Hoku según hacia dónde mire
            offset_x = -45 if self.hoku_vista.mirando_derecha else 45
            destino_x = self.hoku_vista.rect.centerx + offset_x
            destino_y = self.hoku_vista.rect.top - 25 # Flota un poquito arriba de su cabeza
            
            # El truco matemático: se acerca un 8% (0.08) a su destino en cada frame.
            # Esto hace que flote orgánicamente y te siga con un retraso suave muy lindo.
            ac.rect.centerx += (destino_x - ac.rect.centerx) * 0.08
            ac.rect.centery += (destino_y - ac.rect.centery) * 0.08

            # 3. CONDICIÓN ESPECIAL: Llegada al Escenario 12 (La Salida)
            # (Asegurate de que "EscenarioDoce" coincida con el nombre real de tu clase)
            if escenario_actual.__class__.__name__ == "EscenarioDoce":
                # Cambiamos su destino para que vuele hacia arriba escapando de la pantalla
                destino_y = -100 
                ac.rect.centery += (destino_y - ac.rect.centery) * 0.04 # Sube despidiéndose
                
                # Una vez que sale por completo de la pantalla, lo eliminamos del juego
                if ac.rect.bottom < 0:
                    self.acompanantes.remove(ac)

        # =========================
        # ENEMIGOS DEL ESCENARIO
        # =========================
        enemigos = escenario_actual.enemigos

        # =========================
        # MOVIMIENTO HOKU
        # =========================
        dx, dy = (
            self.controlador_hoku.obtener_movimiento()
        )

        esta_atacando = (
            self.controlador_hoku.atacando
        )

        saltando = (
            self.controlador_hoku.saltando
        )
        
        # NUEVO: Leemos si se presionó la tecla de interacción
        interactuando = (
            self.controlador_hoku.interactuando
        )
        
        # NUEVO: Ejecutamos lógica de interacción si se presionó la tecla
        if interactuando:
            self.verificar_interacciones()

        # =========================
        # 1. UPDATE HOKU
        # =========================
        self.hoku_vista.update(
            dx,
            dy,
            esta_atacando,
            saltando,
            self.dt,
            self.limite_pantalla,
            enemigos,
            escenario=escenario_actual
        )

        # =========================
        # 2. ESCENARIO ACTUAL
        # =========================
        escenario_actual.actualizar(self.hoku_vista)

        # NUEVO: Le conectamos la referencia de Hoku a la Cabra automáticamente
        for enemigo in escenario_actual.enemigos:
            if hasattr(enemigo, 'modelo') and enemigo.modelo.__class__.__name__ == "CabraDeFuego":
                enemigo.modelo.jugador_logico = self.hoku_logico

        # NUEVO: Actualizamos lógica visual de diálogos (fade y proximidad)
        self.vista_dialogos.actualizar(
            self.hoku_vista.rect, 
            escenario_actual.npcs
        )

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
        # UPDATE ATAQUES
        # =========================
        for ataque in self.ataques:

            ataque.update(self.dt)

            for enemigo in enemigos:

                if (
                    ataque.rect.colliderect(
                        enemigo.rect
                    )
                    and enemigo.modelo
                    not in ataque.golpeados
                ):

                    # Hoku daña enemigo
                    self.hoku_logico.atacar(
                        enemigo.modelo
                    )

                    # Flash blanco
                    if hasattr(enemigo, "recibir_golpe"):
                        enemigo.recibir_golpe()

                    ataque.golpeados.append(
                        enemigo.modelo
                    )

        # =========================
        # DAÑO POR CONTACTO Y PROYECTILES
        # =========================
        for enemigo in enemigos:
            
            # 1. Chequeo de daño por el cuerpo del enemigo
            if not self.hoku_vista.invulnerable:
                if self.hoku_vista.rect.colliderect(enemigo.rect) and enemigo.modelo.estaVivo():
                    enemigo.modelo.atacar(self.hoku_logico)
                    self.hoku_vista.tiempo_danio = 0
                    self.hoku_vista.invulnerable = True

            # 2. Chequeo de daño por proyectiles
            if hasattr(enemigo, "proyectiles_pantalla"):
                for proyectil in enemigo.proyectiles_pantalla:
                    if self.hoku_vista.rect.colliderect(proyectil.rect) and not self.hoku_vista.invulnerable:
                        enemigo.modelo.atacar(self.hoku_logico) 
                        self.hoku_vista.tiempo_danio = 0
                        self.hoku_vista.invulnerable = True
                        proyectil.activo = False

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

        self.pantalla.fill(
            self.NEGRO
        )

        escenario_actual = (
            self.gestor_escenarios.escenario_actual
        )

        # =========================
        # DIBUJAR ESCENARIO
        # =========================
        escenario_actual.dibujar(
            self.pantalla
        )

        # =========================
        # DIBUJAR ENEMIGOS
        # =========================
        for enemigo in escenario_actual.enemigos:

            enemigo.dibujar(
                self.pantalla
            )

        # =========================
        # DIBUJAR HOKU
        # =========================
        self.hoku_vista.dibujar(
            self.pantalla
        )

        # =========================
        # DIBUJAR ACOMPAÑANTES
        # =========================
        # 🔧 Dibujamos al fueguito por encima de Hoku en cualquier pantalla donde esté
        for ac in self.acompanantes:
            if hasattr(ac, 'dibujar'):
                ac.dibujar(self.pantalla)

        # =========================
        # DIBUJAR ATAQUES
        # =========================
        for ataque in self.ataques:

            ataque.dibujar(
                self.pantalla
            )

        # =========================
        # DIBUJAR HUD
        # =========================
        self.hud_hoku.dibujar(
            self.pantalla
        )
        
        # =========================
        # DIBUJAR INTERFAZ DIÁLOGOS
        # =========================
        # 🔧 NUEVO: Se dibuja por encima de todo
        self.vista_dialogos.dibujar(
            self.pantalla, 
            self.hoku_vista.rect, 
            escenario_actual.npcs
        )

    # ==================================================
    # TRANSICIONES
    # ==================================================
    def controlar_transiciones(self):

        self.gestor_escenarios.verificar_transicion(
            self.hoku_vista
        )

    # ==================================================
    # INTERACCIONES
    # ==================================================
    def verificar_interacciones(self):
        """ 🔧 NUEVO: Verifica colisión con NPCs y gatilla sus diálogos lógicos """
        
        escenario_actual = self.gestor_escenarios.escenario_actual
        
        # 1. Contamos enemigos vivos en el nivel
        enemigos_vivos = sum(1 for enemigo in escenario_actual.enemigos if enemigo.modelo.estaVivo())
        
        # 2. Recorremos los NPCs del escenario
        for npc in escenario_actual.npcs:
            
            # Ampliamos el rectángulo lógico igual que hicimos para lo visual
            area_interaccion = npc.rect.inflate(250, 250)
            
            # 3. Si Hoku está en el área de interacción
            if self.hoku_vista.rect.colliderect(area_interaccion):
                
                # 4. Inicia o avanza el diálogo en el modelo
                if hasattr(npc, 'modelo') and npc.modelo:
                    npc.modelo.interactuar(self.hoku_logico, enemigos_vivos)


# ======================================================
# MAIN
# ======================================================
def main():

    juego = GameController()

    juego.ejecutar()


if __name__ == "__main__":

    main()