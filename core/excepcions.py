class BackgammonError(Exception):
    """Clase base para todas las excepciones del juego."""
    pass


class EntradaInvalidaError(BackgammonError):
    """Error cuando el input del usuario no es válido."""
    pass


class MovimientoInvalidoError(BackgammonError):
    """Error para un movimiento no permitido por las reglas."""
    pass


class MovimientoFueraDeRangoError(MovimientoInvalidoError):
    """Error cuando se intenta mover fuera de las posiciones válidas (1-24)."""
    pass


class MovimientoColorError(MovimientoInvalidoError):
    """Error cuando se intenta mover una ficha que no es del color del jugador."""
    pass


class SacarFichaError(MovimientoInvalidoError):
    """Error cuando se intenta sacar fichas pero no es permitido."""
    pass


class RendicionError(BackgammonError):
    """Se lanza cuando un jugador decide rendirse."""
    pass


class JuegoTerminadoError(BackgammonError):
    """Se lanza cuando el juego ha terminado."""
    pass
