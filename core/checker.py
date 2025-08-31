'''fichas- Responsabilidades:

-Designar color y posicion
-validar movimiento
-saber si esta en barra
-o si esta afuera



'''
class Ficha:
    def __init__(self, color, posicion=None):
        self.__color__=color
        self.__posicion__=posicion  # puede ser de: (0 a 23), estar en barra o afuera

    def obtener_color(self):
        return self.__color__

    def obtener_posicion(self):
        return self.__posicion__

    def mover(self, nueva_posicion): #cambia la posiicon de la ficha
        self.__posicion__ = nueva_posicion

    def esta_en_barra(self): #si esta en barra
        return self.__posicion__ == "barra"

    def esta_afuera(self): # si ya salio
        return self.__posicion__ == "afuera"
