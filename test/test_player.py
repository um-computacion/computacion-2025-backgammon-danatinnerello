import unittest
from core.player import Jugador

class TestJugador(unittest.TestCase):
    def setUp(self):
        self.jugador = Jugador("Dana","blanco")

    def test_obtener_nombre(self):
        self.assertEqual(self.jugador.obtener_nombre(),"Dana")

    def test_obtener_color(self):
        self.assertEqual(self.jugador.obtener_color(),"blanco")

    def test_sacar_ficha(self):
        # al iniciar tiene 15 fichas restantes
        self.assertTrue(self.jugador.sacar_ficha_a_afuera())
        # después de sacar una, se testa que le queden 14
        self.assertEqual(self.jugador.__fichas_restantes__,14)
        
    def test_gano(self):
        # simulamos que saco todas las fichas
        for _ in range(15):
            self.jugador.sacar_ficha_a_afuera()
        self.assertTrue(self.jugador.gano())

    def test_sacar_ficha_sin_fichas(self):
        self.jugador.__fichas_restantes__ = 0
        self.assertFalse(self.jugador.sacar_ficha_a_afuera())
