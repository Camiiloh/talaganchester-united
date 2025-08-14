#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para actualizar cancha.html con los equipos más recientes
"""

import json
import re
import os

def actualizar_cancha_simple():
    """Actualiza cancha.html con los equipos del archivo equipos.json"""
    
    # Cargar equipos
    try:
        with open('equipos.json', 'r', encoding='utf-8') as f:
            equipos = json.load(f)
    except FileNotFoundError:
        print("Error: No se encontró equipos.json")
        return False
    except Exception as e:
        print(f"Error leyendo equipos.json: {e}")
        return False
    
    # Leer archivo HTML
    try:
        with open('cancha.html', 'r', encoding='utf-8') as f:
            html_content = f.read()
    except FileNotFoundError:
        print("Error: No se encontró cancha.html")
        return False
    except Exception as e:
        print(f"Error leyendo cancha.html: {e}")
        return False
    
    # Actualizar título del partido
    html_content = actualizar_titulo_partido(html_content, equipos)
    
    # Buscar la sección de jugadores
    inicio_pattern = r'<!-- JUGADORES SOCCER-FIELD INICIO -->'
    fin_pattern = r'<!-- JUGADORES SOCCER-FIELD FIN -->'
    
    inicio_match = re.search(inicio_pattern, html_content)
    fin_match = re.search(fin_pattern, html_content)
    
    if not inicio_match or not fin_match:
        print("Error: No se encontraron los marcadores en cancha.html")
        return False
    
    # Generar HTML de jugadores
    nuevos_jugadores = generar_jugadores_html(equipos)
    
    # Reemplazar la sección de posiciones
    nuevo_html = (
        html_content[:inicio_match.end()] + 
        "\n" + nuevos_jugadores + "\n" + 
        html_content[fin_match.start():]
    )
    
    # Actualizar también el listado inferior
    nuevo_html = actualizar_listado_equipos(nuevo_html, equipos)
    
    # Guardar archivo actualizado
    try:
        with open('cancha.html', 'w', encoding='utf-8') as f:
            f.write(nuevo_html)
        print("cancha.html actualizado correctamente")
        return True
    except Exception as e:
        print(f"Error escribiendo cancha.html: {e}")
        return False

def generar_jugadores_html(equipos):
    """Genera el HTML de los jugadores en sus posiciones usando el mismo sistema que cancha-v2"""
    
    equipo_negro = equipos.get('negro', [])
    equipo_rojo = equipos.get('rojo', [])
    negro_posiciones = equipos.get('negro_posiciones', {})
    rojo_posiciones = equipos.get('rojo_posiciones', {})
    
    html_jugadores = []
    
    # Generar posiciones para equipo negro (izquierda) basadas en funciones
    pos_negro = obtener_posiciones_por_funcion(equipo_negro, negro_posiciones, 'izq')
    
    # Generar posiciones para equipo rojo (derecha) basadas en funciones
    pos_rojo = obtener_posiciones_por_funcion(equipo_rojo, rojo_posiciones, 'der')
    
    # Generar jugadores equipo negro
    for jugador in equipo_negro:
        if jugador in pos_negro:
            pos = pos_negro[jugador]
            foto_path = f"fotos/{jugador}.png"
            
            # Verificar si existe la foto
            if os.path.exists(foto_path):
                html_jugadores.append(
                    f'<div class="player black-team has-photo" style="left: {pos["left"]}; top: {pos["top"]}">'
                    f'<img src="{foto_path}" alt="{jugador}" class="player-photo player-photo-borde-sombra"></div>'
                )
            else:
                html_jugadores.append(
                    f'<div class="player black-team" style="left: {pos["left"]}; top: {pos["top"]}">'
                    f'<span class="player-name">{jugador}</span></div>'
                )
    
    # Generar jugadores equipo rojo
    for jugador in equipo_rojo:
        if jugador in pos_rojo:
            pos = pos_rojo[jugador]
            foto_path = f"fotos/{jugador}.png"
            
            # Verificar si existe la foto
            if os.path.exists(foto_path):
                html_jugadores.append(
                    f'<div class="player red-team has-photo" style="left: {pos["left"]}; top: {pos["top"]}">'
                    f'<img src="{foto_path}" alt="{jugador}" class="player-photo player-photo-borde-sombra"></div>'
                )
            else:
                html_jugadores.append(
                    f'<div class="player red-team" style="left: {pos["left"]}; top: {pos["top"]}">'
                    f'<span class="player-name">{jugador}</span></div>'
                )
    
    return "\n".join(html_jugadores)

def obtener_posiciones_por_funcion(equipo, posiciones_dict, lado):
    """Genera posiciones basadas en funciones, ajustadas para cancha.html"""
    
    # Agrupar por función
    arqueros = [n for n, pos in posiciones_dict.items() if pos and pos.lower() == 'arquero']
    defensas = [n for n, pos in posiciones_dict.items() if pos and pos.lower() == 'defensa']
    mediocampos = [n for n, pos in posiciones_dict.items() if pos and pos.lower() == 'mediocampo']
    delanteros = [n for n, pos in posiciones_dict.items() if pos and pos.lower() == 'delantero']
    sin_funcion = [n for n, pos in posiciones_dict.items() if not pos]
    
    # Configuración de posiciones X según el lado
    if lado == 'izq':
        x_base = {'arquero': 2, 'defensa': 18, 'mediocampo': 35, 'delantero': 45, 'sin_funcion': 40}
    else:  # lado == 'der'
        x_base = {'arquero': 98, 'defensa': 82, 'mediocampo': 65, 'delantero': 55, 'sin_funcion': 60}
    
    posiciones = {}
    
    # Procesar cada línea de jugadores
    lineas = [
        ('arquero', arqueros),
        ('defensa', defensas),
        ('mediocampo', mediocampos),
        ('delantero', delanteros),
        ('sin_funcion', sin_funcion)
    ]
    
    for funcion, grupo in lineas:
        n = len(grupo)
        if n == 0:
            continue
            
        for i, nombre in enumerate(grupo):
            # Calcular posición Y - más centrada y mejor distribuida
            if n == 1:
                y = 50  # Centro para un solo jugador
            elif n == 2:
                y = 25 + 50 * i  # 25% y 75% para dos jugadores
            elif n == 3:
                y = 20 + 30 * i  # 20%, 50%, 80% para tres jugadores
            else:
                y = round(20 + 60 * i / (n - 1))  # de 20% a 80%
            
            x = x_base[funcion]
            
            posiciones[nombre] = {'left': f'{x}%', 'top': f'{y}%'}
    
    return posiciones

def actualizar_listado_equipos(html_content, equipos):
    """Actualiza el listado de equipos en la parte inferior de cancha.html"""
    # Buscar la sección del listado
    inicio_pattern = r'<!-- LISTADO EQUIPOS INICIO -->'
    fin_pattern = r'<!-- LISTADO EQUIPOS FIN -->'
    
    inicio_match = re.search(inicio_pattern, html_content)
    fin_match = re.search(fin_pattern, html_content)
    
    if not inicio_match or not fin_match:
        print("Advertencia: No se encontraron los marcadores del listado")
        return html_content
    
    # Generar HTML del listado
    nuevo_listado = generar_listado_html(equipos)
    
    # Reemplazar la sección
    nuevo_html = (
        html_content[:inicio_match.end()] + 
        "\n" + nuevo_listado + "\n" + 
        html_content[fin_match.start():]
    )
    
    return nuevo_html

def generar_listado_html(equipos):
    """Genera el HTML del listado de equipos"""
    equipo_negro = equipos.get('negro', [])
    equipo_rojo = equipos.get('rojo', [])
    
    # Generar HTML para equipo negro
    html_negro = '''          <div class="team-info black">
            <h3>⚫ Equipo Negro</h3>
            <div class="formation"></div>
<ul>'''
    
    for jugador in equipo_negro:
        html_negro += f'''
<li><img src="fotos/{jugador}.png" alt="{jugador}" style="width:28px;height:28px;vertical-align:middle;border-radius:6px;margin-right:6px;box-shadow:0 2px 8px #222a3655;"> <strong>{jugador}</strong></li>'''
    
    html_negro += '''
</ul>
          </div>'''
    
    # Generar HTML para equipo rojo
    html_rojo = '''          <div class="team-info red">
            <h3>🔴 Equipo Rojo</h3>
            <div class="formation"></div>
<ul>'''
    
    for jugador in equipo_rojo:
        html_rojo += f'''
<li><img src="fotos/{jugador}.png" alt="{jugador}" style="width:28px;height:28px;vertical-align:middle;border-radius:6px;margin-right:6px;box-shadow:0 2px 8px #e5393555;"> <strong>{jugador}</strong></li>'''
    
    html_rojo += '''
</ul>
          </div>'''
    
    return html_negro + "\n" + html_rojo

def actualizar_titulo_partido(html_content, equipos):
    """Actualiza el título del partido en el HTML"""
    import datetime
    
    # Formatear fecha
    fechaTexto = equipos.get('fecha', 'Fecha por confirmar')
    if fechaTexto != 'Fecha por confirmar' and fechaTexto != 'Por confirmar':
        try:
            fecha = datetime.datetime.strptime(fechaTexto, '%Y-%m-%d')
            fechaTexto = fecha.strftime('%A %d de %B').replace('Monday', 'Lunes').replace('Tuesday', 'Martes').replace('Wednesday', 'Miércoles').replace('Thursday', 'Jueves').replace('Friday', 'Viernes').replace('Saturday', 'Sábado').replace('Sunday', 'Domingo')
            fechaTexto = fechaTexto.replace('January', 'Enero').replace('February', 'Febrero').replace('March', 'Marzo').replace('April', 'Abril').replace('May', 'Mayo').replace('June', 'Junio').replace('July', 'Julio').replace('August', 'Agosto').replace('September', 'Septiembre').replace('October', 'Octubre').replace('November', 'Noviembre').replace('December', 'Diciembre')
        except:
            pass
    
    hora = equipos.get('hora', 'Por confirmar')
    if hora != 'Por confirmar':
        hora = f"{hora} hrs"
    
    cancha = equipos.get('cancha', 'Por confirmar')
    if cancha != 'Por confirmar' and cancha.isdigit():
        cancha = f"Cancha {cancha}"
    
    nuevo_titulo = f"⚽ Partido {fechaTexto} - {hora} - {cancha}"
    
    # Buscar y reemplazar el título
    patron_titulo = r'<h1 id="partido-info">.*?</h1>'
    nuevo_html = re.sub(patron_titulo, f'<h1 id="partido-info">{nuevo_titulo}</h1>', html_content)
    
    return nuevo_html

if __name__ == '__main__':
    print("Actualizando cancha.html...")
    if actualizar_cancha_simple():
        print("Cancha simple actualizada!")
    else:
        print("Error actualizando cancha simple")
