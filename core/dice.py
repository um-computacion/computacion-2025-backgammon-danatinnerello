'''Responsabilidades:

-simula dados
-Administrar tiradas dobles

'''

import random



class Dados:
    def __init__(self):
        self.__dado1 = 0
        self.__dado2 = 0
        self.__tiradas_restantes = []

    def tirar_dados(self):
        self.__dado1 = random.randint(1, 6)
        self.__dado2 = random.randint(1, 6)
        if self.__dado1 == self.__dado2:
            self.__tiradas_restantes = [self.__dado1] * 4   #duplicamos si los dados son iguales
        else:
            self.__tiradas_restantes = [self.__dado1, self.__dado2] #sino solo guarda los valores
        return self.__dado1, self.__dado2

    def obtener_tiradas_restantes(self):
        return self.__tiradas_restantes

    def usar_tirada(self, valor): #controla si el valor esta en las tiradas restantes
        if valor in self.__tiradas_restantes:
            self.__tiradas_restantes.remove(valor)
            return True
        return False