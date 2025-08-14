#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script simple para agregar confirmaciones al archivo local
Sin necesidad del servidor Flask
"""

import json
import os
from datetime import datetime

def agregar_confirmaciones(jugadores, fecha=None, fuente='Manual', hora=None, cancha=None):
    """Agrega confirmaciones al archivo local con información completa del partido"""
    
    if not fecha:
        fecha = datetime.now().strftime('%Y-%m-%d')
    
    archivo = 'confirmaciones_automaticas.json'
    
    # Cargar datos existentes
    if os.path.exists(archivo):
        with open(archivo, 'r', encoding='utf-8') as f:
            datos = json.load(f)
    else:
        datos = {}
    
    # Crear entrada para la fecha
    entrada_partido = {
        'jugadores': jugadores,
        'timestamp': datetime.now().isoformat(),
        'fuentes': {jugador: fuente for jugador in jugadores}
    }
    
    # Agregar hora y cancha si se proporcionan
    if hora:
        entrada_partido['hora'] = hora
    if cancha:
        entrada_partido['cancha'] = cancha
    
    datos[fecha] = entrada_partido
    
    # Guardar datos
    with open(archivo, 'w', encoding='utf-8') as f:
        json.dump(datos, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Confirmaciones guardadas para {fecha}")
    print(f"👥 Jugadores: {len(jugadores)}")
    print(f"📝 Lista: {', '.join(jugadores)}")

def leer_jugadores_desde_txt(archivo_txt='jugadores_confirmados.txt'):
    """Lee jugadores, fecha, hora y cancha desde un archivo de texto"""
    try:
        with open(archivo_txt, 'r', encoding='utf-8') as f:
            lineas = [linea.strip() for linea in f.readlines() if linea.strip()]
        
        # Valores por defecto
        fecha = None
        hora = None
        cancha = None
        jugadores = []
        
        # Buscar información del partido en las primeras líneas
        i = 0
        while i < len(lineas):
            linea = lineas[i].upper()
            
            if linea.startswith('FECHA:'):
                fecha = lineas[i].split(':', 1)[1].strip()
                i += 1
            elif linea.startswith('HORA:'):
                hora = lineas[i].split(':', 1)[1].strip()
                i += 1
            elif linea.startswith('CANCHA:'):
                cancha = lineas[i].split(':', 1)[1].strip()
                i += 1
            elif linea == '---' or linea == 'JUGADORES:':
                i += 1
                break
            else:
                # Si no encuentra formato especial, tratar como jugador
                break
        
        # El resto son jugadores
        while i < len(lineas):
            if lineas[i] and not lineas[i].startswith('---'):
                jugadores.append(lineas[i])
            i += 1
        
        print(f"📄 Archivo leído: {archivo_txt}")
        print(f"👥 Jugadores encontrados: {len(jugadores)}")
        if fecha:
            print(f"📅 Fecha: {fecha}")
        if hora:
            print(f"⏰ Hora: {hora}")
        if cancha:
            print(f"🏟️ Cancha: {cancha}")
            
        return {
            'jugadores': jugadores,
            'fecha': fecha,
            'hora': hora,
            'cancha': cancha
        }
        
    except FileNotFoundError:
        print(f"❌ No se encontró el archivo {archivo_txt}")
        print(f"💡 Crea el archivo con el formato:")
        print(f"FECHA: 2025-08-15")
        print(f"HORA: 21:00")
        print(f"CANCHA: 2")
        print(f"---")
        print(f"Pablo")
        print(f"Maxi")
        print(f"...")
        return {'jugadores': [], 'fecha': None, 'hora': None, 'cancha': None}
    except Exception as e:
        print(f"❌ Error leyendo {archivo_txt}: {e}")
        return {'jugadores': [], 'fecha': None, 'hora': None, 'cancha': None}

if __name__ == '__main__':
    import sys
    
    print("📝 Leyendo confirmaciones desde archivo de texto...")
    
    # Leer todo desde archivo de texto
    datos = leer_jugadores_desde_txt()
    
    if not datos['jugadores']:
        print("❌ No hay jugadores para procesar")
        exit(1)
    
    # Usar fecha del archivo o parámetro de línea de comandos
    fecha_final = None
    if len(sys.argv) > 1:
        fecha_final = sys.argv[1]
        print(f"📅 Fecha desde parámetro: {fecha_final}")
    elif datos['fecha']:
        fecha_final = datos['fecha']
        print(f"📅 Fecha desde archivo: {fecha_final}")
    
    # Agregar confirmaciones con todos los datos
    agregar_confirmaciones(
        jugadores=datos['jugadores'], 
        fecha=fecha_final,
        fuente="Archivo TXT",
        hora=datos['hora'],
        cancha=datos['cancha']
    )
    
    print("\n💡 Ahora puedes:")
    print("   1. Ejecutar: python sorteo_posiciones_especificas.py")
    print("   2. Los títulos se actualizarán automáticamente")
    print("   3. Abrir tu sitio web para ver los cambios")
    
    print(f"\n✅ Información del partido procesada:")
    print(f"   📅 Fecha: {fecha_final or 'Fecha actual'}")
    print(f"   ⏰ Hora: {datos['hora'] or 'No especificada'}")
    print(f"   🏟️ Cancha: {datos['cancha'] or 'No especificada'}")
    print(f"   👥 Jugadores: {len(datos['jugadores'])}")
