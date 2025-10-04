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
        self.ancho_triangulo= self.ancho // 14  # 12 triangulos + margenes
        self.alto_triangulo= self.alto // 2
        self.radio_ficha = self.ancho_triangulo // 3  # tamaño de la ficha

    def dibujar_tablero(self):
        # Colores de los triangulos
        colores= [(180, 100, 80), (250, 220, 200)]

        # Parte superior (12 triangulos)
        for i in range(12):
            x = i * self.ancho_triangulo 
            puntos = [
                (x, 0),
                (x + self.ancho_triangulo, 0),
                (x + self.ancho_triangulo // 2, self.alto_triangulo)
            ]
            pygame.draw.polygon(self.pantalla, colores[i % 2], puntos)

        # Parte inferior (12 triángulos)
        for i in range(12):
            x = i * self.ancho_triangulo 
            puntos = [
                (x, self.alto),
                (x + self.ancho_triangulo, self.alto),
                (x + self.ancho_triangulo // 2, self.alto - self.alto_triangulo)
            ]
            pygame.draw.polygon(self.pantalla, colores[i % 2], puntos)

    def dibujar_fichas(self, estado: dict):
        """Dibuja las fichas en el tablero según el estado del juego"""
        for punto, datos in estado.items():
            color = (255, 255, 255) if datos["color"] == "blanco" else (0, 0, 0)
            cantidad = datos["cantidad"]

            #Determinar posicion del triangulo
            if punto<= 12:  # parte inferior
                x= (12 - punto) * self.ancho_triangulo + self.ancho_triangulo // 2
                y_base= self.alto - self.radio_ficha
                step= -self.radio_ficha * 2
            else:  # parte superior
                x= (punto - 13) * self.ancho_triangulo + self.ancho_triangulo // 2
                y_base= self.radio_ficha
                step= self.radio_ficha * 2

            # Dibujar las fichas en "torres"
            for i in range(cantidad):
                y= y_base + step * i
                pygame.draw.circle(self.pantalla,color,(x, y),self.radio_ficha)
                pygame.draw.circle(self.pantalla,(0, 0, 0),(x, y),self.radio_ficha,2)  # borde