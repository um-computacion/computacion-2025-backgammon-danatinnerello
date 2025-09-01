import unittest
from core.player import Jugador

class TestJugador(unittest.TestCase):
    def setUp(self):
        self.jugador = Jugador("Dana","blanco")
        #crea un jugador llamado Dana de color blanco

    def test_obtener_nombre(self): #devuelve el nombre asignado al jugador
        self.assertEqual(self.jugador.obtener_nombre(),"Dana")

    def test_obtener_color(self): #devuelve el color asignado al jugador
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
        self.assertTrue(self.jugador.gano()) #por lo tanto gana

    def test_sacar_ficha_sin_fichas(self):
        #si no tiene fichas restantes, no puede sacar mas
        self.jugador.__fichas_restantes__ =0
        self.assertFalse(self.jugador.sacar_ficha_a_afuera())
 
    
    def test_agregar_y_quitar_de_barra(self):
        #testea que funcione el agregar y quitar fichas de la barra
        self.jugador.__barra__ =0
        self.jugador.agregar_a_barra()
        self.assertTrue(self.jugador.tiene_en_barra())
        self.assertTrue(self.jugador.quitar_de_barra())

    def test_quitar_de_barra_sin_fichas(self):
        #si no hay fichas en la barra,quitar debe devolver Falso
        self.jugador.__barra__ = 0
        self.assertFalse(self.jugador.quitar_de_barra())
