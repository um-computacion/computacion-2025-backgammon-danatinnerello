"""fichas- Responsabilidades:

-Designar color y posicion
-validar movimiento
-saber si esta en barra
-o si esta afuera


"""
class Ficha:
    """Representa una ficha de Backgammon con color y posición."""

    def __init__(self, color, posicion=None):
        """
        Args:
            color (str): color de la ficha ("Blanca" o "Negra")
            posicion (int|str): índice del punto (0-23), 'barra' o 'afuera'
        """
        self.__color__ = color
        self.__posicion__ = posicion  # Puede estar en tablero, barra o afuera

    def obtener_color(self):
        """Devuelve el color de la ficha."""
        return self.__color__

    def obtener_posicion(self):
        """Devuelve la posición actual de la ficha."""
        return self.__posicion__

    def mover(self, nueva_posicion):
        """Cambia la posición actual de la ficha."""
        self.__posicion__ = nueva_posicion

    def esta_en_barra(self):
        """Devuelve True si la ficha está en la barra."""
        return self.__posicion__ == "barra"

    def esta_afuera(self):
        """Devuelve True si la ficha ya fue sacada del tablero."""
        return self.__posicion__ == "afuera"

