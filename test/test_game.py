import unittest
from core.game import Juego

class TestJuego(unittest.TestCase):
    def setUp(self):
        self.juego = Juego("Jugador1","Jugador2")
        #inicia un nuevo juego con dos jugadores

    def test_verificar_ganador_sin_ganador(self):
        #verifica que al iniciar el juego no hay ganador
        self.assertIsNone(self.juego.verificar_ganador())

    def test_controlar_turnos(self):
        # simulamos turno inicial manualmente
        self.juego.__turno__ = self.juego.__jugador1__
        self.juego.controlar_turnos()
        self.assertEqual(self.juego.__turno__, self.juego.__jugador2__)
    
    def test_controlar_turnos_de_jugador2_a_jugador1(self):
        #si es el turno del jugador2, debe pasar al jugador1
        self.juego.__turno__ =self.juego.__jugador2__
        self.juego.controlar_turnos()
        self.assertEqual(self.juego.__turno__, self.juego.__jugador1__)

    def test_verificar_ganador_con_jugador1(self):
        #detecta cuando el jugador1 gana
        #simulamos que jugador1 no tiene fichas restantes
        self.juego.mostrar_jugador1().__fichas_restantes__= 0
        ganador =self.juego.verificar_ganador()
        self.assertEqual(ganador, self.juego.__jugador1__)
        self.assertTrue(self.juego.mostrar_juego_terminado())

    def test_verificar_ganador_con_jugador2(self):
        #lo mismo que el anterior peo con el jugador2
        # simulamos que jugador2 no tiene fichas restantes
        self.juego.mostrar_jugador2().__fichas_restantes__ =0
        ganador = self.juego.verificar_ganador()
        self.assertEqual(ganador, self.juego.__jugador2__)
        self.assertTrue(self.juego.mostrar_juego_terminado())

    def test_verificar_ganador_sin_ganador_retorna_none(self):
        #Si nadie gana,devuelve None y no terminar el juego
        resultado = self.juego.verificar_ganador()
        self.assertIsNone(resultado)
        self.assertFalse(self.juego.mostrar_juego_terminado())

