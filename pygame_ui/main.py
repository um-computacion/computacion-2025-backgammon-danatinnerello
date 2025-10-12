"""
main.py
Responsabilidad:
- Punto de entrada del juego con Pygame.
- Inicializa la ventana y configura el bucle principal del juego.
- Se encarga de llamar a los métodos de dibujo (board_renderer).
- Captura eventos (mouse, teclado) usando events.py.
- Mantiene el loop de juego (update → draw → events).
"""
import pygame
from pygame_ui.board_renderer import TableroGrafico, estado_desde_board
from core.player import Jugador
from core.game import Juego

pygame.init()

def pedir_nombres(pantalla):
    fuente = pygame.font.Font(None, 48)
    texto1 = fuente.render("Jugador 1 (Blancas):", True, (0, 0, 0))
    texto2 = fuente.render("Jugador 2 (Negras):", True, (0, 0, 0))
    pantalla.fill((240, 230, 200))
    pantalla.blit(texto1, (250, 200))
    pantalla.blit(texto2, (250, 300))
    pygame.display.flip()
    return "Jugador 1", "Jugador 2"

def dibujar_dados(pantalla, valores, jugador_actual):
    """Muestra el turno actual y los valores de los dados en pantalla"""
    fuente = pygame.font.Font(None, 48)
    texto_turno = fuente.render(
        f"Turno: {jugador_actual.obtener_nombre()} ({jugador_actual.obtener_color()})", True, (0, 0, 0)
    )
    pantalla.blit(texto_turno, (50, 15))
    if valores:
        texto_dados = fuente.render(f"Dados: {valores}", True, (0, 0, 0))
        pantalla.blit(texto_dados, (600, 15))

def main():
    pantalla = pygame.display.set_mode((1000, 600))
    pygame.display.set_caption("Backgammon - Pygame UI")

    jugador1 = Jugador("Jugador 1", "Blanca")
    jugador2 = Jugador("Jugador 2", "Negra")
    juego = Juego(jugador1, jugador2)

    tablero = juego.mostrar_tablero()
    renderer = TableroGrafico(pantalla)
    estado = estado_desde_board(tablero)

    renderer.dibujar_tablero()
    renderer.dibujar_fichas(estado)
    pygame.display.flip()

    
    running = True
    punto_seleccionado = None
    dados_actuales = []
    puede_mover = False

    #Bucle
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE:
                    #Tira los dados
                    dados_actuales = juego.__dados__.tirar_dados()
                    puede_mover = True
                    print(f"Dados tirados: {dados_actuales}")

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                punto = renderer.obtener_punto_desde_click(event.pos)
                if punto and puede_mover:
                    jugador_actual = juego.mostrar_turno()
                    if punto_seleccionado is None:
                        punto_seleccionado = punto
                        print(f"{jugador_actual.obtener_nombre()} seleccionó el punto {punto_seleccionado}")
                    else:
                        try:
                            juego.valida_mover_ficha(jugador_actual, punto_seleccionado, punto)
                            print(f"{jugador_actual.obtener_nombre()} movió de {punto_seleccionado} a {punto}")
                        except Exception as e:
                            print(f"No se pudo mover la ficha: {e}")
                        punto_seleccionado = None

                        #Actualiza tablero
                        estado = estado_desde_board(juego.mostrar_tablero())
                        renderer.dibujar_tablero()
                        renderer.dibujar_fichas(estado)
                        dibujar_dados(pantalla, dados_actuales, jugador_actual)
                        pygame.display.flip()

                        #Cambia turno si no quedan tiradas
                        if not juego.__dados__.obtener_tiradas_restantes():
                            print("Fin del turno, cambiando jugador...")
                            juego.controlar_turnos()
                            dados_actuales = []
                            puede_mover = False

        # Redibuja tablero y dados en cada frame
        renderer.dibujar_tablero()
        renderer.dibujar_fichas(estado_desde_board(juego.mostrar_tablero()))
        dibujar_dados(pantalla, dados_actuales, juego.mostrar_turno())
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
