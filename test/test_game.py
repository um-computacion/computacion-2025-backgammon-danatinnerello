import unittest
from core.game import Juego

class TestJuego(unittest.TestCase):
    def setUp(self):
        self.juego = Juego("Jugador1","Jugador2")

    def test_verificar_ganador_sin_ganador(self):
        self.assertIsNone(self.juego.verificar_ganador())

    def test_controlar_turnos(self):
        # simulamos turno inicial manualmente
        self.juego.__turno__ = self.juego.__jugador1__
        self.juego.controlar_turnos()
        self.assertEqual(self.juego.__turno__, self.juego.__jugador2__)
