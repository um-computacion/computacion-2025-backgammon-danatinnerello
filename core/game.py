''' Responsabilidades: controlador principal

-Iniciar tablero,jugadores y dados
-controlar turnos
-verificar ganador 
-interactuar con el CLI o Pygame

'''
from board import Tablero
from dice import Dados
from player import Jugador

class Juego:
    def __init__(self,jugador1,jugador2,):
        self.__tablero__ = Tablero()
        self.__jugador1__ = jugador1
        self.__jugador2__ = jugador2
        self.__dados__ = Dados()

    def controlar_turnos(self):
        if self.__turno__ == self.__jugador1__:
            self.__turno__ = self.__jugador2__
        else:
            self.__turno__ = self.__jugador1__

    def verificar_ganador(self):
        for jugador in self.__jugadores__:
            if jugador.gano():
                self.__juego_terminado__ = True
                return jugador
        return None

   


