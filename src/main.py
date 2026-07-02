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
from src.vistas.menu.menu_pausa import MenuPausa 

# =========================
# CONTROLADORES
# =========================
from src.controladores.controlador_hoku import ControladorHoku
from src.controladores.gestor_escenarios import GestorEscenarios
from src.controladores.gestor_audio import GestorAudio
from src.controladores.gestor_base_datos import GestorBaseDatos
from src.controladores.gestor_cinematicas import GestorCinematicas  
from src.controladores.minijuego_grieta import MinijuegoGrieta 

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
        self.BLANCO = (255, 255, 255) 

        # =========================
        # VENTANA
        # =========================
        self.pantalla = pygame.display.set_mode((self.ANCHO, self.ALTO))
        pygame.display.set_caption("Hoku")

        # =========================
        # CLOCK Y ESTADO
        # =========================
        self.clock = pygame.time.Clock()
        self.ejecutando = True
        self.estado_juego = "MENU"

        # =========================
        # LÍMITES PANTALLA
        # =========================
        self.limite_pantalla = pygame.Rect(0, 0, self.ANCHO, self.ALTO)

        # =========================
        # INICIALIZACIÓN (BASE DE DATOS)
        # =========================
        self.bd = GestorBaseDatos()

        # =========================
        # INICIALIZACIÓN (MENÚ Y AUDIO)
        # =========================
        self.menu_principal = MenuPrincipalGrafico(self.ANCHO, self.ALTO)
        self.menu_pausa = MenuPausa(self.ANCHO, self.ALTO) 
        
        self.audio = GestorAudio()
        self.ruta_musica_actual = "src/assets/musica/menu/MenuSong.mp3"
        self.audio.reproducir_musica(self.ruta_musica_actual, volumen=1.0)

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

        # =========================
        # GESTOR DE CINEMÁTICAS
        # =========================
        self.gestor_cine = GestorCinematicas(self.pantalla)
        self.cine_inicial_vista = False  
        self.fase_escenario_12 = 0

        # =========================
        # MINIJUEGO GRIETA
        # =========================
        self.minijuego = MinijuegoGrieta(self.pantalla)


    # ==================================================
    # LOOP PRINCIPAL
    # ==================================================
    def ejecutar(self):
        while self.ejecutando:
            self.dt = self.clock.tick(self.FPS)
            self.eventos()
            
            if self.estado_juego == "MENU":
                self.actualizar_menu()
                self.dibujar_menu()
            elif self.estado_juego == "JUGANDO":
                self.actualizar_juego()
                self.dibujar_juego()
            elif self.estado_juego == "PAUSA":
                self.actualizar_pausa()
                self.dibujar_juego()  
                self.menu_pausa.dibujar(self.pantalla)  
            elif self.estado_juego == "REZANDO":
                self.actualizar_juego()
                self.dibujar_juego()
            elif self.estado_juego == "CINEMATICA":  
                self.gestor_cine.actualizar(self.dt)
                # Si estamos mostrando solo un texto del final del juego, no hace falta dibujar el fondo del escenario 12 viejo por atrás
                if self.gestor_cine.modo_texto and self.gestor_cine.frames == []:
                    self.pantalla.fill(self.NEGRO)
                    self.gestor_cine.dibujar()
                else:
                    self.dibujar_juego()
            elif self.estado_juego == "MINIJUEGO":  
                # AL GANAR, SALTA A NUESTRO FLUJO FINAL DE TEXTOS ELEGANTES
                self.minijuego.actualizar(self.dt, self.mostrar_texto_victoria)
                self.minijuego.dibujar()

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
            
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_e:
                    escenario = self.gestor_escenarios.escenario_actual
                    if escenario and hasattr(escenario, "templo") and escenario.templo.verificar_cercania(self.hoku_vista.rect):
                        self.hoku_logico.curar()
                        escenario.templo.interactuar(self)

                if evento.key == pygame.K_ESCAPE and self.estado_juego != "REZANDO" and self.estado_juego != "CINEMATICA" and self.estado_juego != "MINIJUEGO":
                    if self.estado_juego == "JUGANDO":
                        self.estado_juego = "PAUSA"
                    elif self.estado_juego == "PAUSA" and not self.menu_pausa.mostrando_confirmacion:
                        self.estado_juego = "JUGANDO"

        if self.estado_juego == "MENU":
            self.menu_principal.procesar_eventos(self.eventos_actuales)
        elif self.estado_juego == "JUGANDO":
            self.controlador_hoku.procesar_eventos(self.eventos_actuales)
        elif self.estado_juego == "PAUSA":
            self.menu_pausa.procesar_eventos(self.eventos_actuales)

    # ==================================================
    # LÓGICA Y DIBUJO: MENÚ PRINCIPAL
    # ==================================================
    def actualizar_menu(self):
        tiene_guardado = False
        try:
            partida = self.bd.cargar_partida()
            if partida is not None:
                tiene_guardado = True
        except Exception as e:
            print(f"Error al verificar guardado en el menú: {e}")
            
        self.menu_principal.actualizar_opciones_disponibles(tiene_guardado)
        self.menu_principal.actualizar(self.dt)
        
        if self.menu_principal.iniciar_juego:
            try:
                with self.bd.obtener_conexion() as conn:
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM partida")
                    cursor.execute("DELETE FROM jefes_derrotados")
                    conn.commit()
            except Exception as e:
                print(f"Error al limpiar la base de datos para nueva partida: {e}")

            self.ataques.clear()
            self.acompanantes.clear()
            self.cine_inicial_vista = False  
            
            self.hoku_logico = Hoku()
            self.hoku_vista.modelo = self.hoku_logico
            self.hud_hoku.personaje = self.hoku_logico
            
            self.gestor_escenarios = GestorEscenarios()
            self.gestor_escenarios.cargar_escenario(1)
            
            self.hoku_vista.rect.x = 600
            self.hoku_vista.rect.y = 100
            self.hoku_vista.bloqueando_accion = False
            self.hoku_vista.invulnerable = False
            self.hoku_vista.tiempo_danio = 0
            if hasattr(self.hoku_vista, "cambiar_animacion"):
                self.hoku_vista.cambiar_animacion("quieto")
                
            self.estado_juego = "JUGANDO"
            self.menu_principal.iniciar_juego = False
            
        elif self.menu_principal.cargar_partida:
            self.cargar_partida_guardada()
            self.menu_principal.cargar_partida = False

    def dibujar_menu(self):
        self.menu_principal.dibujar(self.pantalla)

    # ==================================================
    # LÓGICA: MENÚ DE PAUSA
    # ==================================================
    def actualizar_pausa(self):
        if self.menu_pausa.continuar_juego:
            self.estado_juego = "JUGANDO"
            self.menu_pausa.continuar_juego = False
            
        elif self.menu_pausa.cargar_checkpoint:
            self.cargar_partida_guardada()
            self.menu_pausa.cargar_checkpoint = False
            
        elif self.menu_pausa.retornar_al_menu:
            self.estado_juego = "MENU"
            
            tiene_guardado = False
            try:
                partida = self.bd.cargar_partida()
                if partida is not None:
                    tiene_guardado = True
            except Exception:
                pass
            self.menu_principal.actualizar_opciones_disponibles(tiene_guardado)
            
            self.menu_pausa.retornar_al_menu = False 
            self.menu_pausa.continuar_juego = False
            self.menu_pausa.cargar_checkpoint = False
            self.menu_pausa.indice_seleccionado = 0
            self.menu_principal.iniciar_juego = False 

    def cargar_partida_guardada(self):
        try:
            datos = self.bd.cargar_partida()
            if datos:
                self.ataques.clear()
                self.acompanantes.clear()
                self.hoku_vista.bloqueando_accion = False
                self.hoku_vista.invulnerable = False
                self.hoku_vista.tiempo_danio = 0
                if hasattr(self.hoku_vista, "cambiar_animacion"):
                    self.hoku_vista.cambiar_animacion("quieto")

                escenario_id = datos.get("escenario_id", 1)
                pos_x = datos.get("pos_x", 600)
                pos_y = datos.get("pos_y", 100)
                vida_guardada = datos.get("vida_actual", self.hoku_logico.vida_maxima)
                
                self.gestor_escenarios = GestorEscenarios()
                self.gestor_escenarios.cargar_escenario(escenario_id)
                
                self.hoku_vista.rect.x = pos_x
                self.hoku_vista.rect.y = pos_y
                self.hoku_logico.vida = vida_guardada
                self.hud_hoku.personaje = self.hoku_logico
                
                self.estado_juego = "JUGANDO"
            else:
                self.gestor_escenarios = GestorEscenarios()
                self.gestor_escenarios.cargar_escenario(1)
                self.estado_juego = "JUGANDO"
        except Exception as e:
            print(f"Error crítico al cargar partida: {e}")
            self.gestor_escenarios = GestorEscenarios()
            self.gestor_escenarios.cargar_escenario(1)
            self.estado_juego = "JUGANDO"

    # ==================================================
    # LÓGICA: JUEGO 
    # ==================================================
    def actualizar_juego(self):
        escenario_actual = self.gestor_escenarios.escenario_actual
        escenario_nombre = escenario_actual.__class__.__name__ if escenario_actual else ""

        # 🎵 CAMBIO DE MÚSICA SEGÚN EL ESCENARIO
        if escenario_nombre == "EscenarioSeis":
            self.cambiar_bgm("src/assets/musica/combate/FightTheme.mp3", volumen=0.2)
        else:
            # Si no está con el jefe, y estamos jugando, que mantenga la música ambiental estándar
            if self.estado_juego == "JUGANDO":
                self.cambiar_bgm("src/assets/musica/ambiente/MainSong-1.mp3", volumen=1.0)

        if escenario_actual is None:
            return

        # CONFIGURACIÓN DE LAS CINEMÁTICAS EN ESCENARIO 12
        if escenario_actual.__class__.__name__ == "EscenarioDoce":
            
            # CASO 1: Es la primera vez absoluta que entrás al escenario (Fase 0)
            if self.fase_escenario_12 == 0:
                if not self.gestor_cine.reproduciendo:
                    self.fase_escenario_12 = 1 # Pasamos a Fase 1 (Caminando solo/buscando al fuego)
                    self.cine_inicial_vista = True 
                    self.estado_juego = "CINEMATICA"
                    
                    config_cima = [
                        {"ruta": "src/assets/images/cinematica/hoku-cinematica-1.png", "columnas": 4, "filas": 1, "fps": 1},
                        {"ruta": "src/assets/images/cinematica/hoku-cinematica-2.png", "columnas": 14, "filas": 1, "fps": 7}
                    ]
                    
                    self.gestor_cine.cargar_desde_spritesheet(
                        configuracion_tiras=config_cima, 
                        callback=self.finalizar_cine_inicial,
                        texto_interludio="Debo subir hacia allá..."
                    )
                    return

            # CASO 2: Ya viste la intro, y regresás con el Fuego Fatuo (Fase 1 y tenés acompañantes)
            elif self.fase_escenario_12 == 1 and len(self.acompanantes) > 0:
                if not self.gestor_cine.reproduciendo:
                    self.fase_escenario_12 = 2 # 🔒 BLOQUEO ABSOLUTO: Pasamos a Fase 2 (Final iniciado)
                    self.disparar_cine_final()
                    return

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
            ac.rect.centery += (destino_y - ac.rect.centery) * 0.04

            if escenario_actual.__class__.__name__ == "EscenarioDoce":
                destino_y = -100 
                ac.rect.centery += (destino_y - ac.rect.centery) * 0.04 
                if ac.rect.bottom < 0:
                    self.acompanantes.remove(ac)

        # 2. Inputs Hoku
        enemigos = escenario_actual.enemigos
        
        if self.estado_juego == "REZANDO":
            dx, dy = 0, 0
            esta_atacando = False
            saltando = False
            interactuando = self.controlador_hoku.interactuando
        else:
            dx, dy = self.controlador_hoku.obtener_movimiento()
            esta_atacando = self.controlador_hoku.atacando
            saltando = self.controlador_hoku.saltando
            interactuando = self.controlador_hoku.interactuando
        
        if interactuando:
            self.verificar_interacciones()

        # 3. Update Hoku y Escenario
        self.hoku_vista.update(dx, dy, esta_atacando, saltando, self.dt, self.limite_pantalla, enemigos, escenario=escenario_actual)
        escenario_actual.actualizar(self.hoku_vista)    

        if hasattr(escenario_actual, "templo") and escenario_actual.templo:
            escenario_actual.templo.actualizar(self.dt)

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
                    try:
                        self.hoku_logico.atacar(enemigo.modelo)
                    except Exception:
                        pass 
                    
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
    # DIBUJO: JUEGO 
    # ==================================================
    def dibujar_juego(self):
        self.pantalla.fill(self.NEGRO)
        escenario_actual = self.gestor_escenarios.escenario_actual
        if escenario_actual is None:
            return

        escenario_actual.dibujar(self.pantalla, self.hoku_vista.rect, self.estado_juego)

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

        self.gestor_cine.dibujar()

    # ==================================================
    # CALLBACKS Y PROGRESO DE CINEMÁTICAS
    # ==================================================
    def finalizar_cine_inicial(self):
        self.estado_juego = "JUGANDO"
        
        if len(self.acompanantes) > 0:
            self.disparar_cine_final()

    # CONFIGURACIÓN DE LA CINEMÁTICA FINAL
    def disparar_cine_final(self):
        self.estado_juego = "CINEMATICA"
        
        config_final = {
            "ruta": "src/assets/images/cinematica/fuego-fatuo-cinematica-Sheet.png", 
            "columnas": 4, 
            "filas": 1,
            "fps": 1,
        }
        
        self.gestor_cine.cargar_desde_spritesheet(
            configuracion_tiras=config_final, 
            callback=self.comenzar_minijuego,
            texto_interludio="El Fuego Fatuo comió a Hoku...\nAhora comenzará un nuevo desafío."
        )

    def comenzar_minijuego(self):
        """Inicializa y activa el estado del minijuego del parcial"""
        # (Opcional) Si eventualmente le ponés música al minijuego, descomentá la línea de abajo:
        # self.cambiar_bgm("src/assets/musica/ambiente/musica_minijuego.mp3", volumen=0.8)
        
        self.minijuego.reiniciar()
        self.estado_juego = "MINIJUEGO"

    # ==================================================
    # 🌟 NUEVA LÓGICA DE FIN DE LA DEMO
    # ==================================================
    def mostrar_texto_victoria(self):
        """Dispara la pantalla con el interludio poético de victoria"""
        self.estado_juego = "CINEMATICA"
        
        # 🎵 ¡ACÁ ENTRA LA MÚSICA DE LOS CRÉDITOS! 
        # Arranca justo de fondo mientras se lee este lindo texto.
        self.cambiar_bgm("src/assets/musica/creditos/CreditSong.mp3", volumen=0.3) # 👈 Cambiá la ruta por tu archivo de créditos
        
        texto_vic = "El Fuego ha ayudado a Hoku, y pudo alcanzar su objetivo\npara poder seguir con su aventura."
        self.gestor_cine.mostrar_solo_texto(texto_vic, self.mostrar_creditos_finales)

    def mostrar_creditos_finales(self):
        """Muestra la pantalla final de agradecimientos"""
        self.estado_juego = "CINEMATICA"
        
        # No tocamos la música acá para que siga sonando de corrido la que empezó en el texto anterior
        texto_cred = "¡Muchas gracias por jugar esta Demo!\n\nDiseño y Arte: Camila Simon\nProgramación: Camila Simon\nMusica Original: Santiago Palleres\n\nuwu"
        self.gestor_cine.mostrar_solo_texto(texto_cred, self.regresar_al_menu)

    def regresar_al_menu(self):
        """Devuelve limpio al jugador al Menú Principal en lugar de romper el ejecutable"""
        print("¡Demo de Hoku finalizada exitosamente! uwu")
        
        # Reseteamos todo el progreso narrativo
        self.cine_inicial_vista = False
        self.fase_escenario_12 = 0 
        self.acompanantes.clear() 
        self.ataques.clear()
        
        self.estado_juego = "MENU"
        
        # Al volver al menú principal, restauramos su música original
        self.cambiar_bgm("src/assets/musica/menu/MenuSong.mp3", volumen=1.0)

    # ==================================================
    # 🛠️ FUNCIÓN DE CONTROL SEGURO DE AUDIO
    # ==================================================
    def cambiar_bgm(self, ruta_cancion, volumen=1.0):
        """Usa el GestorAudio evitando que la misma canción se reinicie en bucle"""
        if not hasattr(self, "ruta_musica_actual"):
            self.ruta_musica_actual = None
            
        if self.ruta_musica_actual != ruta_cancion:
            self.ruta_musica_actual = ruta_cancion
            self.audio.reproducir_musica(ruta_cancion, volumen)

    # ==================================================
    # MÉTODOS AUXILIARES
    # ==================================================
    def controlar_transiciones(self):
        # Guardamos cuál era el escenario antes de verificar la transición
        escenario_anterior = self.gestor_escenarios.escenario_actual.__class__.__name__ if self.gestor_escenarios.escenario_actual else None
        
        self.gestor_escenarios.verificar_transicion(self.hoku_vista)
        
        # Si el escenario cambió, reiniciamos la protección del cine para que pueda volver a reproducirse
        escenario_nuevo = self.gestor_escenarios.escenario_actual.__class__.__name__ if self.gestor_escenarios.escenario_actual else None
        if escenario_anterior != escenario_nuevo and escenario_nuevo == "EscenarioDoce":
            self.cine_inicial_vista = False

    def verificar_interacciones(self):
        escenario_actual = self.gestor_escenarios.escenario_actual
        if escenario_actual is None:
            return
        
        if escenario_actual.__class__.__name__ == "EscenarioDoce" and len(self.acompanantes) > 0:
            self.disparar_cine_final()
            return

        enemigos_vivos = sum(1 for enemigo in escenario_actual.enemigos if enemigo.modelo.estaVivo())
        
        for npc in escenario_actual.npcs:
            area_interaccion = npc.rect.inflate(250, 250)
            if self.hoku_vista.rect.colliderect(area_interaccion):
                if hasattr(npc, 'modelo') and npc.modelo:
                    npc.modelo.interactuar(self.hoku_logico, enemigos_vivos)

    # ==================================================
    # MUSICA Y AUDIOS
    # ==================================================
    def cambiar_bgm(self, ruta_cancion, volumen=1.0):
        """Usa el GestorAudio de forma segura para no reiniciar la misma canción en bucle"""
        # Creamos una variable fantasma en el init si no existe para registrar la ruta
        if not hasattr(self, "ruta_musica_actual"):
            self.ruta_musica_actual = None
            
        if self.ruta_musica_actual != ruta_cancion:
            self.ruta_musica_actual = ruta_cancion
            self.audio.reproducir_musica(ruta_cancion, volumen)

# ======================================================
# MAIN
# ======================================================
def main():
    juego = GameController()
    juego.ejecutar()

if __name__ == "__main__":
    main()