from core.excepcions import MovimientoInvalidoError

"""Responsabilidades:

-saber que fichas estan en cada punto
-validar movimiento
-guardar movimiento

"""
class Tablero:
    """Representa el tablero del juego con 24 puntos y la gestión de fichas."""

    def __init__(self):
        """Inicializa el tablero con las posiciones iniciales del Backgammon."""
        # Contenedor principal: lista de 24 puntos, cada punto tiene una pila de fichas
        self.__contenedor__ = [[] for _ in range(24)]
        # Configuración inicial de fichas (posición clásica de Backgammon)
        self.__contenedor__[0] = ["Negra"] * 2
        self.__contenedor__[11] = ["Negra"] * 5
        self.__contenedor__[16] = ["Negra"] * 3
        self.__contenedor__[18] = ["Negra"] * 5

        self.__contenedor__[23] = ["Blanca"] * 2
        self.__contenedor__[12] = ["Blanca"] * 5
        self.__contenedor__[7] = ["Blanca"] * 3
        self.__contenedor__[5] = ["Blanca"] * 5

        # Diccionario para fichas capturadas (en la barra)
        self.__barra__ = {"Blanca": [], "Negra": []}

        # Diccionario para fichas que ya salieron del tablero
        self.__afuera__ = {"Blanca": [], "Negra": []}

    def mostrar_contenedor(self):
        """Devuelve la lista interna que contiene las posiciones de las fichas."""
        return self.__contenedor__

    def imprimir_contenedor(self):
        """Imprime el estado actual del tablero en consola (para depuración o CLI)."""
        for i in range(24):
            fichas = " , ".join(self.__contenedor__[i]) if self.__contenedor__[i] else "."
            print(f"{i:2}: {fichas}")

    def mostrar_barra(self):
        """Devuelve el diccionario de fichas que están en la barra (capturadas)."""
        return self.__barra__

    def mostrar_afuera(self):
        """Devuelve el diccionario de fichas que ya fueron sacadas del tablero."""
        return self.__afuera__

    def mover_ficha(self, color, desde, hacia):
        """
        Mueve una ficha desde un punto hacia otro.
        Si hay una ficha enemiga sola, la captura y la envía a la barra.

        Args:
            color (str): color del jugador ("Blanca" o "Negra")
            desde (int): punto origen (0-23)
            hacia (int): punto destino (0-23)

        Returns:
            bool: True si hubo una captura, False si fue un movimiento normal
        """
        # Verificación de rango válido
        if desde < 0 or desde > 23 or hacia < 0 or hacia > 23:
            raise MovimientoInvalidoError("Punto de origen o destino fuera de rango (1-24).")

        # Verifica que haya fichas en la posición origen
        if not self.__contenedor__[desde]:
            raise MovimientoInvalidoError(f"No hay fichas en la posición {desde}")

        # Verifica que la ficha a mover sea del color correcto
        if self.__contenedor__[desde][-1] != color:
            raise MovimientoInvalidoError("Esa ficha no te pertenece")

        destino = self.__contenedor__[hacia]

        # Si el destino está bloqueado por 2 o más fichas enemigas, no se puede mover
        if len(destino) >= 2 and destino[0] != color:
            raise MovimientoInvalidoError("Destino bloqueado por fichas enemigas")

        ficha = self.__contenedor__[desde].pop()  # Quita la ficha del origen
        captura = False

        # Si hay una ficha enemiga sola, se la captura
        if len(destino) == 1 and destino[0] != color:
            self.enviar_a_barra(hacia)
            captura = True

        destino.append(ficha)  # Agrega la ficha al destino
        return captura

    def validar_movimiento(self, color, desde, hacia, tiradas_restantes=None):
        """
        Verifica si un movimiento es válido según las reglas básicas del Backgammon.
        """
        if hacia < 0 or hacia > 23 or desde < 0 or desde > 23:
            return False
        if not self.__contenedor__[desde]:
            return False
        if self.__contenedor__[desde][-1] != color:
            return False

        # Dirección de movimiento según el color
        if color == "Blanca" and hacia >= desde:
            return False
        if color == "Negra" and hacia <= desde:
            return False

        destino = self.__contenedor__[hacia]
        if len(destino) >= 2 and destino[0] != color:
            return False
        return True

    def enviar_a_barra(self, posicion):
        """Envía la ficha de una posición a la barra correspondiente (cuando es capturada)."""
        if self.__contenedor__[posicion]:
            ficha = self.__contenedor__[posicion].pop()
            self.__barra__[ficha].append(ficha)

    def valida_mover_desde_barra(self, color, hacia, tiradas_restantes=None):
        """
        Verifica si es posible reingresar una ficha desde la barra al tablero.
        """
        if not self.__barra__[color]:
            return False
        if hacia < 0 or hacia > 23:
            return False

        destino = self.__contenedor__[hacia]
        if len(destino) >= 2 and destino[0] != color:
            return False

        # Si hay tiradas, valida que coincidan con la distancia de entrada
        if tiradas_restantes is not None:
            diferencia = hacia if color == "Negra" else 24 - hacia
            if diferencia not in tiradas_restantes:
                return False
        return True

    def aplicar_movimiento_desde_barra(self, color, hacia):
        """
        Aplica el movimiento de reingreso desde la barra.
        Devuelve True si se capturó una ficha enemiga.
        """
        ficha_reingreso = self.__barra__[color].pop()
        destino = self.__contenedor__[hacia]
        captura = False
        color_enemigo = "Negra" if color == "Blanca" else "Blanca"

        if len(destino) == 1 and destino[0] == color_enemigo:
            self.enviar_a_barra(hacia)
            captura = True

        destino.append(ficha_reingreso)
        return captura

    def sacar_ficha(self, color, desde):
        """
        Saca una ficha del tablero cuando todas las del jugador están en su cuadrante final.
        """
        if self.__contenedor__[desde] and self.__contenedor__[desde][-1] == color:
            ficha = self.__contenedor__[desde].pop()
            self.__afuera__[color].append(ficha)
            return True
        return False

    def todas_en_ultimo_cuadrante(self, color):
        """
        Verifica si todas las fichas del jugador están en su casa (último cuadrante).
        """
        rango = range(0, 6) if color == "Blanca" else range(18, 24)
        for i, punto in enumerate(self.__contenedor__):
            for ficha in punto:
                if ficha == color and i not in rango:
                    return False
        return True

    def mostrar_estado(self):
        """Devuelve una representación textual del tablero."""
        estado = []
        for i in range(24):
            punto = self.__contenedor__[i]
            if punto:
                estado.append(f"{i+1:2}: {len(punto)} {punto[-1]}")
            else:
                estado.append(f"{i+1:2}: vacío")
        estado.append(f"Barra: {self.__barra__}")
        estado.append(f"Afuera: {self.__afuera__}")
        return "\n".join(estado)