"""
Estado: Encendido esperando. Permite elegir FRIO/CALOR.
"""

import sys
sys.path.append('..')

from estado_ac import EstadoAC


class EstadoStandby(EstadoAC):
    """Encendido esperando. Permite elegir FRIO/CALOR."""

    def encender(self) -> None:
        self._log("STANDBY", "Sistema ya esta encendido")

    def apagar(self) -> None:
        from estados.estado_apagado import EstadoApagado
        self._log("STANDBY", "Apagando sistema... transicionando a APAGADO")
        self._ac.set_estado(EstadoApagado(self._ac))

    def set_modo(self, modo: str) -> None:
        if modo not in ("FRIO", "CALOR"):
            self._log("STANDBY", f"Modo invalido: {modo}. Use FRIO o CALOR")
            return
        from estados.estado_arranque import EstadoArranque
        self._ac.modo = modo
        self._log("STANDBY", f"Modo {modo} seleccionado -> transicionando a ARRANQUE")
        self._ac.set_estado(EstadoArranque(self._ac))

    def monitorear(self) -> None:
        self._log("STANDBY", f"En espera | Temp actual: {self._ac.temperatura_actual}C")

    def reset(self) -> None:
        self._log("STANDBY", "No hay error que resetear")
