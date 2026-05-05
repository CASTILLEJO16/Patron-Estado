"""
Clase base abstracta para el patrón Estado.
"""

from abc import ABC, abstractmethod


class EstadoAC(ABC):
    """Clase base abstracta para todos los estados del AC."""

    def __init__(self, ac: 'AireAcondicionado'):
        from aire_acondicionado import AireAcondicionado
        self._ac = ac

    @abstractmethod
    def encender(self) -> None: pass

    @abstractmethod
    def apagar(self) -> None: pass

    @abstractmethod
    def set_modo(self, modo: str) -> None: pass

    @abstractmethod
    def monitorear(self) -> None: pass

    @abstractmethod
    def reset(self) -> None: pass

    def _log(self, etiqueta: str, mensaje: str) -> None:
        print(f"[{etiqueta}] {mensaje}")
