"""
board_renderer.py
Responsabilidad:
- Encargado de dibujar todo lo visual del tablero.
- Dibuja los 24 triángulos (puntos) del Backgammon.
- Dibuja las fichas de los jugadores en la posición correcta.
- No contiene reglas del juego (la lógica sigue en core/).
- Solo “pinta” lo que le dicen que pinte.
"""

import pygame

class Tablero:
    def __init__(self,pantalla):
        self.pantalla = pantalla
        self.ancho= self.pantalla.get_width()
        self.alto= self.pantalla.get_height()
        self.ancho_triangulo = self.ancho // 14
        self.ancho_barra = self.ancho_triangulo  # barra central del mismo ancho que un triangulo
        self.alto_triangulo= self.alto // 2
        self.radio_ficha = self.ancho_triangulo // 3  # tamaño de la ficha

    def dibujar_tablero(self):
        # Colores de los triangulos
        colores= [(180, 100, 80), (250, 220, 200)]

        #Dibuja barras
        color_barra_central = (100, 70, 50)
        color_borde = (60, 40, 30)

        # Barra central
        x_barra = 6 * self.ancho_triangulo
        pygame.draw.rect(self.pantalla,color_barra_central,
            pygame.Rect(x_barra, 0, self.ancho_barra, self.alto))
        pygame.draw.rect(self.pantalla,color_borde,
            pygame.Rect(x_barra, 0, self.ancho_barra, self.alto),2)

        # Barra exterior izquierda
        pygame.draw.rect(self.pantalla,color_barra_central,
            pygame.Rect(0, 0, self.ancho_barra // 2, self.alto))
        pygame.draw.rect(self.pantalla,color_borde,
            pygame.Rect(0, 0, self.ancho_barra // 2, self.alto),2)

        # Barra exterior derecha
        pygame.draw.rect(self.pantalla,color_barra_central,
            pygame.Rect(self.ancho - self.ancho_barra // 2, 0, self.ancho_barra // 2, self.alto))
        pygame.draw.rect(self.pantalla,color_borde,
            pygame.Rect(self.ancho - self.ancho_barra // 2, 0, self.ancho_barra // 2, self.alto),2)

        #Parte superior izquierda(6 triangulos)
        for i in range(6):
            x = i * self.ancho_triangulo + self.ancho_barra // 2
            puntos = [(x, 0),
                    (x + self.ancho_triangulo, 0),
                    (x + self.ancho_triangulo // 2, self.alto_triangulo)]
            pygame.draw.polygon(self.pantalla, colores[i % 2], puntos)

        #Parte superior derecha(6 triangulos)
        for i in range(6):
            x = (i + 7) * self.ancho_triangulo + self.ancho_barra // 2
            puntos = [(x, 0),
                    (x + self.ancho_triangulo, 0),
                    (x + self.ancho_triangulo // 2, self.alto_triangulo)]
            pygame.draw.polygon(self.pantalla, colores[i % 2], puntos)

        #Parte inferior izquierda(6 triangulos)
        for i in range(6):
            x = i * self.ancho_triangulo + self.ancho_barra // 2
            puntos = [(x, self.alto),
                    (x + self.ancho_triangulo, self.alto),
                    (x + self.ancho_triangulo // 2, self.alto - self.alto_triangulo)]
            pygame.draw.polygon(self.pantalla, colores[i % 2], puntos)

        #Parte inferior derecha (6 triangulos)
        for i in range(6):
            x = (i + 7) * self.ancho_triangulo + self.ancho_barra // 2
            puntos = [(x, self.alto),
                    (x + self.ancho_triangulo, self.alto),
                    (x + self.ancho_triangulo // 2, self.alto - self.alto_triangulo)]
            pygame.draw.polygon(self.pantalla, colores[i % 2], puntos)

    def dibujar_fichas(self, estado: dict):
        """Dibuja las fichas en el tablero según el estado del juego"""
        for punto, datos in estado.items():
            color = (255, 255, 255) if datos["color"] == "blanco" else (0, 0, 0)
            cantidad = datos["cantidad"]

            # Ajuste según el lado del tablero (barra en el medio)
            if punto <= 12:  # parte inferior (1 a 12)
                if punto <= 6:
                    # Triángulos de la derecha del jugador negro
                    x = (6 - punto) * self.ancho_triangulo + self.ancho_triangulo // 2 + self.ancho_barra // 2 + (7 * self.ancho_triangulo)
                else:
                    # Triángulos de la izquierda del jugador negro
                    x = (12 - punto) * self.ancho_triangulo + self.ancho_triangulo // 2 + self.ancho_barra // 2
                y_base = self.alto - self.radio_ficha
                step = -self.radio_ficha * 2

            else:  # parte superior (13 a 24)
                if punto <= 18:
                    # Triángulos de la izquierda del jugador blanco
                    x = (punto - 13) * self.ancho_triangulo + self.ancho_triangulo // 2 + self.ancho_barra // 2
                else:
                    # Triángulos de la derecha del jugador blanco
                    x = (punto - 19) * self.ancho_triangulo + self.ancho_triangulo // 2 + self.ancho_barra // 2 + (7 * self.ancho_triangulo)
                y_base = self.radio_ficha
                step = self.radio_ficha * 2

            # Dibujar las fichas en "torres"
            for i in range(cantidad):
                y = y_base + step * i
                pygame.draw.circle(self.pantalla, color, (x, y), self.radio_ficha)
                pygame.draw.circle(self.pantalla, (0, 0, 0), (x, y), self.radio_ficha, 2)
