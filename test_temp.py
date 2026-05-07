#!/usr/bin/env python3
"""Prueba específica del ajuste de temperatura."""

import urllib.request
import json

BASE_URL = 'http://localhost:5000/api'

def api_call(endpoint, data=None):
    url = f'{BASE_URL}/{endpoint}'
    if data:
        body = json.dumps(data).encode()
        req = urllib.request.Request(url, data=body, headers={'Content-Type': 'application/json'}, method='POST')
    else:
        req = urllib.request.Request(url, method='POST')
    
    try:
        resp = urllib.request.urlopen(req)
        return json.loads(resp.read().decode())
    except Exception as e:
        return {'error': str(e)}

print("=" * 50)
print("PRUEBA DE AJUSTE DE TEMPERATURA")
print("=" * 50)

# Estado inicial
print("\n1. Estado inicial:")
r = api_call('state')
print(f"   Temp deseada: {r['temp_deseado']}°C")

# Subir temperatura
print("\n2. Subir temperatura (+1):")
r = api_call('temp', {'delta': 1})
print(f"   Temp deseada: {r['temp_deseado']}°C")

# Subir más
print("\n3. Subir temperatura (+3):")
r = api_call('temp', {'delta': 3})
print(f"   Temp deseada: {r['temp_deseado']}°C")

# Bajar temperatura
print("\n4. Bajar temperatura (-2):")
r = api_call('temp', {'delta': -2})
print(f"   Temp deseada: {r['temp_deseado']}°C")

# Verificar estado completo
print("\n5. Estado completo:")
r = api_call('state')
print(f"   Estado: {r['state']}")
print(f"   Temp actual: {r['temp_actual']}°C")
print(f"   Temp deseada: {r['temp_deseado']}°C")

print("\n" + "=" * 50)
print("PRUEBA COMPLETADA")
print("=" * 50)
