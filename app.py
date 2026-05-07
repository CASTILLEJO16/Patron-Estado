"""
Backend Flask para integrar la interfaz web con el sistema AC en Python.
Con simulación automática de temperatura y cambios de estado.
"""

import threading
import time
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from aire_acondicionado import AireAcondicionado
from estados.estado_arranque import EstadoArranque
from estados.estado_activo_frio import EstadoActivoFrio
from estados.estado_activo_calor import EstadoActivoCalor
from estados.estado_mantenimiento import EstadoMantenimiento
from estados.estado_ajuste import EstadoAjuste
from estados.estado_error import EstadoError

app = Flask(__name__, static_folder='.')
CORS(app)

# Instancia global del AC
ac = AireAcondicionado(temperatura_inicial=28.0)

# Configuración de simulación automática
SIMULACION_ACTIVA = True
INTERVALO_SIMULACION = 1.0  # segundos entre cada ciclo de simulación (más rápido)

# Thread de simulación
def simulacion_automatica():
    """Thread que simula automáticamente el comportamiento del AC."""
    while SIMULACION_ACTIVA:
        estado_class = ac._estado.__class__.__name__
        
        # Solo simular si no está apagado ni en error
        if estado_class not in ['EstadoApagado', 'EstadoError']:
            # Simular cambio de temperatura según el modo y estado
            if estado_class in ['EstadoArranque', 'EstadoActivoFrio', 'EstadoAjuste'] and ac.modo == 'FRIO':
                # Enfriando: bajar temperatura
                if ac.temperatura_actual > ac.temperatura_deseada:
                    ac.temperatura_actual = max(ac.temperatura_deseada - 0.5, ac.temperatura_actual - 0.8)
            elif estado_class in ['EstadoArranque', 'EstadoActivoCalor', 'EstadoAjuste'] and ac.modo == 'CALOR':
                # Calentando: subir temperatura
                if ac.temperatura_actual < ac.temperatura_deseada:
                    ac.temperatura_actual = min(ac.temperatura_deseada + 0.5, ac.temperatura_actual + 0.8)
            elif estado_class == 'EstadoMantenimiento':
                # Mantenimiento: pequeñas fluctuaciones
                diff = ac.temperatura_deseada - ac.temperatura_actual
                if abs(diff) > 0.3:
                    # Ajustar suavemente hacia el objetivo
                    ac.temperatura_actual += diff * 0.1
            
            # Llamar a monitorear para que el estado evalúe transiciones
            ac.monitorear()
        
        time.sleep(INTERVALO_SIMULACION)

# Iniciar thread de simulación
thread_simulacion = threading.Thread(target=simulacion_automatica, daemon=True)
thread_simulacion.start()

# Mapeo de nombres de estado
ESTADO_NAMES = {
    'EstadoApagado': 'APAGADO',
    'EstadoStandby': 'STANDBY',
    'EstadoArranque': 'ARRANQUE',
    'EstadoActivoFrio': 'ACTIVO_FRIO',
    'EstadoActivoCalor': 'ACTIVO_CALOR',
    'EstadoMantenimiento': 'MANTENIMIENTO',
    'EstadoAjuste': 'AJUSTE',
    'EstadoError': 'ERROR'
}

# Configuración de estados
ESTADOS_CONFIG = {
    'APAGADO': {'name': 'Apagado', 'color': '#5a6080', 'desc': 'Sin energía al compresor.', 'comp': 0},
    'STANDBY': {'name': 'Standby', 'color': '#a0a8c0', 'desc': 'Sistema listo, esperando selección de modo.', 'comp': 0},
    'ARRANQUE': {'name': 'Arranque', 'color': '#e8c840', 'desc': 'Compresor subiendo al 130% para alcanzar temperatura rápido.', 'comp': 130},
    'ACTIVO_FRIO': {'name': 'Activo — frío', 'color': '#00d4ff', 'desc': 'Enfriamiento activo a alta potencia.', 'comp': 90},
    'ACTIVO_CALOR': {'name': 'Activo — calor', 'color': '#ff6b35', 'desc': 'Calefacción activa a alta potencia.', 'comp': 90},
    'MANTENIMIENTO': {'name': 'Mantenimiento', 'color': '#00e5a0', 'desc': 'Temperatura alcanzada. Compresor a baja potencia manteniendo estabilidad.', 'comp': 15},
    'AJUSTE': {'name': 'Ajuste', 'color': '#c8a020', 'desc': 'Cambio ambiental detectado. Regulando frecuencia del compresor.', 'comp': 55},
    'ERROR': {'name': 'Error / Protección', 'color': '#ff2d55', 'desc': 'Bloqueo de seguridad. Ejecuta reset() para recuperar.', 'comp': 0}
}


def get_estado_info():
    """Obtiene información del estado actual del AC."""
    estado_class = ac._estado.__class__.__name__
    estado_key = ESTADO_NAMES.get(estado_class, 'APAGADO')
    config = ESTADOS_CONFIG.get(estado_key, ESTADOS_CONFIG['APAGADO'])
    
    return {
        'state': estado_key,
        'state_name': config['name'],
        'color': config['color'],
        'description': config['desc'],
        'compressor': config['comp'],
        'temp_actual': ac.temperatura_actual,
        'temp_deseado': ac.temperatura_deseada,
        'modo': ac.modo
    }


@app.route('/')
def index():
    return send_from_directory('.', 'index.html')


@app.route('/api/state', methods=['GET'])
def get_state():
    """Obtiene el estado actual del AC."""
    return jsonify(get_estado_info())


@app.route('/api/encender', methods=['POST'])
def api_encender():
    """Enciende el AC."""
    ac.encender()
    return jsonify(get_estado_info())


@app.route('/api/apagar', methods=['POST'])
def api_apagar():
    """Apaga el AC."""
    ac.apagar()
    return jsonify(get_estado_info())


@app.route('/api/modo', methods=['POST'])
def api_set_modo():
    """Establece el modo (FRIO/CALOR) y ajusta temperatura inicial para simulación."""
    data = request.get_json()
    modo = data.get('modo', 'FRIO')
    
    # Ajustar temperatura según el modo para que se vea el efecto
    if modo == 'FRIO':
        # Para frío: empezar con temperatura alta para que baje
        if ac.temperatura_actual <= ac.temperatura_deseada:
            ac.temperatura_actual = 28.0  # Reset a temperatura caliente
    elif modo == 'CALOR':
        # Para calor: empezar con temperatura baja para que suba
        if ac.temperatura_actual >= ac.temperatura_deseada:
            ac.temperatura_actual = 15.0  # Reset a temperatura fría
    
    ac.set_modo(modo)
    return jsonify(get_estado_info())


@app.route('/api/temp', methods=['POST'])
def api_set_temp():
    """Ajusta la temperatura deseada."""
    data = request.get_json()
    delta = data.get('delta', 0)
    ac.temperatura_deseada = max(16, min(30, ac.temperatura_deseada + delta))
    return jsonify(get_estado_info())


@app.route('/api/monitor', methods=['POST'])
def api_monitor():
    """Ejecuta un ciclo de monitoreo."""
    ac.monitorear()
    return jsonify(get_estado_info())


@app.route('/api/simular', methods=['POST'])
def api_simular():
    """Simula cambio de temperatura ambiental."""
    data = request.get_json()
    nueva_temp = data.get('temperatura')
    if nueva_temp is not None:
        ac.simular_cambio_ambiental(nueva_temp)
    return jsonify(get_estado_info())


@app.route('/api/error', methods=['POST'])
def api_error():
    """Simula un error del sistema."""
    ac.set_estado(EstadoError(ac))
    return jsonify(get_estado_info())


@app.route('/api/reset', methods=['POST'])
def api_reset():
    """Resetea el sistema desde error."""
    ac.reset()
    return jsonify(get_estado_info())


@app.route('/api/ciclo', methods=['POST'])
def api_ciclo():
    """Ejecuta un ciclo completo de simulación automática."""
    results = []
    
    # Ciclo de enfriamiento
    ac.apagar()
    ac.simular_cambio_ambiental(28.0)
    ac.temperatura_deseada = 22.0
    ac.encender()
    ac.set_modo('FRIO')
    results.append(get_estado_info())
    
    # Simular enfriamiento progresivo
    temp = 28.0
    while temp > 23.0:
        ac.simular_cambio_ambiental(temp)
        ac.monitorear()
        temp -= 1.5
        results.append(get_estado_info())
    
    return jsonify({'ciclo': results, 'final': get_estado_info()})


if __name__ == '__main__':
    print("="*50)
    print("  Servidor Flask - AC Inverter")
    print("  Accede a: http://localhost:5000")
    print("="*50)
    app.run(debug=True, port=5000)
