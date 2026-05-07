# Aire Acondicionado Inverter - Patrón Estado

Sistema completo en Python 3.10+ usando el Patrón de Diseño Estado que simula el comportamiento de un aire acondicionado con tecnología Inverter, con interfaz web conectada al backend Python.

## Estructura del Proyecto

```
Patron-Estado/
├── estado_ac.py                # Clase base abstracta EstadoAC
├── aire_acondicionado.py       # Contexto (AireAcondicionado)
├── main.py                     # Simulación por consola
├── app.py                      # Backend Flask (API REST)
├── estados/                    # 8 estados concretos
│   ├── __init__.py
│   ├── estado_apagado.py
│   ├── estado_standby.py
│   ├── estado_arranque.py
│   ├── estado_activo_frio.py
│   ├── estado_activo_calor.py
│   ├── estado_mantenimiento.py
│   ├── estado_ajuste.py
│   └── estado_error.py
├── index.html                  # Interfaz web conectada al backend
├── requirements.txt            # Dependencias Flask
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

## Instalación

```bash
# Instalar dependencias
pip install -r requirements.txt
```

## Uso - Sistema Integrado (Interfaz Web + Python)

**1. Iniciar el backend Flask:**
```bash
python app.py
```
El servidor iniciará en `http://localhost:5000`

**2. Abrir la interfaz web:**
Abre `http://localhost:5000` en tu navegador (o abre `index.html` directamente).

**Cómo funciona la integración:**
- El frontend JavaScript se comunica con el backend Python vía API REST
- Todas las acciones (encender, cambiar modo, ajustar temp) llaman al backend
- El backend ejecuta la lógica del Patrón Estado en Python real
- Los estados y temperaturas se sincronizan automáticamente cada 2 segundos

### API Endpoints

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/api/state` | GET | Obtener estado actual |
| `/api/encender` | POST | Encender el AC |
| `/api/apagar` | POST | Apagar el AC |
| `/api/modo` | POST | Cambiar modo (FRIO/CALOR) |
| `/api/temp` | POST | Ajustar temperatura |
| `/api/monitor` | POST | Ejecutar monitoreo |
| `/api/error` | POST | Simular error |
| `/api/reset` | POST | Resetear sistema |
| `/api/ciclo` | POST | Ejecutar ciclo completo |

## Uso - Solo Consola (opcional)

Para ejecutar solo la simulación por consola sin interfaz web:
```bash
python main.py
```

## Tecnologías

- **Backend**: Python 3.10+, Flask, Patrón Estado (State Pattern)
- **Frontend**: HTML5, CSS3, JavaScript (Fetch API)
- **Diseño**: Space Mono + Syne, interfaz 3D CSS

## Características de la Interfaz Web

- **Mini-split visual** montado en pared con display LED
- **Control remoto** interactivo con botones reales
- **Partículas de aire** animadas según el modo
- **Panel de métricas** en tiempo real (temperatura, compresor)
- **Log de transiciones** entre estados
- **Simulación automática** de ciclo completo
- **Conexión real** con el backend Python via API REST
