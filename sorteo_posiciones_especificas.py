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

def cargar_info_partido():
    """Carga la información del partido desde jugadores_confirmados.txt o confirmaciones_automaticas.json
    
    Returns:
        tuple: (info_partido, modo_automatico) donde modo_automatico indica si se leyó desde jugadores_confirmados.txt
    """
    info_default = {
        'fecha': 'Fecha por confirmar',
        'hora': '22:00',
        'cancha': 'Por confirmar'
    }
    
    # Prioridad 1: Intentar leer desde jugadores_confirmados.txt
    try:
        if os.path.exists('jugadores_confirmados.txt'):
            print("📄 Leyendo información desde jugadores_confirmados.txt")
            with open('jugadores_confirmados.txt', 'r', encoding='utf-8') as f:
                contenido = f.read().strip()
            
            # Parsear el formato del archivo
            lineas = contenido.split('\n')
            info = info_default.copy()
            
            for linea in lineas:
                if linea.startswith('FECHA:'):
                    info['fecha'] = linea.replace('FECHA:', '').strip()
                elif linea.startswith('HORA:'):
                    info['hora'] = linea.replace('HORA:', '').strip()
                elif linea.startswith('CANCHA:'):
                    info['cancha'] = linea.replace('CANCHA:', '').strip()
                elif linea.strip() == '---':
                    break  # Termina la sección de metadatos
            
            print(f"✅ Información cargada: {info['fecha']} - {info['hora']} - {info['cancha']}")
            return info, True  # True = modo automático desde jugadores_confirmados.txt
    except Exception as e:
        print(f"⚠️ Error leyendo jugadores_confirmados.txt: {e}")
    
    # Prioridad 2: Fallback a confirmaciones_automaticas.json (código original)
    try:
        print("📄 Fallback: leyendo desde confirmaciones_automaticas.json")
        # Cargar desde confirmaciones_automaticas.json
        with open('confirmaciones_automaticas.json', 'r', encoding='utf-8') as f:
            confirmaciones = json.load(f)
        
        # Buscar la fecha más reciente disponible (priorizando fechas futuras)
        fechas_disponibles = sorted(confirmaciones.keys(), reverse=True)
        fecha_hoy = datetime.now().strftime('%Y-%m-%d')
        
        # Priorizar fechas futuras, luego hoy, luego pasadas
        fecha_seleccionada = None
        datos_partido = None
        
        # Primero buscar fechas futuras
        for fecha in fechas_disponibles:
            if fecha > fecha_hoy:
                fecha_seleccionada = fecha
                datos_partido = confirmaciones[fecha]
                print(f"ℹ️  Usando fecha futura: {fecha}")
                break
        
        # Si no hay fechas futuras, usar la de hoy si existe
        if not fecha_seleccionada and fecha_hoy in confirmaciones:
            fecha_seleccionada = fecha_hoy
            datos_partido = confirmaciones[fecha_hoy]
            print(f"ℹ️  Usando fecha de hoy: {fecha_hoy}")
        
        # Si no hay hoy ni futuras, usar la más reciente
        if not fecha_seleccionada and fechas_disponibles:
            fecha_seleccionada = fechas_disponibles[0]
            datos_partido = confirmaciones[fecha_seleccionada]
            print(f"ℹ️  Usando fecha más reciente: {fecha_seleccionada}")
        
        if not fecha_seleccionada:
            return info_default, False  # False = modo interactivo
        
        # Extraer información del partido
        resultado = info_default.copy()
        
        # La fecha viene de la clave del JSON (formato YYYY-MM-DD)
        resultado['fecha'] = fecha_seleccionada
        
        # Buscar hora y cancha en los datos, si existen
        if 'hora' in datos_partido:
            resultado['hora'] = datos_partido['hora']
        if 'cancha' in datos_partido:
            resultado['cancha'] = datos_partido['cancha']
            
        print(f"✅ Info del partido cargada: {resultado['fecha']} - {resultado['hora']} - Cancha {resultado['cancha']}")
        return resultado, False  # False = modo interactivo
        
    except FileNotFoundError:
        print("⚠️  No se encontró confirmaciones_automaticas.json, usando valores por defecto")
        return info_default, False  # False = modo interactivo
    except Exception as e:
        print(f"⚠️  Error cargando info del partido: {e}")
        return info_default, False  # False = modo interactivo

def jugadores_confirmados(todos_jugadores):
    """Filtra jugadores confirmados basado en jugadores_confirmados.txt o confirmaciones_automaticas.json"""
    
    # Prioridad 1: Intentar leer desde jugadores_confirmados.txt
    try:
        if os.path.exists('jugadores_confirmados.txt'):
            print("📄 Leyendo jugadores desde jugadores_confirmados.txt")
            with open('jugadores_confirmados.txt', 'r', encoding='utf-8') as f:
                contenido = f.read().strip()
            
            # Buscar la sección después de "---"
            lineas = contenido.split('\n')
            en_seccion_jugadores = False
            nombres_confirmados = []
            
            for linea in lineas:
                if linea.strip() == '---':
                    en_seccion_jugadores = True
                    continue
                
                if en_seccion_jugadores and linea.strip():
                    # Limpiar el nombre (quitar espacios extra)
                    nombre = linea.strip()
                    if nombre:
                        nombres_confirmados.append(nombre)
            
            # Buscar jugadores en la base de datos
            confirmados = []
            for nombre in nombres_confirmados:
                jugador = next((j for j in todos_jugadores if j['nombre'].lower() == nombre.lower()), None)
                if jugador:
                    confirmados.append(jugador)
                else:
                    print(f"⚠️  Jugador '{nombre}' no encontrado en la base de datos")
            
            print(f"✅ {len(confirmados)} jugadores confirmados cargados desde jugadores_confirmados.txt")
            if confirmados:
                return confirmados
                
    except Exception as e:
        print(f"⚠️ Error leyendo jugadores_confirmados.txt: {e}")
    
    # Prioridad 2: Fallback a confirmaciones_automaticas.json (código original)
    try:
        print("📄 Fallback: leyendo jugadores desde confirmaciones_automaticas.json")
        with open('confirmaciones_automaticas.json', 'r', encoding='utf-8') as f:
            confirmaciones = json.load(f)
        
        # Buscar confirmaciones para hoy
        fecha_hoy = datetime.now().strftime('%Y-%m-%d')
        
        if fecha_hoy in confirmaciones and 'jugadores' in confirmaciones[fecha_hoy]:
            nombres_confirmados = confirmaciones[fecha_hoy]['jugadores']
        else:
            # Buscar la fecha más reciente disponible
            fechas_disponibles = sorted(confirmaciones.keys(), reverse=True)
            if fechas_disponibles:
                fecha_reciente = fechas_disponibles[0]
                nombres_confirmados = confirmaciones[fecha_reciente]['jugadores']
                print(f"⚠️  Usando confirmaciones de {fecha_reciente} (no hay para hoy)")
            else:
                print("❌ Error: No hay confirmaciones disponibles")
                return []
        
        confirmados = []
        for nombre in nombres_confirmados:
            jugador = next((j for j in todos_jugadores if j['nombre'].lower() == nombre.lower()), None)
            if jugador:
                confirmados.append(jugador)
            else:
                print(f"⚠️  Jugador '{nombre}' no encontrado en la base de datos")
        
        print(f"✅ {len(confirmados)} jugadores confirmados cargados")
        return confirmados
        
    except FileNotFoundError:
        print("❌ Error: No se encontró confirmaciones_automaticas.json")
        return []
    except json.JSONDecodeError:
        print("❌ Error: confirmaciones_automaticas.json tiene formato inválido")
        return []
    except Exception as e:
        print(f"❌ Error cargando confirmaciones: {e}")
        return []

def generar_formaciones_posibles(jugadores_campo=5):
    """Genera formaciones con posiciones ESPECÍFICAS - cada posición tiene máximo 1 jugador
    
    IMPORTANTE: LCB, RCB, LM, CM, RM, CF son posiciones ESPECÍFICAS.
    Solo CM y CF pueden tener 2 jugadores en casos especiales (2 mediocentros, 2 delanteros).
    """
    formaciones = []
    
    if jugadores_campo == 5:
        # Formaciones para equipos de 6 (1 GK + 5 campo)
        # REGLA: LCB, RCB, LM, RM máximo 1 cada uno
        formaciones_basicas = [
            {'LCB': 1, 'RCB': 1, 'LM': 1, 'CM': 1, 'RM': 0, 'CF': 1},  # 2-3-1
            {'LCB': 1, 'RCB': 1, 'LM': 0, 'CM': 2, 'RM': 1, 'CF': 0},  # 2-3-0 (doble pivote)
            {'LCB': 1, 'RCB': 1, 'LM': 1, 'CM': 1, 'RM': 1, 'CF': 0},  # 2-3-0
            {'LCB': 1, 'RCB': 0, 'LM': 1, 'CM': 1, 'RM': 1, 'CF': 1},  # 1-3-1
            {'LCB': 0, 'RCB': 1, 'LM': 1, 'CM': 1, 'RM': 1, 'CF': 1},  # 1-3-1
            {'LCB': 1, 'RCB': 1, 'LM': 1, 'CM': 0, 'RM': 1, 'CF': 1},  # 2-2-1
            {'LCB': 1, 'RCB': 0, 'LM': 1, 'CM': 2, 'RM': 1, 'CF': 0},  # 1-4-0
            {'LCB': 0, 'RCB': 1, 'LM': 1, 'CM': 2, 'RM': 1, 'CF': 0},  # 1-4-0
        ]
    elif jugadores_campo == 6:
        # Formaciones para equipos de 7 (1 GK + 6 campo)
        # REGLA: LCB, RCB, LM, RM máximo 1 cada uno
        # IMPORTANTE: LM, CM, RM son posiciones ESPECÍFICAS - no se repiten jugadores
        formaciones_basicas = [
            {'LCB': 1, 'RCB': 1, 'LM': 1, 'CM': 2, 'RM': 1, 'CF': 0},  # 2-4-0 (doble pivote centro)
            {'LCB': 1, 'RCB': 1, 'LM': 1, 'CM': 1, 'RM': 1, 'CF': 1},  # 2-3-1 (clásico)
            {'LCB': 1, 'RCB': 1, 'LM': 1, 'CM': 0, 'RM': 1, 'CF': 2},  # 2-2-2 (doble 9)
            {'LCB': 1, 'RCB': 1, 'LM': 0, 'CM': 2, 'RM': 1, 'CF': 1},  # 2-3-1 (sin mediocampo izq)
            {'LCB': 1, 'RCB': 1, 'LM': 1, 'CM': 2, 'RM': 0, 'CF': 1},  # 2-3-1 (sin mediocampo der)
            {'LCB': 1, 'RCB': 0, 'LM': 1, 'CM': 2, 'RM': 1, 'CF': 1},  # 1-4-1 (sin defensa der)
            {'LCB': 0, 'RCB': 1, 'LM': 1, 'CM': 2, 'RM': 1, 'CF': 1},  # 1-4-1 (sin defensa izq)
        ]
    else:
        return []
    
    # ✅ VALIDACIÓN ESTRICTA: Verificar que ninguna posición lateral tenga más de 1 jugador
    formaciones_validas = []
    for formacion in formaciones_basicas:
        total = sum(formacion.values())
        
        # Verificar que LCB, RCB, LM, RM tengan máximo 1
        if (formacion['LCB'] <= 1 and formacion['RCB'] <= 1 and 
            formacion['LM'] <= 1 and formacion['RM'] <= 1 and
            total == jugadores_campo):
            formaciones_validas.append(formacion)
        else:
            print(f"⚠️  Formación inválida descartada: {formacion} (posiciones laterales duplicadas)")
    
    return formaciones_validas

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
    """Optimiza las posiciones para un equipo específico - FLEXIBLE para 6 o 7 jugadores"""
    if len(jugadores_equipo) not in [6, 7]:
        return None, 0, []
    
    # El primer jugador debe ser el mejor arquero
    arquero = jugadores_equipo[0]
    jugadores_campo = jugadores_equipo[1:]
    
    # Generar formaciones según el número de jugadores de campo
    if len(jugadores_campo) == 5:  # Equipos de 6 total
        formaciones_posibles = generar_formaciones_posibles(5)
    elif len(jugadores_campo) == 6:  # Equipos de 7 total  
        formaciones_posibles = generar_formaciones_posibles(6)
    else:
        return None, 0, []
    
    mejor_formacion = None
    mejor_puntaje = -1
    mejor_asignacion = []
    
    # Probar todas las formaciones disponibles
    for formacion in formaciones_posibles:
        puntaje, asignacion = asignar_flexible(jugadores_campo, formacion)
        
        if puntaje > mejor_puntaje:
            mejor_puntaje = puntaje
            mejor_formacion = formacion
            mejor_asignacion = asignacion
    
    return mejor_formacion, mejor_puntaje, mejor_asignacion

def asignar_flexible(jugadores_campo, formacion):
    """Asigna jugadores a posiciones de forma más flexible
    
    IMPORTANTE: Cada jugador solo puede estar en UNA posición específica.
    Usa permutaciones para garantizar que no haya duplicados.
    """
    posiciones_necesarias = []
    
    # Crear lista de posiciones necesarias según la formación
    for posicion, cantidad in formacion.items():
        for _ in range(cantidad):
            posiciones_necesarias.append(posicion)
    
    if len(posiciones_necesarias) != len(jugadores_campo):
        return 0, []
    
    # Asignación simple: mejores puntajes posibles
    import itertools
    mejor_puntaje = 0
    mejor_asignacion = []
    
    # Probar todas las permutaciones (para 5-6 jugadores es factible)
    # NOTA: itertools.permutations garantiza que cada jugador aparezca EXACTAMENTE una vez
    for permutacion in itertools.permutations(jugadores_campo):
        puntaje_total = 0
        asignacion_temp = []
        jugadores_usados = set()  # ✅ VALIDACIÓN ADICIONAL: verificar unicidad
        
        for i, jugador in enumerate(permutacion):
            posicion = posiciones_necesarias[i]
            
            # ✅ VERIFICACIÓN: Asegurar que cada jugador solo aparezca una vez
            if jugador['nombre'] in jugadores_usados:
                print(f"⚠️  ERROR: Jugador {jugador['nombre']} duplicado en asignación!")
                continue  # Saltar esta permutación inválida
            
            jugadores_usados.add(jugador['nombre'])
            
            # Usar puntaje de la posición (sin penalizaciones estrictas)
            puntaje = jugador['puntajes_posicion'][posicion]
            puntaje_total += puntaje
            asignacion_temp.append((jugador['nombre'], posicion, puntaje))
        
        # ✅ VERIFICACIÓN FINAL: Confirmar que se usaron todos los jugadores
        if len(jugadores_usados) != len(jugadores_campo):
            continue  # Saltar si hay jugadores faltantes
        
        if puntaje_total > mejor_puntaje:
            mejor_puntaje = puntaje_total
            mejor_asignacion = asignacion_temp
    
    return mejor_puntaje, mejor_asignacion

def puede_jugar_posicion(jugador, posicion):
    """Verifica si un jugador puede jugar en una posición específica"""
    posiciones_validas = [pos.strip() for pos in jugador['posicion'].split(',')]
    return posicion in posiciones_validas

def validar_equipos_sin_duplicados(equipo1, equipo2, info_sorteo):
    """Valida que no haya jugadores duplicados en posiciones
    
    REGLAS ESTRICTAS:
    - Cada jugador aparece EXACTAMENTE una vez
    - LCB, RCB, LM, RM: máximo 1 jugador por posición
    - CM, CF: máximo 2 jugadores por posición
    
    Returns:
        bool: True si no hay duplicados, False si hay algún problema
    """
    print("\n🔍 Validando equipos (sin duplicados)...")
    
    errores = []
    advertencias = []
    
    # Validar equipo 1
    jugadores_eq1 = set()
    posiciones_eq1 = {}
    
    for nombre, posicion, puntaje in info_sorteo['asignacion1']:
        if nombre in jugadores_eq1:
            errores.append(f"❌ EQUIPO ROJO: Jugador '{nombre}' aparece más de una vez")
        jugadores_eq1.add(nombre)
        
        if posicion in posiciones_eq1:
            posiciones_eq1[posicion].append(nombre)
        else:
            posiciones_eq1[posicion] = [nombre]
    
    # Validar equipo 2
    jugadores_eq2 = set()
    posiciones_eq2 = {}
    
    for nombre, posicion, puntaje in info_sorteo['asignacion2']:
        if nombre in jugadores_eq2:
            errores.append(f"❌ EQUIPO NEGRO: Jugador '{nombre}' aparece más de una vez")
        jugadores_eq2.add(nombre)
        
        if posicion in posiciones_eq2:
            posiciones_eq2[posicion].append(nombre)
        else:
            posiciones_eq2[posicion] = [nombre]
    
    # ✅ VALIDACIÓN ESTRICTA: Posiciones laterales solo 1 jugador
    posiciones_unicas = ['GK', 'LCB', 'RCB', 'LM', 'RM']
    posiciones_dobles_permitidas = ['CM', 'CF']  # Solo estas pueden tener 2
    
    for posicion, jugadores in posiciones_eq1.items():
        if posicion in posiciones_unicas and len(jugadores) > 1:
            errores.append(f"❌ EQUIPO ROJO: Posición {posicion} tiene {len(jugadores)} jugadores: {', '.join(jugadores)} (DEBE ser 1)")
        elif posicion in posiciones_dobles_permitidas and len(jugadores) > 2:
            errores.append(f"❌ EQUIPO ROJO: Posición {posicion} tiene {len(jugadores)} jugadores: {', '.join(jugadores)} (máximo 2)")
    
    for posicion, jugadores in posiciones_eq2.items():
        if posicion in posiciones_unicas and len(jugadores) > 1:
            errores.append(f"❌ EQUIPO NEGRO: Posición {posicion} tiene {len(jugadores)} jugadores: {', '.join(jugadores)} (DEBE ser 1)")
        elif posicion in posiciones_dobles_permitidas and len(jugadores) > 2:
            errores.append(f"❌ EQUIPO NEGRO: Posición {posicion} tiene {len(jugadores)} jugadores: {', '.join(jugadores)} (máximo 2)")
    
    # Mostrar resultados
    if errores:
        print("❌ Se encontraron ERRORES CRÍTICOS:")
        for error in errores:
            print(f"   {error}")
        return False
    elif advertencias:
        print("⚠️  Se encontraron advertencias:")
        for adv in advertencias:
            print(f"   {adv}")
        print("✅ Sin errores críticos - continuando...")
        return True
    else:
        print("✅ Validación exitosa: Todos los jugadores están asignados correctamente")
        print(f"   - Equipo Rojo: {len(jugadores_eq1)} jugadores únicos en {len(posiciones_eq1)} posiciones")
        print(f"   - Equipo Negro: {len(jugadores_eq2)} jugadores únicos en {len(posiciones_eq2)} posiciones")
        
        # Mostrar distribución de posiciones
        print("   📊 Distribución Equipo Rojo:")
        for pos in ['GK', 'LCB', 'RCB', 'LM', 'CM', 'RM', 'CF']:
            if pos in posiciones_eq1:
                print(f"      {pos}: {len(posiciones_eq1[pos])} jugador(es)")
        
        print("   📊 Distribución Equipo Negro:")
        for pos in ['GK', 'LCB', 'RCB', 'LM', 'CM', 'RM', 'CF']:
            if pos in posiciones_eq2:
                print(f"      {pos}: {len(posiciones_eq2[pos])} jugador(es)")
        
        return True

def sorteo_con_posiciones_especificas(jugadores, num_intentos=10000, jugadores_por_equipo=6, margen_error=0.3):
    """Realiza el sorteo optimizando posiciones específicas - FLEXIBLE para 6 o 7 jugadores por equipo
    
    Args:
        jugadores: Lista de jugadores con sus datos
        num_intentos: Número máximo de intentos de optimización
        jugadores_por_equipo: Jugadores por equipo (6 o 7)
        margen_error: Margen de error aceptable en diferencia de promedios (por ejemplo, 0.3 puntos)
    """
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
        
        # DEBUG: Mostrar información de debug cada 100 intentos
        if (intento + 1) % 100 == 0:
            print(f"   Intento {intento + 1}: Formación1={formacion1 is not None}, Formación2={formacion2 is not None}")
            if formacion1 is None:
                print(f"      ❌ Equipo1 falló: {[j['nombre'] for j in equipo1]}")
            if formacion2 is None:
                print(f"      ❌ Equipo2 falló: {[j['nombre'] for j in equipo2]}")
        
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
            
            # 🆕 MARGEN DE ERROR: Si estamos dentro del margen aceptable, parar búsqueda
            if diferencia <= margen_error:
                print(f"✅ Encontrado equilibrio aceptable en intento {intento + 1}: diferencia = {diferencia:.3f} (≤ {margen_error})")
                break
        
        # Mostrar progreso con mejor diferencia
        if (intento + 1) % 100 == 0:
            print(f"   Intento {intento + 1}: Mejor diferencia = {mejor_diferencia:.3f}")
    
    return mejor_equipo1, mejor_equipo2, mejor_info

def formatear_formacion(formacion):
    """Convierte la formación a string legible"""
    defensas = formacion['LCB'] + formacion['RCB']
    mediocampos = formacion['LM'] + formacion['CM'] + formacion['RM']
    delanteros = formacion['CF']
    return f"1-{defensas}-{mediocampos}-{delanteros}"

def guardar_equipos(equipo1, equipo2, info_sorteo, info_partido, jugadores_por_equipo=6):
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
        "promedio_rojo": round(info_sorteo['puntaje1']/jugadores_por_equipo, 2),
        "promedio_negro": round(info_sorteo['puntaje2']/jugadores_por_equipo, 2),
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

def mostrar_equipos_detallados(equipo1, equipo2, info_sorteo, info_partido, jugadores_por_equipo=6):
    """Muestra los equipos con posiciones específicas detalladas"""
    print(f"\n⚽ Partido {info_partido['fecha']} - {info_partido['hora']} - {info_partido['cancha']}")
    print("📋 Formaciones con Posiciones Específicas (Respetando Posiciones Válidas)")
    print("=" * 80)
    
    # Equipo Rojo
    formacion1_str = formatear_formacion(info_sorteo['formacion1'])
    
    # Calcular promedio general del equipo rojo
    promedio_general_rojo = sum(j['puntaje'] for j in equipo1) / len(equipo1)
    
    print(f"\n🔴 EQUIPO ROJO - Formación {formacion1_str} (Promedio general: {promedio_general_rojo:.2f}, Promedio por posición: {info_sorteo['puntaje1']/jugadores_por_equipo:.2f}):")
    
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
    
    # Calcular promedio general del equipo negro
    promedio_general_negro = sum(j['puntaje'] for j in equipo2) / len(equipo2)
    
    print(f"\n⚫ EQUIPO NEGRO - Formación {formacion2_str} (Promedio general: {promedio_general_negro:.2f}, Promedio por posición: {info_sorteo['puntaje2']/jugadores_por_equipo:.2f}):")
    
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
    
    print(f"\n📊 Diferencia de promedios (por posición): {info_sorteo['diferencia']:.3f}")
    print(f"📊 Diferencia de promedios (general): {abs(promedio_general_rojo - promedio_general_negro):.3f}")
    print(f"🎲 Formaciones: Rojo {formacion1_str} vs Negro {formacion2_str}")
    print("⭐ = Posición válida | ⚠️ = Fuera de posición (penalizado)")
    print("=" * 80)

def actualizar_archivos_html():
    """Actualiza los archivos HTML desde equipos.json"""
    try:
        # Actualizar cancha simple
        import subprocess
        import sys
        result = subprocess.run([sys.executable, 'actualizar_cancha_simple.py'], 
                              capture_output=True, text=True, cwd='.')
        if result.returncode == 0:
            print("✅ Cancha simple actualizada automáticamente")
        else:
            print(f"⚠️  Error actualizando cancha simple: {result.stderr}")
    except Exception as e:
        print(f"⚠️  Error ejecutando actualización de cancha: {e}")
    
    try:
        # Actualizar index.html
        result = subprocess.run([sys.executable, 'actualizar_index.py'], 
                              capture_output=True, text=True, cwd='.')
        if result.returncode == 0:
            print("✅ Index.html actualizado automáticamente")
        else:
            print(f"⚠️  Error actualizando index.html: {result.stderr}")
    except Exception as e:
        print(f"⚠️  Error ejecutando actualización de index: {e}")
    
    print("✅ Sorteo completado - Los archivos HTML se actualizarán automáticamente desde la web")

def main():
    print("🚀 SORTEO CON POSICIONES ESPECÍFICAS (7 POSICIONES)")
    print("=" * 60)
    print("Posiciones: GK, LCB, RCB, LM, CM, RM, CF")
    print("=" * 60)
    
    # Cargar información del partido
    info_partido, modo_automatico = cargar_info_partido()
    print(f"📅 Partido: {info_partido['fecha']} - {info_partido['hora']} - {info_partido['cancha']}")
    if modo_automatico:
        print("🤖 Modo automático detectado (desde jugadores_confirmados.txt)")
    print("=" * 60)
    
    # Cargar jugadores
    jugadores = cargar_jugadores()
    if not jugadores:
        return
    
    # Filtrar confirmados
    confirmados = jugadores_confirmados(jugadores)
    
    if len(confirmados) < 12:
        print(f"❌ Error: Se necesitan al menos 12 jugadores confirmados (tienes {len(confirmados)})")
        return
    
    # Determinar configuración de equipos según número de jugadores
    if len(confirmados) == 12:
        print("📊 Configuración: 2 equipos de 6 jugadores (1 GK + 5 campo)")
        jugadores_por_equipo = 6
        suplentes = []
    elif len(confirmados) == 14:
        print("📊 Configuración: 2 equipos de 7 jugadores (1 GK + 6 campo)")
        jugadores_por_equipo = 7
        suplentes = []
    elif len(confirmados) > 14:
        # Más de 14: usar 14 y dejar suplentes
        arqueros = [j for j in confirmados if puede_jugar_posicion(j, 'GK')]
        otros = [j for j in confirmados if not puede_jugar_posicion(j, 'GK')]
        
        if len(arqueros) >= 2:
            confirmados_finales = arqueros[:2] + otros[:12]  # 2 arqueros + 12 de campo
            suplentes = [j['nombre'] for j in confirmados if j not in confirmados_finales]
            print(f"📊 Configuración: 2 equipos de 7 jugadores de {len(confirmados)} disponibles")
            print(f"   Suplentes: {suplentes}")
            confirmados = confirmados_finales
            jugadores_por_equipo = 7
        else:
            print(f"❌ Error: Se necesitan al menos 2 arqueros válidos (tienes {len(arqueros)})")
            return
    elif len(confirmados) == 13:
        # 13 jugadores: usar 12 para equipos de 6
        arqueros = [j for j in confirmados if puede_jugar_posicion(j, 'GK')]
        otros = [j for j in confirmados if not puede_jugar_posicion(j, 'GK')]
        
        if len(arqueros) >= 2:
            confirmados_finales = arqueros[:2] + otros[:10]  # 2 arqueros + 10 de campo
            suplentes = [j['nombre'] for j in confirmados if j not in confirmados_finales]
            print(f"📊 Configuración: 2 equipos de 6 jugadores (1 suplente)")
            print(f"   Suplente: {suplentes}")
            confirmados = confirmados_finales
            jugadores_por_equipo = 6
        else:
            print(f"❌ Error: Se necesitan al menos 2 arqueros válidos (tienes {len(arqueros)})")
            return
    
    print(f"👥 Jugadores confirmados: {len(confirmados)}")
    for jugador in confirmados:
        print(f"   - {jugador['nombre']} (General: {jugador['puntaje']})")
    
    # Configurar intentos
    if modo_automatico:
        # Modo automático: usar valores por defecto optimizados para rotación
        intentos = 1000
        margen_error = 0.4  # Margen más amplio para permitir más rotación
        print(f"🤖 Configuración automática: {intentos} intentos, margen de error {margen_error:.1f}")
    else:
        # Modo interactivo: preguntar al usuario
        try:
            intentos_str = input(f"\nNúmero de intentos para optimización (100-5000) [1000]: ").strip()
            intentos = int(intentos_str) if intentos_str else 1000
            intentos = max(100, min(5000, intentos))
        except ValueError:
            intentos = 1000
        
        # 🆕 Configurar margen de error para permitir rotación
        try:
            margen_str = input(f"\nMargen de error aceptable en diferencia de promedios (0.1-1.0) [0.3]: ").strip()
            margen_error = float(margen_str) if margen_str else 0.3
            margen_error = max(0.1, min(1.0, margen_error))
            print(f"📊 Margen de error configurado: {margen_error:.1f} puntos (permite más rotación de jugadores)")
        except ValueError:
            margen_error = 0.3
    
    # Realizar sorteo
    equipo1, equipo2, info_sorteo = sorteo_con_posiciones_especificas(confirmados, intentos, jugadores_por_equipo, margen_error)
    
    if equipo1 is None:
        print("❌ Error: No se pudo generar un sorteo válido")
        return
    
    # ✅ VALIDAR que no haya duplicados
    if not validar_equipos_sin_duplicados(equipo1, equipo2, info_sorteo):
        print("⚠️  ADVERTENCIA: Se detectaron problemas en la asignación de jugadores")
        respuesta = input("¿Deseas continuar de todos modos? (s/n) [n]: ").strip().lower()
        if respuesta != 's':
            print("❌ Sorteo cancelado por el usuario")
            return
    
    # Mostrar resultados
    mostrar_equipos_detallados(equipo1, equipo2, info_sorteo, info_partido, jugadores_por_equipo)
    
    # Guardar resultados
    guardar_equipos(equipo1, equipo2, info_sorteo, info_partido, jugadores_por_equipo)
    print(f"\n✅ Sorteo con posiciones específicas completado y guardado en equipos.json")
    
    # Actualizar HTML
    actualizar_archivos_html()

if __name__ == "__main__":
    main()
