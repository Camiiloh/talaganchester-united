import json

# Cargar jugadores (usando utf-8-sig para manejar BOM)
with open('jugadores_posiciones_especificas.json', encoding='utf-8-sig') as f:
    jugadores = json.load(f)

# Ordenar por puntaje
jugadores_sorted = sorted(jugadores, key=lambda x: x['puntaje'], reverse=True)

print('📊 PROMEDIOS DE JUGADORES (ordenados por puntaje general)')
print('='*70)
for i, j in enumerate(jugadores_sorted):
    print(f'{i+1:2}. {j["nombre"]:20} - {j["puntaje"]:.2f}  ({j["posicion"]})')

print('\n' + '='*70)
print(f'Total de jugadores: {len(jugadores)}')
promedio_general = sum(j['puntaje'] for j in jugadores) / len(jugadores)
print(f'Promedio general: {promedio_general:.2f}')
