#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para agregar confirmaciones desde archivo TXT con fecha específica
"""

import sys
from datetime import datetime, timedelta
from agregar_confirmaciones import agregar_confirmaciones, leer_jugadores_desde_txt

def mostrar_ayuda():
    print("📝 Uso del script:")
    print("   python agregar_fecha_especifica.py [fecha] [archivo_jugadores]")
    print("")
    print("📅 Ejemplos de fecha:")
    print("   python agregar_fecha_especifica.py 2025-08-20")
    print("   python agregar_fecha_especifica.py hoy")
    print("   python agregar_fecha_especifica.py mañana")
    print("   python agregar_fecha_especifica.py +7  (en 7 días)")
    print("")
    print("📄 Archivo de jugadores (opcional):")
    print("   python agregar_fecha_especifica.py 2025-08-20 mi_lista.txt")
    print("   (por defecto usa jugadores_confirmados.txt)")

def parsear_fecha(fecha_str):
    """Convierte string de fecha a formato YYYY-MM-DD"""
    hoy = datetime.now()
    
    if fecha_str.lower() == 'hoy':
        return hoy.strftime('%Y-%m-%d')
    elif fecha_str.lower() == 'mañana':
        return (hoy + timedelta(days=1)).strftime('%Y-%m-%d')
    elif fecha_str.startswith('+'):
        try:
            dias = int(fecha_str[1:])
            return (hoy + timedelta(days=dias)).strftime('%Y-%m-%d')
        except ValueError:
            return None
    else:
        # Intentar parsear como fecha directa
        try:
            datetime.strptime(fecha_str, '%Y-%m-%d')
            return fecha_str
        except ValueError:
            return None

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("❌ Falta especificar la fecha")
        mostrar_ayuda()
        exit(1)
    
    fecha_str = sys.argv[1]
    archivo_jugadores = sys.argv[2] if len(sys.argv) > 2 else 'jugadores_confirmados.txt'
    
    if fecha_str in ['-h', '--help', 'help']:
        mostrar_ayuda()
        exit(0)
    
    fecha = parsear_fecha(fecha_str)
    if not fecha:
        print(f"❌ Formato de fecha inválido: {fecha_str}")
        mostrar_ayuda()
        exit(1)
    
    print(f"📅 Procesando confirmaciones para: {fecha}")
    print(f"📄 Leyendo jugadores desde: {archivo_jugadores}")
    
    jugadores = leer_jugadores_desde_txt(archivo_jugadores)
    
    if not jugadores:
        print("❌ No se pudieron cargar los jugadores")
        exit(1)
    
    agregar_confirmaciones(
        jugadores=jugadores,
        fecha=fecha,
        fuente=f"Archivo TXT ({archivo_jugadores})"
    )
    
    print(f"\n🚀 Listo! Confirmaciones agregadas para {fecha}")
    print("   Ahora puedes correr el sorteo con:")
    print("   python sorteo_posiciones_especificas.py")
