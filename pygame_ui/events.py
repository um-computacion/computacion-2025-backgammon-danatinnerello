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


class ManejadorEventos:
    """Manejador central de eventos para la interfaz Pygame.

    Este objeto traduce eventos de Pygame (mouse/teclado) a llamadas a la lógica
    central del juego (core.game.Juego). Mantiene mensajes UI temporales, estado
    de selección de origen y controla el flujo de turno cuando corresponda.

    Atributos principales:
    - juego: instancia de core.game.Juego
    - renderer: instancia de TableroGrafico (para mapear clicks)
    - mensaje_ui / tiempo_mensaje: mensajería temporal para mostrar al usuario
    - punto_origen: punto seleccionado por el jugador (None si no hay selección)
    - ganador / tiempo_fin_juego: control del fin del juego
    """

    def __init__(self, juego, renderer):
        self.juego = juego
        self.renderer = renderer
        self.mensaje_ui = ""
        self.tiempo_mensaje = 0
        self.punto_origen = None
        self.running = True
        self.ganador = None
        self.tiempo_fin_juego = 0
        self.duracion_mensaje_final = 5000  # 5 segundos

    def _actualizar_mensaje(self, mensaje, duracion_ms):
        """Actualiza el mensaje visible en la UI durante duracion_ms milisegundos."""
        self.mensaje_ui = mensaje
        self.tiempo_mensaje = duracion_ms

    def manejar_eventos(self, dt):
        """Procesa la cola de eventos de Pygame.

        Args:
            dt (int): delta-time en milisegundos desde la última frame.

        Comportamiento:
        - Maneja cierre de ventana.
        - Detecta clicks y teclas y dirige a submétodos:
          - reingreso desde barra (prioridad)
          - sacar ficha (si todas en la casa)
          - movimiento normal / selección de origen
        - Maneja tecla ESPACIO para forzar fin de turno cuando no hay movimientos.
        """

        # Manejo del temporizador de fin de juego (para cerrar la ventana)
        if self.ganador is not None:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            return

        self.tiempo_mensaje = max(0, self.tiempo_mensaje - dt)

        jugador = self.juego.mostrar_turno()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                punto_click = self.renderer.obtener_punto_desde_click(pos)
                barra_click = self.renderer.obtener_barra_lateral_desde_click(pos)

                color_jugador = jugador.obtener_color()
                ficha_en_barra = self.juego.mostrar_tablero().mostrar_barra()[
                    color_jugador
                ]
                todas_en_casa = self.juego.mostrar_tablero().todas_en_ultimo_cuadrante(
                    color_jugador
                )

                # PRIORIDAD 1: REINGRESO DESDE BARRA
                if ficha_en_barra:
                    if punto_click is not None:
                        self._manejar_reingreso(punto_click, jugador, color_jugador)
                    else:
                        self.punto_origen = None
                        self._actualizar_mensaje(
                            "Ficha en barra. Debe reingresar. Click en el punto destino.",
                            1500,
                        )

                # PRIORIDAD 2: SACAR FICHA (SI TODAS ESTÁN EN CASA)
                elif todas_en_casa and barra_click is not None:
                    if self.punto_origen is not None:
                        self._manejar_sacar_ficha(self.punto_origen, jugador)
                    else:
                        self._actualizar_mensaje(
                            "Selecciona una ficha para sacarla o un movimiento normal.",
                            1500,
                        )

                # PRIORIDAD 3: MOVIMIENTO NORMAL O SELECCIÓN DE ORIGEN
                elif punto_click is not None:
                    self._manejar_movimiento_normal(punto_click, jugador)

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self._verificar_final_turno_forzado(jugador)

    def _verificar_final_turno_forzado(self, jugador):
        """Forzar cierre del turno si no hay movimientos posibles.

        Si el jugador tiene tiradas pero no puede mover con ellas, cambia el turno
        y reinicia los dados; también muestra mensajes apropiados en la UI.
        """
        if self.juego.__dados__.obtener_tiradas_restantes():
            if not self.juego.hay_movimientos_posibles(jugador):
                self.juego.controlar_turnos()
                self.juego.__dados__.reiniciar()  # Limpia los dados restantes

                ganador = self.juego.verificar_ganador()
                if ganador:
                    self.ganador = ganador
                    self._actualizar_mensaje(
                        f"¡Ganó {ganador.obtener_nombre()}!",
                        self.duracion_mensaje_final,
                    )
                    self.tiempo_fin_juego = pygame.time.get_ticks()
                else:
                    self._actualizar_mensaje(
                        "No hay movimientos posibles. Se pasa el turno.", 1800
                    )
            else:
                self._actualizar_mensaje("Aún tienes movimientos posibles.", 1500)
        else:
            self._actualizar_mensaje(
                "Ya no quedan tiradas disponibles. El turno terminó.", 1500
            )

    def _manejar_sacar_ficha(self, punto_origen, jugador):
        """Intentar sacar (bear off) una ficha desde punto_origen para 'jugador'.

        Captura excepciones provenientes del core y muestra mensajes en la UI.
        Actualiza el estado interno (punto_origen) y puede declarar ganador.
        """
        try:
            self.juego.valida_sacar_ficha(jugador, punto_origen)
            self.punto_origen = None

            ganador = self.juego.verificar_ganador()
            if ganador:
                self.ganador = ganador
                self._actualizar_mensaje(
                    f"¡Ganó {ganador.obtener_nombre()}!", self.duracion_mensaje_final
                )
                self.tiempo_fin_juego = (
                    pygame.time.get_ticks()
                )  # Guardar tiempo para el cierre

            elif not self.juego.__dados__.obtener_tiradas_restantes():
                self._actualizar_mensaje(
                    f"Turno de {self.juego.mostrar_turno().obtener_nombre()} ({jugador.obtener_color()})",
                    1500,
                )
            else:
                self._actualizar_mensaje(f"Ficha sacada desde {punto_origen}.", 1500)

        except Exception as e:
            self._actualizar_mensaje(f"Error al sacar ficha: {e}", 1800)
            self.punto_origen = None

    def _manejar_reingreso(self, punto_destino, jugador, color):
        """Gestiona el reingreso de fichas desde la barra al punto_destino.

        Lógica:
        - Busca un dado válido entre las tiradas restantes que corresponda al punto.
        - Llama a juego.valida_mover_desde_barra con el dado elegido.
        - Maneja reversiones, cambio de turno y mensajes UI.

        Args:
            punto_destino (int): punto al que el jugador desea reingresar (1-24).
            jugador: instancia de Jugador que intenta reingresar.
            color (str): color del jugador ("Blanca" / "Negra").
        """
        try:
            dados_restantes = self.juego.__dados__.obtener_tiradas_restantes()

            if not dados_restantes:
                raise MovimientoInvalidoError(
                    "No tienes dados disponibles para reingresar."
                )

            dado_elegido = None
            # Lógica para encontrar el dado correcto
            for dado in sorted(dados_restantes, reverse=True):
                destino_calc = (
                    24 - dado if color == "Blanca" else dado - 1
                )  # INDEX (0-23)
                if destino_calc == punto_destino - 1:
                    dado_elegido = dado
                    break

            if dado_elegido is None:
                raise MovimientoInvalidoError(
                    f"No hay dado que entre al punto {punto_destino}."
                )

            # Ejecutar el movimiento exitoso (Core consume el dado)
            captura = self.juego.valida_mover_desde_barra(jugador, dado_elegido)
            self.punto_origen = None  # Limpiar selección

            # Verificar si aún hay fichas en la barra y si hay movimientos posibles con los dados restantes
            color_jugador = jugador.obtener_color()
            barra_tiene_fichas = self.juego.mostrar_tablero().mostrar_barra()[
                color_jugador
            ]

            if barra_tiene_fichas and not self.juego.hay_movimientos_posibles(jugador):

                # Caso: Quedan fichas en barra, pero los dados restantes no sirven para reingresar.
                self.juego.controlar_turnos()  # Forzar el cambio de turno
                # No es estrictamente necesario, pero asegura que el siguiente jugador tire:
                if self.juego.__dados__.obtener_tiradas_restantes():
                    self.juego.__dados__.reiniciar()

                self._actualizar_mensaje(
                    f"Ficha reingresada. No hay movimientos posibles restantes desde la barra. Turno de {self.juego.mostrar_turno().obtener_nombre()}",
                    3000,  # Un mensaje más largo para que se lea
                )
                return  # Terminar aquí, el turno ya cambió.

            # Lógica de fin de turno normal (si se agotaron los dados O si hay ganador)

            ganador = self.juego.verificar_ganador()
            if ganador:
                self.ganador = ganador
                self._actualizar_mensaje(
                    f"¡Ganó {ganador.obtener_nombre()}!", self.duracion_mensaje_final
                )
                self.tiempo_fin_juego = pygame.time.get_ticks()

            # Si el core cambió el turno (porque no quedan dados), actualizamos el mensaje.
            elif not self.juego.__dados__.obtener_tiradas_restantes():
                self._actualizar_mensaje(
                    f"Turno de {self.juego.mostrar_turno().obtener_nombre()}", 1500
                )
            else:
                # Si aún quedan dados y no pasó el turno
                mensaje = f"Reingreso exitoso con dado {dado_elegido}"
                if captura:
                    mensaje = (
                        f"¡Capturaste ficha al reingresar con dado {dado_elegido}!"
                    )
                self._actualizar_mensaje(mensaje, 1500)

        except Exception as e:
            self.punto_origen = None
            self._actualizar_mensaje(f"No se pudo reingresar: {e}", 2000)

    def _manejar_movimiento_normal(self, punto_destino, jugador):
        """Gestiona selección de origen y ejecución de movimientos normales (origen -> destino).

        - Si no hay origen seleccionado: guarda punto_destino como origen.
        - Si hay origen: intenta aplicar movimiento con juego.valida_mover_ficha,
          maneja capturas, mensajes y cambio de turno si se agotan los dados.

        Args:
            punto_destino (int): punto clicado por el jugador
            jugador: instancia de Jugador que realiza el movimiento
        """
        try:
            if self.punto_origen is None:
                self.punto_origen = punto_destino
                self._actualizar_mensaje(
                    f"Punto {self.punto_origen} seleccionado.", 1000
                )
            else:
                # Intento de movimiento (Origen -> Destino)

                # Llama a la lógica central.
                captura, dados_usados = self.juego.valida_mover_ficha(
                    jugador, self.punto_origen, punto_destino
                )
                self.punto_origen = None  # Limpiar después del éxito

                dados_str = " + ".join(map(str, sorted(dados_usados, reverse=True)))

                # Verificar Ganador
                ganador = self.juego.verificar_ganador()
                if ganador:
                    self.ganador = ganador
                    self._actualizar_mensaje(
                        f"¡Ganó {ganador.obtener_nombre()}!",
                        self.duracion_mensaje_final,
                    )
                    self.tiempo_fin_juego = pygame.time.get_ticks()
                    return

                if not self.juego.__dados__.obtener_tiradas_restantes():
                    self._actualizar_mensaje(
                        f"Turno de {self.juego.mostrar_turno().obtener_nombre()}", 1500
                    )
                else:
                    # Aún quedan dados para el mismo jugador. Mostrar el mensaje del movimiento.
                    mensaje = f"Movimiento válido (Usaste: {dados_str})"
                    if captura:
                        mensaje = (
                            f"¡Capturaste una ficha enemiga! (Usaste: {dados_str})"
                        )
                    self._actualizar_mensaje(mensaje, 1500)

        except Exception as e:
            self._actualizar_mensaje(f"Movimiento inválido: {e}", 1800)
            self.punto_origen = None
