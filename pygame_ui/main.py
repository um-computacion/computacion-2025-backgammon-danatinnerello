"""
main.py
Responsabilidad:
- Punto de entrada del juego con Pygame.
- Inicializa la ventana y configura el bucle principal del juego.
- Se encarga de llamar a los métodos de dibujo (board_renderer).
- Captura eventos (mouse, teclado) usando events.py.
- Mantiene el loop de juego (update → draw → events).
"""

import pygame
from pygame_ui.board_renderer import TableroGrafico, estado_desde_board
from core.player import Jugador
from core.game import Juego
from core.checker import Ficha
pygame.init()




jugador1 = Jugador("Jugador 1", "Blanca")
jugador2 = Jugador("Jugador 2", "Negra")
juego = Juego(jugador1, jugador2)


def pedir_nombres(pantalla):
    fuente = pygame.font.Font(None, 40)
    color_texto = (30, 30, 30)
    color_fondo = (230, 210, 180)

    nombres = ["", ""]
    etiquetas = ["Jugador 1 (Blancas):", "Jugador 2 (Negras):"]
    actual = 0
    escribiendo = True

    while escribiendo:
        pantalla.fill(color_fondo)

        for i, texto in enumerate(etiquetas):
            t = fuente.render(texto, True, color_texto)
            pantalla.blit(t, (100, 150 + i * 100))
            entrada = fuente.render(nombres[i], True, (0, 0, 0))
            pantalla.blit(entrada, (450, 150 + i * 100))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if actual < 1:
                        actual += 1
                    else:
                        escribiendo = False
                elif event.key == pygame.K_BACKSPACE:
                    nombres[actual] = nombres[actual][:-1]
                else:
                    nombres[actual] += event.unicode

    # Si no escribieron nada, usar nombres por defecto
    if nombres[0] == "":
        nombres[0] = "Blancas"
    if nombres[1] == "":
        nombres[1] = "Negras"

    return nombres[0], nombres[1]



def main():
    
    pantalla = pygame.display.set_mode((1000, 600))
    pygame.display.set_caption("Backgammon - Ludoteka Style")

    nombre1,nombre2 = pedir_nombres(pantalla)
    jugador1 = Jugador(nombre1, "Blanca")
    jugador2 = Jugador(nombre2, "Negra")

    juego = Juego(jugador1,jugador2)
    tablero = juego.__tablero__
    renderer = TableroGrafico(pantalla)
    estado = estado_desde_board(tablero)

    renderer.dibujar_tablero()
    renderer.dibujar_fichas(estado)
    clock = pygame.time.Clock()
    
    punto_seleccionado = None

    #actualiza estado
    pygame.display.flip()

    # Bucle principal
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False  # salir del bucle con el botón de cerrar
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                punto = renderer.obtener_punto_desde_click(event.pos)
                if punto:
                    if punto_seleccionado is None:
                        punto_seleccionado = punto
                        print(f"Seleccionaste el punto {punto_seleccionado}")
                    else:
                        jugador = juego.mostrar_turno()
                        try:
                            # Movimiento normal
                            juego.valida_mover_ficha(jugador, punto_seleccionado, punto)
                            print(f"{jugador.obtener_nombre()} movió una ficha de {punto_seleccionado} a {punto}")

                            # Redibujar tablero
                            estado = estado_desde_board(juego.mostrar_tablero())
                            renderer.dibujar_tablero()
                            renderer.dibujar_fichas(estado)
                            pygame.display.flip()

                            # Cambiar turno si corresponde
                            juego.controlar_turnos()

                        except Exception as e:
                            print(f"No se pudo mover la ficha: {e}")
                        punto_seleccionado = None

                        # Redibujar tablero actualizado
                        estado = estado_desde_board(tablero)
                        renderer.dibujar_tablero()
                        renderer.dibujar_fichas(estado)
                        pygame.display.flip()

        clock.tick(30)  # Limita a 30 FPS

    pygame.quit()

if __name__ == "__main__":
    main()
