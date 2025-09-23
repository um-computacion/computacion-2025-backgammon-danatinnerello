import unittest
from unittest.mock import patch
import cli.cli as cli
from core.player import Jugador


class TestCLI(unittest.TestCase):
    def run_cli_with_inputs(self, inputs,  interactive=False):
        # ejecuta el main con entradas simuladas
        with patch("builtins.input", side_effect=inputs + [EOFError]), \
             patch("builtins.print") as mock_print:
            try:
                cli.main(interactive=interactive)
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
        self.assertTrue(any("debe estar entre 1 y 24" in line for line in salida))

    def test_movimiento_sin_fichas(self):
        #posicion 2 arranca vacia
        salida= self.run_cli_with_inputs(["Dana", "abi", "2", "3"])
        self.assertTrue(any("no hay fichas" in line for line in salida))

    def test_movimiento_ficha_otro_color(self):
        #turnode la Blanca pero intenta mover desde posicion 0 que hya fichas negras
        salida= self.run_cli_with_inputs(["Dana", "abi", "1", "2"])
        self.assertTrue(any("esa ficha no te pertenece" in line for line in salida))

    def test_sacar_ficha_no_permitido(self):
        #intenta sacar desde 12 (Blanca, pero no estan todas en el ultimo cuadrante)
        salida= self.run_cli_with_inputs(["Dana", "abi", "13", "-1"])
        self.assertTrue(any("no puedes sacar fichas" in line for line in salida))

    def test_movimiento_normal_valido(self):
    #establecemos un contenedor con una ficha Blanca en la ultima posicion
        cont = [[] for _ in range(24)]
        cont[23] = ["Blanca"]

        with patch("core.board.Tablero.mostrar_contenedor", return_value=cont), \
            patch("core.dice.Dados.usar_tirada", return_value=True), \
            patch("core.board.Tablero.validar_movimiento", return_value=True), \
            patch("core.board.Tablero.mover_ficha", return_value=False):
            salida = self.run_cli_with_inputs(["Dana", "abi", "24", "23"])
        #verifica que se haya impreso un movimiento de ficha
        self.assertTrue(
            any("ficha movida de" in line for line in salida))
    
    def test_movimiento_desde_barra_invalido(self):
        # Forzamos que la barra tenga fichas pero el movimiento sea inválido
        with patch("core.board.Tablero.mostrar_barra", return_value={"Blanca": ["ficha"], "Negra": []}), \
             patch("core.board.Tablero.mover_desde_barra", return_value=False):
            salida = self.run_cli_with_inputs(["Ana", "Beto", "3"])
        self.assertTrue(any("movimiento invalido desde la barra" in line for line in salida))

    def test_movimiento_desde_barra_valido(self):
        # Ficha en barra y movimiento exitoso
        with patch("core.board.Tablero.mostrar_barra", return_value={"Blanca": ["ficha"], "Negra": []}), \
             patch("core.board.Tablero.mover_desde_barra", return_value=True), \
             patch("core.dice.Dados.usar_tirada", return_value=True):
            salida = self.run_cli_with_inputs(["Ana", "Beto", "3"])
        self.assertTrue(any("ficha movida de la barra a la posiciion" in line for line in salida))

    def test_sacar_ficha_valido(self):
        # Todas en el último cuadrante y dado correcto
        with patch("core.board.Tablero.todas_en_ultimo_cuadrante", return_value=True), \
             patch("core.board.Tablero.sacar_ficha", return_value=True), \
             patch("core.dice.Dados.usar_tirada", return_value=True):
            salida = self.run_cli_with_inputs(["Ana", "Beto", "24", "-1"])
        self.assertTrue(any("ficha sacada desde" in line for line in salida))

    def test_sacar_ficha_no_puedes_por_dado(self):
        # Todas en el último cuadrante pero no hay dado válido
        with patch("core.board.Tablero.todas_en_ultimo_cuadrante", return_value=True), \
             patch("core.board.Tablero.sacar_ficha", return_value=False), \
             patch("core.dice.Dados.usar_tirada", return_value=False):
            salida = self.run_cli_with_inputs(["Ana", "Beto", "24", "-1"])
        self.assertTrue(any("No puedes sacar una ficha desde esa posicion" in line for line in salida))

    def test_input_invalido_en_movimiento(self):
        # Forzar que se ingrese algo no numérico
        salida = self.run_cli_with_inputs(["dana", "caro", "abc"])
        self.assertTrue(any("Error:" in line for line in salida))

    def test_opcion_rendirse(self):
        salida = self.run_cli_with_inputs(["dana","caro","2"], interactive=True)
        self.assertTrue(any("se ha rendido" in line for line in salida))

    def test_opcion_salir(self):
        salida = self.run_cli_with_inputs(["dana","caro","3"], interactive=True)
        self.assertTrue(any("Juego finalizado por el usuario" in line for line in salida))

    def test_opcion_invalida(self):
        salida = self.run_cli_with_inputs(["dana","caro","99","1"], interactive=True)
        self.assertTrue(any("Opcion invalida" in line for line in salida))


    def test_movimiento_invalido_por_validacion(self):
        # Forzamos que validar_movimiento devuelva False para provocar "movimiento invalido"
        cont = [[] for _ in range(24)]
        cont[0] = ["Blanca"]  # una ficha válida en la primera posición
        with patch("core.board.Tablero.mostrar_contenedor", return_value=cont), \
            patch("core.dice.Dados.usar_tirada", return_value=True), \
            patch("core.board.Tablero.validar_movimiento", return_value=False):
            salida = self.run_cli_with_inputs(["Ana", "Beto", "1", "2"])
        self.assertTrue(any("movimiento invalido" in line for line in salida))


    def test_captura_de_ficha(self):
        # Simulamos que mover_ficha devuelve True → captura
        cont = [[] for _ in range(24)]
        cont[0] = ["Blanca"]
        with patch("core.board.Tablero.mostrar_contenedor", return_value=cont), \
            patch("core.dice.Dados.usar_tirada", return_value=True), \
            patch("core.board.Tablero.validar_movimiento", return_value=True), \
            patch("core.board.Tablero.mover_ficha", return_value=True):
            salida = self.run_cli_with_inputs(["Ana", "Beto", "1", "2"])
        self.assertTrue(any("capturaste una ficha enemiga" in line for line in salida))

    def test_tirada_doble(self):
        # Simulamos tirada doble (cuatro dados) y forzamos salida inmediata
        jugador_falso = Jugador("Fake", "Blanca")
        with patch("core.dice.Dados.tirar_dados", return_value=[3, 3, 3, 3]), \
            patch("core.dice.Dados.quedan_tiradas", return_value=False), \
            patch("core.game.Juego.verificar_ganador", return_value=jugador_falso):
            salida = self.run_cli_with_inputs(["Ana", "Beto"])
        # Verificamos que salió el mensaje de tirada doble
        self.assertTrue(any("Tirada doble:" in line for line in salida))


    def test_ganador_detectado(self):
        # Simulamos que ya hay un ganador al inicio
        jugador_falso = Jugador("Test", "Blanca")
        with patch("core.dice.Dados.tirar_dados", return_value=[1, 2]), \
            patch("core.dice.Dados.quedan_tiradas", return_value=False), \
            patch("core.game.Juego.verificar_ganador", return_value=jugador_falso):
            salida = self.run_cli_with_inputs(["Ana", "Beto"])
        # Verificamos que el mensaje de ganador aparezca
        self.assertTrue(any("ganoo Test.Color Blanca" in line for line in salida))

        

if __name__ == "__main__":
    unittest.main()
