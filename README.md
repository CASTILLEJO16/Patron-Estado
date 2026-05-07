# Aire Acondicionado Inverter - Patrón Estado

Sistema completo en Python 3.10+ usando el Patrón de Diseño Estado que simula el comportamiento de un aire acondicionado con tecnología Inverter.

## Estructura del Proyecto

```
Patron-Estado/
├── estado_ac.py                # Clase base abstracta EstadoAC
├── aire_acondicionado.py       # Contexto (AireAcondicionado)
├── main.py                     # Punto de entrada y simulación
├── estados/
│   ├── __init__.py
│   ├── estado_apagado.py
│   ├── estado_standby.py
│   ├── estado_arranque.py
│   ├── estado_activo_frio.py
│   ├── estado_activo_calor.py
│   ├── estado_mantenimiento.py
│   ├── estado_ajuste.py
│   └── estado_error.py
├── index.html                  # Interfaz web visual del mini-split
└── README.md                   # Este archivo
```

## Estados Implementados (8 concretos)

1. **Apagado** - Sin energía al compresor
2. **Standby** - Sistema listo, esperando modo
3. **Arranque** - Compresor al 130% inicial
4. **Activo Frío** - Enfriamiento alta potencia
5. **Activo Calor** - Calefacción alta potencia
6. **Mantenimiento** - Mantiene temperatura con 15% potencia
7. **Ajuste** - Adapta frecuencia por cambio ambiental
8. **Error/Protección** - Bloqueo por anomalías

## Ejecución

### Python (consola):
```bash
python main.py
```

### Interfaz Web:
Abrir `index.html` en cualquier navegador moderno.

Características de la interfaz:
- Visualización 3D del mini-split montado en pared
- Control remoto interactivo
- Partículas de flujo de aire animadas
- Panel lateral con métricas en tiempo real
- Log de transiciones de estado
- Botón de simulación automática

## Tecnologías

- **Backend**: Python 3.10+, ABC, OOP
- **Frontend**: HTML5, CSS3, JavaScript vanilla
- **Diseño**: Fuente Space Mono + Syne

## Características

- Simulación de 3 ciclos: enfriamiento, error/recuperación, calefacción
- Compresor Inverter que ajusta frecuencia según demanda
- Transiciones automáticas entre estados
- Interfaz visual con retroalimentación en tiempo real
