import json
import re

# Cargar equipos.json
with open('equipos.json', 'r', encoding='utf-8') as f:
    equipos = json.load(f)

# --- Actualizar index.html ---
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Formato fijo para el título manteniendo el id para el script JS
fecha = equipos.get('fecha', '').strip()
hora = equipos.get('hora', '').replace('hrs', '').strip()
cancha = equipos.get('cancha', '').strip()

# Formatear la cancha correctamente
if cancha.lower().find('por confirmar') != -1:
    cancha_formateada = cancha
elif cancha.isdigit():
    cancha_formateada = f"Cancha {cancha}"
else:
    cancha_formateada = cancha

titulo = f'<h1 id="partido-info">⚽ Partido {fecha} - {hora} hrs - {cancha_formateada}</h1>'
html = re.sub(r'<h1[^>]*>[^<]*</h1>', titulo, html)

# Actualizar equipos y jugadores
rojo_html = f'''
            <div class="team-section">
              <div class="team-header team-red">
                <h3>Rojo</h3>
                <div class="team-stats">
                  <span class="team-average">Promedio: {equipos["promedio_rojo"]:.2f}</span>
                  <span class="team-count">{len(equipos["rojo"])} jugadores</span>
                </div>
              </div>
              <div class="team-players">\n'''
for nombre in equipos["rojo"]:
    rojo_html += f'                <div class="team-player"><span class="player-name">{nombre}</span></div>\n'
rojo_html += '              </div>\n            </div>\n'

negro_html = f'''
            <div class="team-section">
              <div class="team-header team-black">
                <h3>Negro</h3>
                <div class="team-stats">
                  <span class="team-average">Promedio: {equipos["promedio_negro"]:.2f}</span>
                  <span class="team-count">{len(equipos["negro"])} jugadores</span>
                </div>
              </div>
              <div class="team-players">\n'''
for nombre in equipos["negro"]:
    negro_html += f'                <div class="team-player"><span class="player-name">{nombre}</span></div>\n'
negro_html += '              </div>\n            </div>\n'

nuevo_equipos = f'<div class="teams-grid">\n{rojo_html}{negro_html}          </div>\n        </div>\n      </main>'
html = re.sub(r'<div class="teams-grid">[\s\S]*?</main>', nuevo_equipos, html)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

# --- Actualizar cancha.html ---
with open('cancha.html', 'r', encoding='utf-8') as f:
    cancha_html = f.read()

# Formato fijo para el título en la cancha manteniendo el id
if cancha.lower().find('por confirmar') != -1:
    cancha_formateada = cancha
elif cancha.isdigit():
    cancha_formateada = f"Cancha {cancha}"
else:
    cancha_formateada = cancha
    
cancha_titulo = f'<h1 id="partido-info">⚽ Partido {fecha} - {hora} hrs - {cancha_formateada}</h1>'
cancha_html = re.sub(r'<h1[^>]*>[^<]*</h1>', cancha_titulo, cancha_html)

# --- Generar bloques visuales de jugadores en la cancha ---
# Posiciones fijas por orden (7 jugadores por equipo)
posiciones = [
    {"left": "10%",  "top": "50%"},    # arquero
    {"left": "22%", "top": "30%"},   # defensa 1
    {"left": "22%", "top": "70%"},   # defensa 2
    {"left": "38%", "top": "40%"},   # mediocampo 1
    {"left": "38%", "top": "60%"},   # mediocampo 2
    {"left": "60%", "top": "35%"},   # delantero 1
    {"left": "60%", "top": "65%"}    # delantero 2
]
posiciones_der = [
    {"right": "8%",  "top": "50%"},
    {"right": "22%", "top": "30%"},
    {"right": "22%", "top": "70%"},
    {"right": "38%", "top": "40%"},
    {"right": "38%", "top": "60%"},
    {"right": "60%", "top": "35%"},
    {"right": "60%", "top": "65%"}
]



# Mostrar solo la foto, sin tag de función

# Ahora: Rojo a la izquierda (posiciones), Negro a la derecha (posiciones_der)
# El orden visual de cada equipo se mantiene (rojo normal, negro invertido para coherencia de posiciones)



# =============================
# Visualización realista por función futbolística
# =============================
# Cada jugador se ubica según su función: arquero, defensa, mediocampo, delantero
# Cada línea se distribuye horizontalmente según la cantidad de jugadores en esa función





def genera_bloques_equipo(equipo, posiciones_dict, lado='izq', color_class=''):
    bloques = []
    # Agrupar por función
    arqueros = [j for j, pos in posiciones_dict.items() if pos.lower() == 'arquero']
    defensas = [j for j, pos in posiciones_dict.items() if pos.lower() == 'defensa']
    mediocampos = [j for j, pos in posiciones_dict.items() if pos.lower() == 'mediocampo']
    delanteros = [j for j, pos in posiciones_dict.items() if pos.lower() == 'delantero']
    # Franjas verticales: cada línea tiene un left/right fijo, los jugadores se distribuyen en top
    if lado == 'izq':
        x_key = 'left'
        x_fr = {
            'arquero': 2,
            'defensa': 18,
            'mediocampo': 35,
            'delantero': 45
        }
    else:
        x_key = 'right'
        x_fr = {
            'arquero': 2,
            'defensa': 15,    # defensas del rojo en right: 15%
            'mediocampo': 27, # mediocampistas del rojo en right: 27%
            'delantero': 37
        }
    lineas = [
        ('arquero', arqueros),
        ('defensa', defensas[:3]),
        ('mediocampo', mediocampos[:3]),
        ('delantero', delanteros[:3])
    ]
    for nombre_funcion, grupo in lineas:
        n = len(grupo)
        if n == 0:
            continue
        for i, nombre in enumerate(grupo):
            if n == 1:
                y = 50
            else:
                y = int(15 + 70 * i/(n-1))  # de 15% a 85%
            x = x_fr[nombre_funcion]
            style = f'{x_key}: {x}%; top: {y}%'
            bloques.append(f'<div class="player {color_class} has-photo" style="{style}"><img src="fotos/{nombre}.png" alt="{nombre}" class="player-photo player-photo-borde-sombra"></div>')
    return bloques


# Cargar posiciones asignadas desde equipos.json si existen (mover aquí para evitar error de variable no definida)
rojo_posiciones = equipos.get('rojo_posiciones', {})
negro_posiciones = equipos.get('negro_posiciones', {})

# Generar bloques para cada equipo: negro a la izquierda, rojo a la derecha
bloques_negro = genera_bloques_equipo(equipos["negro"], negro_posiciones, lado='izq', color_class='black-team')
bloques_rojo = genera_bloques_equipo(equipos["rojo"], rojo_posiciones, lado='der', color_class='red-team')

# Cargar posiciones asignadas desde equipos.json si existen
rojo_posiciones = equipos.get('rojo_posiciones', {})
negro_posiciones = equipos.get('negro_posiciones', {})

# Generar bloques para cada equipo
bloques_negro = genera_bloques_equipo(equipos["negro"], negro_posiciones, lado='izq', color_class='black-team')
bloques_rojo = genera_bloques_equipo(equipos["rojo"], rojo_posiciones, lado='der', color_class='red-team')

# Limpiar e insertar entre los nuevos marcadores de soccer-field
soccerfield_inicio = '<!-- JUGADORES SOCCER-FIELD INICIO -->'
soccerfield_fin = '<!-- JUGADORES SOCCER-FIELD FIN -->'
patron = re.compile(rf'{soccerfield_inicio}[\s\S]*?{soccerfield_fin}')
bloques = '\n'.join(bloques_negro + bloques_rojo)
cancha_html = patron.sub(f'{soccerfield_inicio}\n{bloques}\n{soccerfield_fin}', cancha_html)

# Actualizar listado de equipos abajo de la cancha
negro_li = '\n'.join([
    f'<li><img src="fotos/{nombre}.png" alt="{nombre}" style="width:28px;height:28px;vertical-align:middle;border-radius:6px;margin-right:6px;box-shadow:0 2px 8px #222a3655;"> <strong>{nombre}</strong></li>'
    for nombre in equipos["negro"]
])
rojo_li = '\n'.join([
    f'<li><img src="fotos/{nombre}.png" alt="{nombre}" style="width:28px;height:28px;vertical-align:middle;border-radius:6px;margin-right:6px;box-shadow:0 2px 8px #e5393555;"> <strong>{nombre}</strong></li>'
    for nombre in equipos["rojo"]
])

# Limpiar todas las listas <ul>...</ul> dentro de cada bloque de equipo antes de insertar la nueva lista
import re
def reemplaza_lista_equipo(html, equipo, lista_html):
    # Eliminar todas las listas <ul>...</ul> dentro del bloque del equipo
    patron = rf'(<div class="team-info {equipo}">[\s\S]*?)(<ul>[\s\S]*?</ul>)+'
    while re.search(patron, html, flags=re.DOTALL):
        html = re.sub(patron, rf'\1', html, flags=re.DOTALL)
    # Si no existe <div class="formation"></div>, agregarlo
    if not re.search(rf'<div class="team-info {equipo}">[\s\S]*?<div class="formation"></div>', html, flags=re.DOTALL):
        html = re.sub(
            rf'(<div class="team-info {equipo}">)',
            rf'\1\n<div class="formation"></div>',
            html,
            flags=re.DOTALL
        )
    # Insertar la nueva lista justo después del <div class="formation"></div>
    html = re.sub(
        rf'(<div class="team-info {equipo}">[\s\S]*?<div class="formation"></div>)',
        rf'\1\n<ul>\n{lista_html}\n</ul>',
        html,
        flags=re.DOTALL
    )
    return html

# Cambiar el orden de aparición: primero equipo negro, luego equipo rojo
cancha_html = reemplaza_lista_equipo(cancha_html, "black", negro_li)
cancha_html = reemplaza_lista_equipo(cancha_html, "red", rojo_li)
with open('cancha.html', 'w', encoding='utf-8') as f:
    f.write(cancha_html)

# --- Actualizar cancha-v2.html ---
with open('cancha-v2.html', 'r', encoding='utf-8') as f:
    cancha_v2_html = f.read()

# Actualizar título en cancha-v2.html
if cancha.lower().find('por confirmar') != -1:
    cancha_formateada = cancha
elif cancha.isdigit():
    cancha_formateada = f"Cancha {cancha}"
else:
    cancha_formateada = cancha
    
cancha_v2_titulo = f'<h1 id="partido-info">⚽ Partido {fecha} - {hora} hrs - {cancha_formateada}</h1>'
cancha_v2_html = re.sub(r'<h1[^>]*>[^<]*</h1>', cancha_v2_titulo, cancha_v2_html)

with open('cancha-v2.html', 'w', encoding='utf-8') as f:
    f.write(cancha_v2_html)

print('index.html, cancha.html y cancha-v2.html actualizados desde equipos.json.')
