"""Responsabilidades:

-simula dados
- Generar tiradas aleatorias.
- Manejar tiradas dobles (se repiten 4 veces).
- Llevar el control de las tiradas restantes.

"""
import random

class Dados:
    """Clase que representa los dos dados del juego."""

    def __init__(self):
        """Inicializa los dados sin valores aún."""
        self.__dado1__ = 0
        self.__dado2__ = 0
        self.__tiradas_restantes__ = []

    def tirar_dados(self):
        """
        Simula la tirada de ambos dados.
        Si salen iguales, se duplican las jugadas disponibles (4 en total).
        """
        self.__dado1__ = random.randint(1, 6)
        self.__dado2__ = random.randint(1, 6)

        if self.__dado1__ == self.__dado2__:
            # Si los dados son iguales (doble), se juegan 4 veces el mismo número
            self.__tiradas_restantes__ = [self.__dado1__] * 4
        else:
            # Si son diferentes, solo se pueden usar una vez cada uno
            self.__tiradas_restantes__ = [self.__dado1__, self.__dado2__]

        return self.__tiradas_restantes__

    def obtener_tiradas_restantes(self):
        """Devuelve las tiradas que aún no fueron usadas."""
        return self.__tiradas_restantes__

    def usar_tirada(self, valor, revertir=False):
        """
        Usa una tirada específica o la revierte en caso de error.

        Args:
            valor (int): valor del dado usado
            revertir (bool): True si se quiere devolver el dado a la lista
        """
        if revertir:
            self.__tiradas_restantes__.append(valor)
            return True

        if valor in self.__tiradas_restantes__:
            self.__tiradas_restantes__.remove(valor)
            return True
        return False

    def quedan_tiradas(self):
        """Devuelve True si todavía hay tiradas disponibles."""
        return len(self.__tiradas_restantes__) > 0

    def reiniciar(self):
        """Borra las tiradas restantes (usado al pasar el turno)."""
        self.__tiradas_restantes__ = []