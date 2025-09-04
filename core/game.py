''' Responsabilidades: controlador principal

-Iniciar tablero,jugadores y dados
-controlar turnos
-verificar ganador 
-interactuar con el CLI o Pygame

'''
from core.board import Tablero
from core.dice import Dados
from core.player import Jugador

class Juego:
    def __init__(self,jugador1,jugador2,):
        self.__tablero__ = Tablero()
        self.__jugador1__ = Jugador(jugador1,"blanco")
        self.__jugador2__ = Jugador(jugador2,"negro")
        self.__jugadores__= [self.__jugador1__, self.__jugador2__]
        self.__dados__ = Dados()
        self.__turno__ = self.__jugador1__
        self.__juego_terminado__ = False

    def mostrar_jugador1(self):
        return self.__jugador1__
    
    def mostrar_jugador2(self):
        return self.__jugador2__

    def mostrar_juego_terminado(self):
        return self.__juego_terminado__
    
    def controlar_turnos(self):
        if self.__turno__ == self.__jugador1__: #si tiro el jugador uno, lo cambia al otro
            self.__turno__ = self.__jugador2__
        else:  # y sino al reves
            self.__turno__ = self.__jugador1__

    def verificar_ganador(self):
        for jugador in self.__jugadores__: #si el jugador primero esta en jugadores
            if jugador.gano(): #segundo llama al metodo gano
                self.__juego_terminado__ = True #si gano cambia el estado del juego
                return jugador
        return None

    

