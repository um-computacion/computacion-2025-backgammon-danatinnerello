"""
events.py
Responsabilidad:
- Manejo de eventos de usuario (mouse y teclado).
- Detecta clicks sobre fichas o triángulos del tablero.
- Detecta teclas para lanzar dados o realizar acciones.
- Traduce la interacción del jugador en órdenes para la lógica del juego (core/).
"""
"""
events.py
Responsabilidad:
- Manejo de eventos de usuario (mouse y teclado).
- Detecta clicks sobre fichas o triángulos del tablero.
- Detecta teclas para lanzar dados o realizar acciones.
- Traduce la interacción del jugador en órdenes para la lógica del juego (core/).
"""

import pygame
from core.excepcions import MovimientoInvalidoError, SacarFichaError

# Función auxiliar para obtener el estado del tablero (Copiada de board_renderer para uso interno)
def estado_desde_board(board):
    estado = {}
    puntos = board.__contenedor__
    for i, pila in enumerate(puntos):
        if not pila:
            continue
        ficha = pila[0]
        # Asumiendo que las fichas tienen un método obtener_color() o son strings que se pueden capitalizar.
        color = ficha.obtener_color().capitalize() if hasattr(ficha, "obtener_color") else str(ficha).capitalize()
        estado[i + 1] = {"color": color, "cantidad": len(pila)}
    return estado

def obtener_color_de_ficha_repr(ficha):
    if ficha is None:
        return None
    if hasattr(ficha, "obtener_color"):
        return ficha.obtener_color().capitalize()
    return str(ficha).capitalize()

def pasar_turno(juego):
    juego.controlar_turnos()
    juego.__dados__.tirar_dados()
    return f"Turno de {juego.mostrar_turno().obtener_nombre()}"


class ManejadorEventos:
    def __init__(self, juego, renderer):
        self.juego = juego
        self.renderer = renderer
        self.punto_origen = None
        self.ficha_barra_seleccionada = False
        self.mensaje = ""
        self.tiempo_mensaje = 0
        self.running = True

    def _actualizar_mensaje(self, mensaje, tiempo=1500): # Aumentado tiempo por defecto
        self.mensaje = mensaje
        self.tiempo_mensaje = tiempo

    def manejar_eventos(self, dt):
        
        # Actualizar temporizador de mensaje
        if self.tiempo_mensaje > 0:
            self.tiempo_mensaje -= dt
            if self.tiempo_mensaje <= 0:
                self.mensaje = ""

        # Lógica de juego fuera de eventos (obligación de reingresar, verificar fin de turno)
        self._verificar_flujo_obligatorio()
        
        # Captura de eventos Pygame
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return

            if self.juego.verificar_ganador():
                continue

            if event.type == pygame.KEYDOWN:
                self._manejar_keydown(event)

            if event.type == pygame.MOUSEBUTTONDOWN:
                self._manejar_mousedown(event)

        # Lógica de fin de turno si no hay movimientos posibles
        self._verificar_final_turno_forzado()

    def _verificar_flujo_obligatorio(self):
        jugador = self.juego.mostrar_turno()
        color = jugador.obtener_color()
        barra = self.juego.mostrar_tablero().mostrar_barra()
        tiradas = self.juego.__dados__.obtener_tiradas_restantes()

        # Si el jugador tiene fichas en la barra y NO puede reingresar con ninguna tirada -> pasar turno
        if barra[color] and tiradas:
            puede_reingresar = False
            for dado in tiradas:
                destino = 24 - dado if color == "Blanca" else dado - 1
                # Usamos una validación simple solo de posición
                if self.juego.mostrar_tablero().valida_mover_desde_barra(color, destino):
                    puede_reingresar = True
                    break
            
            if not puede_reingresar:
                self._actualizar_mensaje("No hay movimientos válidos desde la barra. Se pasa el turno.", 1800) # Tiempo ajustado
                pasar_turno(self.juego)

    def _verificar_final_turno_forzado(self):
        jugador = self.juego.mostrar_turno()
        tiradas = self.juego.__dados__.obtener_tiradas_restantes()
        ganador = self.juego.verificar_ganador()

        if not ganador and tiradas and not self.juego.hay_movimientos_posibles(jugador):
            self._actualizar_mensaje("No hay movimientos posibles. Se pasa el turno.", 1800) # Tiempo ajustado
            pasar_turno(self.juego)
            

    def _manejar_keydown(self, event):
        if event.key == pygame.K_RETURN:
            if not self.juego.__dados__.obtener_tiradas_restantes():
                self.juego.__dados__.tirar_dados()
                self._actualizar_mensaje("Dados tirados", 1500)
            else:
                self._actualizar_mensaje("Ya tiene tiradas disponibles", 1500)

    def _manejar_mousedown(self, event):
        x, y = event.pos
        jugador = self.juego.mostrar_turno()
        color = jugador.obtener_color()
        barra = self.juego.mostrar_tablero().mostrar_barra()

        # CLICK EN BARRA CENTRAL
        centro_x = self.renderer.ancho // 2
        if abs(x - centro_x) < self.renderer.ancho_barra:
            self._manejar_click_barra_central(barra, color)
            return

        # Si hay fichas en barra, bloquear otros movimientos (a menos que ya se haya seleccionado la barra)
        if barra[color] and not self.ficha_barra_seleccionada:
            self._actualizar_mensaje("Debe reingresar ficha(s) de la barra antes de mover otras fichas.", 1500) # Tiempo ajustado
            return

        # CLICK EN BARRA LATERAL (Sacar ficha)
        barra_lateral = self.renderer.obtener_barra_lateral_desde_click((x, y))
        if barra_lateral:
            self._manejar_sacar_ficha(jugador, barra_lateral)
            return

        # CLICK EN TABLERO (Movimiento Normal / Reingreso)
        if y < self.renderer.alto:
            self._manejar_click_tablero(x, y, jugador, color)

    def _manejar_click_barra_central(self, barra, color):
        if barra[color]:
            self.ficha_barra_seleccionada = True
            self._actualizar_mensaje("Ficha en barra seleccionada: elige punto destino para reingresar.", 1500)

    def _manejar_sacar_ficha(self, jugador, barra_lateral):
        if self.punto_origen is None:
            self._actualizar_mensaje("Seleccione la ficha (punto) que desea sacar y luego haga click en la barra lateral.", 1800)
            return

        try:
            # Asumo que valida_sacar_ficha en tu core *valida y ejecuta* y *retorna el dado usado*.
            dado_usado = self.juego.valida_sacar_ficha(jugador, self.punto_origen)
            
            # Usar el dado retornado para el mensaje.
            self._actualizar_mensaje(f"Sacaste una ficha desde {self.punto_origen} usando dado {dado_usado}", 1500) # Tiempo ajustado
            self.punto_origen = None
    
            if not self.juego.__dados__.obtener_tiradas_restantes():
                self._actualizar_mensaje(pasar_turno(self.juego), 1500)

            ganador = self.juego.verificar_ganador()
            if ganador:
                self._actualizar_mensaje(f"¡Ganó {ganador.obtener_nombre()}!", 999999)
        except Exception as e:
            self._actualizar_mensaje(f"No se pudo sacar ficha: {e}", 2000) # Tiempo ajustado
            self.punto_origen = None # Asegúrate de limpiar el origen si falla

    def _manejar_click_tablero(self, x, y, jugador, color):
        
        #Obtener el estado actual del tablero para la detección de clicks en fichas.
        estado = estado_desde_board(self.juego.mostrar_tablero())
        
        #Primero, intentar obtener el punto desde un click EN LA FICHA superior.
        punto = self.renderer.obtener_punto_desde_click_en_ficha((x, y), estado)

        if punto is None:
            # Si no se clicó en una ficha, y ya hay un punto de origen seleccionado (movimiento de destino), 
            #o estamos reingresando, permitimos el click en el punto (triángulo) vacío.
            if self.punto_origen is not None or self.ficha_barra_seleccionada:
                punto = self.renderer.obtener_punto_desde_click((x, y))
            
            # Si no se clica en nada, salir.
            if punto is None:
                return

        # Lógica de manejo de movimiento/reingreso 
        if self.ficha_barra_seleccionada:
            self._manejar_reingreso(punto, jugador, color)
        else:
            self._manejar_movimiento_normal(punto, jugador)
            
    def _manejar_reingreso(self, punto_destino, jugador, color):
        # self.ficha_barra_seleccionada = False  <-- Se comenta para manejar la deselección solo si tiene éxito.

        try:
            tablero_obj = self.juego.mostrar_tablero()
            contenedor = tablero_obj.mostrar_contenedor()
            pila_dest = contenedor[punto_destino - 1]
            
            # Verificar bloqueo por 2+ fichas enemigas
            if pila_dest and obtener_color_de_ficha_repr(pila_dest[0]) != color and len(pila_dest) >= 2:
                raise MovimientoInvalidoError("punto ocupado por 2+ fichas enemigas.")

            # Lógica para encontrar y usar el dado
            dados_validos = self._encontrar_dados_reingreso(punto_destino, color)

            if not dados_validos:
                raise MovimientoInvalidoError("No se puede reingresar en ese punto con las tiradas actuales.")

            # REGLA: Usar el dado MÁS grande que te permite reingresar si hay varios.
            dado_elegido = max(dados_validos)
            
            # Ejecutar el movimiento 
            captura = self.juego.valida_mover_desde_barra(jugador, dado_elegido)
            
            mensaje = f"Reingresaste ficha con dado {dado_elegido}"
            if captura:
                mensaje = f"¡Capturaste ficha al reingresar con dado {dado_elegido}!"
                
            self._actualizar_mensaje(mensaje, 1500) # Tiempo ajustado
            self.ficha_barra_seleccionada = False # Deseleccionar solo si tiene éxito.

            ganador = self.juego.verificar_ganador()
            if ganador:
                self._actualizar_mensaje(f"¡Ganó {ganador.obtener_nombre()}!", 999999)

        except Exception as e:
            self.ficha_barra_seleccionada = True # Mantener la barra seleccionada si falla el reingreso.
            self._actualizar_mensaje(f"No se pudo reingresar: {e}", 2000) # Tiempo ajustado

    def _encontrar_dados_reingreso(self, punto_destino, color):
        tablero_obj = self.juego.mostrar_tablero()
        tiradas = self.juego.__dados__.obtener_tiradas_restantes()
        dados_validos = []

        for dado in tiradas:
            destino_calc = 24 - dado if color == "Blanca" else dado - 1
            if destino_calc == punto_destino - 1 and tablero_obj.valida_mover_desde_barra(color, destino_calc):
                dados_validos.append(dado)
        return dados_validos

    def _manejar_movimiento_normal(self, punto_destino, jugador):
        try:
            if self.punto_origen is None:
                self.punto_origen = punto_destino
                self._actualizar_mensaje(f"Punto {self.punto_origen} seleccionado.", 1000)
            else:
                captura = self.juego.valida_mover_ficha(jugador, self.punto_origen, punto_destino)
                
                mensaje = "Movimiento válido"
                if captura:
                    mensaje = "Capturaste una ficha enemiga"
                    
                self._actualizar_mensaje(mensaje, 1500)
                self.punto_origen = None
                
                ganador = self.juego.verificar_ganador()
                if ganador:
                    self._actualizar_mensaje(f"¡Ganó {ganador.obtener_nombre()}!", 999999)
        except Exception as e:
            self._actualizar_mensaje(f"Movimiento inválido: {e}", 1800) # Tiempo ajustado
            self.punto_origen = None # Limpiar el origen si falla