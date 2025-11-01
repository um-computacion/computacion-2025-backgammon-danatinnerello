import unittest
from core.game import Juego
from core.player import Jugador
from core.board import Tablero
from core.dice import Dados
from core.excepcions import MovimientoInvalidoError, SacarFichaError


class TestJuego(unittest.TestCase):
    def setUp(self):
        self.j1 = Jugador("Alice", "Blanca")
        self.j2 = Jugador("Bob", "Negra")
        self.tablero = Tablero()
        self.dados = Dados()
        self.juego = Juego(self.j1, self.j2, self.tablero, self.dados)

    def _limpiar_tablero(self):
        """Función auxiliar para limpiar el tablero de fichas iniciales."""
        for i in range(24):
            self.tablero.mostrar_contenedor()[i] = []
        self.tablero.mostrar_barra()["Blanca"] = []
        self.tablero.mostrar_barra()["Negra"] = []
        self.tablero.mostrar_afuera()["Blanca"] = []
        self.tablero.mostrar_afuera()["Negra"] = []

    def test_verificar_ganador_none_al_inicio(self):
        self.assertIsNone(self.juego.verificar_ganador())

    def test_valida_mover_ficha_invalido(self):
        with self.assertRaises(MovimientoInvalidoError):
            # Posición 0 tiene fichas negras, no blancas (J1)
            self.juego.valida_mover_ficha(self.j1, 1, 2)

    def test_valida_sacar_ficha_invalido(self):
        # Al inicio, las fichas no están en el último cuadrante
        with self.assertRaises(SacarFichaError):
            self.juego.valida_sacar_ficha(self.j1, 1)

    def test_valida_mover_desde_barra_invalido(self):
        # J1 no tiene fichas en barra para mover, lanza excepción por dado no usado o falta de ficha
        self.dados.__tiradas_restantes__ = [3]
        with self.assertRaises(MovimientoInvalidoError):
            self.juego.valida_mover_desde_barra(self.j1, 3)

    def test_hay_movimientos_posibles_false_en_tablero_vacio(self):
        self._limpiar_tablero()
        self.juego.__dados__.__tiradas_restantes__ = [6]
        self.assertFalse(self.juego.hay_movimientos_posibles(self.j1))

    def test_valida_mover_ficha_con_dado_incorrecto(self):
        # fuerza un dado que no corresponde al movimiento (diferencia 1)
        self.juego.__dados__.__tiradas_restantes__ = [6]
        # J1 (Blanca) intenta mover de 6 a 5 (diferencia 1). Fallará el consumo de dado.
        with self.assertRaises(MovimientoInvalidoError):
            self.juego.valida_mover_ficha(self.j1, 6, 5)

    def test_valida_sacar_ficha_con_dado_incorrecto(self):
        # forzamos que todas estén en último cuadrante (para pasar la primera validación)
        self.juego.mostrar_tablero().todas_en_ultimo_cuadrante = lambda c: True
        # pero el dado no corresponde a la posición 20 (20 está a 5 de distancia de 24)
        self.juego.__dados__.__tiradas_restantes__ = [6]
        with self.assertRaises(SacarFichaError):
            self.juego.valida_sacar_ficha(self.j1, 20)

    def test_valida_mover_desde_barra_dado_invalido(self):
        self.juego.__dados__.__tiradas_restantes__ = [3]
        # Se necesita dado 3, pero se bloquea la entrada en el tablero.
        self.juego.mostrar_tablero().mostrar_barra()["Blanca"].append("Blanca")
        # Bloquear el punto 19 (entrada con dado 6)
        self.juego.mostrar_tablero().mostrar_contenedor()[18] = ["Negra", "Negra"]
        with self.assertRaises(MovimientoInvalidoError):
            self.juego.valida_mover_desde_barra(self.j1, 6)  # Intenta entrar con dado 6

    def test_hay_movimientos_posibles_con_barra(self):
        # jugador tiene ficha en barra y dado que le permite salir
        self.juego.__dados__.__tiradas_restantes__ = [6]
        self.juego.__tablero__.mostrar_barra()["Blanca"].append("Blanca")
        # limpiar el punto de destino (19/índice 18) para que sea posible reingresar
        self.juego.__tablero__.mostrar_contenedor()[18] = []
        self.assertTrue(self.juego.hay_movimientos_posibles(self.j1))

    def test_controlar_turnos_alterna_correcto(self):
        turno_inicial = self.juego.mostrar_turno()
        self.juego.controlar_turnos()
        self.assertNotEqual(turno_inicial, self.juego.mostrar_turno())
        self.juego.controlar_turnos()
        self.assertEqual(turno_inicial, self.juego.mostrar_turno())

    def test_verificar_ganador_jugador1(self):
        # forzamos que jugador1 saque todas sus fichas
        self.j1.__fichas_restantes__ = 0
        ganador = self.juego.verificar_ganador()
        self.assertEqual(ganador, self.j1)

    def test_valida_mover_ficha_falla_en_validar(self):
        # Mock de la validación para que siempre falle
        original_valida = self.tablero.validar_movimiento
        self.tablero.validar_movimiento = lambda c, d, h: False
        with self.assertRaises(MovimientoInvalidoError):
            # El Core llama a validar_movimiento(color, desde, hacia)
            self.juego.valida_mover_ficha(self.j1, 1, 2)
        self.tablero.validar_movimiento = original_valida

    def test_valida_sacar_ficha_falla(self):
        # Mock para que la validación de cuadrante falle
        original_cuadrante = self.tablero.todas_en_ultimo_cuadrante
        self.tablero.todas_en_ultimo_cuadrante = lambda c: False
        with self.assertRaises(SacarFichaError):
            self.juego.valida_sacar_ficha(self.j1, 23)
        self.tablero.todas_en_ultimo_cuadrante = original_cuadrante

    def test_valida_mover_desde_barra_falla_dado(self):
        # Mock para que la tirada de dado falle
        original_usar = self.dados.usar_tirada
        self.dados.usar_tirada = lambda dado, revertir=False: False
        with self.assertRaises(MovimientoInvalidoError):
            self.juego.valida_mover_desde_barra(self.j1, 3)
        self.dados.usar_tirada = original_usar

    def test_hay_movimientos_posibles_false(self):
        # Limpiamos el tablero y nos aseguramos de que no haya movimientos
        self._limpiar_tablero()
        # Ponemos una ficha en una posición que no se puede mover con el dado 6 (ej: punto 24)
        self.tablero.mostrar_contenedor()[23].append("Blanca")
        self.dados.__tiradas_restantes__ = [6]
        self.tablero.validar_movimiento = lambda c, d, h, t: False
        self.assertFalse(self.juego.hay_movimientos_posibles(self.j1))

    def test_verificar_ganador_jugador2(self):
        self.j2.__fichas_restantes__ = 0
        ganador = self.juego.verificar_ganador()
        self.assertEqual(ganador, self.j2)

    def test_hay_movimientos_posibles_true_sin_barra(self):
        self._limpiar_tablero()
        # Colocamos una ficha que puede moverse 1 espacio (24 -> 23)
        self.tablero.mostrar_contenedor()[23] = ["Blanca"]
        self.dados.__tiradas_restantes__ = [1]
        self.assertTrue(self.juego.hay_movimientos_posibles(self.j1))

    def test_hay_movimientos_posibles_con_barra_bloqueada(self):
        self._limpiar_tablero()
        self.tablero.mostrar_barra()["Blanca"].append("Blanca")
        # bloquear todas las entradas de la blanca con 2 negras (índices 18 al 23)
        for i in range(18, 24):
            self.tablero.mostrar_contenedor()[i] = ["Negra", "Negra"]
        self.dados.__tiradas_restantes__ = [1, 2, 3, 4, 5, 6]
        self.assertFalse(self.juego.hay_movimientos_posibles(self.j1))

    def test_hay_movimientos_posibles_con_barra_libre(self):
        self._limpiar_tablero()
        self.tablero.mostrar_barra()["Blanca"].append("Blanca")
        self.dados.__tiradas_restantes__ = [6]
        # destino (índice 18/punto 19) está libre
        self.assertTrue(self.juego.hay_movimientos_posibles(self.j1))

    def test_controlar_turnos_alterna_correctamente(self):
        turno_inicial = self.juego.mostrar_turno()
        self.juego.controlar_turnos()
        self.assertNotEqual(turno_inicial, self.juego.mostrar_turno())

    def test_verificar_ganador_detecta_correctamente(self):
        self.j1.__fichas_restantes__ = 0
        ganador = self.juego.verificar_ganador()
        self.assertEqual(ganador, self.j1)
        self.assertTrue(self.juego.mostrar_juego_terminado())

    def test_valida_sacar_ficha_dado_mayor_no_valido_por_fichas_mas_lejanas(self):
        # PRUEBA DE BLOQUEO DE DADO MAYOR
        self._limpiar_tablero()

        # 1. Ficha que queremos sacar: Casilla 2 (Índice 1)
        self.tablero.mostrar_contenedor()[1] = ["Blanca"]
        # 2. Ficha que bloquea (MÁS LEJANA): Casilla 1 (Índice 0)
        self.tablero.mostrar_contenedor()[0] = ["Blanca"]

        self.tablero.todas_en_ultimo_cuadrante = lambda c: True
        self.dados.__tiradas_restantes__ = [6]  # Dado mayor

        # Debe lanzar un error porque hay una ficha en la Casilla 1 que está más lejos que el origen (Casilla 2)
        with self.assertRaisesRegex(
            SacarFichaError,
            "No puedes usar el dado 6. Hay fichas en posiciones más lejanas.",
        ):
            self.juego.valida_sacar_ficha(self.j1, 2)

    def test_valida_mover_desde_barra_blancas(self):
        # PRUEBA DE REINGRESO BLANCAS (ÉXITO)
        self._limpiar_tablero()  # Limpiar para evitar bloqueos iniciales
        self.tablero.mostrar_barra()["Blanca"].append("Blanca")
        self.dados.__tiradas_restantes__ = [
            6
        ]  # Dado 6 → entra en casilla 19 (índice 18)

        result = self.juego.valida_mover_desde_barra(self.j1, 6)

        # 1. Verificar que se devolvió un booleano (captura o no)
        self.assertIsInstance(result, bool)
        # 2. Verificar que la ficha se movió al destino (índice 18)
        self.assertIn("Blanca", self.tablero.mostrar_contenedor()[18])
        # 3. Verificar que salió de la barra
        self.assertEqual(len(self.tablero.mostrar_barra()["Blanca"]), 0)

    def test_valida_mover_desde_barra_valido(self):
        # PRUEBA DE REINGRESO NEGRAS (ÉXITO)
        self._limpiar_tablero()  # Limpiar para evitar bloqueos iniciales
        self.tablero.mostrar_barra()["Negra"].append("Negra")
        self.dados.__tiradas_restantes__ = [
            3
        ]  # Dado 3 → entra en posición 3 (índice 2)

        result = self.juego.valida_mover_desde_barra(self.j2, 3)

        # 1. Verificar que se devolvió un booleano (captura o no)
        self.assertIsInstance(result, bool)
        # 2. Verificar que la ficha se movió al destino (índice 2)
        self.assertIn("Negra", self.tablero.mostrar_contenedor()[2])
        # 3. Verificar que salió de la barra
        self.assertEqual(len(self.tablero.mostrar_barra()["Negra"]), 0)

    def test_valida_sacar_ficha_para_negras_con_dado_exacto(self):
        self._limpiar_tablero()
        # ficha negra en la casilla 24 (índice 23)
        self.tablero.mostrar_contenedor()[23] = ["Negra"]
        self.tablero.todas_en_ultimo_cuadrante = lambda c: True
        self.dados.__tiradas_restantes__ = [1]  # dado exacto (24-23 = 1)

        self.juego.valida_sacar_ficha(self.j2, 24)
        self.assertEqual(self.j2.__fichas_restantes__, 14)

    def test_valida_mover_desde_barra_blancas_con_captura(self):
        self._limpiar_tablero()
        self.tablero.mostrar_barra()["Blanca"].append("Blanca")
        self.dados.__tiradas_restantes__ = [
            6
        ]  # Dado 6 → entra en casilla 19 (índice 18)
        # Colocar un blot enemigo en la posición 19
        self.tablero.mostrar_contenedor()[18] = ["Negra"]

        result = self.juego.valida_mover_desde_barra(self.j1, 6)

        self.assertTrue(result)  # Debe devolver True por la captura
        self.assertIn("Blanca", self.tablero.mostrar_contenedor()[18])
        self.assertIn(
            "Negra", self.tablero.mostrar_barra()["Negra"]
        )  # Ficha enemiga capturada

    def test_valida_mover_ficha_bloqueado(self):
        # Mover una ficha (Blanca) a un punto bloqueado (2 Negras)
        self._limpiar_tablero()
        self.tablero.mostrar_contenedor()[5] = ["Blanca"]  # Origen (Punto 6)
        self.tablero.mostrar_contenedor()[4] = [
            "Negra",
            "Negra",
        ]  # Destino (Punto 5, Diferencia 1)
        self.dados.__tiradas_restantes__ = [1]

        with self.assertRaisesRegex(
            MovimientoInvalidoError, "destino bloqueado"
        ):  # <--- CAMBIO
            self.juego.valida_mover_ficha(self.j1, 6, 5)

    def test_sacar_ficha_falla_tablero(self):
        # Simular que el tablero no puede sacar la ficha (e.g., ya no queda ninguna)
        self._limpiar_tablero()
        self.tablero.mostrar_contenedor()[0] = ["Blanca"]
        self.tablero.todas_en_ultimo_cuadrante = lambda c: True
        self.dados.__tiradas_restantes__ = [1]

        # Mock para que tablero.sacar_ficha devuelva False (simulando fallo interno)
        original_sacar = self.tablero.sacar_ficha
        self.tablero.sacar_ficha = lambda c, d: False

        with self.assertRaisesRegex(SacarFichaError, "No se pudo sacar ficha"):
            self.juego.valida_sacar_ficha(self.j1, 1)

        self.tablero.sacar_ficha = original_sacar  # Restaurar mock

    def test_mover_desde_barra_falla_reversion(self):
        # Intentar reingresar (el dado se consume), pero la validación falla (se debe revertir)
        self._limpiar_tablero()
        self.tablero.mostrar_barra()["Blanca"].append("Blanca")
        self.dados.__tiradas_restantes__ = [6]

        # Bloquear el punto de entrada (Punto 19)
        self.tablero.mostrar_contenedor()[18] = ["Negra", "Negra"]

        with self.assertRaisesRegex(
            MovimientoInvalidoError, "Movimiento invalido desde la barra"
        ):
            self.juego.valida_mover_desde_barra(self.j1, 6)

        # Verificar que el dado fue revertido
        self.assertIn(6, self.dados.obtener_tiradas_restantes())
        self.assertEqual(len(self.dados.obtener_tiradas_restantes()), 1)

    def test_hay_mov_barra_no_puede_salir(self):
        # Jugador tiene fichas en barra pero todos los puntos de entrada están bloqueados
        self._limpiar_tablero()
        self.tablero.mostrar_barra()["Blanca"].append("Blanca")
        self.dados.__tiradas_restantes__ = [1, 2, 3, 4, 5, 6]
        # Bloquear todos los puntos de entrada (índices 18 al 23)
        for i in range(18, 24):
            self.tablero.mostrar_contenedor()[i] = ["Negra", "Negra"]

        # El método debe devolver False porque no hay movimientos posibles
        self.assertFalse(self.juego.hay_movimientos_posibles(self.j1))

    def test_hay_mov_tablero_bloqueado(self):
        # Jugador sin fichas en barra, pero el único movimiento posible está bloqueado.
        self._limpiar_tablero()
        self.tablero.mostrar_contenedor()[5] = ["Blanca"]  # Única ficha en Punto 6
        self.dados.__tiradas_restantes__ = [1]
        # Bloquear el destino (Punto 5, índice 4)
        self.tablero.mostrar_contenedor()[4] = ["Negra", "Negra"]

        # El método debe devolver False
        self.assertFalse(self.juego.hay_movimientos_posibles(self.j1))

    def test_valida_mover_ficha_cambia_turno_al_final(self):
        # Limpiar y dejar una sola tirada exacta para el movimiento
        self._limpiar_tablero()
        self.tablero.mostrar_contenedor()[5] = ["Blanca"]  # Punto 6
        self.tablero.mostrar_contenedor()[4] = []  # Punto 5
        self.dados.__tiradas_restantes__ = [1]

        turno_inicial = self.juego.mostrar_turno()

        # Ejecutar el único movimiento con el dado restante (6 -> 5)
        self.juego.valida_mover_ficha(self.j1, 6, 5)

        # El turno debe haber cambiado automáticamente
        self.assertNotEqual(turno_inicial, self.juego.mostrar_turno())
        self.assertEqual(len(self.dados.obtener_tiradas_restantes()), 0)

    def test_valida_mover_desde_barra_cambia_turno_al_final(self):
        # Ficha en barra y una sola tirada exacta
        self.tablero.mostrar_barra()["Negra"].append("Negra")
        self.dados.__tiradas_restantes__ = [1]  # Dado 1 -> entra en punto 1 (índice 0)
        self.tablero.mostrar_contenedor()[0] = []

        turno_inicial = self.juego.mostrar_turno()

        # Mover ficha desde la barra con el dado restante
        self.juego.valida_mover_desde_barra(self.j2, 1)

        # El turno debe haber cambiado
        self.assertNotEqual(turno_inicial, self.juego.mostrar_turno())
        self.assertEqual(len(self.dados.obtener_tiradas_restantes()), 0)

    def test_valida_mover_desde_barra_falla_tablero_revierte_dado(self):
        # Ficha en barra y dado disponible
        self.tablero.mostrar_barra()["Blanca"].append("Blanca")
        self.dados.__tiradas_restantes__ = [3]

        # Bloquear el punto de entrada (Punto 22, índice 21)
        self.tablero.mostrar_contenedor()[21] = ["Negra", "Negra"]

        # Asegurarse de que el dado fue consumido temporalmente por Juego.valida_mover_desde_barra
        # y luego revertido si falla la validación del tablero
        self.assertEqual(len(self.dados.obtener_tiradas_restantes()), 1)

        with self.assertRaisesRegex(
            MovimientoInvalidoError, "Movimiento invalido desde la barra"
        ):
            # Intenta reingresar con dado 3 a punto 22 (índice 21)
            self.juego.valida_mover_desde_barra(self.j1, 3)

        # Debe confirmar que el dado fue revertido
        self.assertIn(3, self.dados.obtener_tiradas_restantes())

    def test_hay_movimientos_posibles_sacar_ficha_dado_mayor(self):
        # Tablero en posición de sacar fichas
        self._limpiar_tablero()
        self.tablero.todas_en_ultimo_cuadrante = lambda c: True

        # Ficha más lejana en Punto 3 (índice 2), requiere dado 4 para salir (3 + 1 = 4)
        self.tablero.mostrar_contenedor()[2] = ["Blanca"]

        # Dado disponible: 6 (mayor que el 4 requerido, y es la ficha más lejana)
        self.dados.__tiradas_restantes__ = [6]

        # Debe ser posible sacar la ficha con el dado mayor (6)
        self.assertTrue(self.juego.hay_movimientos_posibles(self.j1))

    def test_hay_movimientos_posibles_movimiento_normal(self):
        # Limpiar tablero, sin barra, no todas en el cuadrante final
        self._limpiar_tablero()
        self.tablero.todas_en_ultimo_cuadrante = lambda c: False

        # Ficha Negra en Punto 1 (índice 0)
        self.tablero.mostrar_contenedor()[0] = ["Negra"]
        # Dado 1 disponible, permite mover a Punto 2 (índice 1)
        self.dados.__tiradas_restantes__ = [1]

        # Debe ser posible el movimiento (0 -> 1)
        self.assertTrue(self.juego.hay_movimientos_posibles(self.j2))

    def test_init_nombres_vacios_lanza_error(self):
        # Cubre la rama de validación de nombre vacío
        with self.assertRaisesRegex(MovimientoInvalidoError, "no pueden estar vacíos"):
            Juego(Jugador("", "Blanca"), self.j2, self.tablero, self.dados)

    def test_init_nombres_duplicados_lanza_error(self):
        # Cubre la rama de validación de nombres iguales
        jugador_duplicado = Jugador("Alice", "Negra")
        with self.assertRaisesRegex(MovimientoInvalidoError, "deben ser diferentes"):
            Juego(self.j1, jugador_duplicado, self.tablero, self.dados)

    def test_init_nombres_invalidos_caracteres(self):
        # Cubre la rama de validación de isalpha()
        jugador_invalido = Jugador("Alice123", "Negra")
        with self.assertRaisesRegex(
            MovimientoInvalidoError, "solo pueden contener letras"
        ):
            Juego(self.j1, jugador_invalido, self.tablero, self.dados)

    def test_hay_mov_posibles_normal_false(self):
        self._limpiar_tablero()
        # Colocamos una ficha en un punto intermedio, no en la casa (Punto 10, índice 9)
        self.tablero.mostrar_contenedor()[9] = ["Blanca"]
        # Dado que no le permite moverse (ej. 1), y el resto del tablero está vacío/bloqueado.
        self.dados.__tiradas_restantes__ = [1]

        # Bloqueamos el único destino posible (Punto 9)
        self.tablero.mostrar_contenedor()[8] = ["Negra", "Negra"]

        # Ahora, NO hay movimientos posibles (debe ser False)
        self.assertFalse(self.juego.hay_movimientos_posibles(self.j1))

    def test_valida_mover_ficha_falla_consumo_principal(self):
        # El Core encuentra un dado principal, pero este falla en el consumo (debe ser imposible, pero cubre la línea)
        self._limpiar_tablero()
        self.dados.__tiradas_restantes__ = [1, 2]
        self.tablero.mostrar_contenedor()[5] = ["Blanca"]  # Origen 6

        original_usar = self.dados.usar_tirada
        self.dados.usar_tirada = (
            lambda dado, r=False: False
        )  # Mock para que falle el consumo

        with self.assertRaisesRegex(
            MovimientoInvalidoError, "El dado ya no está disponible."
        ):
            # Intenta mover 1 espacio
            self.juego.valida_mover_ficha(self.j1, 6, 5)

        self.dados.usar_tirada = original_usar

    def test_valida_mover_ficha_pasos_compuestos_con_dobles(self):
        # Mover 4+4 = 8, asegurando que el Core detecte la combinación de dobles.
        self._limpiar_tablero()
        self.tablero.mostrar_contenedor()[10] = ["Blanca"]  # Origen 11
        self.dados.__tiradas_restantes__ = [4, 4, 4, 4]  # Dobles 4

        # El movimiento es 11 -> 3 (8 espacios). Paso intermedio 7 (11-4)
        self.juego.valida_mover_ficha(self.j1, 11, 3)

        self.assertEqual(len(self.dados.obtener_tiradas_restantes()), 2)

    def test_valida_sacar_ficha_falla_interno_dado_mayor(self):
        # Mock para que el tablero falle al sacar ficha (dado mayor)
        self._limpiar_tablero()
        self.tablero.todas_en_ultimo_cuadrante = lambda c: True
        self.tablero.mostrar_contenedor()[5] = ["Blanca"]  # Origen 6 (distancia 19)
        self.dados.__tiradas_restantes__ = [6]

        original_sacar = self.tablero.sacar_ficha
        self.tablero.sacar_ficha = lambda c, d: False

        with self.assertRaisesRegex(SacarFichaError, "Fallo interno del tablero"):
            self.juego.valida_sacar_ficha(self.j1, 6)

        self.tablero.sacar_ficha = original_sacar

    def test_valida_sacar_ficha_falla_interno_dado_exacto(self):
        # Mock para que el tablero falle al sacar ficha (dado exacto)
        self._limpiar_tablero()
        self.tablero.todas_en_ultimo_cuadrante = lambda c: True
        self.tablero.mostrar_contenedor()[0] = ["Blanca"]  # Origen 1 (distancia 24)
        self.dados.__tiradas_restantes__ = [6]

        original_sacar = self.tablero.sacar_ficha
        self.tablero.sacar_ficha = lambda c, d: False

        with self.assertRaisesRegex(SacarFichaError, "Fallo interno del tablero"):
            self.juego.valida_sacar_ficha(self.j1, 1)

        self.tablero.sacar_ficha = original_sacar

    def test_hay_mov_posibles_normal_false_no_es_ficha_tuya(self):
        # Se asegura de no romper si hay fichas enemigas en los puntos.
        self._limpiar_tablero()
        self.tablero.mostrar_contenedor()[5] = ["Negra"]  # Ficha enemiga en Punto 6
        self.dados.__tiradas_restantes__ = [1]

        # El jugador J1 (Blanca) no debe encontrar movimientos, incluso si el destino está libre.
        self.assertFalse(self.juego.hay_movimientos_posibles(self.j1))

    def test_valida_mover_ficha_falla_consumo_secundario_revierte(self):
        # Escenario: Movimiento compuesto (6+2=8). Falla al consumir el dado 2 (secundario).
        # Ajustamos el origen/destino a un movimiento que sí es válido en el tablero.
        self._limpiar_tablero()
        self.tablero.mostrar_contenedor()[12] = ["Blanca"]  # Origen 13
        self.dados.__tiradas_restantes__ = [6, 2]  # Dados

        # Mock: El consumo del dado 2 debe fallar (return False), y el dado 6 debe pasar.
        original_usar = self.dados.usar_tirada

        def mock_usar_tirada(dado, revertir=False):
            # Fallar solo cuando se intenta consumir el dado 2, no en reversión.
            if dado == 2 and not revertir:
                return False
            return original_usar(dado, revertir)

        self.dados.usar_tirada = mock_usar_tirada

        # Mover 13 (index 12) a 5 (index 4), diferencia 8.
        with self.assertRaisesRegex(
            MovimientoInvalidoError, "No se pudo usar el segundo dado"
        ):
            self.juego.valida_mover_ficha(self.j1, 13, 5)

        # Verificar que el dado 6 (principal) fue revertido correctamente.
        self.assertIn(6, self.dados.obtener_tiradas_restantes())
        self.assertIn(2, self.dados.obtener_tiradas_restantes())
        self.dados.usar_tirada = original_usar


if __name__ == "__main__":
    unittest.main()
