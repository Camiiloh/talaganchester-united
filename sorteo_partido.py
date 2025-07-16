






# --- Actualizar cancha.html automáticamente ---
import re


import json
import random

# Cargar base de datos de jugadores
with open('jugadores.json', 'r', encoding='utf-8') as f:
    jugadores_db = json.load(f)



fecha_str = "17/07"
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

# Lista de confirmados para el partido (ajustar nombres según base de datos)
confirmados = [
    "Camilo",
    "Cristobal",
    "FranciscoH",
    "Ivan",
    "Pancho",
    "Maxi Vargas",
    "pablodona",
    "Enrique",
    "Diego",
    "Marco",
    "Juan R",
    "Carlos P."
]

# Filtrar jugadores confirmados con coincidencia parcial (case-insensitive, ignora espacios)
def normaliza(s):
    return s.lower().replace(" ", "")

jugadores_partido = []
for n in confirmados:
    for j in jugadores_db:
        if normaliza(n) in normaliza(j["nombre"]):
            jugadores_partido.append(j)
            break


# Balancear equipos por puntaje promedio (algoritmo simple: greedy)
jugadores_ordenados = sorted(jugadores_partido, key=lambda x: x['puntaje'], reverse=True)
team1, team2 = [], []
sum1, sum2 = 0, 0
for j in jugadores_ordenados:
    if len(team1) < len(jugadores_partido)//2 and (sum1 <= sum2 or len(team2) >= len(jugadores_partido)//2):
        team1.append(j)
        sum1 += j['puntaje']
    else:
        team2.append(j)
        sum2 += j['puntaje']

prom1 = sum1 / len(team1) if team1 else 0
prom2 = sum2 / len(team2) if team2 else 0


# --- Actualizar index.html automáticamente ---
import re
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Actualizar fecha en el título
html = re.sub(r'<h1>⚽ Partido.*? - 21:00 hrs - Cancha 1</h1>',
              f'<h1>⚽ Partido {fecha_partido} - 21:00 hrs - Cancha 1</h1>', html)

# Actualizar listado de jugadores confirmados
jugadores_grid = ''
for idx, nombre in enumerate(confirmados, 1):
    jugadores_grid += f'<div class="player-card"><span class="player-number">{idx}</span><span class="player-name">{nombre}</span></div>\n'
html = re.sub(r'<div class="players-grid">.*?</div>\s*<div class="stats-section">',
              f'<div class="players-grid">\n{jugadores_grid}</div>\n        <div class="stats-section">', html, flags=re.DOTALL)

# Actualizar cantidad de jugadores confirmados
html = re.sub(r'<h2>\d+ Jugadores Confirmados</h2>',
              f'<h2>{len(confirmados)} Jugadores Confirmados</h2>', html)

# Actualizar equipos
equipos_regex = re.compile(r'(<div class="teams-grid">)(.*?)(</div>\s*</div>\s*</main>)', re.DOTALL)

rojo_html = f'''
            <div class="team-section">
              <div class="team-header team-red">
                <h3>Rojo</h3>
                <div class="team-stats">
                  <span class="team-average">Promedio: {prom1:.2f}</span>
                  <span class="team-count">{len(team1)} jugadores</span>
                </div>
              </div>
              <div class="team-players">\n'''
for j in team1:
    rojo_html += f'                <div class="team-player"><span class="player-name">{j["nombre"]}</span></div>\n'
rojo_html += '              </div>\n            </div>\n'

negro_html = f'''
            <div class="team-section">
              <div class="team-header team-black">
                <h3>Negro</h3>
                <div class="team-stats">
                  <span class="team-average">Promedio: {prom2:.2f}</span>
                  <span class="team-count">{len(team2)} jugadores</span>
                </div>
              </div>
              <div class="team-players">\n'''
for j in team2:
    negro_html += f'                <div class="team-player"><span class="player-name">{j["nombre"]}</span></div>\n'
negro_html += '              </div>\n            </div>\n'

nuevo_equipos = f'<div class="teams-grid">\n{rojo_html}{negro_html}          </div>\n        </div>\n      </main>'

html_nuevo = equipos_regex.sub(lambda m: nuevo_equipos, html)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html_nuevo)
# Al final del script, después de definir fecha_partido, team1, team2
def actualizar_cancha_html():
    with open('cancha.html', 'r', encoding='utf-8') as f:
        cancha_html = f.read()

    # Actualizar fecha en el header de cancha.html
    cancha_html = re.sub(r'Partido [^<]+', f'Partido {fecha_partido} - 21:00 hrs', cancha_html)

    # Generar listas para equipos
    def jugadores_li(equipo):
        def jugador_li(j):
            nombre = j["nombre"]
            if nombre.strip().lower() == 'iván':
                img = 'fotos/Ivan.png'
            elif nombre.strip() == 'Francisco H':
                img = 'fotos/FranciscoH.png'
            else:
                base = nombre.split()[0].split('(')[0].strip()
                img = f'fotos/{base}.png'
            return f'<li><img src="{img}" alt="{nombre}" style="width:28px;height:28px;vertical-align:middle;border-radius:6px;margin-right:6px;box-shadow:0 2px 8px #2196f355;"> <strong>{nombre}</strong></li>'
        return '\n'.join([jugador_li(j) for j in equipo])

    cancha_html = re.sub(r'(<div class="team-info black">[\s\S]*?<ul>)[\s\S]*?(</ul>)',
        r'\1\n' + jugadores_li(team2) + r'\2', cancha_html)
    cancha_html = re.sub(r'(<div class="team-info red">[\s\S]*?<ul>)[\s\S]*?(</ul>)',
        r'\1\n' + jugadores_li(team1) + r'\2', cancha_html)

    # --- Generar bloques de jugadores en cancha según posición ---
    # Definir posiciones y ubicaciones para cada equipo
    posiciones = [
        ("arquero",   {"left": "8%",  "top": "50%"},   {"right": "2%",  "top": "50%"}),
        ("defensa",   {"left": "20%", "top": "35%"},   {"right": "15%", "top": "20%"}),
        ("defensa",   {"left": "20%", "top": "65%"},   {"right": "15%", "top": "80%"}),
        ("mediocampo",{"left": "35%", "top": "50%"},   {"right": "15%", "top": "50%"}),
        ("delantero", {"left": "45%", "top": "35%"},   {"right": "35%", "top": "35%"}),
        ("delantero", {"left": "45%", "top": "65%"},   {"right": "35%", "top": "65%"}),
    ]

    # Mapear nombres de posiciones del JSON a los usados en el HTML
    def map_posicion(p):
        p = p.lower()
        if "arquer" in p:
            return "arquero"
        if "defens" in p:
            return "defensa"
        if "mediocampo" in p or "creador" in p:
            return "mediocampo"
        if "delantero" in p or "atacante" in p:
            return "delantero"
        return "delantero"  # fallback

    def get_img(nombre):
        # Usa el primer nombre antes de espacio o paréntesis para la imagen
        # Si el nombre es 'Iván', usar 'ivan.png' (minúsculas)
        # Si el nombre en confirmados es 'Ivan' o 'FranciscoH', usar la imagen exacta
        if nombre.strip() in ['Ivan', 'Iván']:
            return 'fotos/Ivan.png'
        if nombre.strip() in ['FranciscoH', 'Francisco H']:
            return 'fotos/FranciscoH.png'
        # Por defecto, usar el primer nombre (sin paréntesis) y mayúsculas originales
        base = nombre.split()[0].split('(')[0].strip()
        return f'fotos/{base}.png'

    def generar_bloques(equipo, color):
        # color: 'black' o 'red'
        # 1. Agrupar por posición
        pos_dict = {"arquero": [], "defensa": [], "mediocampo": [], "delantero": []}
        for j in equipo:
            pos = map_posicion(j["posicion"])
            pos_dict[pos].append(j)
        # 2. Si no hay arquero, elegir uno aleatorio
        if not pos_dict["arquero"]:
            candidatos = equipo.copy()
            elegido = random.choice(candidatos)
            pos_dict["arquero"].append(elegido)
            # Quitarlo de su posición original
            for k in pos_dict:
                if elegido in pos_dict[k] and k != "arquero":
                    pos_dict[k].remove(elegido)
        # 3. Armar lista ordenada para la cancha
        orden = [
            pos_dict["arquero"][:1],
            pos_dict["defensa"][:2],
            pos_dict["mediocampo"][:1],
            pos_dict["delantero"][:2],
        ]
        jugadores_ordenados = [j for sub in orden for j in sub]
        # Si faltan jugadores, rellenar con los que sobren
        ya = set(id(j) for j in jugadores_ordenados)
        extras = [j for j in equipo if id(j) not in ya]
        jugadores_ordenados += extras
        # 4. Generar bloques HTML
        bloques = []
        for idx, j in enumerate(jugadores_ordenados):
            if idx >= len(posiciones):
                break
            pos, pos_black, pos_red = posiciones[idx]
            style = ''
            if color == 'black':
                style = f'left: {pos_black["left"]}; top: {pos_black["top"]};'
            else:
                style = f'right: {pos_red["right"]}; top: {pos_red["top"]};'
            clase = f'player {color}-team {map_posicion(j["posicion"])} has-photo'
            # Agregar borde y sombra a la imagen
            bloque = f'<div class="{clase}" data-position="{map_posicion(j["posicion"])}" style="{style}">\n  <img src="{get_img(j["nombre"])}" alt="{j["nombre"]}" class="player-photo player-photo-borde-sombra">\n</div>'
            bloques.append(bloque)
        return '\n\n'.join(bloques)

    # Reemplazar el comentario por los bloques de jugadores
    jugadores_html = generar_bloques(team2, 'black') + '\n' + generar_bloques(team1, 'red')
    cancha_html = re.sub(r'<!-- Aquí van solo las fotos de los jugadores, generado por el script -->', jugadores_html, cancha_html)

    with open('cancha.html', 'w', encoding='utf-8') as f:
        f.write(cancha_html)

# Llamar la función solo al final, cuando todo está definido
actualizar_cancha_html()