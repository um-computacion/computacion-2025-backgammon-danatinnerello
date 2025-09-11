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
    nombre1 = input("Ingrese el nombre del jugador 1 (fichas Blanca): ")
    nombre2 = input("Ingrese el nombre del jugador 2 ( fichas Negra): ")
    jugador1 = Jugador(nombre1, "Blanca")
    jugador2 = Jugador(nombre2, "Negra")
    juego = Juego(jugador1, jugador2)
    dados = Dados()
    while True:
        print("Tablero")
        print(juego.mostrar_tablero().mostrar_estado())    
        try:
            # decir a quien le toca tirar
            print(f"Turno de:{juego.mostrar_turno()} ")
            # tirar dados
            tirada = dados.tirar_dados()
            print(f"Tirada: {tirada}")
            # cambiar posiicon de ficha : bucle de movimiento para el turno
            while dados.quedan_tiradas():
                jugador_actual = juego.mostrar_turno()
                print(f"Tiradas restantes:{dados.obtener_tiradas_restantes()}")
                #mover desde la barra
                try:
                    #si hay fichas en la barra las debe mover primero
                    if juego.mostrar_tablero().mostrar_barra()[jugador_actual.obtener_color()]:
                        dado_a_usar=int(input("Ingresa el valor del dado para mover desde la barra: "))
                        if jugador_actual.obtener_color()=="Blanca":
                            hacia=24-dado_a_usar
                        else:# Negra
                            hacia=dado_a_usar-1
                        if dados.usar_tirada(dado_a_usar) and juego.mostrar_tablero().mover_desde_barra(jugador_actual.obtener_color(), hacia):
                            print(f"ficha movida de la barra a la posiciion {hacia}")
                        else:
                            print("movimiento invalido desde la barra")
                            continue
                    #movimiento normal y para sacarlas a afuera
                    else:
                        desde=int(input("mover desde posicion(0-23): "))
                        hacia = int(input("mover hacia posicion(0-23 o -1 para sacar): "))
                        # validaciones
                        if desde< 0 or desde> 23:
                            raise ValueError("La posicion 'desde' debe estar entre 0 y 23")
                        if hacia!= -1 and (hacia< 0 or hacia> 23):
                            raise ValueError("la posicion 'hacia' debe estar entre 0 y 23")
                        contenedor=juego.mostrar_tablero().mostrar_contenedor()
                        if not contenedor[desde]:
                            raise ValueError(f"no hay fichas en la posicion {desde}")
                        if contenedor[desde][-1] != jugador_actual.obtener_color():
                            raise ValueError("esa ficha no te pertenece")
                        # ejecutar movimiento
                        if hacia == -1:
                            # Sacar ficha 
                            if juego.mostrar_tablero().todas_en_ultimo_cuadrante(jugador_actual.obtener_color()):
                                dado_a_usar = (desde + 1) if jugador_actual.obtener_color() == "Blanca" else(24-desde)
                                if dados.usar_tirada(dado_a_usar) and juego.mostrar_tablero().sacar_ficha(jugador_actual.obtener_color(), desde):
                                    jugador_actual.sacar_ficha_a_afuera()
                                    print(f"ficha sacada desde {desde}")
                                else:
                                    print("No puedes sacar una ficha desde esa posicion con el dado actual")
                            else:
                                print("no puedes sacar fichas. No todas estan en el último cuadrante.")
                      #movimineto normal

                except ValueError as e:
                    print("Error:", e)

        except ValueError as e:
            print("Error:", e)

        break

        # verificar ganador
        # cambio de turno


if __name__ == "__main__":
    main()
