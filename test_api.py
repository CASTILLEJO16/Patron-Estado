#!/usr/bin/env python3
"""Script de prueba para verificar la API del AC."""

import urllib.request
import json

BASE_URL = 'http://localhost:5000/api'

def api_call(endpoint, data=None):
    url = f'{BASE_URL}/{endpoint}'
    if data:
        body = json.dumps(data).encode()
        req = urllib.request.Request(url, data=body, headers={'Content-Type': 'application/json'}, method='POST')
    else:
        req = urllib.request.Request(url, method='POST' if endpoint != 'state' else 'GET')
    
    try:
        resp = urllib.request.urlopen(req)
        return json.loads(resp.read().decode())
    except Exception as e:
        return {'error': str(e)}

def test_all():
    print("=" * 50)
    print("PRUEBA DE API - Sistema AC Inverter")
    print("=" * 50)
    
    # 1. Estado inicial
    print("\n1. Estado inicial:")
    r = api_call('state')
    print(f"   Estado: {r['state']} | Temp: {r['temp_actual']}°C | Modo: {r['modo']}")
    
    # 2. Encender
    print("\n2. Encender (transicion a STANDBY):")
    r = api_call('encender')
    print(f"   Estado: {r['state']} | {r['state_name']}")
    
    # 3. Seleccionar modo FRIO
    print("\n3. Seleccionar modo FRIO (transicion a ARRANQUE):")
    r = api_call('modo', {'modo': 'FRIO'})
    print(f"   Estado: {r['state']} | Modo: {r['modo']} | Comp: {r['compressor']}%")
    
    # 4. Simular temperatura alta para mantener arranque
    print("\n4. Simular temp 28°C (debe seguir en ARRANQUE):")
    r = api_call('simular', {'temperatura': 28.0})
    print(f"   Estado: {r['state']} | Temp: {r['temp_actual']}°C")
    
    # 5. Monitorear - bajar temperatura
    print("\n5. Monitorear (transicion a ACTIVO_FRIO):")
    r = api_call('simular', {'temperatura': 25.0})
    r = api_call('monitor')
    print(f"   Estado: {r['state']} | Temp: {r['temp_actual']}°C | Comp: {r['compressor']}%")
    
    # 6. Llegar a temperatura objetivo
    print("\n6. Llegar a temp objetivo (transicion a MANTENIMIENTO):")
    r = api_call('simular', {'temperatura': 22.0})
    r = api_call('monitor')
    print(f"   Estado: {r['state']} | Temp: {r['temp_actual']}°C | Comp: {r['compressor']}%")
    
    # 7. Cambiar modo a CALOR
    print("\n7. Cambiar a modo CALOR (transicion a ARRANQUE):")
    r = api_call('modo', {'modo': 'CALOR'})
    print(f"   Estado: {r['state']} | Modo: {r['modo']} | Comp: {r['compressor']}%")
    
    # 8. Simular error
    print("\n8. Simular ERROR:")
    r = api_call('error')
    print(f"   Estado: {r['state']} | {r['state_name']}")
    
    # 9. Intentar encender en error (debe fallar)
    print("\n9. Intentar encender en ERROR (debe bloquearse):")
    r = api_call('encender')
    print(f"   Estado: {r['state']} | (sigue en ERROR)")
    
    # 10. Reset
    print("\n10. Reset (transicion a STANDBY):")
    r = api_call('reset')
    print(f"   Estado: {r['state']} | {r['state_name']}")
    
    # 11. Apagar
    print("\n11. Apagar (transicion a APAGADO):")
    r = api_call('apagar')
    print(f"   Estado: {r['state']} | {r['state_name']}")
    
    print("\n" + "=" * 50)
    print("TODAS LAS PRUEBAS COMPLETADAS")
    print("=" * 50)

if __name__ == '__main__':
    test_all()
