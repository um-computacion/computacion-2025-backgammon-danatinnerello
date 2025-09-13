import unittest
from unittest.mock import patch
import cli.cli as cli
from core.player import Jugador


class TestCLI(unittest.TestCase):

    def run_cli_with_inputs(self, inputs):
        # ejecuta el main con entradas simuladas
        with patch("builtins.input", side_effect=inputs + [EOFError]), \
             patch("builtins.print") as mock_print:
            try:
                cli.main()
            except (EOFError, SystemExit): 
                #al final lanza EOFError para cortar el bucle infinito
                pass
            #Devuelve todos los prints capturados como lista de strings.
        return [" ".join(map(str, args)) for args, _ in mock_print.call_args_list] 

    def test_inicio_juego(self):
        salida= self.run_cli_with_inputs(["Dana", "abi"])
        self.assertIn("Bienvenidos al juego Backgammon", salida[0])
        self.assertTrue(any("Turno de:" in line for line in salida))

    def test_movimiento_fuera_de_rango(self):
        salida= self.run_cli_with_inputs(["Dana", "abi", "25", "0"])
        self.assertTrue(any("debe estar entre 0 y 23" in line for line in salida))

    def test_movimiento_sin_fichas(self):
        #posicion 2 arranca vacia
        salida= self.run_cli_with_inputs(["Dana", "abi", "2", "3"])
        self.assertTrue(any("no hay fichas" in line for line in salida))

    def test_movimiento_ficha_otro_color(self):
        #turnode la Blanca pero intenta mover desde posicion 0 que hya fichas negras
        salida= self.run_cli_with_inputs(["Dana", "abi", "0", "1"])
        self.assertTrue(any("esa ficha no te pertenece" in line for line in salida))

    def test_sacar_ficha_no_permitido(self):
        #intenta sacar desde 12 (Blanca, pero no estan todas en el ultimo cuadrante)
        salida= self.run_cli_with_inputs(["Dana", "abi", "12", "-1"])
        self.assertTrue(any("no puedes sacar fichas" in line for line in salida))

    def test_movimiento_normal_valido(self):
        #mover dados de 23 a 22 (Blanca)
        with patch("random.randint", return_value=1):
            salida= self.run_cli_with_inputs(["Dana", "abi", "23", "22"])
        self.assertTrue(any("ficha movida de 23 a 22" in line for line in salida))



if __name__ == "__main__":
    unittest.main()
