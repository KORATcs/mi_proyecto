import pygame
import sys

# MODELOS
from src.modelos.personajes.protagonista.hoku import Hoku
from src.modelos.personajes.enemigos.bichiluz import Bichiluz

# VISTAS
from src.vistas.personajes.hoku_grafico import HokuGrafico
from src.vistas.personajes.bichiluz_grafico import BichiluzGrafico
from src.vistas.ataques.ataque_grafico import ZarpazoGrafico
from src.vistas.ui.hud import HUD

# CONTROLADOR
from src.controladores.controlador_hoku import ControladorHoku
from src.controladores.controlador_bichiluz import ControladorBichiluz


def main():
    pygame.init()

    ANCHO, ALTO = 1280, 720
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Hoku - Prototipo")

    NEGRO = (0, 0, 0)
    VELOCIDAD = 5
    FPS = 75

    reloj = pygame.time.Clock()
    limite_pantalla = pygame.Rect(0, 0, ANCHO, ALTO)

    # MODELOS
    hoku_logico = Hoku()
    bichiluz_logico = Bichiluz()

    # VISTAS
    hoku_vista = HokuGrafico(100, 100, hoku_logico)
    bichiluz_vista = BichiluzGrafico(500, 300, bichiluz_logico)

    # HUD
    hud_hoku = HUD(hoku_logico, 20, 20)
    hud_bichiluz = HUD(bichiluz_logico, 20, 70)

    # 🎮 CONTROLADOR
    controlador = ControladorHoku()
    controlador2 = ControladorBichiluz()

    # 🧱 LISTAS ESCALABLES
    enemigos = []
    enemigos.append(bichiluz_vista)

    ataques = []

    corriendo = True

    while corriendo:
        dt = reloj.tick(FPS)

        # 🎯 EVENTOS
        eventos = pygame.event.get()
        for evento in eventos:
            if evento.type == pygame.QUIT:
                corriendo = False
            
            # EL ATAQUE POR ESPACIO DEBE IR AQUÍ ADENTRO
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    # Este ataque manual (el de colisión directa de rects) 
                    # también debería estar aquí si quieres conservarlo
                    if hoku_vista.rect.colliderect(bichiluz_vista.rect):
                        hoku_logico.atacar(bichiluz_logico)

        # 🎮 INPUT
        controlador.procesar_eventos(eventos)
        #controlador2.procesar_eventos(eventos)

        dx, dy = controlador.obtener_movimiento()
        esta_atacando = controlador.atacando
        saltando = controlador.saltando

        bichi1, bichi2 = controlador2.obtener_movimiento()
        atacar = controlador.atacando

        # 🔄 normalizar diagonal
        if bichi1 != 0 and bichi2 != 0:
            bichi1 *= 0.7
            bichi2 *= 0.7

        dx *= VELOCIDAD
        dy *= VELOCIDAD

        bichi1 *= VELOCIDAD
        bichi2 *= VELOCIDAD


        # ⚔️ CREAR ATAQUE
        if esta_atacando and not hoku_vista.bloqueando_accion:
            offset = 40 if hoku_vista.mirando_derecha else -40

            nuevo_ataque = ZarpazoGrafico(
                hoku_vista.rect.x + offset,
                hoku_vista.rect.y,
                hoku_vista.mirando_derecha,
                hoku_vista.animaciones
            )

            ataques.append(nuevo_ataque)

        # 🧠 UPDATE PERSONAJES
        hoku_vista.update(dx, dy, esta_atacando, saltando, dt, limite_pantalla, enemigos)

        #for enemigo in enemigos:
         #   enemigo.actualizar(dt)

        """DE FORMA MOMENTANEA"""
        for enemigo in enemigos:
            enemigo.actualizar(bichi1, bichi2, dt, limite_pantalla)
            

        # 💥 DAÑO POR CONTACTO
        for enemigo in enemigos:
            if hoku_vista.rect.colliderect(enemigo.rect):
                if hoku_vista.tiempo_danio >= hoku_vista.cooldown_danio:
                    enemigo.modelo.atacar(hoku_logico)
                    hoku_vista.tiempo_danio = 0

        # ⚔️ UPDATE ATAQUES
        for ataque in ataques:
            ataque.update(dt)

            for enemigo in enemigos:
                # Verificamos colisión Y que no haya sido golpeado por ESTE ataque aún
                if ataque.rect.colliderect(enemigo.rect) and enemigo.modelo not in ataque.golpeados:
                    hoku_logico.atacar(enemigo.modelo)
                    ataque.golpeados.append(enemigo.modelo) # <--- Marcamos como golpeado

        # limpiar ataques
        ataques = [a for a in ataques if a.activo]

        # 🎨 RENDER
        pantalla.fill(NEGRO)

        for enemigo in enemigos:
            enemigo.dibujar(pantalla)

        hoku_vista.dibujar(pantalla)

        for ataque in ataques:
            ataque.dibujar(pantalla)


        hud_hoku.dibujar(pantalla)
        hud_bichiluz.dibujar(pantalla)

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()