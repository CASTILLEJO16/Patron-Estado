"""
Contexto del patrón Estado.
"""

from typing import Optional


class AireAcondicionado:
    """Contexto del patrón Estado. Guarda temperaturas, modo y estado actual."""

    def __init__(self, temperatura_inicial: float = 28.0):
        self.temperatura_deseada: float = 22.0
        self.temperatura_actual: float = temperatura_inicial
        self.modo: str = "FRIO"
        self._estado: Optional['EstadoAC'] = None

        from estados.estado_apagado import EstadoApagado
        self.set_estado(EstadoApagado(self))

    def set_estado(self, estado: 'EstadoAC') -> None:
        self._estado = estado

    def encender(self) -> None: self._estado.encender()
    def apagar(self) -> None: self._estado.apagar()
    def set_modo(self, modo: str) -> None: self._estado.set_modo(modo)
    def monitorear(self) -> None: self._estado.monitorear()
    def reset(self) -> None: self._estado.reset()

    def simular_cambio_ambiental(self, nueva_temperatura: float) -> None:
        self.temperatura_actual = nueva_temperatura
