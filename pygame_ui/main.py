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
ANCHO_PANTALLA = 1000
ALTO_TABLERO = 500
ALTO_PANEL = 100
ALTO_PANTALLA = ALTO_TABLERO + ALTO_PANEL
FUENTE = pygame.font.Font(None, 28)
COLOR_FONDO = (222, 184, 135)
COLOR_PANEL = (160, 110, 60)

def pantalla_pedir_nombres():
    pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
    pygame.display.set_caption("Backgammon - Ingresar nombres")

    input_boxes = [
        pygame.Rect(400, 250, 400, 50),
        pygame.Rect(400, 350, 400, 50),
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

def dibujar_panel_inferior(pantalla, juego, mensaje=""):
    rect_panel = pygame.Rect(0, ALTO_TABLERO, ANCHO_PANTALLA, ALTO_PANEL)
    pygame.draw.rect(pantalla, COLOR_PANEL, rect_panel)
    pygame.draw.rect(pantalla, (80, 50, 30), rect_panel, 3)

    jugador = juego.mostrar_turno()
    color = jugador.obtener_color()
    turno_texto = FUENTE.render(
        f"Turno: {jugador.obtener_nombre()} ({color})", True, (255, 255, 255)
    )
    dados_texto = FUENTE.render(
        f"Dados: {juego.__dados__.obtener_tiradas_restantes()}", True, (255, 255, 255)
    )
    pantalla.blit(turno_texto, (30, ALTO_TABLERO + 20))
    pantalla.blit(dados_texto, (400, ALTO_TABLERO + 20))
        # Mostrar fichas en barra y afuera
    barra = juego.mostrar_tablero().mostrar_barra()
    afuera = juego.mostrar_tablero().mostrar_afuera()

    texto_barra = FUENTE.render(
        f"Barra → Blancas: {len(barra['Blanca'])} | Negras: {len(barra['Negra'])}",
        True, (255, 255, 255)
    )
    texto_afuera = FUENTE.render(
        f"Afuera → Blancas: {len(afuera['Blanca'])} | Negras: {len(afuera['Negra'])}",
        True, (255, 255, 255)
    )
    pantalla.blit(texto_barra, (600, ALTO_TABLERO + 20))
    pantalla.blit(texto_afuera, (600, ALTO_TABLERO + 50))


    if mensaje:
        mensaje_texto = FUENTE.render(mensaje, True, (255, 255, 0))
        pantalla.blit(mensaje_texto, (30, ALTO_TABLERO + 60))

def main():
    nombre1, nombre2 = pantalla_pedir_nombres()
    if not nombre1 or not nombre2:
        return

    jugador1 = Jugador(nombre1, "Blanca")
    jugador2 = Jugador(nombre2, "Negra")
    juego = Juego(jugador1, jugador2)
    juego.__dados__.tirar_dados()

    pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
    pygame.display.set_caption("Backgammon - Pygame")

    renderer = TableroGrafico(pantalla, alto_tablero=ALTO_TABLERO)
    reloj = pygame.time.Clock()
    punto_origen = None
    mensaje = ""
    tiempo_mensaje = 0 #duracin restante del mensaje en milisegundos

    running = True
    while running:
        dt = reloj.tick(30)  #tiempo entre frames (ms)
        if tiempo_mensaje > 0:
            tiempo_mensaje -= dt
            if tiempo_mensaje <= 0:
                mensaje = ""

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # ENTER = tirar dados solo si no hay tiradas
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                if not juego.__dados__.obtener_tiradas_restantes():
                    juego.__dados__.tirar_dados()
                    mensaje = "Dados tirados"
                    tiempo_mensaje = 1500
                else:
                    mensaje = "Ya tiene tiradas disponibles"
                    tiempo_mensaje = 1500

            # Clicks en tablero para mover
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if y < ALTO_TABLERO:
                    punto = renderer.obtener_punto_desde_click((x, y))
                    if punto is not None:
                        if punto_origen is None:
                            punto_origen = punto
                        else:
                            punto_destino = punto
                            jugador = juego.mostrar_turno()
                            try:
                                captura = juego.valida_mover_ficha(jugador, punto_origen, punto_destino)
                                if captura:
                                    mensaje = "Capturaste una ficha enemiga"
                                else:
                                    mensaje = "Movimiento válido"

                                # revisar ganador
                                ganador = juego.verificar_ganador()
                                if ganador:
                                    mensaje = f"¡Ganó {ganador.obtener_nombre()}!"
                                    tiempo_mensaje = 999999
                                    running = False

                            except Exception as e:
                                mensaje = f"Movimiento inválido: {e}"
                                tiempo_mensaje = 2000

                            punto_origen = None
                            tiempo_mensaje = 1500

        # Si no hay tiradas disponibles y no hay mensaje activo, mostrar el de ENTER
        if not juego.__dados__.obtener_tiradas_restantes() and not mensaje:
            mensaje = "Presione ENTER para tirar los dados"
            tiempo_mensaje = 999999  # persistente hasta tirar

        dibujar_todo(pantalla, renderer, juego, mensaje)
        pygame.display.flip()

    pygame.quit()


def dibujar_todo(pantalla, renderer, juego, mensaje=""):
    pantalla.fill(COLOR_FONDO)
    renderer.dibujar_tablero()
    estado = estado_desde_board(juego.mostrar_tablero())
    renderer.dibujar_fichas(estado)
    dibujar_panel_inferior(pantalla, juego, mensaje)
    renderer.dibujar_barra(juego.mostrar_tablero())


if __name__ == "__main__":
    main()
