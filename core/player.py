''' Responsabilidades:

-guardar nombre
-guardar color
-guardar ficha

'''

class Jugador:
    def __init__(self,nombre,color):
        self.__nombre__=nombre
        self.__color__=color
        self.__fichas__=15

    def obtener_nombre(self):
        return self.__nombre__

    def obtener_color(self):
        return self.__color__

    def gano(self): #gana cuando ya no tiene mas fichas
        return self.__fichas_restantes__ == 0

    def sacar_ficha(self): #metodo para ir restando las fichass que va sacando del tablero
        if self.__fichas_restantes__ > 0:
            self.__fichas_restantes__ -= 1
            return True
        return False