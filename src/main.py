import pygame
import sys

# 1. IMPORTACIONES
from src.modelos.personajes.protagonista.hoku import Hoku
from src.modelos.personajes.jefes.cabra_de_fuego import CabraDeFuego
from src.vistas.personaje_grafico import PersonajeGrafico

def main():
    pygame.init()
    ANCHO, ALTO = 800, 600
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Hoku - Prototipo de juego")
    fuente = pygame.font.SysFont("Arial", 50, bold=True)
    
    NEGRO = (0, 0, 0)
    ROSA = (255, 182, 193)
    NARANJA = (255, 140, 0)
    VELOCIDAD = 5
    FPS = 75
    
    hoku_logico = Hoku()
    jefe_logico = CabraDeFuego()
    jefe_derrotado = False

    hoku_vista = PersonajeGrafico(100, 100, 60, 60, ROSA)
    jefe_vista = PersonajeGrafico(500, 300, 80, 80, NARANJA)

    limite_pantalla = pygame.Rect(0, 0, ANCHO, ALTO)
    reloj = pygame.time.Clock()
    corriendo = True

    while corriendo:
        # 1. GUARDAR POSICIONES
        pos_ant_hoku = hoku_vista.rect.topleft
        pos_ant_jefe = jefe_vista.rect.topleft

        # A. EVENTOS
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False
            
            if evento.type == pygame.KEYDOWN and not jefe_derrotado:
                if evento.key == pygame.K_SPACE:
                    pos_hoku = pygame.Vector2(hoku_vista.rect.center)
                    pos_jefe = pygame.Vector2(jefe_vista.rect.center)
                    distancia = pos_hoku.distance_to(pos_jefe)
                    RANGO_ATAQUE = 100 

                    if distancia <= RANGO_ATAQUE:
                        hoku_logico.atacar(jefe_logico)
                        if jefe_logico._vida <= 0:
                            jefe_derrotado = True

        # B. MOVIMIENTO (Solo si el jefe está vivo)
        teclas = pygame.key.get_pressed()
        if not jefe_derrotado:
            dx, dy = 0, 0
            if teclas[pygame.K_w]: dy -= VELOCIDAD
            if teclas[pygame.K_s]: dy += VELOCIDAD
            if teclas[pygame.K_a]: dx -= VELOCIDAD
            if teclas[pygame.K_d]: dx += VELOCIDAD
            hoku_vista.mover(dx, dy, limite_pantalla)

            jx, jy = 0, 0
            if teclas[pygame.K_UP]:    jy -= VELOCIDAD
            if teclas[pygame.K_DOWN]:  jy += VELOCIDAD
            if teclas[pygame.K_LEFT]:  jx -= VELOCIDAD
            if teclas[pygame.K_RIGHT]: jx += VELOCIDAD
            jefe_vista.mover(jx, jy, limite_pantalla)

            # C. COLISIÓN
            if hoku_vista.colisiona_con(jefe_vista):
                hoku_vista.rect.topleft = pos_ant_hoku
                jefe_vista.rect.topleft = pos_ant_jefe

        # D. RENDERIZADO (Todo esto debe estar DENTRO del while)
        pantalla.fill(NEGRO)
        
        if not jefe_derrotado:
            hoku_vista.dibujar(pantalla)
            jefe_vista.dibujar(pantalla)
        else:
            # Mensaje de victoria
            mensaje = fuente.render("¡EL JEFE HA MUERTO!", True, (255, 255, 0))
            rect_texto = mensaje.get_rect(center=(ANCHO // 2, ALTO // 2))
            pantalla.blit(mensaje, rect_texto)
            # Dibujamos a Hoku solo para que se vea en la pantalla final
            hoku_vista.dibujar(pantalla)

        pygame.display.flip()
        reloj.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()