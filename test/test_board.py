import unittest
from core.board import Tablero

class TestTablero(unittest.TestCase):
    def setUp(self):
        self.tablero = Tablero()

    def test_mostrar_contenedor_devuelve_lista(self):
        contenedor = self.tablero.mostrar_contenedor()
        self.assertIsInstance(contenedor,list)
        self.assertEqual(len(contenedor),24)

    def test_mover_ficha_valido(self):
        # mover una ficha válida de la posición 0 a la 1
        ficha_origen = self.tablero.mostrar_contenedor()[0][-1]
        self.tablero.mover_ficha(ficha_origen, 0, 1)
        self.assertIn(ficha_origen, self.tablero.mostrar_contenedor()[1])

    def test_mover_ficha_desde_vacio_lanza_error(self):
        with self.assertRaises(ValueError):
            self.tablero.mover_ficha("Blanca",2,3)

    def test_mover_ficha_fuera_de_rango(self):
        with self.assertRaises(ValueError):
            self.tablero.mover_ficha("Negra",0,30)
 

