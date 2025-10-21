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

class TableroGrafico:
    def __init__(self, pantalla, alto_tablero=None):
        self.pantalla = pantalla
        self.ancho = self.pantalla.get_width()
        self.alto = alto_tablero if alto_tablero else self.pantalla.get_height()
        self.ancho_triangulo = self.ancho // 14
        self.ancho_barra = self.ancho_triangulo
        self.alto_triangulo = self.alto // 2
        self.radio_ficha = self.ancho_triangulo // 3

    def dibujar_tablero(self):
        # Colores de los triangulos
        colores= [(180, 100, 80), (250, 220, 200)]

        #Dibuja barras
        color_barra_central = (100, 70, 50)
        color_borde = (60, 40, 30)
        color_fondo = (220, 190, 160) 
        self.pantalla.fill(color_fondo)


        # Barra central
        x_barra = (self.ancho / 2) - (self.ancho_barra / 2)
        pygame.draw.rect(self.pantalla,color_barra_central,
            pygame.Rect(x_barra, 0, self.ancho_barra, self.alto))
        pygame.draw.rect(self.pantalla,color_borde,
            pygame.Rect(x_barra, 0, self.ancho_barra, self.alto),2)

        #Parte superior izquierda(6 triangulos)
        for i in range(6):
            x = i * self.ancho_triangulo + self.ancho_barra // 2
            puntos = [(x, 0),
                    (x + self.ancho_triangulo, 0),
                    (x + self.ancho_triangulo // 2, self.alto_triangulo)]
            pygame.draw.polygon(self.pantalla, colores[(i + 1) % 2], puntos)

        #Parte superior derecha(6 triangulos)
        for i in range(6):
            x = x_barra + self.ancho_barra + (i * self.ancho_triangulo)
            puntos = [(x, 0),
                    (x + self.ancho_triangulo, 0),
                    (x + self.ancho_triangulo // 2, self.alto_triangulo)]
            pygame.draw.polygon(self.pantalla, colores[(i+1) % 2], puntos)

        #Parte inferior izquierda(6 triangulos)
        for i in range(6):
            x = i * self.ancho_triangulo + self.ancho_barra // 2
            puntos = [(x, self.alto),
                    (x + self.ancho_triangulo, self.alto),
                    (x + self.ancho_triangulo // 2, self.alto - self.alto_triangulo)]
            pygame.draw.polygon(self.pantalla, colores[i % 2], puntos)

        #Parte inferior derecha (6 triangulos)
        for i in range(6):
            x = x_barra + self.ancho_barra + (i * self.ancho_triangulo)
            puntos = [(x, self.alto),
                    (x + self.ancho_triangulo, self.alto),
                    (x + self.ancho_triangulo // 2, self.alto - self.alto_triangulo)]
            pygame.draw.polygon(self.pantalla, colores[i % 2], puntos)


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


    def dibujar_fichas(self, estado: dict):
        """Dibuja las fichas en el tablero según el estado del juego con punto 1 arriba a la derecha"""
        for punto, datos in estado.items():
            color = (255, 255, 255) if datos["color"] == "Blanca" else (0, 0, 0)
            cantidad = datos["cantidad"]

            # parte superior
            if punto <= 12:
                # Los triángulos van de derecha a izquierda
                if punto <= 6:
                    # Triángulos de la derecha
                    x = (6 - punto) * self.ancho_triangulo + self.ancho_triangulo // 2 \
                        + self.ancho_barra // 2 + (7 * self.ancho_triangulo)
                else:
                    # Triángulos de la izquierda
                    x = (12 - punto) * self.ancho_triangulo + self.ancho_triangulo // 2 \
                        + self.ancho_barra // 2
                y_base = self.radio_ficha
                step = self.radio_ficha * 2

            # parte inferior
            else:
                # Los triángulos van de derecha a izquierda
                if punto <= 18:
                    # Triángulos de la izquierda (19–24)
                    x = (punto - 13) * self.ancho_triangulo + self.ancho_triangulo // 2 \
                        + self.ancho_barra // 2
                else:
                    # Triángulos de la derecha(13–18)
                    x = (punto - 19) * self.ancho_triangulo + self.ancho_triangulo // 2 \
                        + self.ancho_barra // 2 + (7 * self.ancho_triangulo)
                y_base = self.alto - self.radio_ficha
                step = -self.radio_ficha * 2

            # Dibujar fichas en pila
            for i in range(cantidad):
                y = y_base + step * i
                pygame.draw.circle(self.pantalla, color, (x, y), self.radio_ficha)
                pygame.draw.circle(self.pantalla, (0, 0, 0), (x, y), self.radio_ficha, 2)

    def obtener_punto_desde_click(self, pos):
        """
        Devuelve el numero de punto (1-24) segun la posicion del clic del mouse.
        Si se clickea fuera de un punto, devuelve None.
        """
        x, y = pos
        margen = self.ancho // 20
        barra = self.ancho // 20
        mitad = self.alto // 2

        #Determina si el clic esta arriba o abajo
        parte_superior = y < mitad

        #Calcula columna segun x
        if x < margen or x > self.ancho - margen:
            return None  # fuera del tablero

        #Ajusta x relativo al tablero
        x_rel = x - margen
        if x > margen + 6 * self.ancho_triangulo:
            # a la derecha de la barra
            x_rel -= barra

        indice = int(x_rel // self.ancho_triangulo)
        if indice < 0 or indice > 11:
            return None

        # Convertierte a numero de punto
        if parte_superior:
            # 1 a 12 (de derecha a izquierda)
            punto = 12 - indice
        else:
            # 13 a 24 (de izquierda a derecha)
            punto = 13 + indice

        return punto


def estado_desde_board(board):
    """
    Convierte el estado del tablero del core en un formato entendible para el renderer.
    Admite tanto objetos Ficha como strings ("Blanca"/"Negra").
    """
    estado = {}
    puntos = board.__contenedor__

    for i, pila in enumerate(puntos):
        if not pila:
            continue

        ficha = pila[0]

        # Si es un objeto Ficha, obtenemos su color
        if hasattr(ficha, "obtener_color"):
            color = ficha.obtener_color().capitalize()
        else:
            # Si es string, lo usamos directamente
            color = str(ficha).capitalize()

        estado[i + 1] = {"color": color, "cantidad": len(pila)}

    return estado
