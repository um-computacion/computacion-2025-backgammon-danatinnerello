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
from core.game import Juego
from core.player import Jugador
from pygame_ui.events import ManejadorEventos  # Importar el nuevo manejador
from core.excepcions import MovimientoInvalidoError, RendicionError, JuegoTerminadoError

pygame.init()
ANCHO_PANTALLA = 1000
ALTO_TABLERO = 500
ALTO_PANEL = 100
ALTO_PANTALLA = ALTO_TABLERO + ALTO_PANEL
FUENTE = pygame.font.Font(None, 28)
COLOR_FONDO = (222, 184, 135)
COLOR_PANEL = (160, 110, 60)
COLOR_TEXTO = (255, 255, 255)


def pantalla_pedir_nombres():
    pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
    pygame.display.set_caption("Backgammon - Ingresar nombres")

    input_boxes = [pygame.Rect(400, 250, 400, 50), pygame.Rect(400, 350, 400, 50)]
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
                        if event.key == pygame.K_RETURN and all(nombres):
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
        f"Turno: {jugador.obtener_nombre()} ({color})", True, COLOR_TEXTO
    )
    dados_texto = FUENTE.render(
        f"Dados: {juego.__dados__.obtener_tiradas_restantes()}", True, COLOR_TEXTO
    )
    pantalla.blit(turno_texto, (30, ALTO_TABLERO + 20))
    pantalla.blit(dados_texto, (400, ALTO_TABLERO + 20))

    barra = juego.mostrar_tablero().mostrar_barra()
    afuera = juego.mostrar_tablero().mostrar_afuera()

    texto_barra = FUENTE.render(
        f"Barra → Blancas: {len(barra['Blanca'])} | Negras: {len(barra['Negra'])}",
        True,
        COLOR_TEXTO,
    )
    texto_afuera = FUENTE.render(
        f"Afuera → Blancas: {len(afuera['Blanca'])} | Negras: {len(afuera['Negra'])}",
        True,
        COLOR_TEXTO,
    )
    pantalla.blit(texto_barra, (600, ALTO_TABLERO + 20))
    pantalla.blit(texto_afuera, (600, ALTO_TABLERO + 50))

    if mensaje:
        mensaje_texto = FUENTE.render(mensaje, True, (255, 255, 0))
        pantalla.blit(mensaje_texto, (30, ALTO_TABLERO + 60))


def dibujar_todo(pantalla, renderer, juego, mensaje_ui=""):
    pantalla.fill(COLOR_FONDO)
    renderer.dibujar_tablero()
    estado = estado_desde_board(juego.mostrar_tablero())
    renderer.dibujar_fichas(estado)
    renderer.dibujar_barra(juego.mostrar_tablero())
    renderer.dibujar_barra_lateral(juego.mostrar_tablero())
    dibujar_panel_inferior(pantalla, juego, mensaje_ui)
    pygame.display.flip()  # Asegurar que la pantalla se actualiza


def main():
    try:
        nombre1, nombre2 = pantalla_pedir_nombres()
        if not nombre1 or not nombre2:
            return

        jugador1 = Jugador(nombre1, "Blanca")
        jugador2 = Jugador(nombre2, "Negra")

        # La validación de nombres ocurre AQUÍ al crear el objeto Juego:
        juego = Juego(jugador1, jugador2)

    except MovimientoInvalidoError as e:
        print(f"Error de inicialización: {e}")
        return  # Sale si la inicialización falla

    juego.__dados__.tirar_dados()  # Primera tirada (inicia el juego)

    pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
    pygame.display.set_caption("Backgammon - Pygame")

    renderer = TableroGrafico(pantalla, alto_tablero=ALTO_TABLERO)
    reloj = pygame.time.Clock()

    # Crear la instancia del manejador de eventos
    manejador = ManejadorEventos(juego, renderer)

    # Mensaje inicial con la primera tirada
    manejador._actualizar_mensaje(
        f"Turno de {juego.mostrar_turno().obtener_nombre()} - Tira: {juego.__dados__.obtener_tiradas_restantes()}",
        2500,
    )

    running = True
    while running:
        dt = reloj.tick(30)

        if manejador.ganador is not None:
            # Comprueba si han pasado 5 segundos (5000 ms) desde que se declaró el ganador
            tiempo_actual = pygame.time.get_ticks()
            if (
                tiempo_actual - manejador.tiempo_fin_juego
                > manejador.duracion_mensaje_final
            ):
                running = False  # Detiene el bucle principal y cierra el juego
                continue  # Saltar el resto del bucle

        # Tira nuevos dados solo si los anteriores están agotados Y el juego NO ha terminado.
        if (
            not juego.__dados__.obtener_tiradas_restantes()
            and manejador.ganador is None
        ):
            jugador_actual = juego.mostrar_turno()
            juego.__dados__.tirar_dados()

            manejador._actualizar_mensaje(
                f"Turno de {jugador_actual.obtener_nombre()} - Tira: {juego.__dados__.obtener_tiradas_restantes()}",
                2500,  # Mostrar por 2.5 segundos
            )

        # Llamar al manejador de eventos
        manejador.manejar_eventos(dt)
        running = manejador.running

        # Dibujar con el estado actual del manejador
        dibujar_todo(pantalla, renderer, juego, manejador.mensaje_ui)

    pygame.quit()


if __name__ == "__main__":
    main()

# me falta:
# docker
# completar documentacionn
# pulir detalles
