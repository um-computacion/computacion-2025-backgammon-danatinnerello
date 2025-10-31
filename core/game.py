''' Responsabilidades: controlador principal

-Iniciar tablero,jugadores y dados
-controlar turnos
-verificar ganador 
-interactuar con el CLI o Pygame                        

'''
from core.board import Tablero
from core.dice import Dados
from core.player import Jugador
from core.excepcions import (
    MovimientoInvalidoError,
    SacarFichaError,
)

class Juego:
    def __init__(self,nombre_jugador1:Jugador,nombre_jugador2:Jugador,tablero:Tablero = None,dados: Dados =None):
        self.__tablero__ = tablero if tablero else Tablero()
        self.__jugador1__ = nombre_jugador1
        self.__jugador2__ = nombre_jugador2
        self.__jugadores__= [self.__jugador1__, self.__jugador2__]
        self.__dados__ = dados if dados else Dados()
        self.__turno__ = self.__jugador1__
        self.__juego_terminado__ = False

    def mostrar_jugador1(self):
        return self.__jugador1__
    
    def mostrar_jugador2(self):
        return self.__jugador2__

    def mostrar_juego_terminado(self):
        return self.__juego_terminado__
    
    def mostrar_tablero(self):
        return self.__tablero__
    
    def controlar_turnos(self):
        if self.__turno__ == self.__jugador1__: #si tiro el jugador uno, lo cambia al otro
            self.__turno__ = self.__jugador2__
        else:  # y sino al reves
            self.__turno__ = self.__jugador1__

    def mostrar_turno(self):
        return self.__turno__

    def verificar_ganador(self):
        for jugador in self.__jugadores__: #si el jugador primero esta en jugadores
            if jugador.gano(): #segundo llama al metodo gano
                self.__juego_terminado__ = True #si gano cambia el estado del juego
                return jugador
        return None

    def valida_mover_ficha(self, jugador:Jugador, desde, hacia,):
        desde_index = desde - 1
        hacia_index = hacia - 1
        color = jugador.obtener_color()

        # Validación de destino abierto 
        if not self.__tablero__.validar_movimiento(color, desde_index, hacia_index):
            raise MovimientoInvalidoError("Movimiento o destino inválido (destino bloqueado o dirección incorrecta)")

        try:
            # ENCONTRAR QUÉ DADO(S) USAR Y VALIDAR PASOS INTERMEDIOS
            dado_principal, dado_secundario = self._encontrar_dado_y_tipo_movimiento(jugador, desde_index, hacia_index)
        except MovimientoInvalidoError as e:
            raise MovimientoInvalidoError(f"Movimiento inválido: {e}")

        dados_consumidos = []
        
        if dado_secundario is None:
            # CONSUMIR UN SOLO DADO (Movimiento Simple)
            if not self.__dados__.usar_tirada(dado_principal):
                raise MovimientoInvalidoError(f"Error al consumir el dado {dado_principal}. El dado ya no está disponible.")
            dados_consumidos = [dado_principal]
        else:
            # CONSUMIR DOS DADOS (Movimiento Compuesto)
            # Consumimos ambos dados y revertimos si el segundo falla.
            if not self.__dados__.usar_tirada(dado_principal):
                raise MovimientoInvalidoError(f"No se pudo usar el primer dado ({dado_principal}).")
            
            if not self.__dados__.usar_tirada(dado_secundario):
                # Reversión de la tirada anterior para mantener el estado
                self.__dados__.usar_tirada(dado_principal, revertir=True)
                raise MovimientoInvalidoError(f"No se pudo usar el segundo dado ({dado_secundario}).")
            
            dados_consumidos = [dado_principal, dado_secundario]

        #Aplicar movimiento en el tablero
        captura = self.__tablero__.mover_ficha(color, desde_index, hacia_index)
        
        # si ya no quedan tiradas, cambiar turno
        if not self.__dados__.obtener_tiradas_restantes():
            self.controlar_turnos()

        return captura, dados_consumidos #Ahora devuelve una tupla

    def valida_sacar_ficha(self, jugador: Jugador, desde):
        desde_index = desde - 1
        color = jugador.obtener_color()
        tablero = self.__tablero__

        if not tablero.todas_en_ultimo_cuadrante(color):
            raise SacarFichaError("No todas las fichas están en el último cuadrante.")

        tiradas = self.__dados__.obtener_tiradas_restantes()

        # Calcular distancia hasta fuera
        if color == "Blanca":
            distancia = desde_index + 1  # puntos 1–6
            # comprobar si hay fichas más lejos (más hacia el punto 1)
            hay_mas_lejanas = any(tablero.mostrar_contenedor()[i] for i in range(desde_index))
        else:  # Negras
            distancia = 24 - desde_index  # puntos 19–24 → 5,4,3,2,1,0
            # comprobar si hay fichas más lejos (más hacia el punto 24)
            hay_mas_lejanas = any(tablero.mostrar_contenedor()[i] for i in range(desde_index + 1, 24))

        # hay un dado exacto → usarlo directamente
        if distancia in tiradas:
            self.__dados__.usar_tirada(distancia)
            if not tablero.sacar_ficha(color, desde_index):  # chequeo del resultado
                raise SacarFichaError("No se pudo sacar ficha. Fallo interno del tablero.") 
            jugador.sacar_ficha_a_afuera()
            
            if not self.__dados__.obtener_tiradas_restantes():
                self.controlar_turnos()
                
            return distancia

        # dado mayor → permitido si NO hay fichas más lejanas
        if not hay_mas_lejanas:
            dado_mayor = next((d for d in sorted(tiradas) if d > distancia), None)
            if dado_mayor:
                self.__dados__.usar_tirada(dado_mayor)
                if not tablero.sacar_ficha(color, desde_index): #chequeo del resultado
                    raise SacarFichaError("No se pudo sacar ficha. Fallo interno del tablero.")
                jugador.sacar_ficha_a_afuera()
                
                if not self.__dados__.obtener_tiradas_restantes():
                    self.controlar_turnos()
                    
                return dado_mayor
        # VÉA el caso donde el dado es mayor PERO hay fichas más lejanas
        elif hay_mas_lejanas:
            dado_mayor = next((d for d in sorted(tiradas) if d > distancia), None)
            if dado_mayor:
                # La condición hay_mas_lejanas es verdadera Y tenemos un dado mayor que queremos usar
                raise SacarFichaError(f"No puedes usar el dado {dado_mayor}. Hay fichas {color} en posiciones más lejanas (puntos 1-{desde} para Blancas, o {desde+2}-24 para Negras).")

        # Si ninguna opción funcionó:
        raise SacarFichaError("No se puede sacar ficha desde este punto con los dados actuales.")

    def valida_mover_desde_barra(self,jugador:Jugador,dado):
        if not self.__dados__.usar_tirada(dado):
            raise MovimientoInvalidoError("Ese dado no esta disponible")
        
        if jugador.obtener_color() == "Negra":
            hacia = dado - 1         
        else:  # Blanca
            hacia = 24 - dado        
            
        if not self.__tablero__.valida_mover_desde_barra(jugador.obtener_color(),hacia):
            # Si el movimiento es inválido, devolvemos el dado antes de lanzar la excepción
            self.__dados__.usar_tirada(dado, revertir=True)
            raise MovimientoInvalidoError("Movimiento invalido desde la barra")
        
        # El método aplicar_movimiento_desde_barra ahora devuelve si hubo captura
        captura = self.__tablero__.aplicar_movimiento_desde_barra(jugador.obtener_color(),hacia)
        
        # si ya no quedan tiradas, cambiar turno
        if not self.__dados__.obtener_tiradas_restantes():
            self.controlar_turnos()

        return captura
    
    def hay_movimientos_posibles(self, jugador: Jugador):
        tiradas = self.__dados__.obtener_tiradas_restantes()
        color = jugador.obtener_color()
        tablero = self.__tablero__

        # Si tiene fichas en la barra, primero debe intentar reingresar
        if tablero.mostrar_barra()[color]:
            for dado in tiradas:
                hacia = 24 - dado if color == "Blanca" else dado - 1
                if tablero.valida_mover_desde_barra(color, hacia):
                    return True
            return False

        # Si todas están en el último cuadrante, revisar si se puede sacar alguna ficha
        if tablero.todas_en_ultimo_cuadrante(color):
            for desde in range(24):
                if tablero.mostrar_contenedor()[desde] and tablero.mostrar_contenedor()[desde][-1] == color:
                    if color == "Blanca":
                        distancia = desde + 1
                        hay_mas_lejanas = any(tablero.mostrar_contenedor()[i] for i in range(desde))
                    else:
                        distancia = 24 - desde
                        hay_mas_lejanas = any(tablero.mostrar_contenedor()[i] for i in range(desde + 1, 24))

                    for dado in tiradas:
                        if dado == distancia or (dado > distancia and not hay_mas_lejanas):
                            return True
            return False

        # Si no está en el último cuadrante, buscar movimientos normales
        for desde in range(24):
            for dado in tiradas:
                hacia = desde - dado if color == "Blanca" else desde + dado
                if 0 <= hacia < 24:
                    if tablero.validar_movimiento(color, desde, hacia, tiradas):
                        return True
        return False

    def _encontrar_dado_y_tipo_movimiento(self, jugador, desde_index, hacia_index):
        """
        Busca si el movimiento (desde -> hacia) es válido con las tiradas disponibles,
        validando también el punto intermedio.
        Retorna: (dado_principal, dado_secundario_o_None).
        """
        color = jugador.obtener_color()
        tiradas = self.__dados__.obtener_tiradas_restantes()
        diferencia = abs(hacia_index - desde_index)
        
        # Movimiento Simple (usa un solo dado)
        if diferencia in tiradas:
            return (diferencia, None)

        # Movimiento Compuesto (usa dos dados: D1 + D2 = Diferencia)
        tiradas_copia = list(tiradas) # Necesaria para manejar dobles y tiradas simples
        
        for i, dado1 in enumerate(tiradas):
            dado2 = diferencia - dado1
            
            #Chequear si el segundo dado está disponible (debe ser diferente al índice 'i' si es tirada simple)
            if dado2 > 0:
                
                # Crear una lista de tiradas restantes excluyendo el primer dado 'dado1' en el índice 'i'
                tiradas_restantes_para_d2 = tiradas_copia[:i] + tiradas_copia[i+1:]
                
                if dado2 in tiradas_restantes_para_d2:
                    
                    # Calcular el índice intermedio después de mover el primer dado (dado1)
                    if color == "Blanca":
                        intermedio = desde_index - dado1
                    else: # Negra
                        intermedio = desde_index + dado1
                    
                    # Verificar si el punto intermedio está bloqueado (2 o más fichas enemigas)
                    destino_intermedio = self.__tablero__.mostrar_contenedor()[intermedio]
                    if len(destino_intermedio) >= 2 and destino_intermedio[0] != color:
                        # El paso está bloqueado. Probar otra combinación.
                        continue
                    
                    # ¡Movimiento Compuesto Válido!
                    # Devolvemos el par de dados (ordenados para consumo consistente)
                    dados = sorted([dado1, dado2], reverse=True)
                    return (dados[0], dados[1])
                
        # Si no se encontró ninguna combinación válida (ni simple ni compuesta)
        raise MovimientoInvalidoError("La distancia no coincide con las tiradas disponibles, o el punto intermedio está bloqueado.")