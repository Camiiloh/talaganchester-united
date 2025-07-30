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
def normaliza(s):
    return s.lower().replace(" ", "")

# Mapear confirmados a nombres oficiales del JSON
jugadores_partido = []
for n in confirmados:
    for j in jugadores_db:
        if normaliza(n) == normaliza(j["nombre"]):
            jugadores_partido.append(j)
            break


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
if len(arqueros) < 2:
    raise Exception('No hay suficientes arqueros confirmados para el sorteo')
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
    else:
        arquero = equipo[0]
        asignados[arquero['nombre']] = 'Arquero'
    # 2. Separar el resto de los jugadores
    resto = [j for j in equipo if j['nombre'] != arquero['nombre']]
    # 3. Clasificar por preferencia principal
    defensas = [j for j in resto if 'defensa' in j['posicion'].lower()]
    mediocampos = [j for j in resto if 'mediocampo' in j['posicion'].lower()]
    delanteros = [j for j in resto if 'delantero' in j['posicion'].lower()]
    # 4. Asignar defensas (pueden ser 1, 2, 3... según cantidad y preferencias)
    usados = set()
    for j in defensas:
        if j['nombre'] not in asignados:
            asignados[j['nombre']] = 'Defensa'
            usados.add(j['nombre'])
    # 5. Asignar mediocampos
    for j in mediocampos:
        if j['nombre'] not in asignados:
            asignados[j['nombre']] = 'Mediocampo'
            usados.add(j['nombre'])
    # 6. Asignar delanteros
    for j in delanteros:
        if j['nombre'] not in asignados:
            asignados[j['nombre']] = 'Delantero'
            usados.add(j['nombre'])
    # 7. Si quedan jugadores sin asignar, usar su primera preferencia
    for j in resto:
        if j['nombre'] not in asignados:
            primera = j['posicion'].split(',')[0].strip().capitalize()
            asignados[j['nombre']] = primera
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

    # Ejecutar actualizar_html.py para sincronizar los equipos en index.html y cancha.html
    import subprocess
    subprocess.run(["python", "actualizar_html.py"], check=True)