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

if __name__ == '__main__':
    print("📝 Agregando confirmaciones para hoy...")
    
    # Lista de ejemplo (puedes modificar esta lista)
    jugadores_hoy = [
        "Carlos P",
        "Diego", 
        "Erik",
        "Francisco H",
        "Iván",
        "Luisito",
        "Marco",
        "Pancho",
        "Riky",
        "Willians",
        "Camilo",
        "Enrique",
        "Fabián",
        "Jaime"
    ]
    
    agregar_confirmaciones(jugadores_hoy, fuente="Script Local")
    
    print("\n💡 Ahora puedes:")
    print("   1. Abrir http://localhost:8080/estadisticas.html")
    print("   2. Ver que los jugadores se cargan automáticamente")
    print("   3. El sistema dirá 'confirmaciones automáticas (archivo)'")
