"""
Estado: Sin energia. Solo permite encender().
"""

import sys
sys.path.append('..')

from estado_ac import EstadoAC


class EstadoApagado(EstadoAC):
    """Sin energia. Solo permite encender()."""

    def encender(self) -> None:
        from estados.estado_standby import EstadoStandby
        self._log("APAGADO", "Sistema iniciando... transicionando a STANDBY")
        self._ac.set_estado(EstadoStandby(self._ac))

    def apagar(self) -> None:
        self._log("APAGADO", "El sistema ya esta apagado")

    def set_modo(self, modo: str) -> None:
        self._log("APAGADO", "No se puede cambiar modo: sistema apagado")

    def monitorear(self) -> None:
        self._log("APAGADO", "Sin monitoreo activo: sistema apagado")

    def reset(self) -> None:
        self._log("APAGADO", "No hay error que resetear: sistema apagado")
