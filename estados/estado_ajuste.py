"""
Estado: Detecta cambios y recalcula frecuencia del compresor.
"""

import sys
sys.path.append('..')

from estado_ac import EstadoAC


class EstadoAjuste(EstadoAC):
    """Detecta cambios y recalcula frecuencia del compresor."""

    def encender(self) -> None:
        self._log("AJUSTE", "Sistema ya esta encendido")

    def apagar(self) -> None:
        from estados.estado_apagado import EstadoApagado
        self._log("AJUSTE", "Apagando...")
        self._ac.set_estado(EstadoApagado(self._ac))

    def set_modo(self, modo: str) -> None:
        self._log("AJUSTE", "Esperando a estabilizar antes de cambiar modo")

    def monitorear(self) -> None:
        diff = abs(self._ac.temperatura_actual - self._ac.temperatura_deseada)
        self._log(
            "AJUSTE",
            f"Regulando frecuencia Inverter | Temp: {self._ac.temperatura_actual}C | Ajustando hacia: {self._ac.temperatura_deseada}C"
        )
        if diff <= 1.0:
            from estados.estado_mantenimiento import EstadoMantenimiento
            self._log("AJUSTE", "Ajuste completado -> transicionando a MANTENIMIENTO")
            self._ac.set_estado(EstadoMantenimiento(self._ac))
        elif diff > 4.0:
            from estados.estado_arranque import EstadoArranque
            self._log("AJUSTE", "Diferencia grande -> transicionando a ARRANQUE")
            self._ac.set_estado(EstadoArranque(self._ac))

    def reset(self) -> None:
        self._log("AJUSTE", "No hay error que resetear")
