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

pygame.init()


def pedir_nombres(pantalla):
    fuente = pygame.font.Font(None, 48)
    texto1 = fuente.render("Jugador 1 (Blancas):", True, (0, 0, 0))
    texto2 = fuente.render("Jugador 2 (Negras):", True, (0, 0, 0))
    pantalla.fill((240, 230, 200))
    pantalla.blit(texto1, (250, 200))
    pantalla.blit(texto2, (250, 300))
    pygame.display.flip()
    return "Jugador 1", "Jugador 2"


def dibujar_dados(pantalla, valores, jugador_actual):
    """Muestra el turno actual y los valores de los dados en pantalla"""
    fuente = pygame.font.Font(None, 48)
    texto_turno = fuente.render(
        f"Turno: {jugador_actual.obtener_nombre()} ({jugador_actual.obtener_color()})",
        True,
        (0, 0, 0),
    )
    pantalla.blit(texto_turno, (50, 15))
    if valores:
        texto_dados = fuente.render(f"Dados: {valores}", True, (0, 0, 0))
        pantalla.blit(texto_dados, (600, 15))


def main():
    pantalla = pygame.display.set_mode((1000, 600))
    pygame.display.set_caption("Backgammon - Pygame UI")

    jugador1 = Jugador("Jugador 1", "Blanca")
    jugador2 = Jugador("Jugador 2", "Negra")
    juego = Juego(jugador1, jugador2)

    renderer = TableroGrafico(pantalla)

    running = True
    punto_origen = None
    dados_actuales = []
    puede_mover = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Tira dados con el espacio
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not puede_mover:
                    dados_actuales = juego.__dados__.tirar_dados()
                    puede_mover = True

            # Clic del mouse
            elif event.type == pygame.MOUSEBUTTONDOWN and puede_mover:
                pos = pygame.mouse.get_pos()
                punto = renderer.obtener_punto_desde_click(pos)
                if punto is not None:
                    print(f"Seleccionaste el punto {punto}")

                    if punto_origen is None:
                        punto_origen = punto
                        print(f"Origen seleccionado: {punto_origen}")
                    else:
                        punto_destino = punto
                        print(f"Destino seleccionado: {punto_destino}")

                        jugador = juego.mostrar_turno()

                        try:
                            print(f"Intentando mover de {punto_origen} a {punto_destino} ({jugador.obtener_color()})")
                            captura = juego.valida_mover_ficha(jugador, punto_origen, punto_destino)

                            if captura:
                                print("Capturaste una ficha enemiga")
                            else:
                                print("Movimiento valido")

                            # Si ya no quedan tiradas,pasa el turno
                            if not juego.__dados__.obtener_tiradas_restantes():
                                puede_mover = False

                        except Exception as e:
                            print("Movimiento invalido:", e)

                        # limpiar origen para el proximo movimiento
                        punto_origen = None

        # redibuja pantalla
        pantalla.fill((240, 230, 200))
        renderer.dibujar_tablero()
        renderer.dibujar_fichas(estado_desde_board(juego.mostrar_tablero()))
        dibujar_dados(pantalla, dados_actuales, juego.mostrar_turno())
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
