## Registro de Prompts de IA
### Prompt de ejemplo

- Modelo / herramienta usada: ChatGPT GPT-5 (Agosto 2025)

- Instrucciones del sistema: (Ninguna especial, salvo configuración por defecto de ChatGPT)

- Prompt exacto usado: "   "
- Respuesta completa de la IA: 
- Uso de la salida: Usada con modificaciones
    Modificaciones realizadas: Cambié los nombres de atributos al español (players → jugadores, board → tablero).

- Referencia en archivos finales: core/game.py, core/board.py

### Prompt 1

- Modelo / herramienta usada: ChatGPT GPT-5 (Agosto 2025)

- Instrucciones del sistema: (Ninguna especial, salvo configuración por defecto de ChatGPT)

- Prompt exacto usado: "Hola, tengo que programar un juego. Te puedo mandar el archivo y necesito que me ayudes a organizar y planificar la estructura. Igual ahí en el documento dice pero ayúdame a organizarlo en detalle"
- Respuesta completa de la IA: 
Buenísimo, Dana! Estuve leyendo tu documento y ya tenés una guía bastante clara de lo que piden. Te propongo una organización detallada de la estructura del Backgammon en Python.
📂 Estructura de Carpetas:
/backgammon/
├── core/           # lógica del juego (reglas, entidades)
│   ├── game.py
│   ├── board.py
│   ├── player.py
│   ├── dice.py
│   ├── checker.py
│   └── exceptions.py
│
├── cli/            # interfaz por consola
│   └── cli.py
│
├── pygame_ui/      # interfaz gráfica
│   └── ui.py
│
├── assets/         # imágenes, sonidos
│
├── tests/          # unit tests
│
├── requirements.txt
├── README.md
├── CHANGELOG.md
├── JUSTIFICACION.md
└── prompts-*.md
/backgammon/
├── core/           # lógica del juego (reglas, entidades)
│   ├── game.py
│   ├── board.py
│   ├── player.py
│   ├── dice.py
│   ├── checker.py
│   └── exceptions.py
│
├── cli/            # interfaz por consola
│   └── cli.py
│
├── pygame_ui/      # interfaz gráfica
│   └── ui.py
│
├── assets/         # imágenes, sonidos
│
├── tests/          # unit tests
│
├── requirements.txt
├── README.md
├── CHANGELOG.md
├── JUSTIFICACION.md
└── prompts-*.md
/backgammon/
├── core/           # lógica del juego (reglas, entidades)
│   ├── game.py
│   ├── board.py
│   ├── player.py
│   ├── dice.py
│   ├── checker.py
│   └── exceptions.py
│
├── cli/            # interfaz por consola
│   └── cli.py
│
├── pygame_ui/      # interfaz gráfica
│   └── ui.py
│
├── assets/         # imágenes, sonidos
│
├── tests/          # unit tests
│
├── requirements.txt
├── README.md
├── CHANGELOG.md
├── JUSTIFICACION.md
└── prompts-*.md
/backgammon/
├── core/           # lógica del juego (reglas, entidades)
│   ├── game.py
│   ├── board.py
│   ├── player.py
│   ├── dice.py
│   ├── checker.py
│   └── exceptions.py
│
├── cli/            # interfaz por consola
│   └── cli.py
│
├── pygame_ui/      # interfaz gráfica
│   └── ui.py
│
├── assets/         # imágenes, sonidos
│
├── tests/          # unit tests
│
├── requirements.txt
├── README.md
├── CHANGELOG.md
├── JUSTIFICACION.md
└── prompts-*.md
⚙️ Cómo se relacionan:
BackgammonGame
├─ Board
├─ Player (x2)
├─ Dice
└─ Interfaces (CLI / PygameUI)

- Uso de la salida: Usada 

- Referencia en archivos finales: Estructura del proyecto

### Prompt 2

- Modelo / herramienta usada: ChatGPT GPT-5 (Agosto 2025)

- Instrucciones del sistema: (Ninguna especial, salvo configuración por defecto de ChatGPT)

- Prompt exacto usado: "Y cómo puedo organizar las migestone e issue de este mismo proyecto  "
- Respuesta completa de la IA: 
Muy buena pregunta 👌
Lo que conviene es organizar tus milestones como “grandes entregables” (sprints de 14 días como dice tu PDF) y dentro de cada uno dividir en issues pequeñas, concretas y medibles. Así mantenés trazabilidad, commits distribuidos y podés mostrar progreso.
📌 Ejemplo de Milestones

Cada uno dura 2 semanas (coincide con los sprints que pide la materia):
 Milestone 1: Setup inicial y estructura básica
  Crear repositorio con carpetas (core, cli, pygame_ui, tests, etc.).
  Configurar entorno (requirements.txt, Dockerfile si corresponde).
  Clases iniciales vacías (Board, Player, Dice, BackgammonGame).
  Primeros tests de “esqueleto”.
 Milestone 2: Lógica mínima de juego
  Implementar Dice con tests.
  Implementar Board con posiciones iniciales.
  Implementar Player (atributos básicos).
  Testear setup inicial de partida.
 Milestone 3: Movimientos y reglas
  Validación de movimientos (Board.is_valid_move).
  Reglas de captura y reingreso desde barra.
  Verificación de condiciones de victoria.
  Tests para reglas de jugabilidad.
 Milestone 4: Interfaz CLI obligatoria
  Render de tablero en texto.
  Entrada de jugadas por consola.
  Integración BackgammonGame + CLI.
  Tests de interacción CLI (simulación entrada).
 Milestone 5: Interfaz gráfica Pygame
  Cargar imágenes del tablero y fichas.
  Mostrar estado del juego en ventana.
  Interacción con mouse.
  Integración BackgammonGame + PygameUI.
 Milestone 6: Extras + Entrega final
 Guardado opcional en Redis.
 Optimización y refactor (cumplir SOLID).
 Cobertura de tests > 90%.
 Documentación (README, JUSTIFICACION.md, CHANGELOG.md, prompts-*.md).

📋 Ejemplo de Issues por milestone

👉 Milestone 2 (Lógica mínima de juego):
    Crear clase Dice con método roll() que devuelva lista de 2 enteros.
    Tests unitarios de Dice (incluyendo dobles).
    Crear clase Board con representación de 24 puntos.
    Función para inicializar posiciones estándar.
    Crear clase Player con nombre, color y 15 fichas.
    Testear setup inicial (dos jugadores + tablero).
📌 Buenas prácticas al crear issues
    Título corto, tipo: Implementar clase Dice.
    Descripción clara: qué hace, criterios de aceptación, referencias a requerimientos.
    Cada issue debe ser pequeña: resolvible en 1–2 días máx.
    Vincular cada issue a un milestone.
    Hacer commit con mensaje relacionado: feat(core): agregar clase Dice #12.

- Uso de la salida: No usada

- Referencia en archivos finales: Ninguno

### Prompt 3

- Modelo / herramienta usada: ChatGPT GPT-5 (Agosto 2025)

- Instrucciones del sistema: (Ninguna especial, salvo configuración por defecto de ChatGPT)

- Prompt exacto usado: " ![alt text](image-2.png) Qué significa eso "
- Respuesta completa de la IA: 

Lo que ves en la pantalla es un Pull Request en GitHub que intenta unir (mergear) tu rama 54-modificaciones... a la rama main.

El mensaje:

"This branch has conflicts that must be resolved"

significa que los cambios que hiciste en tu rama entran en conflicto con lo que ya existe en main.
Es decir, Git no sabe automáticamente cómo combinar ambos porque hay diferencias en los mismos archivos/líneas.

En tu caso, el conflicto aparece en el archivo .coverage, que es un archivo generado automáticamente por la herramienta de coverage (cuando corrés tests). Ese archivo no debería subirse al repositorio, porque cambia en cada ejecución de los tests. Lo ideal es que esté listado en el archivo .gitignore.

Opciones para resolverlo:

La forma rápida (recomendada):

Eliminá .coverage del control de versiones y agregalo a .gitignore.

Para eso:
echo ".coverage" >> .gitignore
git rm --cached .coverage
git add .gitignore
git commit -m "Ignorar archivo .coverage"
git push
Luego resolvés el merge normalmente.

Si querés resolverlo desde GitHub:

Podés hacer clic en "Resolve conflicts", abrir el archivo en conflicto y elegir si lo eliminás o dejás uno de los dos.

En este caso lo mejor es eliminarlo directamente, porque no tiene sentido mantener .coverage en el repo.

👉 En resumen:
Ese aviso significa que no podés hacer el merge hasta que resuelvas manualmente los conflictos. En tu caso el conflicto está en un archivo que no debería estar en el repositorio, así que lo mejor es borrarlo y añadirlo al .gitignore.

- Uso de la salida: Usada 
- Referencia en archivos finales: 

### Prompt 4

- Modelo / herramienta usada: ChatGPT GPT-5 (Agosto 2025)

- Instrucciones del sistema: (Ninguna especial, salvo configuración por defecto de ChatGPT)

- Prompt exacto usado: " que es el docker en informatica?  "
- Respuesta completa de la IA: 
Docker es una plataforma que permite crear, ejecutar y administrar aplicaciones dentro de “contenedores”.
En términos simples, un contenedor es como una pequeña “caja” que incluye todo lo necesario para que una aplicación funcione: su código, librerías, dependencias, y configuraciones.

🔹 ¿Por qué se usa Docker?

Sin Docker, una aplicación puede funcionar en tu computadora pero fallar en otro entorno (por ejemplo, en un servidor), porque faltan librerías o hay versiones distintas.
Con Docker, la aplicación se ejecuta igual en cualquier lugar, ya sea en tu PC, en otro sistema operativo, o en la nube.
- Uso de la salida: Usada con modificaciones
    Modificaciones realizadas: Cambié los nombres de atributos al español (players → jugadores, board → tablero).
🔹 Conceptos clave

Imagen (image): una “plantilla” inmutable que define el entorno de la app (por ejemplo, una imagen de Python con tu código incluido).

Contenedor (container): una instancia en ejecución de una imagen.

Dockerfile: archivo de texto donde definís cómo construir la imagen (qué sistema base usar, qué librerías instalar, etc.).

Docker Hub: repositorio en línea donde podés encontrar o publicar imágenes.

- Referencia en archivos finales: core/game.py, core/board.py