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
        colores = [(180, 100, 80), (250, 220, 200)]
        color_barra_central = (100, 70, 50)
        color_borde = (60, 40, 30)
        color_fondo = (220, 190, 160)
        self.pantalla.fill(color_fondo)

        # Barra central
        x_barra = (self.ancho / 2) - (self.ancho_barra / 2)
        pygame.draw.rect(self.pantalla, color_barra_central,
                         pygame.Rect(x_barra, 0, self.ancho_barra, self.alto))
        pygame.draw.rect(self.pantalla, color_borde,
                         pygame.Rect(x_barra, 0, self.ancho_barra, self.alto), 2)

        # Triángulos del tablero
        for i in range(6):
            x = i * self.ancho_triangulo + self.ancho_barra // 2
            pygame.draw.polygon(self.pantalla, colores[(i + 1) % 2],
                                [(x, 0), (x + self.ancho_triangulo, 0), (x + self.ancho_triangulo // 2, self.alto_triangulo)])
        for i in range(6):
            x = x_barra + self.ancho_barra + (i * self.ancho_triangulo)
            pygame.draw.polygon(self.pantalla, colores[(i + 1) % 2],
                                [(x, 0), (x + self.ancho_triangulo, 0), (x + self.ancho_triangulo // 2, self.alto_triangulo)])
        for i in range(6):
            x = i * self.ancho_triangulo + self.ancho_barra // 2
            pygame.draw.polygon(self.pantalla, colores[i % 2],
                                [(x, self.alto), (x + self.ancho_triangulo, self.alto),
                                 (x + self.ancho_triangulo // 2, self.alto - self.alto_triangulo)])
        for i in range(6):
            x = x_barra + self.ancho_barra + (i * self.ancho_triangulo)
            pygame.draw.polygon(self.pantalla, colores[i % 2],
                                [(x, self.alto), (x + self.ancho_triangulo, self.alto),
                                 (x + self.ancho_triangulo // 2, self.alto - self.alto_triangulo)])

        # Barras exteriores
        pygame.draw.rect(self.pantalla, color_barra_central,
                         pygame.Rect(0, 0, self.ancho_barra // 2, self.alto))
        pygame.draw.rect(self.pantalla, color_borde,
                         pygame.Rect(0, 0, self.ancho_barra // 2, self.alto), 2)
        pygame.draw.rect(self.pantalla, color_barra_central,
                         pygame.Rect(self.ancho - self.ancho_barra // 2, 0, self.ancho_barra // 2, self.alto))
        pygame.draw.rect(self.pantalla, color_borde,
                         pygame.Rect(self.ancho - self.ancho_barra // 2, 0, self.ancho_barra // 2, self.alto), 2)

    def dibujar_fichas(self, estado: dict):
        fuente = pygame.font.Font(None, 24)
        max_visibles = 5
        for punto, datos in estado.items():
            color = (255, 255, 255) if datos["color"] == "Blanca" else (0, 0, 0)
            cantidad = datos["cantidad"]

            if punto <= 12:
                if punto <= 6:
                    x = (6 - punto) * self.ancho_triangulo + self.ancho_triangulo // 2 + self.ancho_barra // 2 + (7 * self.ancho_triangulo)
                else:
                    x = (12 - punto) * self.ancho_triangulo + self.ancho_triangulo // 2 + self.ancho_barra // 2
                y_base = self.radio_ficha
                step = self.radio_ficha * 2
            else:
                if punto <= 18:
                    x = (punto - 13) * self.ancho_triangulo + self.ancho_triangulo // 2 + self.ancho_barra // 2
                else:
                    x = (punto - 19) * self.ancho_triangulo + self.ancho_triangulo // 2 + self.ancho_barra // 2 + (7 * self.ancho_triangulo)
                y_base = self.alto - self.radio_ficha
                step = -self.radio_ficha * 2

            visibles = min(cantidad, max_visibles)
            for i in range(visibles):
                y = y_base + step * i
                pygame.draw.circle(self.pantalla, color, (x, y), self.radio_ficha)
                pygame.draw.circle(self.pantalla, (0, 0, 0), (x, y), self.radio_ficha, 2)

            if cantidad > max_visibles:
                restantes = cantidad - max_visibles
                y = y_base + step * (visibles - 1)
                color_texto = (0, 0, 0) if color == (255, 255, 255) else (255, 255, 255)
                texto = fuente.render(f"+{restantes}", True, color_texto)
                rect = texto.get_rect(center=(x, y))
                self.pantalla.blit(texto, rect)

    def dibujar_barra(self, tablero):
        """Dibuja las fichas en la barra central (ahora escaladas verticalmente)."""
        barra = tablero.mostrar_barra()
        x_centro = self.ancho // 2
        alto_zona = self.alto // 2 - 20  # espacio disponible para cada mitad

        for color, fichas in barra.items():
            cantidad = len(fichas)
            if cantidad == 0:
                continue

            # Escala dinámica del radio si hay muchas fichas
            radio = max(self.radio_ficha * 0.6, min(self.radio_ficha, alto_zona / (cantidad * 2)))
            step = radio * 2
            color_rgb = (255, 255, 255) if color == "Blanca" else (0, 0, 0)

            for i in range(cantidad):
                y = (self.alto // 2) - ((i + 1) * step) if color == "Blanca" else (self.alto // 2) + (i * step) + step
                pygame.draw.circle(self.pantalla, color_rgb, (x_centro, int(y)), int(radio))
                pygame.draw.circle(self.pantalla, (0, 0, 0), (x_centro, int(y)), int(radio), 2)

            # Muestra número si hay más de 6
            if cantidad > 6:
                texto = pygame.font.Font(None, 28).render(str(cantidad), True, (255, 0, 0))
                self.pantalla.blit(texto, (x_centro - 8, (self.alto // 2) + (40 if color == "Negra" else -60)))

    def dibujar_barra_lateral(self, tablero):
        """Muestra solo la cantidad de fichas fuera (barra lateral derecha)."""
        afuera = tablero.mostrar_afuera()
        fuente = pygame.font.Font(None, 36)
        
        # Coordenada base centrada en la barra lateral derecha
        x_centro_barra = self.ancho - self.ancho_barra // 4

        # Blancas (arriba)
        cantidad_blanca = len(afuera.get("Blanca", []))
        texto_blanca = fuente.render(f"{cantidad_blanca}", True, (0, 0, 0))
        texto_blanca_rect = texto_blanca.get_rect(center=(x_centro_barra, 40))
        pygame.draw.rect(self.pantalla, (255, 255, 255), texto_blanca_rect.inflate(16, 10), border_radius=6)
        self.pantalla.blit(texto_blanca, texto_blanca_rect)

        # Negras (abajo)
        cantidad_negra = len(afuera.get("Negra", []))
        texto_negra = fuente.render(f"{cantidad_negra}", True, (255, 255, 255))
        texto_negra_rect = texto_negra.get_rect(center=(x_centro_barra, self.alto - 40))
        pygame.draw.rect(self.pantalla, (0, 0, 0), texto_negra_rect.inflate(16, 10), border_radius=6)
        self.pantalla.blit(texto_negra, texto_negra_rect)

    def obtener_punto_desde_click(self, pos):
        x, y = pos
        margen = self.ancho // 20
        barra = self.ancho // 20
        mitad = self.alto // 2
        parte_superior = y < mitad
        if x < margen or x > self.ancho - margen:
            return None
        x_rel = x - margen
        if x > margen + 6 * self.ancho_triangulo:
            x_rel -= barra
        indice = int(x_rel // self.ancho_triangulo)
        if indice < 0 or indice > 11:
            return None
        return 12 - indice if parte_superior else 13 + indice

    def obtener_barra_lateral_desde_click(self, pos):
        x, y = pos
        if x < self.ancho_barra // 2:
            return "izquierda"
        elif x > self.ancho - self.ancho_barra // 2:
            return "derecha"
        return None


def estado_desde_board(board):
    estado = {}
    puntos = board.__contenedor__
    for i, pila in enumerate(puntos):
        if not pila:
            continue
        ficha = pila[0]
        color = ficha.obtener_color().capitalize() if hasattr(ficha, "obtener_color") else str(ficha).capitalize()
        estado[i + 1] = {"color": color, "cantidad": len(pila)}
    return estado
