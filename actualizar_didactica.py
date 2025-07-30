import json
import re

# Cargar equipos.json
equipos = json.load(open('equipos.json', encoding='utf-8'))

# Cargar cancha-didactica.html
with open('cancha-didactica.html', encoding='utf-8') as f:
    html = f.read()

# Marcadores para reemplazo automático
tag_inicio = '<!-- JUGADORES DIDACTICA INICIO -->'
tag_fin = '<!-- JUGADORES DIDACTICA FIN -->'

# Definición de roles y tooltips por función
TOOLTIPS = {
    'arquero': {
        'role': 'Protege la portería',
        'skills': 'Reflejos, Agilidad, Comunicación',
        'desc': '🥅 Guardián de la portería',
    },
    'defensa': {
        'role': 'Defiende y marca a los delanteros rivales',
        'skills': 'Marcaje, Despeje, Fuerza',
        'desc': '🛡️ Bloquea ataques enemigos',
    },
    'mediocampo': {
        'role': 'Conecta defensa con ataque, distribuye el juego',
        'skills': 'Pase, Visión, Control del balón',
        'desc': '🎯 Cerebro del equipo',
    },
    'delantero': {
        'role': 'Busca el gol y presiona la defensa rival',
        'skills': 'Finalización, Velocidad, Regate',
        'desc': '⚽ Cazador de goles',
    },
}

# Generar bloques de jugadores para cada equipo
def genera_bloques(equipo, posiciones, lado):
    bloques = []
    for nombre in equipo:
        funcion = posiciones.get(nombre, '').lower()
        if not funcion:
            continue
        t = TOOLTIPS.get(funcion, {})
        # Distribución simple: arquero, defensa, mediocampo, delantero
        if funcion == 'arquero':
            pos = {'left': '8%' if lado=='left' else '', 'right': '8%' if lado=='right' else '', 'top': '50%'}
        elif funcion == 'defensa':
            pos = {'left': '20%' if lado=='left' else '', 'right': '20%' if lado=='right' else '', 'top': '35%'}
        elif funcion == 'mediocampo':
            pos = {'left': '35%' if lado=='left' else '', 'right': '27%' if lado=='right' else '', 'top': '50%'}
        elif funcion == 'delantero':
            pos = {'left': '45%' if lado=='left' else '', 'right': '35%' if lado=='right' else '', 'top': '65%'}
        else:
            pos = {'left': '10%', 'top': '50%'}
        style = ' '.join(f'{k}: {v};' for k,v in pos.items() if v)
        clase = 'black-team' if lado=='left' else 'red-team'
        bloques.append(f'''<div class="player {clase} {funcion} has-photo interactive" data-name="{nombre}" data-position="{funcion.capitalize()}" data-role="{t.get('role','')}" data-skills="{t.get('skills','')}" style="{style}"><img src="fotos/{nombre}.png" alt="{nombre}" class="player-photo"><div class="player-tooltip"><strong>{nombre} - {funcion.capitalize()}</strong><p>{t.get('desc','')}</p></div></div>''')
    return '\n'.join(bloques)

bloques_negro = genera_bloques(equipos['negro'], equipos.get('negro_posiciones', {}), 'left')
bloques_rojo = genera_bloques(equipos['rojo'], equipos.get('rojo_posiciones', {}), 'right')

# Reemplazar sección entre marcadores
def reemplaza_bloques(html, bloques):
    patron = re.compile(rf'{tag_inicio}[\s\S]*?{tag_fin}')
    nuevo = f'{tag_inicio}\n{bloques}\n{tag_fin}'
    return patron.sub(nuevo, html)

html = reemplaza_bloques(html, bloques_negro + '\n' + bloques_rojo)

with open('cancha-didactica.html', 'w', encoding='utf-8') as f:
    f.write(html)

print('cancha-didactica.html actualizado desde equipos.json.')
