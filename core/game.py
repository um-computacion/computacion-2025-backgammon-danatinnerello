''' Responsabilidades: controlador principal

-Iniciar tablero,jugadores y dados
-controlar turnos
-verificar ganador 
-interactuar con el CLI o Pygame

'''
from board import Tablero
from dice import Dados


class Juego:
    def __init__(self,jugador1,jugador2,):
        self.__tablero = Tablero()
        self.__jugador1 = jugador1
        self.__jugador2 = jugador2
        self.__dados = Dados()

    def controlar_turnos():
        ...

    def verificar_ganador():
        ...