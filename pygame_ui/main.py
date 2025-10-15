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
from core.game import Juego, Jugador


pygame.init()
ANCHO_PANTALLA =1000
ALTO_PANTALLA = 600
FUENTE = pygame.font.Font(None, 24)
COLOR_FONDO = (222, 184, 135)  # color madera

def pantalla_pedir_nombres():
    """Pantalla inicial para pedir los nombres de los jugadores"""
    pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
    pygame.display.set_caption("Backgammon - Ingresar nombres")

    input_boxes = [
        pygame.Rect(400, 250, 400, 50),  # Jugador 1
        pygame.Rect(400, 350, 400, 50),  # Jugador 2
    ]
    nombres = ["", ""]
    colores = [(255, 255, 255)] * 2
    activo = [False, False]
    texto_instruccion = FUENTE.render(
        "Ingrese los nombres y presione ENTER para comenzar", True, (0, 0, 0)
    )

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None, None

            if event.type == pygame.MOUSEBUTTONDOWN:
                for i, box in enumerate(input_boxes):
                    activo[i] = box.collidepoint(event.pos)
                    colores[i] = (200, 200, 255) if activo[i] else (255, 255, 255)

            if event.type == pygame.KEYDOWN:
                for i in range(2):
                    if activo[i]:
                        if event.key == pygame.K_RETURN:
                            if all(nombres):
                                return nombres[0], nombres[1]
                        elif event.key == pygame.K_BACKSPACE:
                            nombres[i] = nombres[i][:-1]
                        else:
                            nombres[i] += event.unicode

        pantalla.fill(COLOR_FONDO)
        pantalla.blit(texto_instruccion, (280, 150))

        for i, box in enumerate(input_boxes):
            texto_label = FUENTE.render(
                f"Jugador {i+1} ({'Blancas' if i == 0 else 'Negras'}):", True, (0, 0, 0)
            )
            pantalla.blit(texto_label, (200, 260 + i * 100))
            pygame.draw.rect(pantalla, colores[i], box, 2)
            texto_nombre = FUENTE.render(nombres[i], True, (0, 0, 0))
            pantalla.blit(texto_nombre, (box.x + 10, box.y + 10))

        pygame.display.flip()
        clock.tick(30)

def dibujar_dados(pantalla, valores, jugador_actual):
    """Muestra el turno actual y los valores de los dados en pantalla"""
    fuente = pygame.font.Font(None, 48)
    texto_turno = fuente.render(
        f"Turno: {jugador_actual.obtener_nombre()} ({jugador_actual.obtener_color()})", True, (0, 0, 0)
    )
    pantalla.blit(texto_turno, (50, 15))
    if valores:
        texto_dados = fuente.render(f"Dados: {valores}", True, (0, 0, 0))
        pantalla.blit(texto_dados, (600, 15))


def main():
    nombre1, nombre2 = pantalla_pedir_nombres()
    if not nombre1 or not nombre2:
        return

    jugador1 = Jugador(nombre1, "Blanca")
    jugador2 = Jugador(nombre2, "Negra")

    juego = Juego(jugador1, jugador2)
    tablero = juego.mostrar_tablero()
    juego.__dados__.tirar_dados()
    pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
    pygame.display.set_caption("Backgammon - Pygame")

    renderer = TableroGrafico(pantalla)

    reloj = pygame.time.Clock()
    punto_origen = None
    dados_actuales = []

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                punto = renderer.obtener_punto_desde_click((x, y))


                if punto is not None:
                    if punto_origen is None:
                        punto_origen = punto
                    else:
                        punto_destino = punto
                        jugador = juego.mostrar_turno()

                        try:
                            juego.valida_mover_ficha(jugador, punto_origen, punto_destino)
                            juego.__tablero__.mover_ficha(jugador, punto_origen, punto_destino)
                            if not juego.__dados__.obtener_tiradas_restantes():
                                juego.controlar_turnos()
                                juego.__dados__.tirar_dados()
                        except Exception as e:
                            print(f"Movimiento inválido: {e}")

                        punto_origen = None

        #Dibuja del tablero
        pantalla.fill(COLOR_FONDO)
        renderer.dibujar_tablero()
        estado = estado_desde_board(tablero)
        renderer.dibujar_fichas(estado)

     

        dibujar_dados(pantalla, juego.__dados__.obtener_tiradas_restantes(), juego.mostrar_turno())

        pygame.display.flip()
        reloj.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
