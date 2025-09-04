
import unittest
from core.dice import Dados
from unittest.mock import patch

class TestDados(unittest.TestCase):
    def setUp(self):
        self.dados = Dados()

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

    @patch('random.randint', side_effect=[5, 2])
    def test_simple(self, randint_patched):
        dice = self.dados.tirar_dados()
        self.assertEqual(len(dice), 2)
        self.assertEqual(dice[0], 5)
        self.assertEqual(dice[1], 2)
        self.assertTrue(randint_patched.called)
        self.assertEqual(randint_patched.call_count, 2)

    @patch('random.randint', return_value=1)
    def test_complex(self, randint_patched):
        dice = self.dados.tirar_dados()
        self.assertEqual(len(dice), 4)
        self.assertEqual(dice[0], 1)
        self.assertEqual(dice[1], 1)
        self.assertEqual(dice[2], 1)
        self.assertEqual(dice[3], 1)
        self.assertTrue(randint_patched.called)
        self.assertEqual(randint_patched.call_count, 2)

    