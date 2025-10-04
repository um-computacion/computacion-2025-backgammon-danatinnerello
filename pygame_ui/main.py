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
from pygame_ui.board_renderer import Tablero


def main():
    # Inicializar pygame
    pygame.init()
    pantalla = pygame.display.set_mode((1000, 600))
    pygame.display.set_caption("Backgammon - Pygame")

    reloj = pygame.time.Clock()
    tablero = Tablero(pantalla)

  
    corriendo = True
    while corriendo:
        # Manejo de eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False

        # Fondo color madera
        pantalla.fill((220, 190, 160))

        # Dibujar tablero
        tablero.dibujar_tablero()

        # Estado inicial del backgammon
        estado = {
            24: {"color": "blanco", "cantidad": 2},
            13: {"color": "blanco", "cantidad": 5},
            8:  {"color": "blanco", "cantidad": 3},
            6:  {"color": "blanco", "cantidad": 5},

            1:  {"color": "negro", "cantidad": 2},
            12: {"color": "negro", "cantidad": 5},
            17: {"color": "negro", "cantidad": 3},
            19: {"color": "negro", "cantidad": 5},
        }

        # Dibujar fichas
        tablero.dibujar_fichas(estado)

      
        # Actualizar pantalla
        pygame.display.flip()
        reloj.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
