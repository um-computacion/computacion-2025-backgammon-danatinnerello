import unittest
from core.board import Tablero

class TestTablero(unittest.TestCase):
    def setUp(self):
        self.tablero = Tablero()
        #inicializamos el tablero 

    def test_mostrar_contenedor_devuelve_lista(self):
        #testea que el contenedor sea una lista de 24 posiciones
        contenedor = self.tablero.mostrar_contenedor()
        self.assertIsInstance(contenedor,list)
        self.assertEqual(len(contenedor),24)

    def test_mover_ficha_valido(self):
        # mover una ficha válida de la posición 0 a la 1
        ficha_origen = self.tablero.mostrar_contenedor()[0][-1]
        self.tablero.mover_ficha(ficha_origen, 0, 1)
        self.assertIn(ficha_origen, self.tablero.mostrar_contenedor()[1])

    def test_mover_ficha_desde_vacio_lanza_error(self):
        #nos devuelve error si queremos mover una ficha desde una posicion vacia
        with self.assertRaises(ValueError):
            self.tablero.mover_ficha("Blanca",2,3)

    def test_mover_ficha_fuera_de_rango(self): 
        #nos devuelve error si queremos poner una ficha fuera del rango de posiciones
        with self.assertRaises(ValueError):
            self.tablero.mover_ficha("Negra",0,30)
 

    def test_validar_movimiento_valido(self):
        #Un movimiento válido a una casilla libre nos devuelve verdadero
        self.assertTrue(self.tablero.validar_movimiento("Negra",1))

    def test_validar_movimiento_invalido_por_rango(self):
        #testea que si el destino está fuera del rango 0-23 devuelva falso
        self.assertFalse(self.tablero.validar_movimiento("Blanca",30))

    def test_enviar_a_barra(self):
        #si hay fichas en una posicion, debe enviarlas a la barra
        self.tablero.enviar_a_barra(0)
        self.assertIn("Negra", self.tablero.mostrar_barra()["Negra"])

    def test_sacar_ficha_correcta(self):
        #testea que pueda sacra ficha si el color en la posición coincide
        self.assertTrue(self.tablero.sacar_ficha("Negra",0))
        self.assertIn("Negra", self.tablero.mostrar_afuera()["Negra"])

    def test_sacar_ficha_incorrecta(self):
        #No permite sacar ficha si la posición está vacía o no coincide el color
        self.assertFalse(self.tablero.sacar_ficha("Negra",5))  # posicion con blancas

    def test_mover_ficha_desde_fuera_de_rango(self):
        #testea que lance error si la posicion de origen esto fuera del rango
        with self.assertRaises(ValueError):
            self.tablero.mover_ficha("Negra",-1,5)

    def test_enviar_a_barra_posicion_vacia(self):
        #Si la posicion esta vacia, no debe agregar nada a la barra
        self.tablero.enviar_a_barra(2)  # posicion vacia
        self.assertEqual(self.tablero.mostrar_barra()["Blanca"],[])
        self.assertEqual(self.tablero.mostrar_barra()["Negra"],[])

    def test_mover_desde_barra_sin_fichas(self):
        #si no hay fichas en la barra, no se debe mover nada
        resultado = self.tablero.mover_desde_barra("Blanca",3)
        self.assertFalse(resultado)

    def test_mover_desde_barra_con_ficha_valida(self):
        #mueve una ficha desde la barra a una posicion valida
        self.tablero.mostrar_barra()["Blanca"].append("Blanca")
        resultado=self.tablero.mover_desde_barra("Blanca",3)
        self.assertTrue(resultado)
        self.assertIn("Blanca",self.tablero.mostrar_contenedor()[3])

    def test_sacar_ficha_color_incorrecto(self):
        #si el color en la posición no coincide, no debe sacar ficha
        # en la posición 5 hay fichas blancas
        resultado=self.tablero.sacar_ficha("Negra",5)
        self.assertFalse(resultado)