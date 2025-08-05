# --- Sorteo automático de equipos ---
import json
import random
import datetime
import locale
import unicodedata
import re

# Cargar base de datos de jugadores
with open('jugadores.json', 'r', encoding='utf-8') as f:
    jugadores_db = json.load(f)

# Leer fecha y hora desde partido.txt
with open('partido.txt', 'r', encoding='utf-8') as f:
    datos_partido = dict(
        line.strip().split(':', 1) for line in f if ':' in line
    )
fecha_str = datos_partido.get('fecha', '05/08').strip()
hora_str = datos_partido.get('hora', '21:00').strip()

# Configurar fecha con día de la semana
try:
    locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
except:
    try:
        locale.setlocale(locale.LC_TIME, 'Spanish_Spain')
    except:
        pass

dia, mes = map(int, fecha_str.split('/'))
ano = datetime.datetime.now().year
fecha_dt = datetime.datetime(ano, mes, dia)
dia_semana = fecha_dt.strftime('%A').capitalize()
mes_nombre = fecha_dt.strftime('%B').capitalize()
fecha_partido = f"{dia_semana} {dia:02d} de {mes_nombre}"

# Leer lista de confirmados desde confirmados.txt
with open('confirmados.txt', 'r', encoding='utf-8') as f:
    confirmados = [line.strip() for line in f if line.strip()]

# Función para normalizar nombres
def normaliza(s):
    s = s.lower().replace(" ", "")
    s = ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')
    return s

# Mapear confirmados a nombres oficiales del JSON
jugadores_partido = []
no_encontrados = []
for n in confirmados:
    encontrado = False
    for j in jugadores_db:
        if normaliza(n) == normaliza(j["nombre"]):
            jugadores_partido.append(j)
            encontrado = True
            break
    if not encontrado:
        no_encontrados.append(n)

if no_encontrados:
    print("ATENCIÓN: Los siguientes nombres de confirmados no coinciden con jugadores.json:")
    for nombre in no_encontrados:
        print(f"  - {nombre}")
    print("Corrige los nombres en confirmados.txt para que coincidan con jugadores.json.")
    print()

print(f"Jugadores confirmados encontrados: {len(jugadores_partido)}")
for j in jugadores_partido:
    print(f"  - {j['nombre']} ({j['puntaje']} pts)")
print()

# Sorteo balanceado
arqueros = [j for j in jugadores_partido if 'arquero' in j['posicion'].lower()]
delanteros = [j for j in jugadores_partido if 'delantero' in j['posicion'].lower()]

# Elegir arqueros
if len(arqueros) < 2:
    if len(arqueros) == 1:
        arquero1 = arqueros[0]
        resto_candidatos = [j for j in jugadores_partido if j['nombre'] != arquero1['nombre']]
        arquero2 = min(resto_candidatos, key=lambda x: x['puntaje'])
    else:
        ordenados = sorted(jugadores_partido, key=lambda x: x['puntaje'])
        arquero1, arquero2 = ordenados[:2]
else:
    arquero1, arquero2 = random.sample(arqueros, 2)

# Elegir delanteros
delanteros_validos = [j for j in delanteros if j['nombre'] not in [arquero1['nombre'], arquero2['nombre']]]
if len(delanteros_validos) >= 2:
    delantero1, delantero2 = random.sample(delanteros_validos, 2)
else:
    # Si no hay suficientes delanteros específicos, elegir de todos los disponibles
    todos_validos = [j for j in jugadores_partido if j['nombre'] not in [arquero1['nombre'], arquero2['nombre']]]
    delantero1, delantero2 = random.sample(todos_validos, 2)

# Quitar los elegidos del pool
elegidos = {arquero1['nombre'], arquero2['nombre'], delantero1['nombre'], delantero2['nombre']}
resto = [j for j in jugadores_partido if j['nombre'] not in elegidos]

# Completar equipos balanceando promedio
N = len(jugadores_partido)//2
mejor_team1, mejor_team2 = None, None
mejor_diff = float('inf')

for _ in range(1000):
    random.shuffle(resto)
    t1 = [arquero1, delantero1] + resto[:N-2]
    t2 = [arquero2, delantero2] + resto[N-2:]
    prom1 = sum(j['puntaje'] for j in t1) / N
    prom2 = sum(j['puntaje'] for j in t2) / N
    diff = abs(prom1 - prom2)
    if diff < mejor_diff:
        mejor_diff = diff
        mejor_team1 = t1.copy()
        mejor_team2 = t2.copy()
        mejor_prom1 = prom1
        mejor_prom2 = prom2

team1, team2 = mejor_team1, mejor_team2
prom1, prom2 = mejor_prom1, mejor_prom2

# Función para asignar posiciones dinámicamente
def asigna_posiciones_dinamico(equipo):
    asignados = {}
    # Buscar y asignar arquero
    arqueros = [j for j in equipo if 'arquero' in j['posicion'].lower()]
    if arqueros:
        arquero = arqueros[0]
        asignados[arquero['nombre']] = 'Arquero'
        arquero_nombre = arquero['nombre']
    else:
        arquero = equipo[0]
        asignados[arquero['nombre']] = 'Arquero'
        arquero_nombre = arquero['nombre']

    resto = [j for j in equipo if j['nombre'] != arquero['nombre']]
    max_por_funcion = 3
    posiciones = ['Arquero', 'Defensa', 'Mediocampo', 'Delantero']
    conteo = {p: 0 for p in posiciones}
    conteo['Arquero'] = 1
    usados = set([arquero['nombre']])

    # Asignar según preferencias
    for j in resto:
        if j['nombre'] in usados:
            continue
        preferencias = [p.strip().capitalize() for p in j['posicion'].split(',')]
        asignado = False
        for pref in preferencias:
            if pref == 'Arquero':
                continue
            if pref in conteo and conteo[pref] < max_por_funcion:
                asignados[j['nombre']] = pref
                conteo[pref] += 1
                usados.add(j['nombre'])
                asignado = True
                break
        if not asignado:
            asignados[j['nombre']] = ''

    # Asignar los que quedaron sin posición
    sin_funcion = [n for n, f in asignados.items() if f == '']
    for pos in posiciones:
        if conteo[pos] == 0:
            if sin_funcion:
                candidato = sin_funcion.pop(0)
                asignados[candidato] = pos
                conteo[pos] += 1

    # Distribuir el resto
    idx = 0
    while sin_funcion:
        nombre = sin_funcion.pop(0)
        pos = posiciones[idx % len(posiciones)]
        asignados[nombre] = pos
        conteo[pos] += 1
        idx += 1

    return asignados

# Asignar posiciones
rojo_posiciones = asigna_posiciones_dinamico(team1)
negro_posiciones = asigna_posiciones_dinamico(team2)

# Mostrar resultados
cancha = datos_partido.get('cancha', 'Pasto Sintético').strip() or 'Pasto Sintético'
titulo = f"⚽ Partido {fecha_partido} - {hora_str} hrs - Cancha {cancha}"
print(f"\n{titulo}\n")
print("="*60)

print("\n🔴 EQUIPO ROJO:")
for j in team1:
    posicion = rojo_posiciones.get(j['nombre'], 'Sin asignar')
    print(f"  {posicion:12} - {j['nombre']} ({j['puntaje']} pts)")
print(f"\n  Promedio equipo rojo: {prom1:.2f}")

print("\n⚫ EQUIPO NEGRO:")
for j in team2:
    posicion = negro_posiciones.get(j['nombre'], 'Sin asignar')
    print(f"  {posicion:12} - {j['nombre']} ({j['puntaje']} pts)")
print(f"\n  Promedio equipo negro: {prom2:.2f}")

print(f"\n  Diferencia de promedios: {abs(prom1 - prom2):.2f}")
print("="*60)

# Guardar resultados en equipos.json
equipos_data = {
    "rojo": [j["nombre"] for j in team1],
    "negro": [j["nombre"] for j in team2],
    "rojo_posiciones": rojo_posiciones,
    "negro_posiciones": negro_posiciones,
    "promedio_rojo": prom1,
    "promedio_negro": prom2,
    "fecha": fecha_partido,
    "hora": hora_str,
    "cancha": cancha
}

with open("equipos.json", "w", encoding="utf-8") as f:
    json.dump(equipos_data, f, ensure_ascii=False, indent=2)

print(f"\n✅ Sorteo completado y guardado en equipos.json")

# Ejecutar actualización del HTML si existe el script
try:
    import subprocess
    subprocess.run(["python", "actualizar_html.py"], check=True)
    print("✅ Archivos HTML actualizados correctamente")
except:
    print("⚠️  No se pudo actualizar automáticamente los archivos HTML")
