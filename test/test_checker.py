import unittest
from core.checker import Ficha

class TestFicha(unittest.TestCase):
    def setUp(self):
        self.ficha = Ficha("Blanca",0)

    def test_obtener_color(self):
        #devuelve el color asignado a la ficha
        self.assertEqual(self.ficha.obtener_color(),"Blanca")

    def test_obtener_posicion_inicial(self):
        #testea si devuelve la posicion inicial pasada en el constructor
        self.assertEqual(self.ficha.obtener_posicion(),0)

    def test_mover_cambia_posicion(self):
        #al mover la ficha,actualiza la posicion correctamente
        self.ficha.mover(5)
        self.assertEqual(self.ficha.obtener_posicion(),5)

    def test_esta_en_barra(self):
        #testea si devuelve si la ficha está en la barra
        self.ficha.mover("barra")
        self.assertTrue(self.ficha.esta_en_barra())

    def test_esta_afuera(self):
        #debe detectar si la ficha está fuera del tablero
        self.ficha.mover("afuera")
        self.assertTrue(self.ficha.esta_afuera())