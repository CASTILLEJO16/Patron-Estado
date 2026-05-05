"""
Estado: Enfriando a alta potencia.
"""

import sys
sys.path.append('..')

from estado_ac import EstadoAC


class EstadoActivoFrio(EstadoAC):
    """Enfriando a alta potencia."""

    def encender(self) -> None:
        self._log("ACTIVO_FRIO", "Sistema ya esta encendido")

    def apagar(self) -> None:
        from estados.estado_apagado import EstadoApagado
        self._log("ACTIVO_FRIO", "Apagando...")
        self._ac.set_estado(EstadoApagado(self._ac))

    def set_modo(self, modo: str) -> None:
        if modo == "CALOR":
            from estados.estado_arranque import EstadoArranque
            self._log("ACTIVO_FRIO", "Cambiando a modo CALOR -> transicionando a ARRANQUE")
            self._ac.modo = modo
            self._ac.set_estado(EstadoArranque(self._ac))

    def monitorear(self) -> None:
        self._log(
            "ACTIVO_FRIO",
            f"Enfriamiento alto | Temp: {self._ac.temperatura_actual}C | Objetivo: {self._ac.temperatura_deseada}C"
        )
        if self._ac.temperatura_actual <= self._ac.temperatura_deseada + 0.5:
            from estados.estado_mantenimiento import EstadoMantenimiento
            self._log("ACTIVO_FRIO", "Temperatura alcanzada -> transicionando a MANTENIMIENTO")
            self._ac.set_estado(EstadoMantenimiento(self._ac))

    def reset(self) -> None:
        self._log("ACTIVO_FRIO", "No hay error que resetear")
