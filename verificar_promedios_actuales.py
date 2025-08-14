#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para verificar los promedios por posición de los equipos actuales
"""

import json

def verificar_promedios_equipos_actuales():
    """Verifica los promedios de los equipos según equipos.json"""
    
    try:
        # Cargar equipos actuales
        with open('equipos.json', 'r', encoding='utf-8') as f:
            equipos_data = json.load(f)
        
        # Cargar puntajes de jugadores
        with open('jugadores_posiciones_especificas.json', 'r', encoding='utf-8') as f:
            jugadores_data = json.load(f)
        
        # Crear diccionario de puntajes y posiciones
        puntajes = {}
        puntajes_posicion = {}
        for jugador in jugadores_data:
            puntajes[jugador['nombre']] = jugador['puntaje']
            puntajes_posicion[jugador['nombre']] = jugador['puntajes_posicion']
        
        print("📊 Verificando promedios de equipos actuales (según equipos.json)")
        print("=" * 70)
        
        # Calcular promedio equipo rojo
        equipo_rojo = equipos_data['rojo']
        posiciones_rojo = equipos_data['rojo_posiciones']
        
        print("\n🔴 EQUIPO ROJO:")
        suma_general_rojo = 0
        suma_posicion_rojo = 0
        
        for jugador in equipo_rojo:
            puntaje_general = puntajes.get(jugador, 0)
            posicion = posiciones_rojo.get(jugador, "Sin asignar")
            
            # Mapear posición a clave JSON
            pos_map = {
                "Arquero": "GK",
                "Defensa": "LCB",  # O RCB, tomaremos LCB por defecto
                "Mediocampo": "CM",
                "Delantero": "CF"
            }
            
            pos_key = pos_map.get(posicion, "CM")
            puntaje_posicion = puntajes_posicion.get(jugador, {}).get(pos_key, 0)
            
            suma_general_rojo += puntaje_general
            suma_posicion_rojo += puntaje_posicion
            
            print(f"   {jugador}: {puntaje_general:.1f} general, {puntaje_posicion:.1f} en {posicion}")
        
        promedio_general_rojo = suma_general_rojo / len(equipo_rojo) if equipo_rojo else 0
        promedio_posicion_rojo = suma_posicion_rojo / len(equipo_rojo) if equipo_rojo else 0
        
        print(f"   Promedio general: {promedio_general_rojo:.2f}")
        print(f"   Promedio por posición: {promedio_posicion_rojo:.2f}")
        
        # Calcular promedio equipo negro
        equipo_negro = equipos_data['negro']
        posiciones_negro = equipos_data['negro_posiciones']
        
        print("\n⚫ EQUIPO NEGRO:")
        suma_general_negro = 0
        suma_posicion_negro = 0
        
        for jugador in equipo_negro:
            puntaje_general = puntajes.get(jugador, 0)
            posicion = posiciones_negro.get(jugador, "Sin asignar")
            
            pos_key = pos_map.get(posicion, "CM")
            puntaje_posicion = puntajes_posicion.get(jugador, {}).get(pos_key, 0)
            
            suma_general_negro += puntaje_general
            suma_posicion_negro += puntaje_posicion
            
            print(f"   {jugador}: {puntaje_general:.1f} general, {puntaje_posicion:.1f} en {posicion}")
        
        promedio_general_negro = suma_general_negro / len(equipo_negro) if equipo_negro else 0
        promedio_posicion_negro = suma_posicion_negro / len(equipo_negro) if equipo_negro else 0
        
        print(f"   Promedio general: {promedio_general_negro:.2f}")
        print(f"   Promedio por posición: {promedio_posicion_negro:.2f}")
        
        print("\n📈 RESUMEN:")
        print(f"   Rojo - General: {promedio_general_rojo:.2f}, Por posición: {promedio_posicion_rojo:.2f}")
        print(f"   Negro - General: {promedio_general_negro:.2f}, Por posición: {promedio_posicion_negro:.2f}")
        print(f"   Diferencia general: {abs(promedio_general_rojo - promedio_general_negro):.2f}")
        print(f"   Diferencia por posición: {abs(promedio_posicion_rojo - promedio_posicion_negro):.2f}")
        
        print(f"\n✅ Promedio mostrado en equipos.json: {equipos_data['promedio_rojo']:.2f}")
        
    except FileNotFoundError as e:
        print(f"❌ Archivo no encontrado: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == '__main__':
    verificar_promedios_equipos_actuales()
