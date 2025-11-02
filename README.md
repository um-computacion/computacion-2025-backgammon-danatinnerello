# Backgammon - Proyecto Final Computación 

## Descripción

Implementación completa del juego de mesa Backgammon con dos interfaces de usuario:
- Interfaz gráfica usando Pygame
- Interfaz de línea de comandos (CLI)

### Reglas Implementadas

- **Movimientos básicos**: 
  - Mover fichas según valores de dados
  - Dirección específica según color (Blancas: 24→1, Negras: 1→24)
  - Uso de uno o dos dados para un movimiento
  
- **Capturas**: 
  - Un punto con una sola ficha puede ser capturado
  - Fichas capturadas van a la barra
  - Obligación de reingresar desde barra antes de otros movimientos

- **Bloqueos**:
  - Puntos con 2+ fichas enemigas están bloqueados
  - No se puede mover a través de 6 puntos bloqueados consecutivos

- **Sacar Fichas (Bear Off)**:
  - Permitido solo cuando todas las fichas estén en el último cuadrante
  - Usar dado exacto o mayor si no hay fichas más lejanas
  - Victoria al sacar todas las fichas

## Estructura del Proyecto

```
backgammon/
├── core/                 # Lógica central del juego
│   ├── game.py          # Controlador principal
│   ├── board.py         # Lógica del tablero
│   ├── player.py        # Clase jugador
│   ├── dice.py          # Manejo de dados
│   ├── checker.py       # Clase ficha
│   └── excepcions.py    # Excepciones personalizadas
│
├── cli/                 # Interfaz de línea de comandos
│   └── cli.py          # Implementación CLI
│
├── pygame_ui/          # Interfaz gráfica
│   ├── main.py        # Punto de entrada GUI
│   ├── board_renderer.py # Renderizado del tablero
│   └── events.py      # Manejo de eventos
│
├── test/              # Tests unitarios
│   ├── test_board.py
│   ├── test_game.py
│   ├── test_dice.py
│   ├── test_player.py
│   ├── test_checker.py
│   └── test_cli.py
│
└──                   # Documentación
    ├── README.md
    ├── CHANGELOG.md
    └── JUSTIFICACION.md
```

## Requerimientos

### Sistema
- Python 3.8 o superior
- Sistema operativo: Windows/Linux/MacOS

### Dependencias Principales
- pygame==2.5.2 (interfaz gráfica)
- pytest==7.4.3 (testing)

## Instalación

1. Clonar el repositorio:
```bash
git clone https://github.com/danatinnerello/computacion-2025-backgammon.git
cd computacion-2025-backgammon
```

2. Crear y activar entorno virtual:
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/MacOS
source venv/bin/activate
```

3. Instalar dependencias:
```bash
# Solo para jugar
pip install -r requirements.txt

# Para desarrollo
pip install -r requirements-dev.txt
```

## Uso

### Interfaz Gráfica (Pygame)

```bash
python -m pygame_ui.main
```

#### Controles
- **Mouse**:
  - Click izquierdo en ficha: Seleccionar ficha para mover
  - Click izquierdo en punto: Mover ficha seleccionada
  - Click en barra lateral derecha: Sacar ficha seleccionada
  - Click en barra central: Ver fichas capturadas

- **Teclado**:
  - ESPACIO: Pasar turno si no hay movimientos posibles
  - ESC: Salir del juego

#### Panel de Información
- Jugador actual y color
- Dados disponibles
- Fichas en barra
- Fichas sacadas por cada jugador
- Mensajes de estado/error

### Interfaz de Línea de Comandos (CLI)

```bash
python -m cli.cli
```

#### Comandos Disponibles
1. **Mover Ficha**:
   ```
   Origen: número del punto (1-24)
   Destino: número del punto (1-24)
   
   Casos especiales:
   - Origen 0: Mover desde la barra
   - Destino -1: Sacar ficha
   ```

2. **Rendirse**: Termina el juego, victoria para el oponente
3. **Salir**: Cierra el juego

#### Ejemplo de Turno
```
Turno de Alice (Blanca)
Dados: [6, 3]

1. Mover ficha
2. Rendirse
3. Salir

> 1
Mover ficha desde: 24
Hasta: 21
```

## Testing

### Ejecutar Tests
```bash
# Todos los tests
python -m unittest discover test

# Tests específicos
python -m unittest test.test_board
python -m unittest test.test_game
```

### Cobertura de Tests
```bash
coverage run -m unittest discover
coverage report
coverage html  # Genera reporte HTML
```

## Desarrollo

### Linting
```bash
pylint core/ cli/ pygame_ui/ test/
```

### Documentación
- Los módulos incluyen docstrings detallados
- Ver JUSTIFICACION.md para detalles de diseño
- Changelog en CHANGELOG.md

## Contribuciones
1. Fork del repositorio
2. Crear rama para feature/fix
3. Commit con mensaje descriptivo
4. Pull request con descripción detallada

## Licencia
MIT License - Ver LICENSE.md

## Autora
Dana Tinnerello