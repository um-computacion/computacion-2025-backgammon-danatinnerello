import unittest
from unittest.mock import patch
from cli.cli import main
import cli
from core.player import Jugador
from core.excepcions import (
    MovimientoInvalidoError,
    SacarFichaError,
    EntradaInvalidaError,
)


class TestCLI(unittest.TestCase):
    def run_cli_with_inputs(self, inputs):
        with patch("builtins.input", side_effect=inputs + [EOFError]), patch(
            "builtins.print"
        ) as mock_print:
            try:
                cli.cli.main()
            except (EOFError, SystemExit):
                pass
        return [" ".join(map(str, args)) for args, _ in mock_print.call_args_list]

    def test_inicio_juego(self):
        salida = self.run_cli_with_inputs(["Dana", "abi", "3"])
        self.assertTrue(any("Bienvenidos al juego" in line for line in salida))

    def test_opcion_invalida(self):
        salida = self.run_cli_with_inputs(["Dana", "abi", "99", "3"])
        # Se acepta tanto con tilde/punto como sin ellos
        self.assertTrue(any("Error: Opcion no valida" in line for line in salida))

    def test_rendirse(self):
        salida = self.run_cli_with_inputs(["Dana", "abi", "2"])
        self.assertTrue(any("se ha rendido" in line for line in salida))

    def test_salir(self):
        salida = self.run_cli_with_inputs(["Dana", "abi", "3"])
        self.assertTrue(any("Juego finalizado" in line for line in salida))

    def test_movimiento_normal_valido(self):
        # Mock debe devolver (Captura, Lista de Dados)
        with patch(
            "core.game.Juego.valida_mover_ficha", return_value=(False, [1])
        ):  # <--- CAMBIO AQUÍ
            salida = self.run_cli_with_inputs(["Dana", "abi", "1", "24", "23", "3"])
        self.assertTrue(any("Ficha movida de 24 a 23" in line for line in salida))

    def test_movimiento_normal_captura(self):
        # Mock debe devolver (Captura=True, Lista de Dados)
        with patch(
            "core.game.Juego.valida_mover_ficha", return_value=(True, [1])
        ):  # <--- CAMBIO AQUÍ
            salida = self.run_cli_with_inputs(
                ["Dana", "abi", "1", "1", "12", "11", "3"]
            )
        self.assertTrue(any("Capturaste una ficha enemiga" in line for line in salida))

    def test_movimiento_desde_barra(self):
        with patch("core.game.Juego.valida_mover_desde_barra", return_value=True):
            salida = self.run_cli_with_inputs(["Dana", "abi", "1", "0", "5", "3"])
        self.assertTrue(
            any("Ficha movida desde la barra a 5" in line for line in salida)
        )

    def test_sacar_ficha_valido(self):
        with patch("core.game.Juego.valida_sacar_ficha", return_value=True):
            salida = self.run_cli_with_inputs(["Dana", "abi", "1", "24", "-1", "3"])
        self.assertTrue(any("Ficha sacada desde 24" in line for line in salida))

    def test_movimiento_invalido_excepcion(self):
        with patch(
            "core.game.Juego.valida_mover_ficha",
            side_effect=MovimientoInvalidoError("Movimiento inválido"),
        ):
            salida = self.run_cli_with_inputs(["Dana", "abi", "1", "6", "5", "3"])
        self.assertTrue(any("Error: Movimiento inválido" in line for line in salida))

    def test_sacar_ficha_excepcion(self):
        with patch(
            "core.game.Juego.valida_sacar_ficha",
            side_effect=SacarFichaError("No puedes sacar fichas"),
        ):
            salida = self.run_cli_with_inputs(["Dana", "abi", "1", "12", "-1", "3"])
        self.assertTrue(any("Error: No puedes sacar fichas" in line for line in salida))

    def test_movimiento_invalido_fuera_de_rango(self):
        salida = self.run_cli_with_inputs(["Dana", "abi", "1", "30", "2", "3"])
        self.assertTrue(
            any("Error: Movimiento o destino inválido" in line for line in salida)
        )

    def test_reingreso_con_captura(self):
        # Asegura que la CLI muestre el mensaje de captura en reingreso
        with patch("core.game.Juego.valida_mover_desde_barra", return_value=True):
            salida = self.run_cli_with_inputs(["Dana", "abi", "1", "0", "5", "3"])
        self.assertTrue(any("¡Captura!" in line for line in salida))

    def test_pedir_int_falla_por_valor(self):
        # Asegura que la función pedir_int lance la excepción correcta (cubre la línea 'except ValueError')
        with patch("builtins.input", side_effect=["abc", "3"]), patch(
            "cli.cli.main"
        ), self.assertRaises(EntradaInvalidaError):
            cli.cli.pedir_int("Mensaje:")

    def test_opcion_invalida_numerica_lanza_error(self):
        # Simula una entrada numérica que no es 1, 2, o 3
        salida = self.run_cli_with_inputs(
            ["Dana", "abi", "1", "1", "24", "23", "99", "3"]
        )
        self.assertTrue(any("Opción no válida" in line for line in salida))

    def test_opcion_invalida_numerica_lanza_error(self):
        with patch("core.game.Juego.valida_mover_ficha", return_value=(True, [1])):

            # 2. Secuencia de inputs:
            # - Nombres: "Dana", "abi"
            # - Primer Menú: "1" (Mover)
            # - Movimiento: "10", "11" (Orígen y Destino)
            # - Segundo Menú: "99" (Inválido, lanza excepción)
            # - Tercer Menú: "3" (Salir)
            salida = self.run_cli_with_inputs(
                ["Dana", "abi", "1", "10", "11", "99", "3"]
            )

        # La aserción busca el mensaje de error impreso.
        self.assertTrue(any("Error: Opcion no valida" in line for line in salida))


if __name__ == "__main__":
    unittest.main()
