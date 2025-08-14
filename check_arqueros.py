import json

# Cargar jugadores confirmados
with open('confirmaciones_automaticas.json', 'r', encoding='utf-8') as f:
    confirmaciones = json.load(f)
confirmados = confirmaciones['2025-08-13']['jugadores']

# Cargar base de datos de jugadores
with open('jugadores_posiciones_especificas.json', 'r', encoding='utf-8') as f:
    jugadores = json.load(f)

print('🥅 ARQUEROS CONFIRMADOS:')
arqueros = []
for jugador in jugadores:
    if jugador['nombre'] in confirmados and 'GK' in jugador['posicion']:
        arqueros.append(jugador['nombre'])
        print(f'   • {jugador["nombre"]} (Puntaje GK: {jugador["puntajes_posicion"]["GK"]})')

print(f'\n📊 Total arqueros confirmados: {len(arqueros)}')
print(f'📊 Arqueros necesarios para 2 equipos: 2')
print(f'📊 Estado: {"✅ SUFICIENTES" if len(arqueros) >= 2 else "❌ INSUFICIENTES"}')
