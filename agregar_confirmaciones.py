#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script simple para agregar confirmaciones al archivo local
Sin necesidad del servidor Flask
"""

import json
import os
from datetime import datetime

def agregar_confirmaciones(jugadores, fecha=None, fuente='Manual'):
    """Agrega confirmaciones al archivo local"""
    
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
    datos[fecha] = {
        'jugadores': jugadores,
        'timestamp': datetime.now().isoformat(),
        'fuentes': {jugador: fuente for jugador in jugadores}
    }
    
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
    print("📝 Agregando confirmaciones para hoy...")
    
    # Leer jugadores desde archivo de texto
    jugadores_hoy = leer_jugadores_desde_txt()
    
    if not jugadores_hoy:
        print("❌ No hay jugadores para procesar")
        exit(1)
    
    agregar_confirmaciones(jugadores_hoy, fuente="Archivo TXT")
    
    print("\n💡 Ahora puedes:")
    print("   1. Abrir http://localhost:8080/estadisticas.html")
    print("   2. Ver que los jugadores se cargan automáticamente")
    print("   3. El sistema dirá 'confirmaciones automáticas (archivo)'")
