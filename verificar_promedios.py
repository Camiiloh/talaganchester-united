#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para verificar los promedios de los equipos actuales
"""

import json

def verificar_promedios():
    """Verifica los promedios de los equipos basándose en el último partido"""
    
    try:
        # Cargar historial de partidos
        with open('historial_partidos.json', 'r', encoding='utf-8') as f:
            partidos = json.load(f)
        
        # Cargar puntajes de jugadores
        with open('jugadores_posiciones_especificas.json', 'r', encoding='utf-8') as f:
            jugadores_data = json.load(f)
        
        # Crear diccionario de puntajes
        puntajes = {}
        for jugador in jugadores_data:
            puntajes[jugador['nombre']] = jugador['puntaje']
        
        # Obtener último partido
        ultimo_partido = partidos[0] if partidos else None
        
        if not ultimo_partido:
            print("❌ No hay partidos en el historial")
            return
        
        print(f"📊 Analizando partido del {ultimo_partido['fecha']}")
        print(f"⚽ Resultado: Rojo {ultimo_partido['resultado']['rojo']} - {ultimo_partido['resultado']['negro']} Negro")
        print()
        
        # Calcular promedio equipo rojo
        equipo_rojo = ultimo_partido['equipo_rojo']
        print("🔴 EQUIPO ROJO:")
        suma_rojo = 0
        for jugador in equipo_rojo:
            puntaje = puntajes.get(jugador, 0)
            suma_rojo += puntaje
            print(f"   {jugador}: {puntaje}")
        
        promedio_rojo = suma_rojo / len(equipo_rojo) if equipo_rojo else 0
        print(f"   Promedio: {promedio_rojo:.2f}")
        print()
        
        # Calcular promedio equipo negro
        equipo_negro = ultimo_partido['equipo_negro']
        print("⚫ EQUIPO NEGRO:")
        suma_negro = 0
        for jugador in equipo_negro:
            puntaje = puntajes.get(jugador, 0)
            suma_negro += puntaje
            print(f"   {jugador}: {puntaje}")
        
        promedio_negro = suma_negro / len(equipo_negro) if equipo_negro else 0
        print(f"   Promedio: {promedio_negro:.2f}")
        print()
        
        print("📈 RESUMEN:")
        print(f"   Equipo Rojo: {promedio_rojo:.2f}")
        print(f"   Equipo Negro: {promedio_negro:.2f}")
        print(f"   Diferencia: {abs(promedio_rojo - promedio_negro):.2f}")
        
        # Verificar si hay jugadores sin puntaje
        todos_jugadores = set(equipo_rojo + equipo_negro)
        jugadores_sin_puntaje = []
        for jugador in todos_jugadores:
            if jugador not in puntajes:
                jugadores_sin_puntaje.append(jugador)
        
        if jugadores_sin_puntaje:
            print("\n⚠️  JUGADORES SIN PUNTAJE:")
            for jugador in jugadores_sin_puntaje:
                print(f"   {jugador}")
        
    except FileNotFoundError as e:
        print(f"❌ Archivo no encontrado: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == '__main__':
    verificar_promedios()
