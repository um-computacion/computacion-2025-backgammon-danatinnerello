## Registro de Prompts de IA
### Prompt 1

- Modelo / herramienta usada: ChatGPT GPT-5 (Agosto 2025)

- Instrucciones del sistema: (Ninguna especial, salvo configuración por defecto de ChatGPT)

- Prompt exacto usado: "¿Cómo puedo armar el tablero del juego Backmammon en programación? ¿En una lista podría ser? "
- Respuesta completa de la IA: 
  ¡Muy buena pregunta! Sí, podés representarlo con una lista (o varias listas) en programación, dependiendo de qué tanto detalle quieras manejar.
  El tablero de Backgammon tiene 24 triángulos (llamados puntas), 12 de cada lado. En cada punta puede haber varias fichas de un jugador o del otro.
  Representación con una sola lista:
  Podés usar una lista de 24 elementos, donde cada elemento sea:
  Un número positivo → fichas de un jugador (por ejemplo, jugador A).
  Un número negativo → fichas del otro jugador (jugador B).
  El valor absoluto indica la cantidad de fichas en esa punta.
  Ejemplo en Python:
  # Tablero inicial en Backgammon
  # Notación: + = jugador A, - = jugador B
  tablero = [0] * 24

  # Configuración inicial
  tablero[0] = -2     # 2 fichas del jugador B en la punta 1
  tablero[11] = -5    # 5 fichas del jugador B en la punta 12
  tablero[16] = -3    # 3 fichas del jugador B en la punta 17
  tablero[18] = -5    # 5 fichas del jugador B en la punta 19

  tablero[23] = 2     # 2 fichas del jugador A en la punta 24
  tablero[12] = 5     # 5 fichas del jugador A en la punta 13
  tablero[7] = 3      # 3 fichas del jugador A en la punta 8
  tablero[5] = 5      # 5 fichas del jugador A en la punta 6

  print(tablero)

  Esto te devuelve una lista con la posición inicial oficial.
  Cada índice de la lista representa una punta del tablero (de 0 a 23).


- Uso de la salida: Usada y luego cambiada

    Modificaciones realizadas: Al principio utilice esta estructura pero luego me di cuenta que no me servia para guardar varios datos, en este caso fichas en una misma posiicon asique la cambie en una de la clases con ayuda de los profes.

- Referencia en archivos finales: core/board.py

### Prompt 2

- Modelo / herramienta usada: ChatGPT GPT-5 (Agosto 2025)

- Instrucciones del sistema: (Ninguna especial, salvo configuración por defecto de ChatGPT)

- Prompt exacto usado: " Como seria la lógica para verificar el ganador de este juego "
- Respuesta completa de la IA: 
Muy buena pregunta 👌, porque la condición de victoria en Backgammon no es tan trivial como en otros juegos. Te lo detallo paso a paso:

🏆 ¿Cuándo gana un jugador en Backgammon?
  Objetivo: ser el primer jugador en sacar todas sus fichas del tablero (“bear off”).
  Para poder empezar a sacarlas:
  Todas las fichas del jugador deben estar en su home board (los últimos 6 puntos de su lado).
  Una vez que están ahí, puede ir retirándolas con los valores de los dados.
  Cuando un jugador no tiene más fichas en el tablero → ganó.

🔹 En tu modelo de clases
 Tenés:
  Player que debería guardar cuántas fichas le quedan.
  Board que sabe dónde están las fichas de cada jugador.
  Por lo tanto la lógica de ganador puede estar:
   en Player.has_won(), revisando si le quedan fichas.
   o en BackgammonGame.check_winner(), recorriendo los jugadores y preguntando si alguno ganó.

- Uso de la salida: Usada con modificaciones
    Modificaciones realizadas: la logica del ganador yo lo diseñe en player, aunque igualmente se relaciona con la clase juego.

- Referencia en archivos finales: core/game.py, core/board.py

### Prompt 3

- Modelo / herramienta usada: ChatGPT GPT-5 (Agosto 2025)

- Instrucciones del sistema: (Ninguna especial, salvo configuración por defecto de ChatGPT)

- Prompt exacto usado: "Me explicas cómo se juega al backmammon  "
- Respuesta completa de la IA: 
¡Claro! Te lo explico paso a paso y sencillo para que lo entiendas.
El backgammon es un juego de mesa clásico para dos jugadores. Se juega con:
  Un tablero con 24 triángulos (llamados puntos), que se agrupan en 4 cuadrantes.
  15 fichas para cada jugador (generalmente blancas y negras).
  2 dados.
  1 cubo de doblaje (opcional, para apuestas).

🎯 Objetivo del juego
 Mover todas tus fichas alrededor del tablero y sacarlas antes que el rival (como una carrera).

📍 Cómo se colocan las fichas
  Cada jugador tiene sus fichas en posiciones específicas al inicio:
  2 fichas en el punto 24 (extremo derecho del tablero del rival).
  5 fichas en el punto 13.
  3 fichas en el punto 8.
  5 fichas en el punto 6.
El tablero se coloca de manera que cada jugador mueva sus fichas en direcciones opuestas (uno en sentido horario, el otro antihorario).

🎲 Desarrollo del juego

Inicio: Cada jugador tira un dado. El que saque más alto empieza y juega con la combinación de ambos resultados (ej: si salen 3 y 5, el jugador mueve un 3 y un 5).

Movimientos:
 En tu turno lanzas dos dados.
 El número de cada dado indica cuántos puntos puedes mover una ficha.
 Puedes mover una misma ficha con los dos dados o dos fichas diferentes.
 Si sacas dobles (ej: 4 y 4), tienes derecho a cuatro movimientos de ese número.

Reglas para mover:
 Solo puedes mover a puntos vacíos, con fichas propias o con una ficha del rival.
 Si caes en un punto con una sola ficha rival, la “comes”: la ficha rival va a la barra (centro del tablero) y debe volver a entrar antes de que pueda mover otras.
 No puedes mover a un punto donde haya 2 o más fichas del rival.

Entrar fichas desde la barra:
 Si tienes fichas en la barra, debes usarlas antes de mover cualquier otra.
 Entran según los dados, cayendo en el cuadrante inicial del rival, siempre que ese punto esté abierto.

🏁 Fase final: “Bear off” (retirar fichas)

Cuando todas tus fichas están en tu tablero interno (últimos 6 puntos), puedes empezar a sacarlas:
 Cada dado permite retirar una ficha del punto correspondiente (ej: sacas un 4 → quitas una ficha del punto 4).
 Si no hay fichas en el punto exacto, puedes mover desde un punto más alto.
 El primero en sacar todas sus fichas gana la partida.
- Uso de la salida: Usada 

- Referencia en archivos finales: Usada para desarrollar el juego













