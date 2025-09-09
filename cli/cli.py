from core.game import Juego
from core.player import Jugador
from core.board import Tablero
from core.dice import Dados

'''
menu:
     inicializar juego
     inicilizar jugadores
     inicializar tablero
     inicializar dados
gestionar turnos
verificar tiradas
verificar posiciones 
verificar ganador 

'''
def main():
    print("Bienvenidos al juego Backgammon")
    print("Inicio del juego")
    nombre1 = input("Ingrese el nombre del jugador 1 (fichas blancas): ")
    nombre2 = input("Ingrese el nombre del jugador 2 ( fichas negras): ")
    jugador1 = Jugador(nombre1, "Blancas")
    jugador2 = Jugador(nombre2, "Negras")
    juego = Juego(jugador1, jugador2)
    dados = Dados()
    while True:
        print("Tablero")
        print(juego.__tablero__.mostrar_contenedor())
        try:
            # decir a quien le toca tirar
            print(f"Turno de:{juego.mostrar_turno()} ")
            # tirar dados
            # cambiar posiicon de ficha
            # validar esa posicion
            # guardar ficha en la nueva posicion 
            # verificar si hay ganador
            # cambiar turno
            # verificar si hay fichas en barra

            break
        except Exception as e:
            print(e)


if __name__ == "__main__":
    main()