"""
Estado: Bloqueo de seguridad. Solo sale con reset().
"""

import sys
sys.path.append('..')

from estado_ac import EstadoAC


class EstadoError(EstadoAC):
    """Bloqueo de seguridad. Solo sale con reset()."""

    def encender(self) -> None:
        self._log("ERROR", "BLOQUEADO: No se puede encender hasta hacer reset()")

    def apagar(self) -> None:
        self._log("ERROR", "BLOQUEADO: No se puede apagar normalmente. Use reset()")

    def set_modo(self, modo: str) -> None:
        self._log("ERROR", "BLOQUEADO: No se puede cambiar modo. Use reset()")

    def monitorear(self) -> None:
        self._log("ERROR", f"Sistema en bloqueo de seguridad | Ultima temp: {self._ac.temperatura_actual}C")

    def reset(self) -> None:
        from estados.estado_standby import EstadoStandby
        self._log("ERROR", "Reset ejecutado -> transicionando a STANDBY")
        self._ac.set_estado(EstadoStandby(self._ac))
