# Changelog
Todos los cambios notables de este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog 1.1.0](https://keepachangelog.com/es-ES/1.1.0/)  
y este proyecto sigue [Semantic Versioning](https://semver.org/lang/es/).

## [1.0.0] - Comienzo: 2025-08-20 - Sprint 1
### Agregado
- Creacion de la estructura del juego: carpetas y archivos de tablero y juego

- Creacion de archivos de dados,fichas,excepciones y jugadores.
- Asignacion de las responsabilidades de cada clase
- Creacion de la estructura base de la clase tablero: creacion del tablero y sus metodos(sin desarrollar)

- Creacion de la estructura base de la clase juego y desarrollo de casi toda la clase completa de los dados 

- Creacion de archivos changelog, justificacion, prompts y readme.
- Desarrollo de los metodos o funciones de la clase juego

- Asignacion de responsabilidades a la clase ficha
- En juego agrego un atributo jugadores que contenia los dos objetos creados como jugador
- Desarrollo toda la clase jugador con sus metodos tambien desarrollados

- Desarrollo del metodo mover_ficha() de la clase tablero
- Creacion del entorno virtual e instalacion de coverage

- Creacion del archivo `__init__`
- Comienzo de desarrollo de este archivo changelog.md
- En la clase jugador añadi un atributo que es `__fichas_restantes__`

- Comienzo de desarollo de los promts de documentacion y desarollo

- Cree el archico .coveragerc para que no me testee los archivos que no queria 
- Creacion de los archivos __init__.py en la carpeta test y core
-Testeo del codigo de las clases que habia desarrollado hasta el momento que eran: tablero, juego,jugadores y dados.

- Sume la lista "barra" y el diccionario "afuera" en tablero
- Añadi funciones como validar_movimiento, mostrar_barra , mostrar_afuera_ enviar_a_barra , entre otras en la clase tablero.
- Desarrolle la clase ficha
- En dados sume dos funciones:quedan_tiradas y reiniciar. Tambien añadi doctings
- En juego añadi las funciones para mostrar los jugadores y doctings
- En juego añadi funciones de mostrar_tablero, agregar o quitar de barra y para saber cuantas tiene en barra.

- Agregue doctings en los test que ya tenia 
- Agregue los test de los nuevos metodos o funciones que habia desarrollado y todavia no estaba testeado


### Cambiado
- Cambie la menra de crear el contenedor que esta mal. De: `[0] * 24` a: `[[] for _ in range(24)]`  
- Cambie lo que guardaba en cada posicion del contenedor que yo guardaba un numero y en verdad era si la ficha era negra o blanca y cuantas tambien. Ejemplo se cambo: `self.__contendedor__[0]=-2` por: `self.__contenedor__[0]=["Negra"]*2`


- Tenia tambien dos metodos que eran mover_ficha() y guardar_ficha() que los mofique desarrollandolos en el mismo metodo.
- En juego volvi a cambiar el atributo que contenia a los jugadores. De: `[Jugador(jugador1,"blanco"),Jugador(jugador2,"negro")]` por: ` [self.__jugador1__, self.__jugador2__]`
- Y tambien los metodos para crear cada objeto jugador. De:  `jugador1 ` en este caso solo lo habia inicializado o asignado, lo cambie por: `  Jugador(jugador1,"blanco")` que directamete crea el objeto.

### Corregido
- Corregi los atributos de la clase dados. Estaban asi: `__dado1` y debian ir asi: `__dado1__`

- Corregi el orden en la clase juego, ya que primero se deben crear los objetos jugadores y luego podran guardarse en el atributo jugadores. Yo tenia el orden invertido. 

- En el test de jugador le cambie el nombre a un metodo por eso lo tuve que modificar.

### Eliminado
- 
# Terminacion: 2025-09-02
---

## [2.0.0] - Comienzo: 2025-09-03 -  Sprint 2 
### Agregado
- Implementacion de integracion continua: pylint
- Descarga de librerias requeridas

- Desarrollo de la base del cli, iniciacion de objetos, sin funcionalidades
- Agregue en game metodos para mostrar turnos y contenedor
- Agregue en player el metodo str

- Desarrollo en el cli para validar movimientos a barra 

- Desarrollo en el cli, de moviiento hacia afuera y movimiento normal entre posiciones 
- DEsarrollo en el cli de verificar ganador y cambio de turno

- Comienzo de desarrollo de test del cli

- Desarrollo de test extras para el cli, para cubrir el porcentaje pedido

- Actualizacion de prompts y changelog

### Cambiado 
- Modifique en la clase dados un metodo 
- Modifique tambien en la clase dados los test para testear los mismos ya que en una clase con el profesor gabriel nos enseño a testear por ejemplo el random, entonces desarrolle esos test segun habiamos visto con él.

- Actualizacion de los prompts
- Creacion deel archivo cli.py
- Comentario de lo que me imagino que voy a tener que desarrollar

- MOdifique en la clase bord el metodo de mostrar_contenedor

- Modificacion en board, en el metodo mostrar_contenedor: return

### Corregido

### Emilinado

# Terminacion: 2025-09-16

## [3.0.0] - Comienzo: 2025-09-17 -  Sprint 3

# Agregado

- Implementacion de una estructura de control para que el que juegue pueda abandonar o salir del juego cuando quiera
- Al implementar lo anterior tenia que cambiar todos los test y para no hacerlo implemente el interactive, que cuando era verdadero se ejecutaba la estructura de control junto con todo el cli y si era falso me servia para que los test sigan corriendo bien.
- Agregue algunos test para que cubran lo nuevo en el cli
- Añadi en el metodo mover_ficha la validacion que si es capturada la mande a barra

- Agregue test extras para cubrir lo necesario del codigo cli

- Añadi el metodo imprimir_contenedor

- Agregue verificacion en el metodo mover_ficha en la clase tablero para que verifique el color, verifique una captura, guarda y elimine ficha segun el movimiento
- En validar_movimiento en la clase tablero tambien agregue validaciones, que estaban en el cli y me di cuenta que no iban ahi. 
- En mover_desde_barra lo mismo, agregue validaciones que tenia en el cli, para separar la logica de la interaccion
- Añadi varios test para cubrir los posibles casos de la clase tablero y verificar que funcione.

- Agregue el metodo valida_mover_ficha, valida_sacar_ficha, valida_mover_desde_barra y hay_movimientos_posibles en game que estaban en board o en el cli. 

- Agregue excepciones personalizadas 
- Realice un cli nuevo, limpio solo con interacciion y alicando las excepciones personalizadas

- Añadi validaciones de direccion ya que depende la ficha van en direcciones contrarias
- Añadi test para llegar a la cobertura en board y en game

- En el cli añadi para que siempre que en el bucle siempre muestre el tablero, tirada de daods y turno
- Agregacion de test de game

- Desarrollo de README

# Modificado
- Modificacion de algunos test devido a la implementacion del interactive
- Cambios en el cli para que imprima un mensaje si la ficha fue captura o si fue un movimiento normal
- Modifique el metodo en tablero para ver el estado del mismo de una manera distinta.
- Modificacion de algunos test del cli debido al cambio de indice.

- Modificacion de algunos test del cli para que funcionen

- Modifique el metodo mostrar_contener 

- Modifique algunos test de la clase tablero debido a los cambios que realice en la clase.

- Cree la carpeta .gitignore y añadi todo lo que debia ignorarse.
- Luego de la clase con el profe daniel me di cuenta que mi codigo por partes no cumplia con los principios SOLID netonces realice modificaciones.
- Añadi una validacion para que capture si no tiene movimientos el jugador.(en el cli) 
- Saque validaciones y solo llame metodos de las clases.

# Corregido

- Corregi en el cli el print para tirar dados, para que imprima distinto si es tirada normal o doble.
- Correcciones para que el usuario ingrese losmovimientos de 1-24 y no de 0-23. Esto iplico cambios en algunos metodos del tablero

- Cambie la verificacion: 'if (hacia < 0 or hacia > 23) ^ (desde < 0 or desde > 23):' por ' if desde < 0 or desde > 23 or hacia < 0 or hacia > 23:' 

- Tengo varios test donde no cambie nada del codigo porque me saliaun error para mergear donde decia que se habia modificado el coverage o algo asi. Entonces cree la carpeta .gitignore y ahi puse todo lo que debia ignorar al mergear, asi lo resolvi. Con ayuda de IA.

- En tablero modifique el metodo valida_mover_desde_barra por si tiradas_restantes se pasa
- Separe metodos que tenian mas de una responsabilidad por ejemplo las validaciones po un lado y la funcion por otro.
- Cambie el constructor en game

- En game cambie las ValueError por mis excepiones personalizadas 
- Y eso hizo que tenga que corregir algunos test de board, game, player y todos los del cli.

- En board tambien cambie ValueError por mis excepciones personalizadas 

- Corregi el metodo valida_sacar_ficha para que cuando ya estan todas en el ultimo cuadrante, si te sale un dado mayor igual puede salir afuera.

- Corregi algunos test en board con mis excepciones personalizadas

- Correccion de indice en el metodo "valida_mover_ficha" en game
- Correcion de indice en varios metodos. para que el usuario vea 1-24 pero en la logica funciona de 0-23

- Actualizacion de el archivo JUSTIFICACION


# Emilinado

- Elimine metodos de player que no servian o no los utlizaba
- Elimine todo el cli anterior donde tenia logica e interaccion mezcladas y tambien habia agregado el interactive

# Terminacion: 2025-09-30

## [4.0.0] - Comienzo: 2025-10-01 - Sprint 4 

# Agregado

- Creacion de la estructura del pygame y division de respnsabilidades
- Iniciacion de la pantalla y fondo del tablero

- Comienzo del board_renderer y dibujo de puntos en el tablero

- Dibujo de fichas e integracion en el main
- Inicializacion de la posicion de las fichas ne le tablero

- Agrego barras laterales y central

- Agrego numero a los puntos 

- Integracion de la logica del juego con la intefaz grafica

- Agregacion de metood para la deteccion del clics en un punto e integracion en el main

- Agregue que al tocar una ficha se dtecte el color de la misma
- DEsarrollo de pantalla para que pida a los nombres de los jugadores antes de empezar a jugar
- Inicializacion de jugadores y juego 
- Desarrollo de movimiento basico 
- Redibuja tablero y cambia turno 

- Desarrollo de metodo dibujar dados e implementacion de tirar dados en main

- Deteccion de clics para mover ficha segun el valor de los dados
- Desarrollo de deteccion de fichas enemigas

# Modificado 
- Cambio en el atributo jugador en el game a nombre_jugador

- Modificacion en el orden de los puntos

# Corregido

- Correccion de tamaño de puntos

- Corregido devuelta los puntos para que se vea bien con la barra

- Correciond etamaña de barras para que coincidan con los puntos y se vea bien

- Integracion de que muestre el nombre del juagdor al que le toca jugar

# Eliminado 
-
# Terminacion: 2025-10-14

## [5.0.0] - Comienzo: 2025-10-15 - Sprint 5

# Agregado

- Validacion de movimiento
- Redibuja el tablero para mantenerlo actualizado

- Añadi constantes
- Agreagcion de un panel al final del tablero donde se muestren los mensajes iterativos para el usuario
- Configuracion de fuente, tamaño  y tiempo en pantalla de los mensajes 

- Añadi la configuracion para tirar dados con enter
- Chequeo si no hay movimientos, pasa de turno
- Añadi metodo para dibujar todo y llamarlo al final del bucle como actualizacion

- Integracion de movimientos a la barra central cuando se captura una ficha
- Integracion de validacion de esos movimientos y mensajes para el usuario

- Separacion de fichas en la barra segun el color y si hay mas de tres muestra el numero de excedentes
- Integraciion de movimiento y validacion cuando hay fichas en barra y como deben volver al tablero

- Integracion de que en los puntos, dibuja hasta 5 fichas y despues muestra el numero de las que sobran

- Integracion de la barra lateral donde las fichas ya salen afuera
- Metodo de pasar turno cuando es necesario porque no hay movimientos en el ultimo cuadrante
- Integracion de clics en la barra lateral y verificaciones de que todas esten en el ultimo cuadrante
- Mensajes iterativos para el usuario
- Control de turnos y manejo d eturnos ya en el ultimo cuadrante

- Añado metodo para saber el color de la ficha que se ingreso a la barra
- Si se reingrea una ficha de la barra central en un punto que solo tiene una ficha del otro juagdor se tienen que invetir, desarrollo d etodo esto
- Verificacion del ganador

- Implementacion de la regla del dado mayor, que solo pueda sacar fichas hacia la barra lateral con un adado exacto o mayor(solo si no hay fichas mas lejanas)

- Separacion de la logica y eventos con el main donde solo esta la interaccion con el usuario
- Agregacion de test en board
- Agregacion de test en game

- Añadi un metodo en game para el manejo de movimientos compuestos es decir que utiliza los dos dados, siempre y cuando el punto intermedio este libre
- Añadi que se cierre la pantalla luego de 5 segundos que ya tenemos ganador
- Cambie la manera en que se ven las fichas de afuera en la barra

- Añadi validaciones 
- Añadi test para llegar al porcentaje del coverage

- Integracion del pylint
- Actualizacion del archivo JUSTIFICACION y el README
- Añadi y complete los archivos con doctings

- Actualizacion del changelog
- Actualizacion de prompts

# Modificado 
- Modificacion del tamaño de la pantalla
- Visualizacion de como se ven en la barra, para que sean mas chicas y no se vea feo

- Modificacion en el metodo "sacar_ficha" en game para que funcione con un dado mayor a la cantidad de posiciones que le faaltan a la ficha

- Modifique la deteccion de clics en los puntos

- Modifique la justificacion
# Corregido

- Correccion de colores de puntos para que esten invertidos los de abajo con los de arribba

- Correcion en el cambio de turno que no me pasaba
- Alineacion con los puntos y fichas

- Correccion de que las fichas ingresen a la barra lateral y desaparezcan del tablero y se sumen en la barra

- Correccion en el movimiento de fichas desde la barra central devuelta al tablero. Aveces reingresaba la ficha pero en un punto donde habia don de las enemigas y se cambiaba el color que eso no debe pasar

- Correccion de que pase el turno en el ultimo cuadrante cuando ya el juagdor no tiene tiradas, e ingreso fichass en la barra lateral

- Correccion en game de un metodo que me faltaba la validacion de un movimiento
- Correccion en dice de el metodo "usar_tirada"

- Corregi que la deteccion de clicks para el movimieento sea en la ficha no en el punto

- Correccion del movimiento al ingresar a la barra lateral
- Correccion de usar una excepcion personalizada en un metodo
- Correccion del metodo "validar_ficha"

# Eliminado 

# Terminacion: 2025-11-01