# Changelog
Todos los cambios notables de este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog 1.1.0](https://keepachangelog.com/es-ES/1.1.0/)  
y este proyecto sigue [Semantic Versioning](https://semver.org/lang/es/).

## [Unreleased]
### Agregado
- (Cosas nuevas que todavía no salieron en una versión estable)

### Cambiado
- (Cambios que aún no se liberaron)

### Corregido
- (Errores solucionados en desarrollo)

---

## [1.0.0] - 2025-08-20 - Sprint 1
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

---

## [0.1.0] - 2025-09-03 -  Sprint 2 
### Agregado
- Implementacion de integracion continua: pylint
- Descarga de librerias requeridas

### Cambiado 
- Modifique en la clase dados un metodo 
- Modifique tambien en la clase dados los test para testear los mismos ya que en una clase con el profesor gabriel nos enseño a testear por ejemplo el random, entonces desarrolle esos test segun habiamos visto con él.


### Corregido



### Emilinado


 