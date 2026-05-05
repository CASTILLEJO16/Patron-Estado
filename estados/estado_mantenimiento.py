"""
Estado: Baja potencia manteniendo temp estable.
"""

import sys
sys.path.append('..')

from estado_ac import EstadoAC


class EstadoMantenimiento(EstadoAC):
    """Baja potencia manteniendo temp estable."""

    def encender(self) -> None:
        self._log("MANTENIMIENTO", "Sistema ya esta encendido")

    def apagar(self) -> None:
        from estados.estado_apagado import EstadoApagado
        self._log("MANTENIMIENTO", "Apagando...")
        self._ac.set_estado(EstadoApagado(self._ac))

    def set_modo(self, modo: str) -> None:
        if modo != self._ac.modo:
            from estados.estado_arranque import EstadoArranque
            self._log("MANTENIMIENTO", f"Cambiando a modo {modo} -> ARRANQUE")
            self._ac.modo = modo
            self._ac.set_estado(EstadoArranque(self._ac))

    def monitorear(self) -> None:
        diff = abs(self._ac.temperatura_actual - self._ac.temperatura_deseada)
        self._log(
            "MANTENIMIENTO",
            f"Compresor bajo (Inverter) | Temp estable: {self._ac.temperatura_actual}C | Desvio: {diff:.1f}C"
        )
        if diff > 2.0:
            from estados.estado_ajuste import EstadoAjuste
            self._log("MANTENIMIENTO", "Cambio ambiental detectado -> transicionando a AJUSTE")
            self._ac.set_estado(EstadoAjuste(self._ac))

    def reset(self) -> None:
        self._log("MANTENIMIENTO", "No hay error que resetear")
