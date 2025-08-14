#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema de sorteo avanzado para fútbol con 7 posiciones específicas:
- GK (Goalkeeper/Arquero)
- LCB (Left Center Back/Defensa Central Izquierdo)  
- RCB (Right Center Back/Defensa Central Derecho)
- LM (Left Midfielder/Mediocampo Izquierdo)
- CM (Central Midfielder/Mediocampo Central)
- RM (Right Midfielder/Mediocampo Derecho)
- CF (Center Forward/Delantero Centro)

Genera formaciones tácticas específicas y balance perfecto entre equipos.
"""

import json
import random
import itertools
from datetime import datetime
import os

def convertir_fecha_formato_completo(fecha_corta):
    """Convierte fecha DD/MM a formato completo con día de semana y mes en palabras"""
    if not fecha_corta or '/' not in fecha_corta:
        return fecha_corta
    
    try:
        # Diccionarios para traducción
        dias_semana = {
            0: 'Lunes', 1: 'Martes', 2: 'Miércoles', 3: 'Jueves', 
            4: 'Viernes', 5: 'Sábado', 6: 'Domingo'
        }
        meses = {
            1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril',
            5: 'Mayo', 6: 'Junio', 7: 'Julio', 8: 'Agosto',
            9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'
        }
        
        # Parsear fecha DD/MM
        dia, mes = fecha_corta.split('/')
        dia = int(dia)
        mes = int(mes)
        
        # Usar año actual
        año_actual = datetime.now().year
        fecha_obj = datetime(año_actual, mes, dia)
        
        # Obtener día de la semana
        dia_semana = dias_semana[fecha_obj.weekday()]
        mes_nombre = meses[mes]
        
        return f"{dia_semana} {dia} de {mes_nombre}"
        
    except (ValueError, IndexError):
        # Si hay error, devolver fecha original
        return fecha_corta

def cargar_jugadores(archivo='jugadores_posiciones_especificas.json'):
    """Carga la lista de jugadores con puntajes por posición específica."""
    try:
        with open(archivo, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"❌ Error: No se encontró el archivo {archivo}")
        return []

def cargar_info_partido(archivo='partido.txt'):
    """Carga la información del partido desde partido.txt"""
    info_default = {
        'fecha': 'Fecha por confirmar',
        'hora': '22:00',
        'cancha': 'Por confirmar'
    }
    
    try:
        with open(archivo, 'r', encoding='utf-8') as f:
            lineas = f.readlines()
        
        info_partido = {}
        for linea in lineas:
            linea = linea.strip()
            if ':' in linea:
                clave, valor = linea.split(':', 1)
                clave = clave.strip().lower()
                valor = valor.strip()
                
                if clave == 'fecha':
                    info_partido['fecha'] = valor
                elif clave == 'hora':
                    info_partido['hora'] = valor if valor.endswith('hrs') or valor.endswith('hr') else valor + ' hrs'
                elif clave == 'cancha':
                    info_partido['cancha'] = valor
        
        # Usar valores por defecto si no se encuentran
        for key, default in info_default.items():
            if key not in info_partido:
                info_partido[key] = default
                
        return info_partido
        
    except FileNotFoundError:
        print(f"⚠️  Archivo {archivo} no encontrado, usando valores por defecto")
        return info_default
    except Exception as e:
        print(f"⚠️  Error leyendo {archivo}: {e}, usando valores por defecto")
        return info_default

def jugadores_confirmados(todos_jugadores):
    """Filtra jugadores confirmados basado en confirmados.txt"""
    try:
        with open('confirmados.txt', 'r', encoding='utf-8') as f:
            nombres_confirmados = [line.strip() for line in f if line.strip()]
        
        confirmados = []
        for nombre in nombres_confirmados:
            jugador = next((j for j in todos_jugadores if j['nombre'].lower() == nombre.lower()), None)
            if jugador:
                confirmados.append(jugador)
            else:
                print(f"⚠️  Jugador '{nombre}' no encontrado en la base de datos")
        
        return confirmados
    except FileNotFoundError:
        print("❌ Error: No se encontró confirmados.txt")
        return []

def generar_formaciones_posibles():
    """Genera todas las formaciones posibles con 6 jugadores (1 GK + 5 de campo)"""
    formaciones = []
    
    # Todas las combinaciones que sumen 5 jugadores de campo
    # [LCB, RCB, LM, CM, RM, CF]
    for lcb in range(0, 3):  # 0-2 defensas izquierdos
        for rcb in range(0, 3):  # 0-2 defensas derechos
            for lm in range(0, 3):  # 0-2 mediocampos izquierdos
                for cm in range(0, 3):  # 0-2 mediocampos centrales
                    for rm in range(0, 3):  # 0-2 mediocampos derechos
                        for cf in range(0, 3):  # 0-2 delanteros
                            if lcb + rcb + lm + cm + rm + cf == 5:
                                # Debe tener al menos 1 defensa, 1 mediocampo y 1 delantero
                                total_defensas = lcb + rcb
                                total_mediocampos = lm + cm + rm
                                total_delanteros = cf
                                
                                if total_defensas >= 1 and total_mediocampos >= 1 and total_delanteros >= 1:
                                    formacion = {
                                        'LCB': lcb, 'RCB': rcb, 
                                        'LM': lm, 'CM': cm, 'RM': rm,
                                        'CF': cf
                                    }
                                    formaciones.append(formacion)
    
    return formaciones

def calcular_puntaje_formacion(jugadores_asignados, formacion):
    """Calcula el puntaje total de una formación específica considerando solo posiciones válidas"""
    puntaje_total = 0
    jugadores_usados = []
    
    posiciones = ['LCB', 'RCB', 'LM', 'CM', 'RM', 'CF']
    
    idx_jugador = 1  # Empezar desde 1 (índice 0 es el arquero)
    
    for posicion in posiciones:
        cantidad = formacion[posicion]
        for _ in range(cantidad):
            if idx_jugador < len(jugadores_asignados):
                jugador = jugadores_asignados[idx_jugador]
                
                # Verificar si el jugador puede jugar en esta posición
                posiciones_validas = [pos.strip() for pos in jugador['posicion'].split(',')]
                if posicion in posiciones_validas:
                    puntaje_posicion = jugador['puntajes_posicion'][posicion]
                else:
                    # Penalizar si no puede jugar en esta posición
                    puntaje_posicion = jugador['puntajes_posicion'][posicion] * 0.3  # Reducir a 30%
                
                puntaje_total += puntaje_posicion
                jugadores_usados.append((jugador['nombre'], posicion, puntaje_posicion))
                idx_jugador += 1
    
    return puntaje_total, jugadores_usados

def optimizar_posiciones_equipo(jugadores_equipo):
    """Optimiza las posiciones para un equipo específico priorizando especialidades"""
    if len(jugadores_equipo) != 6:
        return None, 0, []
    
    # El primer jugador debe ser el mejor arquero
    arquero = jugadores_equipo[0]
    jugadores_campo = jugadores_equipo[1:]
    
    formaciones_posibles = generar_formaciones_posibles()
    mejor_formacion = None
    mejor_puntaje = -1
    mejor_asignacion = []
    
    # Probar formaciones limitadas con asignación inteligente por especialidad
    for formacion in formaciones_posibles[:15]:  # Probar más formaciones
        puntaje, asignacion = asignar_por_especialidad(jugadores_campo, formacion)
        
        if puntaje > mejor_puntaje:
            mejor_puntaje = puntaje
            mejor_formacion = formacion
            mejor_asignacion = asignacion
    
    return mejor_formacion, mejor_puntaje, mejor_asignacion

def asignar_por_especialidad(jugadores_campo, formacion):
    """Asigna jugadores a posiciones priorizando sus especialidades usando algoritmo greedy mejorado"""
    posiciones_necesarias = []
    
    # Crear lista de posiciones necesarias según la formación
    for posicion, cantidad in formacion.items():
        for _ in range(cantidad):
            posiciones_necesarias.append(posicion)
    
    if len(posiciones_necesarias) != len(jugadores_campo):
        return 0, []
    
    # Crear lista de candidatos para cada posición con sus puntajes
    candidatos_por_posicion = {}
    for posicion in set(posiciones_necesarias):
        candidatos_por_posicion[posicion] = []
        
        for jugador in jugadores_campo:
            posiciones_validas = [pos.strip() for pos in jugador['posicion'].split(',')]
            
            if posicion in posiciones_validas:
                # Posición válida: usar puntaje completo + bonus por especialidad
                puntaje_base = jugador['puntajes_posicion'][posicion]
                # Bonus si es su mejor posición
                mejor_posicion = max(jugador['puntajes_posicion'].items(), key=lambda x: x[1])
                bonus = 0.5 if mejor_posicion[0] == posicion else 0
                puntaje_final = puntaje_base + bonus
            else:
                # Posición no válida: penalizar fuertemente
                puntaje_final = jugador['puntajes_posicion'][posicion] * 0.2
            
            candidatos_por_posicion[posicion].append((jugador, puntaje_final))
        
        # Ordenar candidatos por puntaje descendente
        candidatos_por_posicion[posicion].sort(key=lambda x: x[1], reverse=True)
    
    # Algoritmo greedy mejorado: asignar primero las posiciones más difíciles de cubrir
    nombres_asignados = set()  # Usar nombres en lugar de objetos completos
    asignacion_final = []
    posiciones_pendientes = posiciones_necesarias.copy()
    
    # Ordenar posiciones por disponibilidad (menos candidatos válidos primero)
    def contar_candidatos_validos(posicion):
        return len([j for j, p in candidatos_por_posicion[posicion] 
                   if posicion in [pos.strip() for pos in j['posicion'].split(',')]])
    
    posiciones_pendientes.sort(key=contar_candidatos_validos)
    
    # Asignar posiciones una por una
    for posicion in posiciones_pendientes:
        mejor_candidato = None
        mejor_puntaje = -1
        
        for jugador, puntaje in candidatos_por_posicion[posicion]:
            if jugador['nombre'] not in nombres_asignados:  # Usar nombre para verificar
                if puntaje > mejor_puntaje:
                    mejor_puntaje = puntaje
                    mejor_candidato = jugador
        
        if mejor_candidato:
            nombres_asignados.add(mejor_candidato['nombre'])  # Agregar nombre
            asignacion_final.append((mejor_candidato['nombre'], posicion, mejor_puntaje))
    
    # Calcular puntaje total
    puntaje_total = sum(puntaje for _, _, puntaje in asignacion_final)
    
    return puntaje_total, asignacion_final

def puede_jugar_posicion(jugador, posicion):
    """Verifica si un jugador puede jugar en una posición específica"""
    posiciones_validas = [pos.strip() for pos in jugador['posicion'].split(',')]
    return posicion in posiciones_validas

def sorteo_con_posiciones_especificas(jugadores, num_intentos=10000):
    """Realiza el sorteo optimizando posiciones específicas y respetando posiciones válidas"""
    if len(jugadores) % 2 != 0:
        print("❌ Error: Número impar de jugadores")
        return None, None, None
    
    # Identificar mejores arqueros que PUEDEN jugar en GK
    arqueros_validos = [j for j in jugadores if puede_jugar_posicion(j, 'GK')]
    if len(arqueros_validos) < 2:
        print("⚠️  Advertencia: Menos de 2 arqueros válidos disponibles")
        # Si no hay suficientes arqueros válidos, usar los mejores disponibles
        jugadores_sorted_gk = sorted(jugadores, key=lambda j: j['puntajes_posicion']['GK'], reverse=True)
    else:
        jugadores_sorted_gk = sorted(arqueros_validos, key=lambda j: j['puntajes_posicion']['GK'], reverse=True)
    
    mejor_diferencia = float('inf')
    mejor_equipo1 = None
    mejor_equipo2 = None
    mejor_info = None
    
    print(f"🔄 Generando equipos con posiciones específicas ({num_intentos} intentos)...")
    
    for intento in range(num_intentos):
        # Mezclar jugadores aleatoriamente
        jugadores_mezclados = jugadores.copy()
        random.shuffle(jugadores_mezclados)
        
        # Dividir en dos equipos
        mitad = len(jugadores_mezclados) // 2
        equipo1_temp = jugadores_mezclados[:mitad]
        equipo2_temp = jugadores_mezclados[mitad:]
        
        # Asegurar que cada equipo tenga un buen arquero
        # Buscar el mejor arquero disponible para cada equipo
        mejores_arqueros = jugadores_sorted_gk[:6]  # Top 6 arqueros
        
        arquero1 = None
        arquero2 = None
        
        # Asignar arqueros priorizando los que SÍ pueden jugar en GK
        for jugador in mejores_arqueros:
            if jugador in equipo1_temp and arquero1 is None:
                arquero1 = jugador
            elif jugador in equipo2_temp and arquero2 is None:
                arquero2 = jugador
        
        # Si no encontramos arqueros válidos, usar los mejores disponibles
        if arquero1 is None:
            candidatos = [j for j in equipo1_temp if puede_jugar_posicion(j, 'GK')]
            if candidatos:
                arquero1 = max(candidatos, key=lambda j: j['puntajes_posicion']['GK'])
            else:
                arquero1 = max(equipo1_temp, key=lambda j: j['puntajes_posicion']['GK'])
                
        if arquero2 is None:
            candidatos = [j for j in equipo2_temp if puede_jugar_posicion(j, 'GK')]
            if candidatos:
                arquero2 = max(candidatos, key=lambda j: j['puntajes_posicion']['GK'])
            else:
                arquero2 = max(equipo2_temp, key=lambda j: j['puntajes_posicion']['GK'])
        
        # Reorganizar equipos con arqueros al principio
        equipo1 = [arquero1] + [j for j in equipo1_temp if j != arquero1]
        equipo2 = [arquero2] + [j for j in equipo2_temp if j != arquero2]
        
        # Optimizar posiciones para cada equipo
        formacion1, puntaje1, asignacion1 = optimizar_posiciones_equipo(equipo1)
        formacion2, puntaje2, asignacion2 = optimizar_posiciones_equipo(equipo2)
        
        if formacion1 is None or formacion2 is None:
            continue
        
        # Agregar puntaje del arquero (con penalización si no puede jugar GK)
        puntaje_arquero1 = arquero1['puntajes_posicion']['GK']
        puntaje_arquero2 = arquero2['puntajes_posicion']['GK']
        
        if not puede_jugar_posicion(arquero1, 'GK'):
            puntaje_arquero1 *= 0.3  # Penalizar si no puede jugar en GK
        if not puede_jugar_posicion(arquero2, 'GK'):
            puntaje_arquero2 *= 0.3
            
        puntaje_total1 = puntaje1 + puntaje_arquero1
        puntaje_total2 = puntaje2 + puntaje_arquero2
        
        diferencia = abs(puntaje_total1 - puntaje_total2)
        
        if diferencia < mejor_diferencia:
            mejor_diferencia = diferencia
            mejor_equipo1 = equipo1
            mejor_equipo2 = equipo2
            mejor_info = {
                'formacion1': formacion1,
                'formacion2': formacion2,
                'puntaje1': puntaje_total1,
                'puntaje2': puntaje_total2,
                'asignacion1': [(arquero1['nombre'], 'GK', puntaje_arquero1)] + asignacion1,
                'asignacion2': [(arquero2['nombre'], 'GK', puntaje_arquero2)] + asignacion2,
                'diferencia': diferencia
            }
        
        # Mostrar progreso cada 100 intentos para el rango reducido
        if (intento + 1) % 100 == 0:
            print(f"   Intento {intento + 1}: Mejor diferencia = {mejor_diferencia:.3f}")
    
    return mejor_equipo1, mejor_equipo2, mejor_info

def formatear_formacion(formacion):
    """Convierte la formación a string legible"""
    defensas = formacion['LCB'] + formacion['RCB']
    mediocampos = formacion['LM'] + formacion['CM'] + formacion['RM']
    delanteros = formacion['CF']
    return f"1-{defensas}-{mediocampos}-{delanteros}"

def guardar_equipos(equipo1, equipo2, info_sorteo, info_partido):
    """Guarda los equipos en equipos.json"""
    
    # Convertir las posiciones específicas a las categorías generales para el campo
    def convertir_posicion_para_campo(posicion_especifica):
        conversion = {
            'GK': 'Arquero',
            'LCB': 'Defensa', 
            'RCB': 'Defensa',
            'LM': 'Mediocampo',
            'CM': 'Mediocampo', 
            'RM': 'Mediocampo',
            'CF': 'Delantero'
        }
        return conversion.get(posicion_especifica, 'Mediocampo')
    
    # Crear diccionarios de posiciones para la visualización del campo
    rojo_posiciones = {}
    negro_posiciones = {}
    
    for nombre, posicion_esp, puntaje in info_sorteo['asignacion1']:
        rojo_posiciones[nombre] = convertir_posicion_para_campo(posicion_esp)
    
    for nombre, posicion_esp, puntaje in info_sorteo['asignacion2']:
        negro_posiciones[nombre] = convertir_posicion_para_campo(posicion_esp)
    
    equipos_data = {
        "fecha": convertir_fecha_formato_completo(info_partido['fecha']),
        "hora": info_partido['hora'],
        "cancha": info_partido['cancha'],
        "metodo": "Posiciones Específicas (7 posiciones)",
        # Formato compatible con actualizar_html.py
        "rojo": [j['nombre'] for j in equipo1],
        "negro": [j['nombre'] for j in equipo2],
        "promedio_rojo": round(info_sorteo['puntaje1']/6, 2),
        "promedio_negro": round(info_sorteo['puntaje2']/6, 2),
        "diferencia": round(info_sorteo['diferencia'], 3),
        # Posiciones para la visualización del campo
        "rojo_posiciones": rojo_posiciones,
        "negro_posiciones": negro_posiciones,
        # Información adicional para el nuevo sistema
        "equipos": {
            "rojo": [j['nombre'] for j in equipo1],
            "negro": [j['nombre'] for j in equipo2]
        },
        "formaciones": {
            "rojo": formatear_formacion(info_sorteo['formacion1']),
            "negro": formatear_formacion(info_sorteo['formacion2'])
        },
        "puntajes": {
            "rojo": round(info_sorteo['puntaje1'], 2),
            "negro": round(info_sorteo['puntaje2'], 2),
            "diferencia": round(info_sorteo['diferencia'], 3)
        },
        "posiciones": {
            "rojo": info_sorteo['asignacion1'],
            "negro": info_sorteo['asignacion2']
        }
    }
    
    with open('equipos.json', 'w', encoding='utf-8') as f:
        json.dump(equipos_data, f, ensure_ascii=False, indent=2)

def mostrar_equipos_detallados(equipo1, equipo2, info_sorteo, info_partido):
    """Muestra los equipos con posiciones específicas detalladas"""
    print(f"\n⚽ Partido {info_partido['fecha']} - {info_partido['hora']} - {info_partido['cancha']}")
    print("📋 Formaciones con Posiciones Específicas (Respetando Posiciones Válidas)")
    print("=" * 80)
    
    # Equipo Rojo
    formacion1_str = formatear_formacion(info_sorteo['formacion1'])
    print(f"\n🔴 EQUIPO ROJO - Formación {formacion1_str} (Promedio: {info_sorteo['puntaje1']/6:.2f}):")
    
    for nombre, posicion, puntaje in info_sorteo['asignacion1']:
        jugador_data = next(j for j in equipo1 if j['nombre'] == nombre)
        puede_jugar = puede_jugar_posicion(jugador_data, posicion)
        
        if puede_jugar:
            icono = "🥅" if posicion == "GK" else "⭐"
        else:
            icono = "⚠️"  # Fuera de posición
            
        pos_nombre = {
            'GK': 'Arquero',
            'LCB': 'Defensa Izq',
            'RCB': 'Defensa Der', 
            'LM': 'Mediocampo Izq',
            'CM': 'Mediocampo Centro',
            'RM': 'Mediocampo Der',
            'CF': 'Delantero Centro'
        }
        
        estado = "" if puede_jugar else " (fuera de posición)"
        print(f"  {icono}{pos_nombre[posicion]:<15} - {nombre:<15} ({puntaje:.1f} pts en pos, {jugador_data['puntaje']:.1f} general){estado}")
    
    # Equipo Negro
    formacion2_str = formatear_formacion(info_sorteo['formacion2'])
    print(f"\n⚫ EQUIPO NEGRO - Formación {formacion2_str} (Promedio: {info_sorteo['puntaje2']/6:.2f}):")
    
    for nombre, posicion, puntaje in info_sorteo['asignacion2']:
        jugador_data = next(j for j in equipo2 if j['nombre'] == nombre)
        puede_jugar = puede_jugar_posicion(jugador_data, posicion)
        
        if puede_jugar:
            icono = "🥅" if posicion == "GK" else "⭐"
        else:
            icono = "⚠️"  # Fuera de posición
            
        pos_nombre = {
            'GK': 'Arquero',
            'LCB': 'Defensa Izq',
            'RCB': 'Defensa Der',
            'LM': 'Mediocampo Izq', 
            'CM': 'Mediocampo Centro',
            'RM': 'Mediocampo Der',
            'CF': 'Delantero Centro'
        }
        
        estado = "" if puede_jugar else " (fuera de posición)"
        print(f"  {icono}{pos_nombre[posicion]:<15} - {nombre:<15} ({puntaje:.1f} pts en pos, {jugador_data['puntaje']:.1f} general){estado}")
    
    print(f"\n📊 Diferencia de promedios: {info_sorteo['diferencia']:.3f}")
    print(f"🎲 Formaciones: Rojo {formacion1_str} vs Negro {formacion2_str}")
    print("⭐ = Posición válida | ⚠️ = Fuera de posición (penalizado)")
    print("=" * 80)

def actualizar_archivos_html():
    """Actualiza los archivos HTML desde equipos.json"""
    print("✅ Sorteo completado - Los archivos HTML se actualizarán automáticamente desde la web")

def main():
    print("🚀 SORTEO CON POSICIONES ESPECÍFICAS (7 POSICIONES)")
    print("=" * 60)
    print("Posiciones: GK, LCB, RCB, LM, CM, RM, CF")
    print("=" * 60)
    
    # Cargar información del partido
    info_partido = cargar_info_partido()
    print(f"📅 Partido: {info_partido['fecha']} - {info_partido['hora']} - {info_partido['cancha']}")
    print("=" * 60)
    
    # Cargar jugadores
    jugadores = cargar_jugadores()
    if not jugadores:
        return
    
    # Filtrar confirmados
    confirmados = jugadores_confirmados(jugadores)
    
    if len(confirmados) < 6:
        print(f"❌ Error: Se necesitan al menos 6 jugadores confirmados (tienes {len(confirmados)})")
        return
    
    if len(confirmados) % 2 != 0:
        print(f"❌ Error: Número impar de jugadores confirmados ({len(confirmados)})")
        return
    
    print(f"👥 Jugadores confirmados: {len(confirmados)}")
    for jugador in confirmados:
        print(f"   - {jugador['nombre']} (General: {jugador['puntaje']})")
    
    # Configurar intentos
    try:
        intentos_str = input(f"\nNúmero de intentos para optimización (100-5000) [1000]: ").strip()
        intentos = int(intentos_str) if intentos_str else 1000
        intentos = max(100, min(5000, intentos))
    except ValueError:
        intentos = 1000
    
    # Realizar sorteo
    equipo1, equipo2, info_sorteo = sorteo_con_posiciones_especificas(confirmados, intentos)
    
    if equipo1 is None:
        print("❌ Error: No se pudo generar un sorteo válido")
        return
    
    # Mostrar resultados
    mostrar_equipos_detallados(equipo1, equipo2, info_sorteo, info_partido)
    
    # Guardar resultados
    guardar_equipos(equipo1, equipo2, info_sorteo, info_partido)
    print(f"\n✅ Sorteo con posiciones específicas completado y guardado en equipos.json")
    
    # Actualizar HTML
    actualizar_archivos_html()

if __name__ == "__main__":
    main()
