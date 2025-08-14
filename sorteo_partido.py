# --- Actualizar cancha.html automáticamente ---
import re


import json
import random

# Cargar base de datos de jugadores
with open('jugadores.json', 'r', encoding='utf-8') as f:
    jugadores_db = json.load(f)




# Leer fecha y hora desde partido.txt
with open('partido.txt', 'r', encoding='utf-8') as f:
    datos_partido = dict(
        line.strip().split(':', 1) for line in f if ':' in line
    )
fecha_str = datos_partido.get('fecha', '24/07').strip()
hora_str = datos_partido.get('hora', '21:00').strip()

import datetime, locale
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

# Filtrar jugadores confirmados con coincidencia parcial (case-insensitive, ignora espacios)
import unicodedata
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


# Balancear equipos por puntaje promedio (algoritmo simple: greedy)

# Sorteo aleatorio balanceado por promedio

# --- Sorteo priorizando arquero y delantero distintos por equipo ---

# --- Sorteo priorizando arquero y delantero distintos por equipo ---
# Definir posiciones por orden de preferencia
posiciones_orden = [
    "Arquero", "Defensa", "Defensa", "Mediocampo", "Delantero", "Delantero", "Extra"
]

arqueros = [j for j in jugadores_partido if 'arquero' in j['posicion'].lower()]
delanteros = [j for j in jugadores_partido if 'delantero' in j['posicion'].lower()]

# Elegir dos arqueros distintos

# Si no hay suficientes arqueros, asignar al de menor puntaje
if len(arqueros) < 2:
    # Permitir que cualquier jugador pueda ir al arco, el de menor puntaje
    if len(arqueros) == 1:
        arquero1 = arqueros[0]
        resto_candidatos = [j for j in jugadores_partido if j['nombre'] != arquero1['nombre']]
        if not resto_candidatos:
            raise Exception('No hay suficientes jugadores para cubrir el arco. Solo hay un jugador disponible.')
        arquero2 = min(resto_candidatos, key=lambda x: x['puntaje'])
    else:
        # No hay arqueros, elegir dos de menor puntaje de todos los jugadores
        ordenados = sorted(jugadores_partido, key=lambda x: x['puntaje'])
        if len(ordenados) < 2:
            raise Exception('No hay suficientes jugadores para cubrir el arco. Faltan jugadores.')
        arquero1, arquero2 = ordenados[:2]
else:
    arquero1, arquero2 = random.sample(arqueros, 2)

# Elegir dos delanteros distintos y que no sean los arqueros
delanteros_validos = [j for j in delanteros if j['nombre'] not in [arquero1['nombre'], arquero2['nombre']]]
if len(delanteros_validos) < 2:
    raise Exception('No hay suficientes delanteros confirmados para el sorteo')
delantero1, delantero2 = random.sample(delanteros_validos, 2)

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


# =============================
# Asignación dinámica de posiciones por equipo
# =============================
# 1. Siempre se asigna un arquero fijo por equipo (el primero que tenga preferencia de arquero).
# 2. El resto de los jugadores se distribuye en defensa, mediocampo y delantera según sus preferencias y la cantidad de confirmados.
# 3. La cantidad de defensas, mediocampistas y delanteros es variable y depende de los jugadores disponibles y sus preferencias.

def asigna_posiciones_dinamico(equipo):
    asignados = {}
    # 1. Buscar y asignar arquero
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
    conteo['Arquero'] = 1  # Ya se asignó el arquero fijo
    usados = set([arquero['nombre']])

    # 1. Asignar hasta 3 por función según preferencias
    for j in resto:
        if j['nombre'] in usados:
            continue
        preferencias = [p.strip().capitalize() for p in j['posicion'].split(',')]
        asignado = False
        for pref in preferencias:
            # Solo el primer arquero puede recibir esa función
            if pref == 'Arquero' or (pref == 'Arquero' and j['nombre'] != arquero_nombre):
                continue
            if pref in conteo and conteo[pref] < max_por_funcion:
                asignados[j['nombre']] = pref
                conteo[pref] += 1
                usados.add(j['nombre'])
                asignado = True
                break
        if not asignado:
            asignados[j['nombre']] = ''

    # 2. Si alguna posición quedó sin al menos 1 jugador, reasignar para cubrir todas las posiciones
    sin_funcion = [n for n, f in asignados.items() if f == '']
    for pos in posiciones:
        if conteo[pos] == 0:
            # Buscar primero entre los sin función
            candidato = None
            if sin_funcion:
                candidato = sin_funcion.pop(0)
            else:
                # Si no hay sin función, buscar entre los que tienen función repetida (más de 1 en la misma función)
                for n, f in asignados.items():
                    if f and conteo[f] > 1 and f != pos:
                        candidato = n
                        conteo[f] -= 1
                        break
            if candidato:
                asignados[candidato] = pos
                conteo[pos] += 1

    # 3. Si aún quedan sin función y alguna posición tiene menos de 3, seguir llenando hasta 3 por función
    for pos in posiciones:
        while conteo[pos] < max_por_funcion and sin_funcion:
            nombre = sin_funcion.pop(0)
            asignados[nombre] = pos
            conteo[pos] += 1

    # 4. Si aún quedan sin función, repartirlos equitativamente en las posiciones (aunque se sobrepase el límite)
    idx = 0
    while sin_funcion:
        nombre = sin_funcion.pop(0)
        pos = posiciones[idx % len(posiciones)]
        asignados[nombre] = pos
        conteo[pos] += 1
        idx += 1

    return asignados

# Asignar posiciones dinámicamente a cada equipo
rojo_posiciones = asigna_posiciones_dinamico(team1)
negro_posiciones = asigna_posiciones_dinamico(team2)


# --- Actualizar index.html automáticamente ---

# Guardar resultados del sorteo en equipos.json para replicar y sincronizar
import os
equipos_data = {
    "rojo": [j["nombre"] for j in team1],
    "negro": [j["nombre"] for j in team2],
    "rojo_posiciones": rojo_posiciones,
    "negro_posiciones": negro_posiciones,
    "promedio_rojo": prom1,
    "promedio_negro": prom2,
    "fecha": fecha_partido,
    "hora": hora_str,
    "cancha": datos_partido.get('cancha', '').strip() or 'por confirmar'
}
with open("equipos.json", "w", encoding="utf-8") as f:
    import json
    json.dump(equipos_data, f, ensure_ascii=False, indent=2)

# Mostrar resultado del sorteo en pantalla
if __name__ == "__main__":
    # Ingreso interactivo y flexible
    fecha_raw = input("Fecha del partido: ").strip()
    hora_raw = input("Hora del partido: ").strip()
    cancha_raw = input("Cancha del partido: ").strip()

    # Normalización de fecha con día de semana y mes en palabras
    import re, datetime
    meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
    fecha_match = re.search(r'(\d{1,2})[\s/-]*(de)?[\s/-]*(\d{1,2}|\w+)', fecha_raw, re.IGNORECASE)
    fecha = fecha_raw
    try:
        if fecha_match:
            dia = int(fecha_match.group(1))
            mes = fecha_match.group(3)
            if mes.isdigit():
                mes_nombre = meses[int(mes)-1]
            else:
                mes_nombre = mes.capitalize()
            # Calcular día de la semana
            ano = datetime.datetime.now().year
            fecha_dt = datetime.datetime(ano, int(mes) if mes.isdigit() else meses.index(mes_nombre)+1, dia)
            dia_semana = fecha_dt.strftime('%A').capitalize()
            fecha = f"{dia_semana} {dia} de {mes_nombre}"
    except Exception:
        pass

    # Normalización de hora
    hora_match = re.search(r'(\d{1,2}):(\d{2})', hora_raw)
    if hora_match:
        hora = f"{hora_match.group(1)}:{hora_match.group(2)}"
    else:
        hora = hora_raw
    hora = hora.replace('hrs', '').replace('hr', '').strip()

    # Normalización de cancha
    cancha = cancha_raw.strip()

    # Formato final para el título
    titulo = f"⚽ Partido {fecha} - {hora} hrs - Cancha {cancha}"
    print(f"\n{titulo}\n")

    print("Equipo Rojo:")
    for j in team1:
        print(f"- {j['nombre']} (puntaje: {j['puntaje']})")
    print(f"Promedio equipo rojo: {prom1:.2f}\n")
    print("Equipo Negro:")
    for j in team2:
        print(f"- {j['nombre']} (puntaje: {j['puntaje']})")
    print(f"Promedio equipo negro: {prom2:.2f}\n")

    # Guardar resultados del sorteo en equipos.json para replicar y sincronizar
    equipos_data = {
        "rojo": [j["nombre"] for j in team1],
        "negro": [j["nombre"] for j in team2],
        "rojo_posiciones": rojo_posiciones,
        "negro_posiciones": negro_posiciones,
        "promedio_rojo": prom1,
        "promedio_negro": prom2,
        "fecha": fecha,
        "hora": f"{hora}",
        "cancha": cancha
    }
    with open("equipos.json", "w", encoding="utf-8") as f:
        import json
        json.dump(equipos_data, f, ensure_ascii=False, indent=2)

    # Los equipos se sincronizarán automáticamente desde la interfaz web
    print("✅ Sorteo completado - Los archivos HTML se actualizarán automáticamente desde la web")