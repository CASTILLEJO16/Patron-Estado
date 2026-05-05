"""
Simulacion del Aire Acondicionado Inverter - 3 ciclos
"""

from aire_acondicionado import AireAcondicionado
from estados.estado_arranque import EstadoArranque
from estados.estado_activo_frio import EstadoActivoFrio
from estados.estado_activo_calor import EstadoActivoCalor
from estados.estado_mantenimiento import EstadoMantenimiento
from estados.estado_error import EstadoError


if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("  SIMULACION: AIRE ACONDICIONADO INVERTER - PATRON ESTADO")
    print("=" * 70)

    # Ciclo 1: Enfriamiento completo
    print("\n--- CICLO 1: Flujo Normal - Modo FRIO ---")
    ac = AireAcondicionado(temperatura_inicial=28.0)
    ac.temperatura_deseada = 22.0

    ac.encender()
    ac.set_modo("FRIO")

    print()
    temp_simulada = 28.0
    while temp_simulada > 24.0:
        ac.simular_cambio_ambiental(temp_simulada)
        ac.monitorear()
        if not isinstance(ac._estado, EstadoArranque):
            break
        temp_simulada -= 1.5

    print()
    while temp_simulada > 22.5:
        ac.simular_cambio_ambiental(temp_simulada)
        ac.monitorear()
        if not isinstance(ac._estado, EstadoActivoFrio):
            break
        temp_simulada -= 0.8

    print()
    ac.simular_cambio_ambiental(22.5)
    ac.monitorear()

    print()
    for _ in range(2):
        ac.monitorear()

    print()
    ac.simular_cambio_ambiental(26.0)
    ac.monitorear()

    print()
    while temp_simulada < 22.8:
        ac.simular_cambio_ambiental(temp_simulada)
        ac.monitorear()
        if isinstance(ac._estado, EstadoMantenimiento):
            break
        temp_simulada -= 0.8

    print()
    ac.monitorear()
    print()
    ac.apagar()

    # Ciclo 2: Error y reset
    print("\n--- CICLO 2: Fallo de Sensor y Recuperacion ---")
    ac2 = AireAcondicionado(temperatura_inicial=25.0)
    ac2.encender()
    ac2.set_modo("FRIO")

    print()
    ac2.simular_cambio_ambiental(23.0)
    ac2.monitorear()

    print()
    print("[!] ALERTA: Fallo de sensor detectado!")
    ac2.set_estado(EstadoError(ac2))

    print()
    ac2.encender()
    ac2.apagar()
    ac2.set_modo("CALOR")
    ac2.monitorear()

    print()
    ac2.reset()
    ac2.monitorear()

    # Ciclo 3: Calefaccion (Modo CALOR)
    print("\n--- CICLO 3: Calefaccion - Modo CALOR ---")
    ac3 = AireAcondicionado(temperatura_inicial=15.0)
    ac3.temperatura_deseada = 22.0

    ac3.encender()
    ac3.set_modo("CALOR")

    print()
    temp_simulada = 15.0
    while temp_simulada < 20.0:
        ac3.simular_cambio_ambiental(temp_simulada)
        ac3.monitorear()
        if not isinstance(ac3._estado, EstadoArranque):
            break
        temp_simulada += 1.5

    print()
    while temp_simulada < 21.5:
        ac3.simular_cambio_ambiental(temp_simulada)
        ac3.monitorear()
        if not isinstance(ac3._estado, EstadoActivoCalor):
            break
        temp_simulada += 0.8

    print()
    ac3.simular_cambio_ambiental(21.8)
    ac3.monitorear()

    print()
    for _ in range(2):
        ac3.monitorear()

    print()
    ac3.apagar()

    print("\n" + "=" * 70)
    print("  SIMULACION COMPLETADA")
    print("=" * 70)
