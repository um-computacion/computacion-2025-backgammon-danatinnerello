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
def main(interactive: bool = False):
    """
    interactive: bool
        - False(default):se ejecuta en modo pruebas compatible con los tests automatizados
        - True:habilita un menu de control con opciones para rendirse o salir
          del juego,pensado para uso interactivo en la terminal
    """
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
            # opciones de control
            # menú solo si interactive=True
            if interactive:
                '''
                Si interactive=True, se muestra un menu de control al inicio de cada turno
                Si la opcion es invalida, se vuelve a pedir'''
                print("Opciones: ")
                print("1- Jugar turno")
                print("2- Rendirse")
                print("3- Salir del juego")
                opcion= input("Seleccione una opcion: ")
                if opcion== "2":
                    print(f"{juego.mostrar_turno().obtener_nombre()} se ha rendido")
                    break
                elif opcion== "3":
                    print("Juego finalizado por el usuario")
                    break
                elif opcion!= "1":
                    print("Opcion invalida")
                    continue

            # inicio del turno
            # decir a quien le toca tirar
            print(f"Turno de:{juego.mostrar_turno()} ")
            # tirar dados
            tirada = dados.tirar_dados()
            if len(tirada)== 4:
                print(f"Tirada doble: {tirada}")
            else:
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
                            print(f"ficha movida de la barra a la posiciion {hacia+1}")
                        else:
                            print("movimiento invalido desde la barra")
                            continue
                    #movimiento normal y para sacarlas a afuera
                    else:
                        desde=int(input("mover desde posicion(1 - 24): ")) -1
                        hacia = int(input("mover hacia posicion(1-24 o 0 para sacar): "))
                        # validaciones
                        if desde< 0 or desde> 23:
                            raise ValueError("La posicion 'desde' debe estar entre 1 y 24")
                        if hacia!= -1 and (hacia< 0 or hacia> 23):
                            raise ValueError("la posicion 'hacia' debe estar entre 1 y 24")
                        contenedor=juego.mostrar_tablero().mostrar_contenedor()
                        if not contenedor[desde]:
                            raise ValueError(f"no hay fichas en la posicion {desde+1}")
                        if contenedor[desde][-1] != jugador_actual.obtener_color():
                            raise ValueError("esa ficha no te pertenece")
                        # ejecutar movimiento
                        if hacia== -1:
                            # Sacar ficha 
                            if juego.mostrar_tablero().todas_en_ultimo_cuadrante(jugador_actual.obtener_color()):
                                dado_a_usar= (desde + 1) if jugador_actual.obtener_color() == "Blanca" else(24-desde)
                                if dados.usar_tirada(dado_a_usar) and juego.mostrar_tablero().sacar_ficha(jugador_actual.obtener_color(), desde):
                                    jugador_actual.sacar_ficha_a_afuera()
                                    print(f"ficha sacada desde {desde+1}")
                                else:
                                    print("No puedes sacar una ficha desde esa posicion con el dado actual")
                            else:
                                print("no puedes sacar fichas. No todas estan en el ultimo cuadrante.")
                        else:
                            # Movimiento normal
                            dado_a_usar=abs(hacia - desde)
                            if (dados.usar_tirada(dado_a_usar) and juego.mostrar_tablero().validar_movimiento(jugador_actual.obtener_color(),hacia)):
                                captura= juego.mostrar_tablero().mover_ficha(jugador_actual.obtener_color(),desde,hacia)
                                if captura:
                                    print(f"capturaste una ficha enemiga en la posicion {hacia+1}")
                                print(f"ficha movida de {desde+1} a {hacia+1}")
                            else:
                                print("movimiento invalido")

                except ValueError as e:
                    print("Error:",e)

        except ValueError as e:
            print("Error:",e)

        print(juego.mostrar_tablero().mostrar_estado())

        # verificar ganador
        ganador=juego.verificar_ganador()
        if ganador:
            print(f"ganoo {ganador.obtener_nombre()}.Color {ganador.obtener_color()} ")
            break

        juego.controlar_turnos()  # cambio de turno
      


if __name__ == "__main__":
    #ejecutar en modo interactivo cuando se corre como script
    main(interactive = True)
