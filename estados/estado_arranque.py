"""
Estado: Compresor al 130%. Fase inicial rapida.
"""

import sys
sys.path.append('..')

from estado_ac import EstadoAC


class EstadoArranque(EstadoAC):
    """Compresor al 130%. Fase inicial rapida."""

    def encender(self) -> None:
        self._log("ARRANQUE", "Sistema ya esta encendido")

    def apagar(self) -> None:
        from estados.estado_apagado import EstadoApagado
        self._log("ARRANQUE", "Apagando desde arranque...")
        self._ac.set_estado(EstadoApagado(self._ac))

    def set_modo(self, modo: str) -> None:
        self._log("ARRANQUE", "No se puede cambiar modo durante arranque")

    def monitorear(self) -> None:
        diff = abs(self._ac.temperatura_actual - self._ac.temperatura_deseada)
        self._log(
            "ARRANQUE",
            f"Compresor al 130% | Temp actual: {self._ac.temperatura_actual}C -> Objetivo: {self._ac.temperatura_deseada}C"
        )
        if diff <= 2.0:
            self._log("ARRANQUE", "Temperatura cercana al objetivo -> transicionando a activo")
            if self._ac.modo == "FRIO":
                from estados.estado_activo_frio import EstadoActivoFrio
                self._ac.set_estado(EstadoActivoFrio(self._ac))
            else:
                from estados.estado_activo_calor import EstadoActivoCalor
                self._ac.set_estado(EstadoActivoCalor(self._ac))

    def reset(self) -> None:
        self._log("ARRANQUE", "No hay error que resetear")
