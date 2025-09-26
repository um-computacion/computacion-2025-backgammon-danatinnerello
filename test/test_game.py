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
        self.juego = Juego(self.j1, self.j2, tablero=Tablero(), dados=Dados())

    def test_turnos_alternan(self):
        turno1 = self.juego.mostrar_turno()
        self.juego.controlar_turnos()
        turno2 = self.juego.mostrar_turno()
        self.assertNotEqual(turno1, turno2)

    def test_verificar_ganador_none_al_inicio(self):
        self.assertIsNone(self.juego.verificar_ganador())

    def test_valida_mover_ficha_invalido(self):
        with self.assertRaises(MovimientoInvalidoError):
            self.juego.valida_mover_ficha(self.j1, 0, 5)

    def test_valida_sacar_ficha_invalido(self):
        with self.assertRaises(SacarFichaError):
            self.juego.valida_sacar_ficha(self.j1, 0)

    def test_valida_mover_desde_barra_invalido(self):
        with self.assertRaises(MovimientoInvalidoError):
            self.juego.valida_mover_desde_barra(self.j1, 3)

    def test_hay_movimientos_posibles_false_en_tablero_vacio(self):
        # vaciar el tablero y la barra
        for i in range(24):
            self.juego.mostrar_tablero().mostrar_contenedor()[i] = []
        self.juego.mostrar_tablero().mostrar_barra()["Blanca"] = []
        self.juego.__dados__.__tiradas_restantes__ = [6]
        self.assertFalse(self.juego.hay_movimientos_posibles(self.j1))
    
    def test_valida_mover_ficha_con_dado_incorrecto(self):
        # fuerza un dado que no corresponde al movimiento
        self.juego.__dados__.__tiradas_restantes__ = [6]
        with self.assertRaises(MovimientoInvalidoError):
            self.juego.valida_mover_ficha(self.j1, 1, 2)  # diferencia = 1, no 6

    def test_valida_sacar_ficha_con_dado_incorrecto(self):
        # fuerza que todas estén en último cuadrante
        self.juego.mostrar_tablero().todas_en_ultimo_cuadrante = lambda c: True
        # pero el dado no corresponde
        self.juego.__dados__.__tiradas_restantes__ = [6]
        with self.assertRaises(SacarFichaError):
            self.juego.valida_sacar_ficha(self.j1, 20)

    def test_valida_mover_desde_barra_dado_invalido(self):
        self.juego.__dados__.__tiradas_restantes__ = [3]
        self.juego.mostrar_tablero().valida_mover_desde_barra = lambda c, h: False
        with self.assertRaises(MovimientoInvalidoError):
            self.juego.valida_mover_desde_barra(self.j1, 3)

    def test_hay_movimientos_posibles_con_barra(self):
        # jugador tiene ficha en barra y dado que le permite salir
        self.juego.__dados__.__tiradas_restantes__ = [6]
        self.juego.__tablero__.mostrar_barra()["Blanca"] = ["ficha"]
        self.juego.__tablero__.valida_mover_desde_barra = lambda c, h: True
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
        self.validar_movimiento = lambda c, d, h, t: False
        with self.assertRaises(MovimientoInvalidoError):
            self.juego.valida_mover_ficha(self.j1, 1, 2)

    

    def test_valida_sacar_ficha_falla(self):
        self.todas_en_ultimo_cuadrante = lambda c: False
        with self.assertRaises(SacarFichaError):
            self.juego.valida_sacar_ficha(self.j1, 23)


    def test_valida_mover_desde_barra_falla_dado(self):
        self.usar_tirada = lambda dado: False
        with self.assertRaises(MovimientoInvalidoError):
            self.juego.valida_mover_desde_barra(self.j1, 3)

    def test_hay_movimientos_posibles_false(self):
        self.__tiradas_restantes__ = [6]
        self.mostrar_barra = lambda: {"Blanca": [], "Negra": []}
        self.validar_movimiento = lambda c, d, h, t: False
        self.assertFalse(self.juego.hay_movimientos_posibles(self.j1))

    def test_verificar_ganador_jugador2(self):
        self.j2.__fichas_restantes__ = 0
        ganador = self.juego.verificar_ganador()
        self.assertEqual(ganador, self.j2)

    def test_hay_movimientos_posibles_true_sin_barra(self):
        # Configuramos dados y tablero para un movimiento válido
        self.juego.__dados__.__tiradas_restantes__ = [1]
        self.juego.__tablero__.mostrar_barra = lambda: {"Blanca": [], "Negra": []}
        self.juego.__tablero__.validar_movimiento = lambda c, d, h, t: True
        self.assertTrue(self.juego.hay_movimientos_posibles(self.j1))


if __name__ == "__main__":
    unittest.main()
