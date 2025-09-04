'''Responsabilidades:

-saber que fichas estan en cada punto
-validar movimiento
-guardar movimiento

'''


class Tablero:
    def __init__(self):
        self.__contenedor__ = [[] for _ in range(24)] 
        #Al iniciarse, creamos el tablero con la posicion inicial de las fichas
        self.__contenedor__[0]=["Negra"]*2
        self.__contenedor__[11]=["Negra"]*5
        self.__contenedor__[16]=["Negra"]*3
        self.__contenedor__[18]=["Negra"]*5

        self.__contenedor__[23]=["Blanca"]*2
        self.__contenedor__[12]=["Blanca"]*5
        self.__contenedor__[7]=["Blanca"]*3
        self.__contenedor__[5]=["Blanca"]*5

        self.__barra__ = {"Blanca": [], "Negra": []} #creamos un diccionario para la barra
        self.__afuera__ = {"Blanca": [], "Negra": []} #creamos un diccionario para las fichas afuera del tablero


    def mostrar_contenedor(self):
        return self.__contenedor__
    
    def mostrar_barra(self):
        return self.__barra__

    def mostrar_afuera(self):
        return self.__afuera__
    
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

    def validar_movimiento(self, color, hacia):
        #valida el movimiento
        if hacia < 0 or hacia > 23: #primero si esta en el rango
            return False
        destino = self.__contenedor__[hacia]
        if len(destino)>= 2 and destino[0]!= color: #luego si hay 2 o mas fichas enemigas
            return False
        return True

    def enviar_a_barra(self, desde):
        #Si cae en una posicion con 1 ficha enemiga o del otro jugador, la manda a la barra
        if not self.__contenedor__[desde]:
            return
        ficha = self.__contenedor__[desde].pop() #elimina del contenedor
        self.__barra__[ficha].append(ficha) #la agrega a la barra

    def mover_desde_barra(self, color, hacia):
        #Saca ficha de la barra(si el movimiento es válido) y vuelve a estar en juego
        if not self.validar_movimiento(color, hacia):
            return False
        if self.__barra__[color]:
            ficha = self.__barra__[color].pop() #saca la ficha de la barra
            self.__contenedor__[hacia].append(ficha) #la agrega al contenedor
            return True
        return False

    def sacar_ficha(self, color, desde):
        #Cuando todas las fichas están en el ultimo cuadrante del contendor, se pueden sacar
        if self.__contenedor__[desde] and self.__contenedor__[desde][-1] == color:
            ficha = self.__contenedor__[desde].pop() #saca la ficha del contenedor
            self.__afuera__[color].append(ficha) #agregala ficha a fuera
            return True
        return False
  
    