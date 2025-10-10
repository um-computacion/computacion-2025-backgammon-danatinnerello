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
from core.board import Tablero

def main():
    pygame.init()

    pantalla = pygame.display.set_mode((1000, 600))
    pygame.display.set_caption("Backgammon - Ludoteka Style")

    tablero = Tablero()
    renderer = TableroGrafico(pantalla)
    estado = estado_desde_board(tablero)

    renderer.dibujar_tablero()
    renderer.dibujar_fichas(estado)
    clock = pygame.time.Clock()

    #actualiza estado
    pygame.display.flip()

    # Bucle principal
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False  # salir del bucle con el botón de cerrar
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False  # salir también con tecla ESC
        clock.tick(30)  # Limita a 30 FPS

    pygame.quit()

if __name__ == "__main__":
    main()
