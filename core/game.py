''' Responsabilidades: controlador principal

-Iniciar tablero,jugadores y dados
-controlar turnos
-verificar ganador 
-interactuar con el CLI o Pygame

'''
from core.board import Tablero
from core.dice import Dados
from core.player import Jugador
from core.excepcions import (
    MovimientoInvalidoError,
    SacarFichaError,
)

class Juego:
    def __init__(self,jugador1:Jugador,jugador2:Jugador,tablero:Tablero = None,dados: Dados =None):
        self.__tablero__ = tablero if tablero else Tablero()
        self.__jugador1__ = jugador1
        self.__jugador2__ = jugador2
        self.__jugadores__= [self.__jugador1__, self.__jugador2__]
        self.__dados__ = dados if dados else Dados()
        self.__turno__ =jugador1
        self.__juego_terminado__ = False

    def mostrar_jugador1(self):
        return self.__jugador1__
    
    def mostrar_jugador2(self):
        return self.__jugador2__

    def mostrar_juego_terminado(self):
        return self.__juego_terminado__
    
    def mostrar_tablero(self):
        return self.__tablero__
    
    def controlar_turnos(self):
        if self.__turno__ == self.__jugador1__: #si tiro el jugador uno, lo cambia al otro
            self.__turno__ = self.__jugador2__
        else:  # y sino al reves
            self.__turno__ = self.__jugador1__

    def mostrar_turno(self):
        return self.__turno__

    def verificar_ganador(self):
        for jugador in self.__jugadores__: #si el jugador primero esta en jugadores
            if jugador.gano(): #segundo llama al metodo gano
                self.__juego_terminado__ = True #si gano cambia el estado del juego
                return jugador
        return None

    def valida_mover_ficha(self,jugador:Jugador,desde,hacia):
        if not self.__tablero__.validar_movimiento(jugador.obtener_color(),desde,hacia, self.__dados__.obtener_tiradas_restantes()):
            raise MovimientoInvalidoError("Movimiento inválido")
        diferencia= abs(hacia - desde)
        if not self.__dados__.usar_tirada(diferencia):
            raise MovimientoInvalidoError("Ese dado no está disponible")
        return self.__tablero__.mover_ficha(jugador.obtener_color(),desde,hacia)

    def valida_sacar_ficha(self, jugador:Jugador, desde):
        if not self.__tablero__.todas_en_ultimo_cuadrante(jugador.obtener_color()):
            raise SacarFichaError("No todas las fichas están en el último cuadrante")
        diferencia= (desde+ 1) if jugador.obtener_color()== "Blanca" else (24- desde)
        if not self.__dados__.usar_tirada(diferencia):
            raise SacarFichaError("Ese dado no sirve para sacar ficha")
        if not self.__tablero__.sacar_ficha(jugador.obtener_color(), desde):
            raise SacarFichaError("No se pudo sacar ficha desde esa posición")
        jugador.sacar_ficha_a_afuera()

    def valida_mover_desde_barra(self,jugador:Jugador,dado):
        if not self.__dados__.usar_tirada(dado):
            raise MovimientoInvalidoError("Ese dado no esta disponible")
        hacia= 24 - dado if jugador.obtener_color()== "Blanca" else dado- 1
        if not self.__tablero__.valida_mover_desde_barra(jugador.obtener_color(),hacia):
            raise MovimientoInvalidoError("Movimiento invalido desde la barra")
        return self.__tablero__.aplicar_movimiento_desde_barra(jugador.obtener_color(),hacia)


    def hay_movimientos_posibles(self, jugador: Jugador):
        tiradas = self.__dados__.obtener_tiradas_restantes()
        color = jugador.obtener_color()

        # Si el jugador tiene fichas en la barra, debe intentar salir primero
        if self.__tablero__.mostrar_barra()[color]:
            for dado in tiradas:
                hacia = 24 - dado if color == "Blanca" else dado - 1
                if self.__tablero__.valida_mover_desde_barra(color, hacia):
                    return True
            return False

        # Si no hay fichas en la barra, revisar todas las posiciones
        for desde in range(24):
            for dado in tiradas:
                hacia = desde - dado if color == "Blanca" else desde + dado
                if 0 <= hacia < 24:
                    if self.__tablero__.validar_movimiento(color, desde, hacia, tiradas):
                        return True
        return False

