'''Responsabilidades:

-simula dados
-Administrar tiradas dobles

'''

import random



class Dados:
    def __init__(self):
        self.__dado1__ = 0
        self.__dado2__ = 0
        self.__tiradas_restantes__ = []

    def tirar_dados(self):
        self.__dado1__ = random.randint(1, 6) #numero aleatorio del uno al seis
        self.__dado2__ = random.randint(1, 6) # lo mismo
        if self.__dado1__ == self.__dado2__:
            self.__tiradas_restantes__ = [self.__dado1__] * 4   #duplicamos si los dados son iguales
        else:
            self.__tiradas_restantes__ = [self.__dado1__, self.__dado2__] #sino solo guarda los valores
        return self.__dado1__, self.__dado2__

    def obtener_tiradas_restantes(self):
        return self.__tiradas_restantes__

    def usar_tirada(self, valor): #controla si el valor esta en las tiradas restantes
        if valor in self.__tiradas_restantes__:
            self.__tiradas_restantes__.remove(valor) #elimina el valor usado
            return True
        return False
    
    def quedan_tiradas(self): #verifica si quedan tiradas
        return len(self.__tiradas_restantes__) > 0

    def reiniciar(self): #reinicia las tiradas
        self.__tiradas_restantes__ = []
