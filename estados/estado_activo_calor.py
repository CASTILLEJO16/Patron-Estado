"""
Estado: Calentando a alta potencia.
"""

import sys
sys.path.append('..')

from estado_ac import EstadoAC


class EstadoActivoCalor(EstadoAC):
    """Calentando a alta potencia."""

    def encender(self) -> None:
        self._log("ACTIVO_CALOR", "Sistema ya esta encendido")

    def apagar(self) -> None:
        from estados.estado_apagado import EstadoApagado
        self._log("ACTIVO_CALOR", "Apagando...")
        self._ac.set_estado(EstadoApagado(self._ac))

    def set_modo(self, modo: str) -> None:
        if modo == "FRIO":
            from estados.estado_arranque import EstadoArranque
            self._log("ACTIVO_CALOR", "Cambiando a modo FRIO -> transicionando a ARRANQUE")
            self._ac.modo = modo
            self._ac.set_estado(EstadoArranque(self._ac))

    def monitorear(self) -> None:
        self._log(
            "ACTIVO_CALOR",
            f"Calefaccion alta | Temp: {self._ac.temperatura_actual}C | Objetivo: {self._ac.temperatura_deseada}C"
        )
        if self._ac.temperatura_actual >= self._ac.temperatura_deseada - 0.5:
            from estados.estado_mantenimiento import EstadoMantenimiento
            self._log("ACTIVO_CALOR", "Temperatura alcanzada -> transicionando a MANTENIMIENTO")
            self._ac.set_estado(EstadoMantenimiento(self._ac))

    def reset(self) -> None:
        self._log("ACTIVO_CALOR", "No hay error que resetear")
