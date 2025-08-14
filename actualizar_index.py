#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para actualizar index.html con los equipos más recientes
"""

import json
import re
import os

def actualizar_index_html():
    """Actualiza index.html con los equipos del archivo equipos.json"""
    
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
        with open('index.html', 'r', encoding='utf-8') as f:
            html_content = f.read()
    except FileNotFoundError:
        print("Error: No se encontró index.html")
        return False
    except Exception as e:
        print(f"Error leyendo index.html: {e}")
        return False
    
    # Actualizar título del partido
    html_content = actualizar_titulo_partido(html_content, equipos)
    
    # Generar HTML de equipos
    nuevo_html_equipos = generar_equipos_html(equipos)
    
    # Buscar la sección de equipos y reemplazarla
    # Patrón para encontrar la sección completa de equipos
    patron_equipos = r'<div class="teams-organization">.*?</div>\s*</div>\s*</main>'
    
    match = re.search(patron_equipos, html_content, re.DOTALL)
    if not match:
        print("Error: No se encontró la sección de equipos en index.html")
        return False
    
    # Reemplazar la sección
    nuevo_html = html_content.replace(match.group(0), nuevo_html_equipos + '\n        </div>\n      </main>')
    
    # Guardar archivo actualizado
    try:
        with open('index.html', 'w', encoding='utf-8') as f:
            f.write(nuevo_html)
        print("index.html actualizado correctamente")
        return True
    except Exception as e:
        print(f"Error escribiendo index.html: {e}")
        return False

def calcular_promedio_equipo(jugadores):
    """Calcula el promedio general de un equipo"""
    if not jugadores:
        return 0.0
    
    # Cargar datos de jugadores para obtener promedios
    try:
        with open('jugadores.json', 'r', encoding='utf-8') as f:
            jugadores_db = json.load(f)
    except:
        # Si no hay jugadores.json, usar valores por defecto
        return 6.0
    
    total = 0
    count = 0
    for nombre in jugadores:
        jugador_data = next((j for j in jugadores_db if j['nombre'].lower() == nombre.lower()), None)
        if jugador_data:
            total += jugador_data.get('promedio', 6.0)
            count += 1
    
    return round(total / count, 2) if count > 0 else 6.0

def generar_equipos_html(equipos):
    """Genera el HTML de los equipos para index.html"""
    
    equipo_rojo = equipos.get('rojo', [])
    equipo_negro = equipos.get('negro', [])
    
    promedio_rojo = calcular_promedio_equipo(equipo_rojo)
    promedio_negro = calcular_promedio_equipo(equipo_negro)
    
    # Generar jugadores del equipo rojo
    jugadores_rojo_html = ""
    for jugador in equipo_rojo:
        jugadores_rojo_html += f'                <div class="team-player"><span class="player-name">{jugador}</span></div>\n'
    
    # Generar jugadores del equipo negro
    jugadores_negro_html = ""
    for jugador in equipo_negro:
        jugadores_negro_html += f'                <div class="team-player"><span class="player-name">{jugador}</span></div>\n'
    
    html_equipos = f'''<div class="teams-organization">
          <h2>🏆 Equipos Organizados</h2>
          <p class="organization-note">Talaganchester United</p>
          
          <div class="teams-grid">

            <div class="team-section">
              <div class="team-header team-red">
                <h3>Rojo</h3>
                <div class="team-stats">
                  <span class="team-average">Promedio: {promedio_rojo}</span>
                  <span class="team-count">{len(equipo_rojo)} jugadores</span>
                </div>
              </div>
              <div class="team-players">
{jugadores_rojo_html.rstrip()}
              </div>
            </div>

            <div class="team-section">
              <div class="team-header team-black">
                <h3>Negro</h3>
                <div class="team-stats">
                  <span class="team-average">Promedio: {promedio_negro}</span>
                  <span class="team-count">{len(equipo_negro)} jugadores</span>
                </div>
              </div>
              <div class="team-players">
{jugadores_negro_html.rstrip()}
              </div>
            </div>
          </div>
        </div>'''
    
    return html_equipos

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
    print("Actualizando index.html...")
    if actualizar_index_html():
        print("index.html actualizado!")
    else:
        print("Error actualizando index.html")
