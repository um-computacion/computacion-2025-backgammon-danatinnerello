## Registro de Prompts de IA
### Prompt 1

- Modelo / herramienta usada: ChatGPT GPT-5 (Agosto 2025)

- Instrucciones del sistema: (Ninguna especial, salvo configuración por defecto de ChatGPT)

- Prompt exacto usado: " me sale que de board tengo poco porcentaje cubierto. me podes hacer mas test para aumentarlo. fijate qu no se repitan "

- Respuesta completa de la IA: 
¡Perfecto! 🚀 Viendo tu clase Tablero, todavía hay varios caminos que no están testeados. Por ejemplo:
En mover_ficha: el caso cuando desde está fuera de rango.
En enviar_a_barra: cuando la posición está vacía (no debería fallar).
En mover_desde_barra: cuando no hay fichas en la barra o cuando el movimiento es inválido.
En sacar_ficha: cuando hay fichas pero de distinto color.
Te paso un bloque de tests adicionales para test_board.py (todos con docstrings y sin repetir lo que ya tenés):
    def test_mover_ficha_desde_fuera_de_rango(self):
        """Debe lanzar error si la posición de origen está fuera del rango"""
        with self.assertRaises(ValueError):
            self.tablero.mover_ficha("Negra", -1, 5)

    def test_enviar_a_barra_posicion_vacia(self):
        """Si la posición está vacía, no debe agregar nada a la barra"""
        self.tablero.enviar_a_barra(2)  # posición vacía
        self.assertEqual(self.tablero._Tablero__barra__["Blanca"], [])
        self.assertEqual(self.tablero._Tablero__barra__["Negra"], [])

    def test_mover_desde_barra_sin_fichas(self):
        """Si no hay fichas en la barra, no se debe mover nada"""
        resultado = self.tablero.mover_desde_barra("Blanca", 3)
        self.assertFalse(resultado)

    def test_mover_desde_barra_con_ficha_valida(self):
        """Debe mover una ficha desde la barra a una posición válida"""
        self.tablero._Tablero__barra__["Blanca"].append("Blanca")
        resultado = self.tablero.mover_desde_barra("Blanca", 3)
        self.assertTrue(resultado)
        self.assertIn("Blanca", self.tablero.mostrar_contenedor()[3])

    def test_sacar_ficha_color_incorrecto(self):
        """Si el color en la posición no coincide, no debe sacar ficha"""
        # en la posición 5 hay fichas blancas
        resultado = self.tablero.sacar_ficha("Negra", 5)
        self.assertFalse(resultado)

- Uso de la salida: usada 

- Referencia en archivos finales: test/ test_board.py

### Prompt 2

- Modelo / herramienta usada: ChatGPT GPT-5 (Agosto 2025)

- Instrucciones del sistema: (Ninguna especial, salvo configuración por defecto de ChatGPT)

- Prompt exacto usado: " y de game tambien por favor  "
- Respuesta completa de la IA: 
¡Genial! 🙌 Me fijo en tu clase Juego (game.py).
Actualmente tus tests (test_game.py) solo prueban:
verificar_ganador cuando nadie gana.
controlar_turnos cambiando de jugador 1 → jugador 2.
Pero faltan varios caminos:
controlar_turnos de vuelta (jugador 2 → jugador 1).
verificar_ganador cuando un jugador realmente gana.
Que verificar_ganador devuelva None si todavía no hay ganador (ya lo tenés, pero se puede reforzar después de un cambio).
Que __juego_terminado__ cambie a True al encontrar un ganador.
Te paso tests adicionales para test_game.py con docstrings y sin repetir lo que ya tenés:
    def test_controlar_turnos_de_jugador2_a_jugador1(self):
        """Si es el turno del jugador2, debe pasar al jugador1"""
        self.juego.__turno__ = self.juego.__jugador2__
        self.juego.controlar_turnos()
        self.assertEqual(self.juego.__turno__, self.juego.__jugador1__)

    def test_verificar_ganador_con_jugador1(self):
        """Debe detectar cuando el jugador1 gana"""
        # simulamos que jugador1 no tiene fichas restantes
        self.juego._Juego__jugador1__._Jugador__fichas_restantes__ = 0
        ganador = self.juego.verificar_ganador()
        self.assertEqual(ganador, self.juego.__jugador1__)
        self.assertTrue(self.juego._Juego__juego_terminado__)

    def test_verificar_ganador_con_jugador2(self):
        """Debe detectar cuando el jugador2 gana"""
        # simulamos que jugador2 no tiene fichas restantes
        self.juego._Juego__jugador2__._Jugador__fichas_restantes__ = 0
        ganador = self.juego.verificar_ganador()
        self.assertEqual(ganador, self.juego.__jugador2__)
        self.assertTrue(self.juego._Juego__juego_terminado__)

    def test_verificar_ganador_sin_ganador_retorna_none(self):
        """Si nadie ganó, debe devolver None y no terminar el juego"""
        resultado = self.juego.verificar_ganador()
        self.assertIsNone(resultado)
        self.assertFalse(self.juego._Juego__juego_terminado__)

- Uso de la salida: Usada 
- Referencia en archivos finales: test/test_game.py

### Prompt 3

- Modelo / herramienta usada: ChatGPT GPT-5 (Agosto 2025)

- Instrucciones del sistema: (Ninguna especial, salvo configuración por defecto de ChatGPT)

- Prompt exacto usado: " Hola, buenas. Mira, necesito que me ayudes. Me sale ese error. Quiero hacer un pull. Porque en git, tengo en el archivo tsli, tengo muchísimos tests, que en github me salen, pero acá no. Y tengo miedo que si hago un commit, me quede el archivo sin nada, en vez de con todo. ¿Cómo puedo hacer para que esté igual lo que tengo en git a lo que tengo acá en visual? "
- Respuesta completa de la IA: 
¡Perfecto, veo lo que pasó! 👀

El error que te aparece dice:
error: Los siguientes archivos locales serán sobrescritos al fusionar:
    core/__pycache__/board.cpython-311.pyc
    ...
Por favor, comitea tus cambios o guárdalos en el stash antes de fusionar.
Eso significa que Git no te deja hacer git pull porque tenés cambios locales (o archivos generados como los .pyc) que entrarían en conflicto con lo que hay en GitHub.

Vos querés asegurarte de que tu repo local quede exactamente igual a lo que está en GitHub (o sea, “tirar lo local y dejar lo remoto”).

👉 Tenés varias formas de hacerlo, según lo que quieras:
🚨 Opción 1: Descartar todos tus cambios locales y dejar tu repo igual al remoto

Si no te importa perder lo que tenés localmente:
git fetch --all
git reset --hard origin/main
Eso va a dejar tu repo local idéntico al de GitHub (se borran cambios locales).
⚡ Opción 2: Guardar lo que tenés localmente por las dudas

Si no querés perder nada, podés usar stash antes de hacer el pull:
git stash
git pull
Después, si querés recuperar tus cambios locales:
git stash pop
🚫 Nota importante

Los archivos que te marca (por ejemplo los __pycache__) son archivos generados automáticamente por Python, no deberían estar versionados en Git. Para evitar ese problema, se suele usar un archivo .gitignore con algo así:
__pycache__/
*.pyc

- Uso de la salida: Usada 

- Referencia en archivos finales: 

### Prompt 4

- Modelo / herramienta usada: ChatGPT GPT-5 (Agosto 2025)

- Instrucciones del sistema: (Ninguna especial, salvo configuración por defecto de ChatGPT)

- Prompt exacto usado: " tengo un porcentaje de 67 porciento cubierto me ayudas a hacer mas test del cli para aumentar ese porcentaje. hacelos con unittest, basandote en mi codigo, sin repetir test anteriores y sin errores por favor "

- Respuesta completa de la IA: 
¡Perfecto 🚀! Ya tenés una buena base de cobertura (~67%). Para subir ese porcentaje hay que cubrir ramas del código que todavía no tocamos en tu cli.py.

Repasando tu main() hay varias situaciones que faltan:

Movimiento inválido desde la barra (mover_desde_barra devuelve False).

Movimiento válido desde la barra (ficha pasa de la barra al tablero).

Sacar ficha válido (cuando todas están en el último cuadrante).

No se puede sacar ficha porque no hay dado adecuado.

Error en la tirada → si se ingresa un valor no numérico al pedir posiciones/dados.

📂 test/test_cli_extra.py
import unittest
from unittest.mock import patch
import cli.cli as cli


class TestCLIExtra(unittest.TestCase):

    def run_cli_with_inputs(self, inputs):
        """Ejecuta cli.main con entradas simuladas y devuelve los prints."""
        with patch("builtins.input", side_effect=inputs + [EOFError]), \
             patch("builtins.print") as mock_print:
            try:
                cli.main()
            except (EOFError, SystemExit):
                pass
        return [" ".join(map(str, args)) for args, _ in mock_print.call_args_list]

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
            salida = self.run_cli_with_inputs(["Ana", "Beto", "23", "-1"])
        self.assertTrue(any("ficha sacada desde" in line for line in salida))

    def test_sacar_ficha_no_puedes_por_dado(self):
        # Todas en el último cuadrante pero no hay dado válido
        with patch("core.board.Tablero.todas_en_ultimo_cuadrante", return_value=True), \
             patch("core.board.Tablero.sacar_ficha", return_value=False), \
             patch("core.dice.Dados.usar_tirada", return_value=False):
            salida = self.run_cli_with_inputs(["Ana", "Beto", "23", "-1"])
        self.assertTrue(any("No puedes sacar una ficha desde esa posicion" in line for line in salida))

    def test_input_invalido_en_movimiento(self):
        # Forzar que se ingrese algo no numérico
        salida = self.run_cli_with_inputs(["Ana", "Beto", "abc"])
        self.assertTrue(any("Error:" in line for line in salida))


if __name__ == "__main__":
    unittest.main()
✅ Qué cubren estos tests nuevos

Movimiento desde la barra inválido (línea print("movimiento invalido desde la barra")).

Movimiento desde la barra válido (línea print("ficha movida de la barra...")).

Sacar ficha correctamente (línea print("ficha sacada desde...")).

No poder sacar ficha por falta de dado (línea "No puedes sacar...").

Error al ingresar un valor no numérico (captura el ValueError y su print("Error: ...")).

⚡ Con estos tests deberías cubrir casi todos los caminos del CLI y subir bastante tu cobertura.

- Uso de la salida: Usada

- Referencia en archivos finales: test/test_cli.py