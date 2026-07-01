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
from src.vistas.ui.vista_dialogos import VistaDialogos
from src.vistas.menu.menu_principal_grafico import MenuPrincipalGrafico

# =========================
# CONTROLADORES
# =========================
from src.controladores.controlador_hoku import ControladorHoku
from src.controladores.gestor_escenarios import GestorEscenarios
from src.controladores.gestor_audio.gestor_audio import GestorAudio

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
        self.BLANCO = (255, 255, 255) # Útil para textos

        # =========================
        # VENTANA
        # =========================
        self.pantalla = pygame.display.set_mode(
            (self.ANCHO, self.ALTO)
        )

        pygame.display.set_caption("Hoku")

        # =========================
        # CLOCK Y ESTADO
        # =========================
        self.clock = pygame.time.Clock()
        self.ejecutando = True

        # 🔧 NUEVO: MAQUINA DE ESTADOS (Puede ser "MENU", "JUGANDO", etc.)
        self.estado_juego = "MENU"

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
        # INICIALIZACIÓN (MENÚ Y AUDIO)
        # =========================
        # 🔧 IMPORTANTE: Acá instanciarás tu menú real cuando lo crees
        self.menu_principal = MenuPrincipalGrafico(self.ANCHO, self.ALTO)
        
        self.audio = GestorAudio()
        self.audio.reproducir_musica("src/assets/musica/ambiente/MainSong-1.mp3", volumen=1.0)


        # =========================
        # INICIALIZACIÓN (JUEGO)
        # =========================
        self.gestor_escenarios = GestorEscenarios()
        self.gestor_escenarios.cargar_escenario(1)
        self.hoku_logico = Hoku()
        self.hoku_vista = HokuGrafico(600, 100, self.hoku_logico)
        self.hud_hoku = HUD(self.hoku_logico, 20, 20)
        self.vista_dialogos = VistaDialogos()
        self.controlador_hoku = ControladorHoku()
        self.ataques = []
        self.acompanantes = [] 


    # ==================================================
    # LOOP PRINCIPAL
    # ==================================================
    def ejecutar(self):
        while self.ejecutando:
            self.dt = self.clock.tick(self.FPS)
            self.eventos()
            
            # NUEVO: Dividimos la lógica según el estado actual

            if self.estado_juego == "MENU":
                self.actualizar_menu()
                self.dibujar_menu()
            elif self.estado_juego == "JUGANDO":
                self.actualizar_juego()
                self.dibujar_juego()

            pygame.display.flip()

        pygame.quit()
        sys.exit()

    # ==================================================
    # EVENTOS
    # ==================================================
    def eventos(self):
        # 1. Obtenemos todas las teclas/clics que se tocaron en este frame
        self.eventos_actuales = pygame.event.get()

        # 2. Revisamos si el jugador cerró la ventana en la cruz (X)
        for evento in self.eventos_actuales:
            if evento.type == pygame.QUIT:
                self.ejecutando = False

        # ==============================================================
        # 🔧 3. DISTRIBUCIÓN DE EVENTOS SEGÚN EL ESTADO
        # ==============================================================
        if self.estado_juego == "MENU":
            # Si estamos en el menú, le mandamos las teclas a la clase MenuPrincipal
            self.menu_principal.procesar_eventos(self.eventos_actuales)
            
        elif self.estado_juego == "JUGANDO":
            # Si estamos jugando, le mandamos las teclas al controlador de Hoku
            self.controlador_hoku.procesar_eventos(self.eventos_actuales)

    # ==================================================
    # LÓGICA Y DIBUJO: MENÚ
    # ==================================================
    def actualizar_menu(self):
        self.menu_principal.actualizar(self.dt)
        if self.menu_principal.iniciar_juego:
            self.estado_juego = "JUGANDO"

    def dibujar_menu(self):
        self.menu_principal.dibujar(self.pantalla)

        self.pantalla.fill(self.NEGRO)
        self.menu_principal.dibujar(self.pantalla)


    # ==================================================
    # LÓGICA: JUEGO (Tu código original de actualizar)
    # ==================================================
    def actualizar_juego(self):
        
        escenario_actual = self.gestor_escenarios.escenario_actual

        # 1. Acompañantes
        for npc in escenario_actual.npcs[:]: 
            if hasattr(npc, 'modelo') and getattr(npc.modelo, 'siguiendo_hoku', False):
                escenario_actual.npcs.remove(npc)  
                self.acompanantes.append(npc)      

        for ac in self.acompanantes:
            if hasattr(ac, 'update'):
                ac.update(self.dt) 
            elif hasattr(ac, 'actualizar'):
                ac.actualizar()

            offset_x = -45 if self.hoku_vista.mirando_derecha else 45
            destino_x = self.hoku_vista.rect.centerx + offset_x
            destino_y = self.hoku_vista.rect.top - 25 
            
            ac.rect.centerx += (destino_x - ac.rect.centerx) * 0.08
            ac.rect.centery += (destino_y - ac.rect.centery) * 0.08

            if escenario_actual.__class__.__name__ == "EscenarioDoce":
                destino_y = -100 
                ac.rect.centery += (destino_y - ac.rect.centery) * 0.04 
                if ac.rect.bottom < 0:
                    self.acompanantes.remove(ac)

        # 2. Inputs Hoku
        enemigos = escenario_actual.enemigos
        dx, dy = self.controlador_hoku.obtener_movimiento()
        esta_atacando = self.controlador_hoku.atacando
        saltando = self.controlador_hoku.saltando
        interactuando = self.controlador_hoku.interactuando
        
        if interactuando:
            self.verificar_interacciones()

        # 3. Update Hoku y Escenario
        self.hoku_vista.update(dx, dy, esta_atacando, saltando, self.dt, self.limite_pantalla, enemigos, escenario=escenario_actual)
        escenario_actual.actualizar(self.hoku_vista)

        for enemigo in escenario_actual.enemigos:
            if hasattr(enemigo, 'modelo') and enemigo.modelo.__class__.__name__ == "CabraDeFuego":
                enemigo.modelo.jugador_logico = self.hoku_logico

        self.vista_dialogos.actualizar(self.hoku_vista.rect, escenario_actual.npcs)

        # 4. Ataques
        if esta_atacando and not self.hoku_vista.bloqueando_accion:
            offset = 40 if self.hoku_vista.mirando_derecha else -40
            nuevo_ataque = ZarpazoGrafico(self.hoku_vista.rect.x + offset, self.hoku_vista.rect.y, self.hoku_vista.mirando_derecha, self.hoku_vista.animaciones)
            self.ataques.append(nuevo_ataque)

        for ataque in self.ataques:
            ataque.update(self.dt)
            for enemigo in enemigos:
                if ataque.rect.colliderect(enemigo.rect) and enemigo.modelo not in ataque.golpeados:
                    self.hoku_logico.atacar(enemigo.modelo)
                    if hasattr(enemigo, "recibir_golpe"):
                        enemigo.recibir_golpe()
                    ataque.golpeados.append(enemigo.modelo)

        # 5. Daño recibido
        for enemigo in enemigos:
            if not self.hoku_vista.invulnerable:
                if self.hoku_vista.rect.colliderect(enemigo.rect) and enemigo.modelo.estaVivo():
                    enemigo.modelo.atacar(self.hoku_logico)
                    self.hoku_vista.tiempo_danio = 0
                    self.hoku_vista.invulnerable = True

            if hasattr(enemigo, "proyectiles_pantalla"):
                for proyectil in enemigo.proyectiles_pantalla:
                    if self.hoku_vista.rect.colliderect(proyectil.rect) and not self.hoku_vista.invulnerable:
                        enemigo.modelo.atacar(self.hoku_logico) 
                        self.hoku_vista.tiempo_danio = 0
                        self.hoku_vista.invulnerable = True
                        proyectil.activo = False

        self.ataques = [ataque for ataque in self.ataques if ataque.activo]
        self.controlar_transiciones()

    # ==================================================
    # DIBUJO: JUEGO (Tu código original de dibujar)
    # ==================================================
    def dibujar_juego(self):
        self.pantalla.fill(self.NEGRO)
        escenario_actual = self.gestor_escenarios.escenario_actual

        escenario_actual.dibujar(self.pantalla)

        for enemigo in escenario_actual.enemigos:
            enemigo.dibujar(self.pantalla)

        self.hoku_vista.dibujar(self.pantalla)

        for ac in self.acompanantes:
            if hasattr(ac, 'dibujar'):
                ac.dibujar(self.pantalla)

        for ataque in self.ataques:
            ataque.dibujar(self.pantalla)

        self.hud_hoku.dibujar(self.pantalla)
        self.vista_dialogos.dibujar(self.pantalla, self.hoku_vista.rect, escenario_actual.npcs)

    # ==================================================
    # MÉTODOS AUXILIARES
    # ==================================================
    def controlar_transiciones(self):
        self.gestor_escenarios.verificar_transicion(self.hoku_vista)

    def verificar_interacciones(self):
        escenario_actual = self.gestor_escenarios.escenario_actual
        enemigos_vivos = sum(1 for enemigo in escenario_actual.enemigos if enemigo.modelo.estaVivo())
        
        for npc in escenario_actual.npcs:
            area_interaccion = npc.rect.inflate(250, 250)
            if self.hoku_vista.rect.colliderect(area_interaccion):
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