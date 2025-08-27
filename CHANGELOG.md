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

## [1.0.0] - 2025-08-20
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


### Cambiado
- Cambie la menra de crear el contenedor que esta mal. De: `[0] * 24` a: `[[] for _ in range(24)]`  
- Cambie lo que guardaba en cada posicion del contenedor que yo guardaba un numero y en verdad era si la ficha era negra o blanca y cuantas tambien. Ejemplo se cambo: `self.__contendedor__[0]=-2` por: `self.__contenedor__[0]=["Negra"]*2`


- Tenia tambien dos metodos que eran mover_ficha() y guardar_ficha() que los mofique desarrollandolos en el mismo metodo.
- En juego volvi a cambiar el atributo que contenia a los jugadores. De: `[Jugador(jugador1,"blanco"),Jugador(jugador2,"negro")]` por: ` [self.__jugador1__, self.__jugador2__]`
- Y tambien los metodos para crear cada objeto jugador. De:  `jugador1 ` en este caso solo lo habia inicializado o asignado, lo cambie por: `  Jugador(jugador1,"blanco")` que directamete crea el objeto.

### Corregido
- Corregi los atributos de la clase dados. Estaban asi: `__dado1` y debian ir asi: `__dado1__`

- Corregi el orden en la clase juego, ya que primero se deben crear los objetos jugadores y luego podran guardarse en el atributo jugadores. Yo tenia el orden invertido. 

### Eliminado
- 

---

## [0.1.0] - 2025-09-03


 