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
        print("Barra:", juego.mostrar_tablero().mostrar_barra())
        print("Fichas afuera:", juego.mostrar_tablero().mostrar_afuera())     
        try:
            # decir a quien le toca tirar
            print(f"Turno de:{juego.mostrar_turno()} ")
            # tirar dados
            tirada = dados.tirar_dados()
            print(f"Tirada: {tirada}")
            # cambiar posiicon de ficha : bucle de movimiento para el turno
            while dados.quedan_tiradas():
                jugador_actual = juego.mostrar_turno()
                print(f"Tiradas restantes: {dados.obtener_tiradas_restantes()}")
            #mover desde la barra
            #comprueba si la lista de fichas de la barra del jugador actual no esta vacia
                if juego.mostrar_tablero().mostrar_barra()[jugador_actual.obtener_color()]:
                    print("Tienes fichas en la barra.Debes mover una de ellas primero")
                    try:
                        dado_a_usar = int(input("Ingresa el valor del dado para mover desde la barra: "))
                        if dados.usar_tirada(dado_a_usar):
                            if jugador_actual.obtener_color()=="negras":
                                hacia=24 - dado_a_usar
                            else:
                                hacia=dado_a_usar - 1
                        
                            if juego.mostrar_tablero().mover_desde_barra(jugador_actual.obtener_color(), hacia):
                                print(f"Ficha movida de la barra a la posición {hacia}")
                            else:
                                print("MOvimiento invalido desde la barra")
                                dados.obtener_tiradas_restantes().append(dado_a_usar)
                        else:
                            print("Dado no disponible.Intentalo de nuevo")
                    except ValueError:
                        print("Entrada invalida.Porfavor, ingresa un numero")
                    break #despues cambiar
               

      
        except Exception as e:
            print(e)

            break 



if __name__ == "__main__":
    main()