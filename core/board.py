'''Responsabilidades:

-saber que fichas estan en cada punto
-validar movimiento
-guardar movimiento

'''
class tablero:
    def __init__(self):
        self.__contendedor = [0] * 24  
        #Al iniciarse 
        self.__contendedor[0]=-2
        self.__contendedor[11]=-5
        self.__contendedor[16]=-3
        self.__contendedor[18]=-5
        self.__contendedor[23]=2
        self.__contendedor[12]=5
        self.__contendedor[7]=3
        self.__contendedor[5]=5

    def mostrar_contenedor(self):
        return self.__contendedor
    
    def mover_ficha(self):
        ...

    def guardar_ficha(self):
        ...