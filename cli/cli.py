from core.game import Juego
from core.player import Jugador
from core.board import Tablero
from core.dice import Dados
from core.excepcions import (
    EntradaInvalidaError,
    MovimientoInvalidoError,
    SacarFichaError,
    RendicionError,
    JuegoTerminadoError,
)


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


def pedir_int(mensaje: str) -> int:
    try:
        return int(input(mensaje))
    except ValueError:
        raise EntradaInvalidaError("Debe ingresar un numero entero")

def main():
    print("Bienvenidos al juego Backgammon")
    nombre1= input("Jugador 1 (Blanca): ")
    nombre2= input("Jugador 2 (Negra): ")
    jugador1= Jugador(nombre1, "Blanca")
    jugador2= Jugador(nombre2, "Negra")
    juego= Juego(jugador1, jugador2)
    while not juego.mostrar_juego_terminado():
        jugador = juego.mostrar_turno()
        print(f"Turno de {jugador.obtener_nombre()} ({jugador.obtener_color()})")
        tirada = juego.__dados__.tirar_dados()
        print("Tirada:", tirada)
        while juego.__dados__.quedan_tiradas():
            try:
                print("1:Mover ficha")
                print("2:Rendirse")
                print("3:Finalizar juego")
                opcion= pedir_int("Opcion: ")

                if opcion== 1:
                    origen= pedir_int("Mover ficha desde: ")
                    destino= pedir_int("Hasta: ")

                    if origen== 0:  # desde barra
                        juego.valida_mover_desde_barra(jugador,destino)
                        print(f"Ficha movida desde la barra a {destino}")
                    elif destino== -1:  # sacar ficha
                        juego.valida_sacar_ficha(jugador,origen)
                        print(f"Ficha sacada desde {origen}")
                    else:  # movimiento normal
                        captura = juego.valida_mover_ficha(jugador, origen, destino)
                        if captura:
                            print("Capturaste una ficha enemiga")
                        else:
                            print(f"Ficha movida de {origen} a {destino}")

                elif opcion== 2:
                    raise RendicionError
                elif opcion== 3:
                    raise JuegoTerminadoError
                else:
                    raise EntradaInvalidaError("Opcion no valida")
                
                #verifica ganador
                ganador= juego.verificar_ganador()
                if ganador:
                    print(f"Ganoo {ganador.obtener_nombre()} ({ganador.obtener_color()})")
                    return
                
                juego.controlar_turnos()  #cambia turno

            except (EntradaInvalidaError, MovimientoInvalidoError, SacarFichaError) as e:
                print(f"Error: {e}")
            except RendicionError:
                print(f"{jugador.obtener_nombre()} se ha rendido")
                return
            except JuegoTerminadoError:
                print("Juego finalizado por el usuario")
                return
        
if __name__ == "__main__":
    main()