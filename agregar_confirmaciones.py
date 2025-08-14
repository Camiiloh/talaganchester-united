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
    """Lee la lista de jugadores desde un archivo de texto"""
    try:
        with open(archivo_txt, 'r', encoding='utf-8') as f:
            jugadores = [linea.strip() for linea in f.readlines() if linea.strip()]
        print(f"📄 Jugadores leídos desde {archivo_txt}: {len(jugadores)}")
        return jugadores
    except FileNotFoundError:
        print(f"❌ No se encontró el archivo {archivo_txt}")
        print(f"💡 Crea el archivo con un jugador por línea")
        return []
    except Exception as e:
        print(f"❌ Error leyendo {archivo_txt}: {e}")
        return []

if __name__ == '__main__':
    import sys
    
    print("📝 Agregando confirmaciones para hoy...")
    
    # Leer jugadores desde archivo de texto
    jugadores_hoy = leer_jugadores_desde_txt()
    
    if not jugadores_hoy:
        print("❌ No hay jugadores para procesar")
        exit(1)
    
    # Parámetros opcionales desde línea de comandos
    # Uso: python agregar_confirmaciones.py [hora] [cancha]
    # Ejemplo: python agregar_confirmaciones.py "21:00" "2"
    
    hora = None
    cancha = None
    
    if len(sys.argv) > 1:
        hora = sys.argv[1]
        print(f"⏰ Hora del partido: {hora}")
    
    if len(sys.argv) > 2:
        cancha = sys.argv[2]
        print(f"🏟️ Cancha: {cancha}")
    
    # Agregar confirmaciones con datos del partido
    agregar_confirmaciones(jugadores_hoy, fuente="Archivo TXT", hora=hora, cancha=cancha)
    
    print("\n💡 Ahora puedes:")
    print("   1. Ejecutar: python sorteo_posiciones_especificas.py")
    print("   2. Los títulos se actualizarán automáticamente con fecha, hora y cancha")
    print("   3. Abrir tu sitio web para ver los cambios")
    
    if hora or cancha:
        print(f"\n✅ Información del partido actualizada:")
        print(f"   📅 Fecha: {datetime.now().strftime('%Y-%m-%d')}")
        if hora:
            print(f"   ⏰ Hora: {hora}")
        if cancha:
            print(f"   🏟️ Cancha: {cancha}")
