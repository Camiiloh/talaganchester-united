import json

# Cargar jugadores confirmados
with open('confirmaciones_automaticas.json', 'r', encoding='utf-8') as f:
    confirmaciones = json.load(f)
confirmados = confirmaciones['2025-08-13']['jugadores']

# Cargar base de datos de jugadores
with open('jugadores_posiciones_especificas.json', 'r', encoding='utf-8') as f:
    jugadores = json.load(f)

print('🔍 DIAGNÓSTICO DEL PROBLEMA:')
print(f'📊 Jugadores confirmados: {len(confirmados)}')

jugadores_validos = []
for nombre in confirmados:
    jugador = next((j for j in jugadores if j['nombre'].lower() == nombre.lower()), None)
    if jugador:
        jugadores_validos.append(jugador)
    else:
        print(f'❌ No encontrado: {nombre}')

print(f'📊 Jugadores válidos encontrados: {len(jugadores_validos)}')

# Verificar formaciones
def generar_formaciones_test():
    formaciones_basicas = [
        {'LCB': 1, 'RCB': 1, 'LM': 1, 'CM': 1, 'RM': 0, 'CF': 1},  # 2-3-1
        {'LCB': 1, 'RCB': 1, 'LM': 0, 'CM': 2, 'RM': 1, 'CF': 0},  # 2-3-0 
        {'LCB': 2, 'RCB': 0, 'LM': 1, 'CM': 1, 'RM': 1, 'CF': 0},  # 2-3-0
    ]
    
    formaciones_validas = []
    for formacion in formaciones_basicas:
        total = sum(formacion.values())
        if total == 5:
            formaciones_validas.append(formacion)
    
    return formaciones_validas

formaciones = generar_formaciones_test()
print(f'📊 Formaciones válidas: {len(formaciones)}')
for i, f in enumerate(formaciones):
    print(f'   {i+1}: {f}')

# Test simple de optimización
if len(jugadores_validos) >= 6:
    equipo_test = jugadores_validos[:6]
    print(f'\n🧪 Test con equipo de 6 jugadores:')
    for j in equipo_test:
        print(f'   • {j["nombre"]} - Posiciones: {j["posicion"]}')
    
    # Simular optimización simple
    import itertools
    mejor_puntaje = 0
    for formacion in formaciones:
        posiciones = []
        for pos, cant in formacion.items():
            posiciones.extend([pos] * cant)
        
        for perm in list(itertools.permutations(equipo_test[1:]))[:10]:  # Solo primeras 10
            puntaje = sum(j['puntajes_posicion'][posiciones[i]] for i, j in enumerate(perm))
            if puntaje > mejor_puntaje:
                mejor_puntaje = puntaje
        
        print(f'   Formación {formacion}: mejor puntaje = {mejor_puntaje:.1f}')
