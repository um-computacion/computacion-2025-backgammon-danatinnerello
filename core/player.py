"""Responsabilidades:

-guardar nombre
-guardar color
-guardar ficha

"""
class Jugador:
    """Representa un jugador del Backgammon."""

    def __init__(self, nombre, color):
        """
        Inicializa un jugador con su nombre y color.
        """
        self.__nombre__ = nombre
        self.__color__ = color
        self.__fichas__ = 15  # Fichas totales
        self.__fichas_restantes__ = 15  # Fichas que faltan sacar

    def __str__(self):
        return f"{self.__nombre__}"

    def mostrar_fichas_restantes(self):
        """Devuelve cuántas fichas le quedan por sacar."""
        return self.__fichas_restantes__

    def obtener_nombre(self):
        """Devuelve el nombre del jugador."""
        return self.__nombre__

    def obtener_color(self):
        """Devuelve el color de sus fichas."""
        return self.__color__

    def gano(self):
        """Devuelve True si el jugador ya no tiene fichas restantes (ganó)."""
        return self.__fichas_restantes__ == 0

    def sacar_ficha_a_afuera(self):
        """
        Resta una ficha de las que quedan dentro del tablero.
        Se usa cuando logra sacar una ficha al exterior.
        """
        if self.__fichas_restantes__ > 0:
            self.__fichas_restantes__ -= 1
            return True
        return False
