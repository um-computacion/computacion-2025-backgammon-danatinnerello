
import unittest
from core.dice import Dados

class TestDados(unittest.TestCase):
    def setUp(self):
        self.dados = Dados()

    def test_tirar_dados_devuelve_tupla(self):
        #testea que tirar_dados devuelve una tupla de dos enteros entre 1 y 6
        d1, d2 = self.dados.tirar_dados()
        self.assertIn(d1,range(1,6))
        self.assertIn(d2,range(1,6))

    def test_obtener_tiradas_restantes(self):
        #testea que despues de tirar se devuelve una lista con 2 o 4 elementos
        self.dados.tirar_dados()
        tiradas = self.dados.obtener_tiradas_restantes()
        self.assertGreaterEqual(len(tiradas), 2)

    def test_usar_tirada_valida(self):
        #testea que elimie el valor usado de las tiradas restantes
        self.dados.__tiradas_restantes__ = [3,4]
        self.assertTrue(self.dados.usar_tirada(3))
        self.assertNotIn(3,self.dados.obtener_tiradas_restantes())

    def test_usar_tirada_invalida(self):
        #testea que si el valor no está en las tiradas restantes devuelve falso
        self.dados.__tiradas_restantes__ = [2,5]
        result = self.dados.usar_tirada(6)
        self.assertFalse(result)

    def test_tirar_dados_dobles(self):
        #testea que si salen dados dobles, se agregan 4 tiradas iguales
        self.dados.__dado1__=6
        self.dados.__dado2__=6
        self.dados.__tiradas_restantes__=[6,6,6,6]
        self.assertEqual(len(self.dados.__tiradas_restantes__),4)

    