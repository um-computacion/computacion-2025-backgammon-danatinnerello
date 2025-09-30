# Backgammon Computación 2025

## Autor
* **Nombre:** Dana Tinnerello

## Descripción
Este es el repositorio del proyecto para el desarrollo de un juego de Backgammon en Python para la materia de Computación 2025. El proyecto se está construyendo de forma incremental.

Este proyecto implementa el clásico juego de **Backgammon** en Python, siguiendo un enfoque de Programación Orientada a Objetos y cumpliendo con las reglas tradicionales.  

El diseño separa la **lógica central del juego (core)** de la **interfaz de usuario (CLI)**, lo que permite extenderlo fácilmente a futuras interfaces, como una interfaz gráfica con **Pygame**.  

---

## Características principales

- Juego completo de Backgammon por consola (**CLI**).  
- Lógica central desacoplada de la presentación.  
- Excepciones personalizadas para movimientos inválidos.  
- Cobertura de pruebas unitarias superior al **90%**.  
- Cumplimiento de principios **SOLID**.  
- Preparado para extenderse a interfaz gráfica con **Pygame**.  

---

## Estructura del proyecto

```
/core        → lógica central del juego (Juego, Tablero, Jugador, Dados, Ficha)
/cli         → interfaz de línea de comando
/tests       → pruebas unitarias e integración
/assets      → recursos gráficos/sonoros (para futura UI con Pygame)
```

---

## Requisitos

- Python 3.10+  
- Docker (para despliegue con contenedor)  

---

## ▶Uso en modo local (sin Docker)

### 1. Clonar el repositorio
```bash
git clone https://github.com/um-computacion/computacion-2025-backgammon-danatinnerello.git
cd computacion-2025-backgammon-danatinnerello
```

### 2. Crear entorno virtual e instalar dependencias
```bash
python3 -m venv venv
source venv/bin/activate   # en Linux/Mac
venv\Scripts\activate      # en Windows

pip install -r requirements.txt
```

### 3. Ejecutar el juego en modo CLI
```bash
python -m cli.cli

python3 -m cli.cli
```

---

## Testing

El proyecto incluye pruebas unitarias e integración para validar la lógica de movimientos, condiciones de victoria y manejo de errores.  

Ejecutar los tests:
```bash
python -m unittest 

python3 -m unittest 
```

Generar reporte de cobertura:
```bash
coverage run -m unittest
coverage report
```

---

## Ejecución con Docker
hacer
---

## Excepciones implementadas

- `MovimientoInvalidoError`: para jugadas que no cumplen reglas.  
- `SacarFichaError`: para intentos de retirar fichas inválidos.  
- `JugadorInvalidoError`: asegura que las acciones correspondan a un jugador válido.  

---

## Documentación adicional

- [JUSTIFICACION.md](JUSTIFICACION.md): archivo con las decisiones de diseño.  
- [CHANGELOG.md](CHANGELOG.md): registro de cambios por sprint.  
- [Prompts](prompts-*): prompts utilizados en desarrollo, testing y documentación.  

---

Trabajo práctico individual desarrollado para la materia **Computación 2025**.  


*NOTA: Este README se actualizará con una descripción más detallada del proyecto y un esquema de funcionamiento a medida que el desarrollo avance.*