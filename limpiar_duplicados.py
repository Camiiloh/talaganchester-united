#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para limpiar duplicados en historial_partidos.json
"""

import json
from datetime import datetime

def limpiar_duplicados():
    """Limpia duplicados del historial de partidos"""
    
    archivo = 'historial_partidos.json'
    
    try:
        # Cargar datos
        with open(archivo, 'r', encoding='utf-8') as f:
            partidos = json.load(f)
        
        print(f"📊 Partidos originales: {len(partidos)}")
        
        # Crear diccionario para detectar duplicados
        partidos_unicos = {}
        duplicados_removidos = 0
        
        for partido in partidos:
            # Crear clave única basada en fecha, hora, cancha y equipos
            equipos_rojo = sorted(partido.get('equipo_rojo', []))
            equipos_negro = sorted(partido.get('equipo_negro', []))
            
            clave_unica = f"{partido.get('fecha', '')}-{partido.get('hora', '')}-{partido.get('cancha', '')}-{'-'.join(equipos_rojo)}-{'-'.join(equipos_negro)}"
            
            if clave_unica in partidos_unicos:
                # Es duplicado - mantener el que tenga timestamp más reciente
                partido_existente = partidos_unicos[clave_unica]
                
                # Comparar timestamps
                timestamp_actual = partido.get('timestamp', '')
                timestamp_existente = partido_existente.get('timestamp', '')
                
                if timestamp_actual > timestamp_existente:
                    print(f"🔄 Reemplazando duplicado más antiguo: {clave_unica}")
                    partidos_unicos[clave_unica] = partido
                else:
                    print(f"🗑️ Eliminando duplicado: {clave_unica}")
                
                duplicados_removidos += 1
            else:
                partidos_unicos[clave_unica] = partido
        
        # Convertir de vuelta a lista
        partidos_limpios = list(partidos_unicos.values())
        
        # Ordenar por fecha (más recientes primero)
        partidos_limpios.sort(key=lambda p: p.get('fecha', ''), reverse=True)
        
        print(f"✅ Partidos después de limpieza: {len(partidos_limpios)}")
        print(f"🗑️ Duplicados removidos: {duplicados_removidos}")
        
        if duplicados_removidos > 0:
            # Crear backup
            backup_file = f'historial_partidos_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
            with open(backup_file, 'w', encoding='utf-8') as f:
                json.dump(partidos, f, indent=2, ensure_ascii=False)
            print(f"💾 Backup creado: {backup_file}")
            
            # Guardar archivo limpio
            with open(archivo, 'w', encoding='utf-8') as f:
                json.dump(partidos_limpios, f, indent=2, ensure_ascii=False)
            print(f"✅ Archivo limpio guardado: {archivo}")
        else:
            print("ℹ️ No se encontraron duplicados")
            
    except FileNotFoundError:
        print(f"❌ No se encontró el archivo {archivo}")
    except json.JSONDecodeError:
        print(f"❌ Error al leer JSON del archivo {archivo}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == '__main__':
    print("🧹 Iniciando limpieza de duplicados...")
    limpiar_duplicados()
    print("🎉 Limpieza completada")
