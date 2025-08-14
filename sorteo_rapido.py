#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema de sorteo simplificado con posiciones específicas - FUNCIONAL
"""

import json
import random
import itertools
from datetime import datetime

def cargar_jugadores(archivo='jugadores_posiciones_especificas.json'):
    """Carga la lista de jugadores con puntajes por posición específica."""
    try:
        with open(archivo, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"❌ Error: No se encontró el archivo {archivo}")
        return []

def jugadores_confirmados(todos_jugadores):
    """Filtra jugadores confirmados basado en confirmaciones_automaticas.json"""
    try:
        with open('confirmaciones_automaticas.json', 'r', encoding='utf-8') as f:
            confirmaciones = json.load(f)
        
        fecha_hoy = datetime.now().strftime('%Y-%m-%d')
        
        if fecha_hoy in confirmaciones and 'jugadores' in confirmaciones[fecha_hoy]:
            nombres_confirmados = confirmaciones[fecha_hoy]['jugadores']
        else:
            fechas_disponibles = sorted(confirmaciones.keys(), reverse=True)
            if fechas_disponibles:
                fecha_reciente = fechas_disponibles[0]
                nombres_confirmados = confirmaciones[fecha_reciente]['jugadores']
                print(f"⚠️  Usando confirmaciones de {fecha_reciente}")
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
        
    except Exception as e:
        print(f"❌ Error cargando confirmaciones: {e}")
        return []

def sorteo_simple(jugadores):
    """Sorteo simple y efectivo"""
    if len(jugadores) % 2 != 0:
        print(f"❌ Error: Número impar de jugadores confirmados ({len(jugadores)})")
        return None, None, None
    
    if len(jugadores) < 12:
        print(f"❌ Error: Se necesitan al menos 12 jugadores confirmados (tienes {len(jugadores)})")
        return None, None, None
    
    # Separar arqueros del resto
    arqueros = [j for j in jugadores if 'GK' in j['posicion']]
    otros = [j for j in jugadores if 'GK' not in j['posicion']]
    
    if len(arqueros) < 2:
        print(f"❌ Error: Se necesitan al menos 2 arqueros (tienes {len(arqueros)})")
        return None, None, None
    
    print(f"✅ Arqueros disponibles: {[a['nombre'] for a in arqueros]}")
    
    # Asignar un arquero a cada equipo
    random.shuffle(arqueros)
    arquero1, arquero2 = arqueros[0], arqueros[1]
    
    # Distribuir el resto de jugadores
    otros_disponibles = otros + arqueros[2:]  # Arqueros extra van al pool general
    random.shuffle(otros_disponibles)
    
    jugadores_por_equipo = len(jugadores) // 2
    equipo1 = [arquero1] + otros_disponibles[:jugadores_por_equipo-1]
    equipo2 = [arquero2] + otros_disponibles[jugadores_por_equipo-1:]
    
    # Calcular puntajes
    puntaje1 = sum(j['puntaje'] for j in equipo1)
    puntaje2 = sum(j['puntaje'] for j in equipo2)
    
    info = {
        'puntaje1': puntaje1,
        'puntaje2': puntaje2,
        'diferencia': abs(puntaje1 - puntaje2),
        'promedio1': puntaje1 / len(equipo1),
        'promedio2': puntaje2 / len(equipo2)
    }
    
    return equipo1, equipo2, info

def guardar_equipos(equipo1, equipo2, info):
    """Guarda los equipos en equipos.json"""
    
    equipos_data = {
        "fecha": "Fecha por confirmar",
        "hora": "22:00 hrs",
        "cancha": "Por confirmar",
        "metodo": "Posiciones Específicas (Simplificado)",
        "rojo": [j['nombre'] for j in equipo1],
        "negro": [j['nombre'] for j in equipo2],
        "promedio_rojo": round(info['promedio1'], 2),
        "promedio_negro": round(info['promedio2'], 2),
        "diferencia": round(info['diferencia'], 3),
        "equipos": {
            "rojo": [j['nombre'] for j in equipo1],
            "negro": [j['nombre'] for j in equipo2]
        },
        "timestamp": datetime.now().isoformat()
    }
    
    try:
        with open('equipos.json', 'w', encoding='utf-8') as f:
            json.dump(equipos_data, f, ensure_ascii=False, indent=2)
        print("✅ Equipos guardados en equipos.json")
        return True
    except Exception as e:
        print(f"❌ Error guardando equipos: {e}")
        return False

def mostrar_resultados(equipo1, equipo2, info):
    """Muestra los resultados del sorteo"""
    print(f"\n🔴 EQUIPO ROJO (Promedio: {info['promedio1']:.2f}):")
    print(f"   🥅 Arquero: {equipo1[0]['nombre']}")
    for jugador in equipo1[1:]:
        print(f"   ⚽ {jugador['nombre']} ({jugador['puntaje']})")
    
    print(f"\n⚫ EQUIPO NEGRO (Promedio: {info['promedio2']:.2f}):")
    print(f"   🥅 Arquero: {equipo2[0]['nombre']}")
    for jugador in equipo2[1:]:
        print(f"   ⚽ {jugador['nombre']} ({jugador['puntaje']})")
    
    print(f"\n📊 RESUMEN:")
    print(f"   • Diferencia: {info['diferencia']:.3f}")
    print(f"   • Balance: {'✅ EXCELENTE' if info['diferencia'] < 1.0 else '⚖️ BUENO' if info['diferencia'] < 2.0 else '⚠️ ACEPTABLE'}")

def main():
    print("🚀 SORTEO RÁPIDO CON POSICIONES ESPECÍFICAS")
    print("=" * 50)
    
    # Cargar jugadores
    jugadores = cargar_jugadores()
    if not jugadores:
        return
    
    # Filtrar confirmados
    confirmados = jugadores_confirmados(jugadores)
    if len(confirmados) < 12:
        return
    
    print(f"\n👥 Jugadores confirmados: {len(confirmados)}")
    for j in confirmados:
        print(f"   • {j['nombre']} (General: {j['puntaje']})")
    
    print(f"\n🎲 Realizando sorteo...")
    
    # Realizar sorteo
    equipo1, equipo2, info = sorteo_simple(confirmados)
    
    if equipo1 and equipo2:
        mostrar_resultados(equipo1, equipo2, info)
        
        # Guardar equipos
        if guardar_equipos(equipo1, equipo2, info):
            print("\n✅ ¡Sorteo completado exitosamente!")
        else:
            print("\n⚠️ Sorteo completado pero error al guardar")
    else:
        print("\n❌ No se pudo realizar el sorteo")

if __name__ == "__main__":
    main()
