import pygame

from src.vistas.escenarios.escenario_1 import EscenarioUno
from src.vistas.escenarios.escenario_2 import EscenarioDos
from src.vistas.escenarios.escenario_3 import EscenarioTres
from src.vistas.escenarios.escenario_4 import EscenarioCuatro
from src.vistas.escenarios.escenario_5 import EscenarioCinco
from src.vistas.escenarios.escenario_6 import EscenarioSeis
from src.vistas.escenarios.escenario_7 import EscenarioSiete
from src.vistas.escenarios.escenario_8 import EscenarioOcho
from src.vistas.escenarios.escenario_9 import EscenarioNueve
from src.vistas.escenarios.escenario_10 import EscenarioDiez
from src.vistas.escenarios.escenario_11 import EscenarioOnce
from src.vistas.escenarios.escenario_12 import EscenarioDoce


class GestorEscenarios:
    """
    Administra todos los escenarios del juego y las transiciones entre ellos.

    Uso típico en el game loop:
        gestor = GestorEscenarios()
        gestor.cargar_escenario(1)          # Empieza en escenario 1

        # Dentro del loop:
        gestor.escenario_actual.actualizar()
        gestor.escenario_actual.dibujar(pantalla)
        gestor.verificar_transicion(jugador)
    """

    # Mapeo de ID -> clase del escenario
    # Se instancian bajo demanda para no cargar todo en memoria de golpe
    _CLASES = {
        1:  EscenarioUno,
        2:  EscenarioDos,
        3:  EscenarioTres,
        4:  EscenarioCuatro,
        5:  EscenarioCinco,
        6:  EscenarioSeis,
        7:  EscenarioSiete,
        8:  EscenarioOcho,
        9:  EscenarioNueve,
        10: EscenarioDiez,
        11: EscenarioOnce,
        12: EscenarioDoce,
    }

    def __init__(self):
        self.escenario_actual = None
        self.id_actual = None

        # Cache opcional: guarda escenarios ya instanciados para no recargarlos
        self._cache = {}

    # ------------------------------------------------------------------
    # CARGA
    # ------------------------------------------------------------------
    def cargar_escenario(self, id_escenario, usar_cache=True):
        """
        Carga y activa el escenario con el ID indicado.
        Si usar_cache=True reutiliza instancias ya creadas (más rápido).
        """
        if id_escenario not in self._CLASES:
            raise ValueError(f"Escenario con ID {id_escenario} no existe.")

        if usar_cache and id_escenario in self._cache:
            self.escenario_actual = self._cache[id_escenario]
        else:
            self.escenario_actual = self._CLASES[id_escenario]()
            if usar_cache:
                self._cache[id_escenario] = self.escenario_actual

        self.id_actual = id_escenario

    # ------------------------------------------------------------------
    # TRANSICIÓN
    # ------------------------------------------------------------------
    def verificar_transicion(self, jugador):
        """
        Llama esto cada frame dentro del game loop.
        Detecta si el jugador salió por algún borde y, de ser así,
        carga el escenario vecino y reposiciona al jugador.

        Parámetros
        ----------
        jugador : objeto con atributos rect (pygame.Rect) y
                  métodos set_posicion(x, y) o acceso directo a rect.x / rect.y.
        """
        direccion, nuevo_id = self.escenario_actual.detectar_salida(jugador.rect)

        if nuevo_id is None:
            return  # El jugador no salió por ningún borde

        # Guardamos las dimensiones antes de cambiar
        ancho = self.escenario_actual.ancho
        alto  = self.escenario_actual.alto

        # Cargamos el nuevo escenario
        self.cargar_escenario(nuevo_id)

        # Reposicionamos al jugador en el borde OPUESTO del nuevo escenario
        self._reposicionar_jugador(jugador, direccion, ancho, alto)

    def _reposicionar_jugador(self, jugador, direccion, ancho_anterior, alto_anterior):
        """
        Coloca al jugador en el extremo opuesto al borde por el que salió.

        Lógica:
          - Salió por la DERECHA  → aparece en el borde IZQUIERDO  del nuevo escenario
          - Salió por la IZQUIERDA→ aparece en el borde DERECHO    del nuevo escenario
          - Salió por ARRIBA      → aparece en el borde INFERIOR    del nuevo escenario
          - Salió por ABAJO       → aparece en el borde SUPERIOR    del nuevo escenario
        """
        margen = 10  # Píxeles de separación del borde para que no vuelva a salir de inmediato

        if direccion == "derecha":
            jugador.rect.x = margen

        elif direccion == "izquierda":
            jugador.rect.x = self.escenario_actual.ancho - jugador.rect.width - margen

        elif direccion == "superior":
            jugador.rect.y = self.escenario_actual.alto - jugador.rect.height - margen

        elif direccion == "inferior":
            jugador.rect.y = margen

        # Resetear física vertical
        if hasattr(jugador, "vel_y"):
            jugador.vel_y = 0
        if hasattr(jugador, "en_suelo"):
            jugador.en_suelo = False

        # Sacar a Hoku de cualquier plataforma en la que haya quedado
        # metido tras la transición (empujarlo hacia arriba si colisiona)
        for plataforma in self.escenario_actual.plataformas:
            if jugador.rect.colliderect(plataforma.rect):
                jugador.rect.bottom = plataforma.rect.top
                if hasattr(jugador, "en_suelo"):
                    jugador.en_suelo = True

    # ------------------------------------------------------------------
    # HELPERS
    # ------------------------------------------------------------------
    def limpiar_cache(self):
        """Libera todos los escenarios cacheados (útil al volver al menú)."""
        self._cache.clear()
        self.escenario_actual = None
        self.id_actual = None