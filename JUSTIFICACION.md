# JUSTIFICACION 

Este documento detalla las decisiones de diseño y las estrategias de desarrollo tomadas para la creacion del juego de Backgammon. El objetivo es justificar la estructura del proyecto y demostrar una comprension profunda de las elecciones realizadas.


## Resumen del Diseño General

El proyecto se penso con un enfoque en la **separación de la logica del negocio y la capa de presentacion**. Esto significa que el núcleo del juego, que maneja las reglas y la mecanica, es completamente independiente de como se muestra al usuario. Este enfoque modular permite implementar multiples interfaces de usuario (como la interfaz de linea de comandos y la grafica con Pygame) sin necesidad de modificar el codigo central.

El diseño del juego se basa en el paradigma de la Programación Orientada a Objetos (POO), con clases bien definidas que representan los componentes clave del Backgammon. Esto no solo facilita el desarrollo y el mantenimiento, sino que también nos permite adherirnos a principios como los SOLID.


## Justificación de las Clases Elegidas

Las siguientes clases se han definido para modelar el juego, con el objetivo de asignar una unica responsabilidad a cada una, de acuerdo con el **Principio de Responsabilidad Unica (SRP)**.

* ` Juego`: Esta clase actua como el **coordinador principal** del juego. Su responsabilidad es gestionar el flujo de la partida, los turnos de los jugadores y las interacciones entre los diferentes componentes, como el tablero y los dados.
* `Tablero`: Representa el tablero fisico del Backgammon. Su función es gestionar los 24 puntos (triangulos), las fichas en cada punto, y las areas especiales como la barra central y el area de "home"(que seria cuando las fichas ya salen del tablero).
* `Jugador`: Modela a un jugador individual. Contiene información como el color de las fichas y la logica para gestionar los movimientos del jugador.
* `Dados`: Se encarga de la logica de los dados. Su unica responsabilidad es simular las tiradas, incluyendo la funcionalidad especial de las tiradas dobles.
* `Ficha`: Representa una sola ficha del juego. Tener una clase separada para las fichas permite gestionar de forma individual las propiedades de cada una, como su posición y color.
* `CLI` y `PygameUI`: Estas clases son las **capas de presentación** del juego. `CLI` se encarga de la interacción basada en texto en la consola, mientras que `PygameUI` maneja la interfaz gráfica. Su separación del `core` demuestra el cumplimiento del Principio de Responsabilidad Única.


## Justificación de Atributos y Decisiones de Diseño Relevantes

Todos los atributos de las clases siguen la convención de `_nombre_` para indicar que son parte interna de la clase y un atributo privado, de acuerdo con las buenas practicas establecidas en la consigna.

* **Desarrollo por Etapas**: El proyecto se abordara con un enfoque de **desarrollo incremental** con entregas quincenales y **commits que reflejan una evolucion constante**, tal como lo indican las pautas.


## Estrategias de Testing y Cobertura

Para garantizar la calidad y robustez del codigo, se ha adoptado una estrategia de testing rigurosa.

* **Pruebas Unitarias**: Se enfocaran en la lógica central (`core/`). El objetivo es alcanzar una cobertura de al menos el 90% con pruebas unitarias para asegurar que las mecanicas del juego, como que los movimientos validos funcionen correctamente.
* **Integración Continua (CI)**: Se configurara un sistema de CI con herramientas. Cada commit desencadenara pruebas automatizadas y medira la cobertura del codigo, proporcionando retroalimentacion en tiempo real sobre la calidad del proyecto.


## Referencias a Requisitos SOLID

El diseño del proyecto se alinea con los principios SOLID para garantizar un codigo limpio, extensible y fácil de mantener.

* **S (Single Responsibility Principle)**: Cada clase tiene una unica y clara responsabilidad, como se detallo en la seccion de justificacion de clases.

* **O (Open/Closed Principle)**: El codigo esta diseñado para ser extensible sin necesidad de modificar el codigo existente. 

* **L (Liskov Substitution Principle)**: Si se crearan subclases de `Jugador` (por ejemplo, `HumanPlayer` y `AIPlayer`), podrían ser usadas indistintamente por la clase `BackgammonGame` sin romper la funcionalidad.

* **D (Dependency Inversion Principle)**: La logica de alto nivel (`BackgammonGame`) no depende de las implementaciones concretas de la interfaz (`CLI`, `PygameUI`), sino de abstracciones. Esto se logra mediante la separación de las capas.


## Anexos

