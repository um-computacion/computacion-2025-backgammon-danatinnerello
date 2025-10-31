import unittest
from core.board import Tablero
from core.excepcions import MovimientoInvalidoError

class TestTablero(unittest.TestCase):
    def setUp(self):
        self.tablero = Tablero()
        #inicializamos el tablero

    def test_mostrar_contenedor_devuelve_lista(self):
        #testea que el contenedor sea una lista de 24 posiciones
        contenedor = self.tablero.mostrar_contenedor()
        self.assertIsInstance(contenedor, list)
        self.assertEqual(len(contenedor), 24)

    def test_mover_ficha_valido(self):
        # mover una ficha válida de la posición 0 a la 1
        ficha_origen = self.tablero.mostrar_contenedor()[0][-1]
        self.tablero.mover_ficha("Negra", 0, 1)
        self.assertIn(ficha_origen, self.tablero.mostrar_contenedor()[1])


    def test_mover_ficha_desde_vacio_lanza_error(self):
        #nos devuelve error si queremos mover una ficha desde una posicion vacia
        with self.assertRaises(MovimientoInvalidoError):
            self.tablero.mover_ficha("Blanca", 2, 3)

    def test_mover_ficha_fuera_de_rango(self):
        #nos devuelve error si queremos poner una ficha fuera del rango de posiciones
        with self.assertRaises(MovimientoInvalidoError):
            self.tablero.mover_ficha("Negra", 0, 30)

    def test_validar_movimiento_valido(self):
        #Un movimiento válido a una casilla libre nos devuelve verdadero
        tiradas = [1, 2]
        self.assertTrue(self.tablero.validar_movimiento("Negra", 0, 1, tiradas))

    def test_enviar_a_barra(self):
        #si hay fichas en una posicion, debe enviarlas a la barra
        self.tablero.enviar_a_barra(0)
        self.assertIn("Negra", self.tablero.mostrar_barra()["Negra"])

    def test_sacar_ficha_correcta(self):
        #testea que pueda sacra ficha si el color en la posición coincide
        self.assertTrue(self.tablero.sacar_ficha("Negra", 0))
        self.assertIn("Negra", self.tablero.mostrar_afuera()["Negra"])

    def test_sacar_ficha_incorrecta(self):
        #No permite sacar ficha si la posición está vacía o no coincide el color
        self.assertFalse(self.tablero.sacar_ficha("Negra", 5))  # posicion con blancas
 
    def test_mover_ficha_desde_fuera_de_rango(self):
        #testea que lance error si la posicion de origen esto fuera del rango
        with self.assertRaises(MovimientoInvalidoError):
            self.tablero.mover_ficha("Negra", -1, 5)

    def test_enviar_a_barra_posicion_vacia(self):
        #Si la posicion esta vacia, no debe agregar nada a la barra
        self.tablero.enviar_a_barra(2)  # posicion vacia
        self.assertEqual(self.tablero.mostrar_barra()["Blanca"], [])
        self.assertEqual(self.tablero.mostrar_barra()["Negra"], [])

    def test_mover_desde_barra_sin_fichas(self):
        #si no hay fichas en la barra, no se debe mover nada
        resultado = self.tablero.valida_mover_desde_barra("Blanca", 0)
        self.assertFalse(resultado)

    def test_mover_desde_barra_con_ficha_valida(self):
        #mueve una ficha desde la barra a una posicion valida
        self.tablero.mostrar_barra()["Blanca"].append("Blanca")
        valido = self.tablero.valida_mover_desde_barra("Blanca", 22)
        self.assertTrue(valido)
        if valido:
            self.tablero.aplicar_movimiento_desde_barra("Blanca", 22)
        self.assertIn("Blanca", self.tablero.mostrar_contenedor()[22])


    def test_sacar_ficha_color_incorrecto(self):
        #si el color en la posición no coincide, no debe sacar ficha
        # en la posición 5 hay fichas blancas
        resultado = self.tablero.sacar_ficha("Negra", 5)
        self.assertFalse(resultado)

    def test_mostrar_barra_vacia(self):
        # Al iniciar, la barra debe estar vacía para ambos colores
        barra = self.tablero.mostrar_barra()
        self.assertEqual(barra, {"Blanca": [], "Negra": []})

    def test_mostrar_afuera_vacio(self):
        # Al iniciar, afuera debe estar vacío para ambos colores
        afuera = self.tablero.mostrar_afuera()
        self.assertEqual(afuera, {"Blanca": [], "Negra": []})

    def test_todas_en_ultimo_cuadrante_blancas(self):
        # Ponemos todas las fichas blancas en la casa (0-5)
        tablero = Tablero()
        for i in range(24):
            tablero.mostrar_contenedor()[i] = []
        tablero.mostrar_contenedor()[0] = ["Blanca"] * 15
        self.assertTrue(tablero.todas_en_ultimo_cuadrante("Blanca"))

    def test_todas_en_ultimo_cuadrante_negras(self):
        # Ponemos todas las fichas negras en la casa (18-23)
        tablero = Tablero()
        for i in range(24):
            tablero.mostrar_contenedor()[i] = []
        tablero.mostrar_contenedor()[23] = ["Negra"] * 15
        self.assertTrue(tablero.todas_en_ultimo_cuadrante("Negra"))

    def test_todas_en_ultimo_cuadrante_falsa(self):
        # Dejamos una ficha blanca fuera de su cuadrante
        tablero = Tablero()
        tablero.mostrar_contenedor()[10] = ["Blanca"]
        self.assertFalse(tablero.todas_en_ultimo_cuadrante("Blanca"))

    def test_mostrar_estado_devuelve_string(self):
        # mostrar_estado debe devolver un string con 26 líneas (24 + barra + afuera)
        estado = self.tablero.mostrar_estado()
        self.assertIsInstance(estado, str)
        lineas = estado.split("\n")
        self.assertEqual(len(lineas), 26)

    def test_mover_ficha_con_captura(self):
        # Creamos situación con captura: blanca mueve a una posición con 1 negra
        tablero = Tablero()
        for i in range(24):
            tablero.mostrar_contenedor()[i] = []
        tablero.mostrar_contenedor()[0] = ["Negra"]  # una ficha negra sola
        tablero.mostrar_contenedor()[1] = ["Blanca"]  # una blanca que se moverá
        captura = tablero.mover_ficha("Blanca", 1, 0)
        self.assertTrue(captura)
        self.assertIn("Negra", tablero.mostrar_barra()["Negra"])

    def test_mover_desde_barra_bloqueado(self):
        # Preparo un destino bloqueado con 2 negras
        self.tablero.mostrar_barra()["Blanca"].append("Blanca")
        self.tablero.mostrar_contenedor()[10] = ["Negra", "Negra"]
        resultado = self.tablero.valida_mover_desde_barra("Blanca", 10)
        self.assertFalse(resultado)

    def test_enviar_a_barra_agrega_ficha_correctamente(self):
        # ponemos una ficha blanca en posición 0
        self.tablero.mostrar_contenedor()[0] = ["Blanca"]
        self.tablero.enviar_a_barra(0)
        self.assertIn("Blanca", self.tablero.mostrar_barra()["Blanca"])
        self.assertEqual(self.tablero.mostrar_contenedor()[0], [])

    def test_aplicar_movimiento_desde_barra(self):
        self.tablero.mostrar_barra()["Negra"].append("Negra")
        self.tablero.aplicar_movimiento_desde_barra("Negra", 3)
        self.assertIn("Negra", self.tablero.mostrar_contenedor()[3])

    def test_todas_en_ultimo_cuadrante_true(self):
        # forzamos a que todas las blancas estén en 0..5
        self.tablero = Tablero()
        self.tablero.__contenedor__ = [[] for _ in range(24)]
        self.tablero.__contenedor__[0] = ["Blanca"] * 15
        self.assertTrue(self.tablero.todas_en_ultimo_cuadrante("Blanca"))

    def test_todas_en_ultimo_cuadrante_false(self):
        # dejamos una ficha blanca fuera de la casa
        self.tablero.__contenedor__[10].append("Blanca")
        self.assertFalse(self.tablero.todas_en_ultimo_cuadrante("Blanca"))

    def test_mostrar_estado_devuelve_string(self):
        estado = self.tablero.mostrar_estado()
        self.assertIsInstance(estado, str)
        self.assertIn("Barra", estado)
        self.assertIn("Afuera", estado)

    def test_mover_ficha_color_incorrecto(self):
        # Intenta mover la ficha que no es tuya (ej: Blanca intenta mover Negras en punto 1)
        with self.assertRaisesRegex(MovimientoInvalidoError, "Esa ficha no te pertenece"):
            self.tablero.mover_ficha("Blanca", 0, 1)

    def test_mover_ficha_destino_bloqueado(self):
        # Mover Negras de 0 a 2. Posición 2 tiene 2 Blancas (bloqueo).
        self.tablero.mostrar_contenedor()[2] = ["Blanca", "Blanca"]
        with self.assertRaises(MovimientoInvalidoError): 
            self.tablero.mover_ficha("Negra", 0, 2)

    def test_validar_movimiento_sentido_incorrecto(self):
        # Blanca debe moverse hacia índice 0. Intenta moverse de 5 a 7 (hacia índice mayor).
        tiradas = [2]
        self.assertFalse(self.tablero.validar_movimiento("Blanca", 5, 7, tiradas))

    def test_validar_movimiento_dado_no_disponible(self):
        # Intenta mover 5 espacios, pero solo queda dado 1.
        tiradas = [1]
        self.assertFalse(self.tablero.validar_movimiento("Negra", 0, 5, tiradas))
    
    def test_validar_movimiento_destino_bloqueado(self):
        # Colocar 2 fichas enemigas en destino. Comprueba el retorno False.
        self.tablero.mostrar_contenedor()[0] = ["Negra", "Negra"] 
        # Mover Blanca de 5 a 0 (inválido). tiradas_restantes debe ser None para probar la rama más general.
        self.assertFalse(self.tablero.validar_movimiento("Blanca", 5, 0))

    def test_valida_mover_desde_barra_sin_tiradas_param(self):
        # Comprueba la rama donde tiradas_restantes no se pasa (es None) en el método valida_mover_desde_barra.
        self.tablero.mostrar_barra()["Blanca"].append("Blanca")
        # El método debe devolver True si la posición está libre, ignorando las tiradas
        self.assertTrue(self.tablero.valida_mover_desde_barra("Blanca", 22, tiradas_restantes=None))

if __name__ == "__main__":
    unittest.main()
