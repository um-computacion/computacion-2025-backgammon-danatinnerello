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
