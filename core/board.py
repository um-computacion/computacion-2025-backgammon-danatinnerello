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
        for i in range(24):
            fichas = " , ".join(self.__contenedor__[i]) if self.__contenedor__[i] else "." 
            print(f"{i:2}: {fichas}")
        return self.__contenedor__
    
    def mostrar_barra(self):
        return self.__barra__

    def mostrar_afuera(self):
        return self.__afuera__
    
    def mover_ficha(self,color,desde,hacia):
        #verifica que la posiicon este entre 0 y 23
        if (hacia < 0 or hacia > 23) ^ (desde < 0 or desde > 23):
            raise ValueError("Punto invalido. Debe estar entre 1 y 24.")
        # verifica que contenga algo la posicion
        if not self.__contenedor__[desde]:
            raise ValueError("No hay fichas en la posicion {desde}")
        #elimina la ficha
        ficha= self.__contenedor__[desde].pop()
        #guarda ficha
        destino= self.__contenedor__[hacia]
        captura= False

        # si hay exactamente 1 ficha enemiga entonces la captura y la manda a barra
        if len(destino)== 1 and destino[0]!= color:
            enemigo= destino.pop()
            self.enviar_a_barra(enemigo) 
            captura= True

        # colocar ficha en destino
        destino.append(ficha)
        return captura

    def validar_movimiento(self, color, hacia):
        #valida el movimiento
        if hacia < 0 or hacia > 23: #primero si esta en el rango
            return False
        destino= self.__contenedor__[hacia]
        if len(destino)>= 2 and destino[0]!= color: #luego si hay 2 o mas fichas enemigas
            return False
        return True

    def enviar_a_barra(self, color):
        #Si cae en una posicion con 1 ficha enemiga o del otro jugador, la manda a la barra
        if not self.__contenedor__[color]:
            return
        ficha= self.__contenedor__[color].pop() #elimina del contenedor
        self.__barra__[ficha].append(ficha) #la agrega a la barra

    def mover_desde_barra(self, color, hacia):
        #Saca ficha de la barra(si el movimiento es válido) y vuelve a estar en juego
        if not self.validar_movimiento(color, hacia):
            return False
        if self.__barra__[color]:
            ficha= self.__barra__[color].pop() #saca la ficha de la barra
            self.__contenedor__[hacia].append(ficha) #la agrega al contenedor
            return True
        return False

    def sacar_ficha(self, color, desde):
        #Cuando todas las fichas están en el ultimo cuadrante del contendor, se pueden sacar
        if self.__contenedor__[desde] and self.__contenedor__[desde][-1] == color:
            ficha= self.__contenedor__[desde].pop() #saca la ficha del contenedor
            self.__afuera__[color].append(ficha) #agregala ficha a fuera
            return True
        return False
  
    def todas_en_ultimo_cuadrante(self,color): # verifica que esten en el ultimmo cuadrante para poder empezar a sacarlas
        if color=="Blanca":
            rango = range(0,6) #casa de las blancas
        else: #ssi color es igual a negras
            rango = range(18,24) #casa de las negras

        for i, punto in enumerate(self.__contenedor__): #recorre las posiciones del contenedor
            for ficha in punto: #recorre las fichas en cada punto
                if ficha == color and i not in rango: #si la ficha es del color y no esta en el rango
                    return False # entonces no todas estan en el ultimo cuadrante
        return True #si recorre todo y no encontro ninguna fuera del rango, todas estan en el ultimo cuadrante

    def mostrar_estado(self):
      #devuelve una representacion en texto del trablero
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

