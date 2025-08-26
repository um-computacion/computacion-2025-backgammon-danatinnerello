'''Responsabilidades:

-saber que fichas estan en cada punto
-validar movimiento
-guardar movimiento

'''
class Tablero:
    def __init__(self):
        self.__contenedor__ = [[] for _ in range(24)] 
        #Al iniciarse 
        self.__contenedor__[0]=["Negra"]*2
        self.__contenedor__[11]=["Negra"]*5
        self.__contenedor__[16]=["Negra"]*3
        self.__contenedor__[18]=["Negra"]*5

        self.__contenedor__[23]=["Blanca"]*2
        self.__contenedor__[12]=["Blanca"]*5
        self.__contenedor__[7]=["Blanca"]*3
        self.__contenedor__[5]=["Blanca"]*5

    def mostrar_contenedor(self):
        return self.__contenedor__
    
    def mover_ficha(self,ficha,desde,hacia):
        #verifica que la posiicon este entre 0 y 23
        if (hacia < 0 or hacia > 23) ^ (desde < 0 or desde > 23):
            raise ValueError("Punto inválido. Debe estar entre 0 y 23.")
        # verifica que contenga algo la posicion
        if not self.__contenedor__[desde]:
            raise ValueError("No hay fichas en la posicion {desde}")
        #elimina la ficha
        ficha = self.__contenedor__[desde].pop()
        #guarda ficha
        self.__contenedor__[hacia].append(ficha)

  
    