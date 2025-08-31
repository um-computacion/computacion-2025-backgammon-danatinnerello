''' Responsabilidades:

-guardar nombre
-guardar color
-guardar ficha

'''

class Jugador:
    def __init__(self,nombre,color):
        self.__nombre__=nombre
        self.__color__=color
        self.__fichas__= 15
        self.__fichas_restantes__= 15

    
    def mostrar_fichas_restantes(self):
        return self.__fichas_restantes__
    
    def obtener_nombre(self):
        return self.__nombre__

    def obtener_color(self):
        return self.__color__

    def gano(self): #gana cuando ya no tiene mas fichas
        return self.__fichas_restantes__ == 0

    def sacar_ficha_a_afuera(self): #metodo para ir restando las fichass que va sacando del tablero
        if self.__fichas_restantes__ > 0: # si es mayor que cero
            self.__fichas_restantes__ -= 1 #le resta una ficha
            return True
        return False
    
    def agregar_a_barra(self):
        self.__barra__ += 1 #agrega una ficha a la barra

    def quitar_de_barra(self):
        if self.__barra__ > 0: #si hay mas de una ficha en la barra
            self.__barra__ -= 1 # le resta una
            return True
        return False

    def tiene_en_barra(self): #muestra si tiene fichas en la barra
        return self.__barra__ > 0