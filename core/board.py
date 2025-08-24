'''Responsabilidades:

-saber que fichas estan en cada punto
-validar movimiento
-guardar movimiento

'''
class Tablero:
    def __init__(self):
        self.__contendedor__ = [0] * 24  
        #Al iniciarse 
        self.__contendedor__[0]=-2
        self.__contendedor__[11]=-5
        self.__contendedor__[16]=-3
        self.__contendedor__[18]=-5
        self.__contendedor__[23]=2
        self.__contendedor__[12]=5
        self.__contendedor__[7]=3
        self.__contendedor__[5]=5

    def mostrar_contenedor(self):
        return self.__contendedor__
    
    def mover_ficha(self):
        ...

    def guardar_ficha(self):
        ...