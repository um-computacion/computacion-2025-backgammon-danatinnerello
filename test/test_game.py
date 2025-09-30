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

    def test_hay_movimientos_posibles_con_barra_bloqueada(self):
        # poner una ficha blanca en la barra
        self.tablero.mostrar_barra()["Blanca"].append("Blanca")
        # bloquear todas las entradas de la blanca con 2 negras
        for i in range(18, 24):
            self.tablero.mostrar_contenedor()[i] = ["Negra", "Negra"]
        # forzamos los dados
        self.dados.__tiradas_restantes__ = [1, 2]
        self.assertFalse(self.juego.hay_movimientos_posibles(self.j1))

    def test_hay_movimientos_posibles_con_barra_libre(self):
        self.tablero.mostrar_barra()["Blanca"].append("Blanca")
        self.dados.__tiradas_restantes__ = [1]
        # destino (23) está libre
        self.assertTrue(self.juego.hay_movimientos_posibles(self.j1))

    def test_controlar_turnos_alterna_correctamente(self):
        turno_inicial = self.juego.mostrar_turno()
        self.juego.controlar_turnos()
        self.assertNotEqual(turno_inicial, self.juego.mostrar_turno())

    def test_verificar_ganador_detecta_correctamente(self):
        # simulamos que j1 ya sacó todas sus fichas
        for _ in range(15):
            self.j1.sacar_ficha_a_afuera()
        ganador = self.juego.verificar_ganador()
        self.assertEqual(ganador, self.j1)
        self.assertTrue(self.juego.mostrar_juego_terminado())

#test para aumentar la cobertura 
    
    def test_mostrar_getters_funcionan(self):
        # cubre los getters simples
        self.assertEqual(self.juego.mostrar_jugador1(), self.j1)
        self.assertEqual(self.juego.mostrar_jugador2(), self.j2)
        self.assertFalse(self.juego.mostrar_juego_terminado())
        self.assertEqual(self.juego.mostrar_tablero(), self.tablero)
        self.assertEqual(self.juego.mostrar_turno(), self.j1)

    def test_valida_sacar_ficha_con_dado_mayor_valido(self):
        # vaciar todo el tablero
        for i in range(24):
            self.tablero.mostrar_contenedor()[i] = []
        # poner solo una ficha blanca en la casa más cercana
        self.tablero.mostrar_contenedor()[0] = ["Blanca"]
        # simular que todas están en el último cuadrante
        self.tablero.todas_en_ultimo_cuadrante = lambda c: True
        # dado mayor al necesario
        self.dados.__tiradas_restantes__ = [6]

        self.juego.valida_sacar_ficha(self.j1, 1)
        self.assertEqual(self.j1.__fichas_restantes__, 14)


    def test_valida_mover_desde_barra_valido(self):
        # poner ficha en la barra negra
        self.tablero.mostrar_barra()["Negra"].append("Negra")
        # dado 3 → entra en posición 2
        self.dados.__tiradas_restantes__ = [3]
        result = self.juego.valida_mover_desde_barra(self.j2, 3)
        self.assertTrue(result)
        self.assertIn("Negra", self.tablero.mostrar_contenedor()[2])

    def test_verificar_ganador_marca_juego_terminado(self):
        self.j1.__fichas_restantes__ = 0
        self.assertFalse(self.juego.mostrar_juego_terminado())
        ganador = self.juego.verificar_ganador()
        self.assertEqual(ganador, self.j1)
        self.assertTrue(self.juego.mostrar_juego_terminado())

    def test_valida_sacar_ficha_dado_mayor_no_valido_por_fichas_mas_lejanas(self):
        # Poner fichas en posiciones más lejanas
        for i in range(24):
            self.tablero.mostrar_contenedor()[i] = []
        self.tablero.mostrar_contenedor()[0] = ["Blanca"]   # ficha en la casilla 1
        self.tablero.mostrar_contenedor()[1] = ["Blanca"]   # otra más lejana en la casa
        self.tablero.todas_en_ultimo_cuadrante = lambda c: True
        self.dados.__tiradas_restantes__ = [6]  # dado mayor

        with self.assertRaises(SacarFichaError):
            self.juego.valida_sacar_ficha(self.j1, 1)  # casilla 1 humana

    def test_valida_sacar_ficha_para_negras_con_dado_exactoy_mayor(self):
        # Vaciar tablero
        for i in range(24):
            self.tablero.mostrar_contenedor()[i] = []
        # ficha negra en la casilla 24 (índice 23)
        self.tablero.mostrar_contenedor()[23] = ["Negra"]
        self.tablero.todas_en_ultimo_cuadrante = lambda c: True
        self.dados.__tiradas_restantes__ = [1]  # dado exacto para negras en 24

        self.juego.valida_sacar_ficha(self.j2, 24)  # 24 humano
        self.assertEqual(self.j2.__fichas_restantes__, 14)

    def test_valida_mover_desde_barra_blancas(self):
        # ficha blanca en barra
        self.tablero.mostrar_barra()["Blanca"].append("Blanca")
        # dado 6 → entra en casilla 19 (24-6 = 18 → humano 19)
        self.dados.__tiradas_restantes__ = [6]
        self.tablero.valida_mover_desde_barra = lambda c, h: True

        result = self.juego.valida_mover_desde_barra(self.j1, 6)
        self.assertTrue(result)

    def test_valida_mover_desde_barra_falla_a_pesar_de_dado(self):
        self.tablero.mostrar_barra()["Blanca"].append("Blanca")
        self.dados.__tiradas_restantes__ = [4]
        # aunque el dado está, no se puede entrar
        self.tablero.valida_mover_desde_barra = lambda c, h: False
        with self.assertRaises(MovimientoInvalidoError):
            self.juego.valida_mover_desde_barra(self.j1, 4)

    def test_hay_movimientos_posibles_sin_tiradas(self):
        self.dados.__tiradas_restantes__ = []
        self.assertFalse(self.juego.hay_movimientos_posibles(self.j1))



if __name__ == "__main__":
    unittest.main()
