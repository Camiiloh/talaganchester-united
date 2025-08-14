#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para actualizar partidos existentes con información de equipos
"""

from database_manager import db_manager
import json

def actualizar_partidos_con_equipos():
    """Actualiza partidos existentes agregando información de equipos"""
    historial = db_manager.get_historial_partidos()
    print(f"📊 Partidos a actualizar: {len(historial)}")
    
    partidos_actualizados = 0
    
    for partido in historial:
        # Si ya tiene equipos, saltarlo
        equipos = partido.get('equipos', {})
        if equipos and equipos.get('rojo') and equipos.get('negro'):
            print(f"✅ Partido {partido['fecha']} ya tiene equipos")
            continue
        
        # Obtener jugadores confirmados
        jugadores = partido.get('jugadores_confirmados', [])
        if len(jugadores) < 2:
            print(f"⚠️ Partido {partido['fecha']} no tiene suficientes jugadores")
            continue
        
        # Dividir jugadores en dos equipos
        medio = len(jugadores) // 2
        equipo_rojo = jugadores[:medio]
        equipo_negro = jugadores[medio:]
        
        # Actualizar partido
        partido['equipos'] = {
            'rojo': equipo_rojo,
            'negro': equipo_negro
        }
        
        # También agregar campos de compatibilidad
        partido['equipo_rojo'] = equipo_rojo
        partido['equipo_negro'] = equipo_negro
        
        print(f"🔄 Actualizando partido {partido['fecha']}:")
        print(f"  🔴 Equipo Rojo ({len(equipo_rojo)}): {equipo_rojo}")
        print(f"  ⚫ Equipo Negro ({len(equipo_negro)}): {equipo_negro}")
        
        # Guardar en base de datos
        if db_manager.save_partido(partido):
            partidos_actualizados += 1
            print(f"✅ Partido {partido['fecha']} actualizado exitosamente")
        else:
            print(f"❌ Error actualizando partido {partido['fecha']}")
    
    print(f"\n📈 Partidos actualizados: {partidos_actualizados}")

if __name__ == '__main__':
    print("🔄 Actualizando partidos existentes con información de equipos...")
    actualizar_partidos_con_equipos()
    print("\n✅ Proceso completado!")
