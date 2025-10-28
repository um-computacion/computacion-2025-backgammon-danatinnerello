"""
main.py
Responsabilidad:
- Punto de entrada del juego con Pygame.
- Inicializa la ventana y configura el bucle principal del juego.
- Se encarga de llamar a los métodos de dibujo (board_renderer).
- Captura eventos (mouse, teclado) usando events.py.
- Mantiene el loop de juego (update → draw → events).
"""

import pygame
from pygame_ui.board_renderer import TableroGrafico, estado_desde_board
from core.game import Juego, Jugador

pygame.init()
ANCHO_PANTALLA = 1000
ALTO_TABLERO = 500
ALTO_PANEL = 100
ALTO_PANTALLA = ALTO_TABLERO + ALTO_PANEL
FUENTE = pygame.font.Font(None, 28)
COLOR_FONDO = (222, 184, 135)
COLOR_PANEL = (160, 110, 60)
COLOR_TEXTO = (255, 255, 255)


def pantalla_pedir_nombres():
    pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
    pygame.display.set_caption("Backgammon - Ingresar nombres")

    input_boxes = [pygame.Rect(400, 250, 400, 50), pygame.Rect(400, 350, 400, 50)]
    nombres = ["", ""]
    colores = [(255, 255, 255)] * 2
    activo = [False, False]
    texto_instruccion = FUENTE.render(
        "Ingrese los nombres y presione ENTER para comenzar", True, (0, 0, 0)
    )
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None, None
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i, box in enumerate(input_boxes):
                    activo[i] = box.collidepoint(event.pos)
                    colores[i] = (200, 200, 255) if activo[i] else (255, 255, 255)
            if event.type == pygame.KEYDOWN:
                for i in range(2):
                    if activo[i]:
                        if event.key == pygame.K_RETURN and all(nombres):
                            return nombres[0], nombres[1]
                        elif event.key == pygame.K_BACKSPACE:
                            nombres[i] = nombres[i][:-1]
                        else:
                            nombres[i] += event.unicode

        pantalla.fill(COLOR_FONDO)
        pantalla.blit(texto_instruccion, (280, 150))
        for i, box in enumerate(input_boxes):
            texto_label = FUENTE.render(
                f"Jugador {i+1} ({'Blancas' if i == 0 else 'Negras'}):", True, (0, 0, 0)
            )
            pantalla.blit(texto_label, (200, 260 + i * 100))
            pygame.draw.rect(pantalla, colores[i], box, 2)
            texto_nombre = FUENTE.render(nombres[i], True, (0, 0, 0))
            pantalla.blit(texto_nombre, (box.x + 10, box.y + 10))
        pygame.display.flip()
        clock.tick(30)


def dibujar_panel_inferior(pantalla, juego, mensaje=""):
    rect_panel = pygame.Rect(0, ALTO_TABLERO, ANCHO_PANTALLA, ALTO_PANEL)
    pygame.draw.rect(pantalla, COLOR_PANEL, rect_panel)
    pygame.draw.rect(pantalla, (80, 50, 30), rect_panel, 3)

    jugador = juego.mostrar_turno()
    color = jugador.obtener_color()
    turno_texto = FUENTE.render(
        f"Turno: {jugador.obtener_nombre()} ({color})", True, COLOR_TEXTO
    )
    dados_texto = FUENTE.render(
        f"Dados: {juego.__dados__.obtener_tiradas_restantes()}", True, COLOR_TEXTO
    )
    pantalla.blit(turno_texto, (30, ALTO_TABLERO + 20))
    pantalla.blit(dados_texto, (400, ALTO_TABLERO + 20))

    barra = juego.mostrar_tablero().mostrar_barra()
    afuera = juego.mostrar_tablero().mostrar_afuera()

    texto_barra = FUENTE.render(
        f"Barra → Blancas: {len(barra['Blanca'])} | Negras: {len(barra['Negra'])}",
        True, COLOR_TEXTO
    )
    texto_afuera = FUENTE.render(
        f"Afuera → Blancas: {len(afuera['Blanca'])} | Negras: {len(afuera['Negra'])}",
        True, COLOR_TEXTO
    )
    pantalla.blit(texto_barra, (600, ALTO_TABLERO + 20))
    pantalla.blit(texto_afuera, (600, ALTO_TABLERO + 50))

    if mensaje:
        mensaje_texto = FUENTE.render(mensaje, True, (255, 255, 0))
        pantalla.blit(mensaje_texto, (30, ALTO_TABLERO + 60))


def pasar_turno(juego):
    juego.controlar_turnos()
    juego.__dados__.tirar_dados()
    return f"Turno de {juego.mostrar_turno().obtener_nombre()}"



def obtener_color_de_ficha_repr(ficha):
    if ficha is None:
        return None
    if hasattr(ficha, "obtener_color"):
        return ficha.obtener_color().capitalize()
    return str(ficha).capitalize()


def crear_representacion_ficha(color_str, ejemplo_contenedor):
    if ejemplo_contenedor:
        muestra = ejemplo_contenedor[0]
        if hasattr(muestra, "obtener_color"):
            return color_str
        else:
            return color_str
    return color_str


def main():
    nombre1, nombre2 = pantalla_pedir_nombres()
    if not nombre1 or not nombre2:
        return

    jugador1 = Jugador(nombre1, "Blanca")
    jugador2 = Jugador(nombre2, "Negra")
    juego = Juego(jugador1, jugador2)
    juego.__dados__.tirar_dados()

    pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
    pygame.display.set_caption("Backgammon - Pygame")

    renderer = TableroGrafico(pantalla, alto_tablero=ALTO_TABLERO)
    reloj = pygame.time.Clock()
    punto_origen = None
    mensaje = ""
    tiempo_mensaje = 0
    esperar_paso_turno = 0
    ganador = None
    ficha_barra_seleccionada = False

    running = True
    while running:
        dt = reloj.tick(30)

        if tiempo_mensaje > 0:
            tiempo_mensaje -= dt
            if tiempo_mensaje <= 0:
                mensaje = ""

        jugador = juego.mostrar_turno()
        color = jugador.obtener_color()
        barra = juego.mostrar_tablero().mostrar_barra()
        tiradas = juego.__dados__.obtener_tiradas_restantes()

        #Si hay fichas en barra, verificar si existe al menos una tirada que permita reingresar
        if barra[color] and tiradas:
            puede_reingresar = False
            for dado in tiradas:
                destino = 24 - dado if color == "Blanca" else dado - 1
                if juego.mostrar_tablero().valida_mover_desde_barra(color, destino):
                    puede_reingresar = True
                    break
            if not puede_reingresar:
                mensaje = "No hay movimientos válidos desde la barra. Se pasa el turno."
                tiempo_mensaje = 1800
                pasar_turno(juego)
                continue

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN and not ganador:
                if not juego.__dados__.obtener_tiradas_restantes():
                    juego.__dados__.tirar_dados()
                    mensaje = "Dados tirados"
                    tiempo_mensaje = 1500
                else:
                    mensaje = "Ya tiene tiradas disponibles"
                    tiempo_mensaje = 1500

            if event.type == pygame.MOUSEBUTTONDOWN and esperar_paso_turno == 0 and not ganador:
                x, y = event.pos
                jugador = juego.mostrar_turno()
                color = jugador.obtener_color()
                barra = juego.mostrar_tablero().mostrar_barra()

                #CLICK EN BARRA CENTRAL
                centro_x = renderer.ancho // 2
                if abs(x - centro_x) < renderer.ancho_barra:
                    if barra[color]:
                        ficha_barra_seleccionada = True
                        mensaje = "Ficha en barra seleccionada: elige punto destino para reingresar."
                        tiempo_mensaje = 2000
                        continue

                #Si hay fichas en la barra del jugador, bloquear otros movimientos
                if barra[color] and not ficha_barra_seleccionada:
                    mensaje = "Debe reingresar ficha(s) de la barra antes de mover otras fichas."
                    tiempo_mensaje = 1800
                    continue

                #Si se está reingresando desde la barra
                if ficha_barra_seleccionada:
                    ficha_barra_seleccionada = False
                    punto_destino = renderer.obtener_punto_desde_click((x, y))
                    if punto_destino is None:
                        mensaje = "Destino inválido para reingresar ficha."
                        tiempo_mensaje = 1500
                        continue

                    tablero_obj = juego.mostrar_tablero()
                    contenedor = tablero_obj.mostrar_contenedor()
                    pila_dest = contenedor[punto_destino - 1]  # lista de fichas en destino
                    # Verificar bloqueo por 2+ fichas enemigas
                    if pila_dest and obtener_color_de_ficha_repr(pila_dest[0]) != color and len(pila_dest) >= 2:
                        mensaje = "No se puede reingresar: punto ocupado por 2+ fichas enemigas."
                        tiempo_mensaje = 2000
                        continue

                    # Buscar los dados que permitirían ese destino (sin consumirlos aún)
                    tiradas = juego.__dados__.obtener_tiradas_restantes()
                    dados_validos = []
                    for dado in tiradas:
                        destino_calc = 24 - dado if color == "Blanca" else dado - 1
                        if destino_calc == punto_destino - 1 and tablero_obj.valida_mover_desde_barra(color, destino_calc):
                            dados_validos.append(dado)

                    if not dados_validos:
                        mensaje = "No se puede reingresar en ese punto con las tiradas actuales."
                        tiempo_mensaje = 2000
                        continue

                    # Elegimos un dado (preferimos el menor — favorece exactos)
                    dado_elegido = min(dados_validos)

                    # Antes de aplicar movimiento, registramos si en destino había exactamente 1 ficha enemiga
                    habia_una_enemiga = False
                    tipo_enemiga_repr = None
                    if pila_dest and obtener_color_de_ficha_repr(pila_dest[0]) != color and len(pila_dest) == 1:
                        habia_una_enemiga = True
                        tipo_enemiga_repr = pila_dest[0]

                    try:
                        # Aplicamos movimiento por el core — este método debe consumir la tirada y actualizar tablero/barra
                        juego.valida_mover_desde_barra(jugador, dado_elegido)
                        mensaje = f"Reingresaste ficha con dado {dado_elegido}"
                        tiempo_mensaje = 1500

                        contenedor_post = tablero_obj.mostrar_contenedor()
                        pila_post = contenedor_post[punto_destino - 1]
                        
                        if habia_una_enemiga:
                            
                            if pila_post and obtener_color_de_ficha_repr(pila_post[0]) != color:
                                # extraemos UNA ficha enemiga de la pila_post (buscamos primer elemento con color enemiga)
                                idx = None
                                for i, f in enumerate(pila_post):
                                    if obtener_color_de_ficha_repr(f) != color:
                                        idx = i
                                        break
                                if idx is not None:
                                    pieza_enemiga = pila_post.pop(idx)
                                    # colocar esa pieza en la barra correspondiente
                                    barra_post = tablero_obj.mostrar_barra()
                                    enemy_color = obtener_color_de_ficha_repr(pieza_enemiga)
                                    # si la estructura de barra es lista por color
                                    if enemy_color in barra_post:
                                        barra_post[enemy_color].append(pieza_enemiga)
                                    else:
                                    
                                        barra_post[enemy_color.capitalize()] = [pieza_enemiga]
                                    # ahora aseguramos que en el punto exista la ficha del jugador
                                    # si no está (por ejemplo core dejó sólo la enemiga y no puso player's),
                                    # insertamos una representación simple
                                    if not any(obtener_color_de_ficha_repr(x) == color for x in pila_post):
                                        repr_ficha = crear_representacion_ficha(color, pila_post)
                                        pila_post.insert(0, repr_ficha)
          

                        ganador = juego.verificar_ganador()
                        if ganador:
                            mensaje = f"¡Ganó {ganador.obtener_nombre()}!"
                            tiempo_mensaje = 999999

                    except Exception as e:
                        mensaje = f"No se pudo reingresar: {e}"
                        tiempo_mensaje = 2000

                    continue  # pasamos al siguiente evento

                #CLICK EN BARRA LATERAL
                barra_lateral = renderer.obtener_barra_lateral_desde_click((x, y))
                if barra_lateral:
                    if punto_origen is None:
                        mensaje = "Seleccione la ficha (punto) que desea sacar y luego haga click en la barra lateral."
                        tiempo_mensaje = 2200
                        continue
                    try:
                        juego.valida_sacar_ficha(jugador, punto_origen)
                        mensaje = f"Sacaste una ficha desde {punto_origen}"
                        tiempo_mensaje = 1500
                        punto_origen = None
                        ganador = juego.verificar_ganador()
                        if ganador:
                            mensaje = f"¡Ganó {ganador.obtener_nombre()}!"
                            tiempo_mensaje = 999999
                    except Exception as e:
                        mensaje = f"No se pudo sacar ficha: {e}"
                        tiempo_mensaje = 2200
                        punto_origen = None
                    continue

                #movimiento normal
                if y < ALTO_TABLERO:
                    punto = renderer.obtener_punto_desde_click((x, y))
                    if punto is not None:
                        try:
                            # seleccionar origen o intentar mover
                            if punto_origen is None:
                                punto_origen = punto
                                mensaje = f"Punto {punto_origen} seleccionado."
                                tiempo_mensaje = 1000
                            else:
                                punto_destino = punto
                                captura = juego.valida_mover_ficha(jugador, punto_origen, punto_destino)
                                if captura:
                                    mensaje = "Capturaste una ficha enemiga"
                                else:
                                    mensaje = "Movimiento válido"
                                punto_origen = None
                                tiempo_mensaje = 1500

                                ganador = juego.verificar_ganador()
                                if ganador:
                                    mensaje = f"¡Ganó {ganador.obtener_nombre()}!"
                                    tiempo_mensaje = 999999
                        except Exception as e:
                            mensaje = f"Movimiento inválido: {e}"
                            tiempo_mensaje = 2000
                            punto_origen = None

        #Si no hay movimientos posibles, pasar turno automáticamente
        if not ganador and tiradas and not juego.hay_movimientos_posibles(juego.mostrar_turno()):
            mensaje = "No hay movimientos posibles. Se pasa el turno."
            tiempo_mensaje = 2000
            pasar_turno(juego)
            continue

        dibujar_todo(pantalla, renderer, juego, mensaje)
        pygame.display.flip()

        # ganador
        if ganador:
            pantalla.fill((0, 0, 0))
            texto = FUENTE.render(
                f"¡Ganó {ganador.obtener_nombre()} ({ganador.obtener_color()})!",
                True,
                (255, 215, 0),
            )
            pantalla.blit(
                texto,
                (
                    ANCHO_PANTALLA // 2 - texto.get_width() // 2,
                    ALTO_TABLERO // 2 - 20,
                ),
            )
            pygame.display.flip()

    pygame.quit()


def dibujar_todo(pantalla, renderer, juego, mensaje=""):
    pantalla.fill(COLOR_FONDO)
    renderer.dibujar_tablero()
    estado = estado_desde_board(juego.mostrar_tablero())
    renderer.dibujar_fichas(estado)
    renderer.dibujar_barra(juego.mostrar_tablero())
    renderer.dibujar_barra_lateral(juego.mostrar_tablero())
    dibujar_panel_inferior(pantalla, juego, mensaje)


if __name__ == "__main__":
    main()


#me falta:
# arreglar que muestre bien las fichas y tirada de dados cuando ingresan a la barra lateral
#despues ver si me falta algo comparado con el cli
#añadir validaciones
#ver si tengo que hacer test
#completar documentacionn
#separra los events
#pulir detalles



