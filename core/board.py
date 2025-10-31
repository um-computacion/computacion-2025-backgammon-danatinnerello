from core.excepcions import MovimientoInvalidoError 

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

    # devuelve la lista interna
    def mostrar_contenedor(self):
        return self.__contenedor__

    # metodo separado para imprimir cuando se necesita mostrar por pantalla
    def imprimir_contenedor(self):
        for i in range(24):
            fichas = " , ".join(self.__contenedor__[i]) if self.__contenedor__[i] else "."
            print(f"{i:2}: {fichas}")

    def mostrar_barra(self):
        return self.__barra__

    def mostrar_afuera(self):
        return self.__afuera__
    
    def mover_ficha(self,color,desde,hacia):
        # verifica que la posición esté entre 0 y 23
        if desde < 0 or desde > 23 or hacia < 0 or hacia > 23:
            raise MovimientoInvalidoError("Punto de origen o destino fuera de rango (1-24).")
        # verifica que contenga algo la posición
        if not self.__contenedor__[desde]:
            raise MovimientoInvalidoError(f"No hay fichas en la posición {desde}")
        # verifica que la ficha a mover sea del color correcto
        if self.__contenedor__[desde][-1] != color:
            raise MovimientoInvalidoError("Esa ficha no te pertenece")

        #guarda ficha
        destino= self.__contenedor__[hacia]
        if len(destino) >= 2 and destino[0] != color:
            raise MovimientoInvalidoError("Destino bloqueado por fichas enemigas")
      
        #elimina la ficha
        ficha= self.__contenedor__[desde].pop()
        captura= False

        # si hay exactamente 1 ficha enemiga entonces la captura y la manda a barra
        if len(destino)== 1 and destino[0]!= color:
            self.enviar_a_barra(hacia) 
            captura= True

        # colocar ficha en destino
        destino.append(ficha)
        return captura

    def validar_movimiento(self, color, desde, hacia, tiradas_restantes=None): 
        # Verifica si el movimiento está en el rango
        if hacia < 0 or hacia > 23 or desde < 0 or desde > 23:
            return False
        # Verifica si hay fichas en la posición de origen
        if not self.__contenedor__[desde]:
            return False
        # Verifica si la ficha a mover es del color correcto
        if self.__contenedor__[desde][-1] != color:
            return False
            
        # Verifica la dirección (Blanca de 23->0, Negra de 0->23)
        if color == "Blanca" and hacia >= desde:
            return False
        if color == "Negra" and hacia <= desde:
            return False
            
        # Verifica si el destino está bloqueado por 2 o más fichas enemigas
        destino = self.__contenedor__[hacia]
        if len(destino) >= 2 and destino[0] != color:
            return False

        return True
    
    def enviar_a_barra(self, posicion):
        # Si hay fichas en la posición, saca la última y la agrega a la barra correspondiente
        if self.__contenedor__[posicion]:
            ficha = self.__contenedor__[posicion].pop()
            self.__barra__[ficha].append(ficha)

    def valida_mover_desde_barra(self, color, hacia,tiradas_restantes = None):
        if not self.__barra__[color]:
            return False
        if hacia < 0 or hacia > 23:
            return False
        destino = self.__contenedor__[hacia]
        if len(destino) >= 2 and destino[0] != color:
            return False
    
         # validacion extra si tiradas_restantes se pasa
        if tiradas_restantes is not None:
            diferencia = hacia if color == "Negra" else 24 - hacia
            if diferencia not in tiradas_restantes:
                return False
        return True

    def aplicar_movimiento_desde_barra(self, color, hacia):
        # Sacar la ficha que va a reingresar de la barra
        ficha_reingreso = self.__barra__[color].pop()
        
        destino = self.__contenedor__[hacia]
        captura = False
        
        # Verificar y ejecutar la captura (Regla de Backgammon)
        color_enemigo = "Negra" if color == "Blanca" else "Blanca" 
        
        # Si hay exactamente 1 ficha enemiga en el destino (blot)
        if len(destino) == 1 and destino[0] == color_enemigo:
            self.enviar_a_barra(hacia) # <-- ¡La clave! Capturar y limpiar el punto
            captura = True

        # Colocar la ficha de reingreso en el destino
        destino.append(ficha_reingreso) 
        
        return captura # Devuelve si hubo captura para que game.py lo maneje
    
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

