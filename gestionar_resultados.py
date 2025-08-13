#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para gestionar resultados de partidos
Permite agregar resultados y mantener las estadísticas actualizadas
"""

import json
import datetime
from pathlib import Path

def cargar_historial():
    """Cargar historial de partidos"""
    archivo = Path('historial_partidos.json')
    if archivo.exists():
        with open(archivo, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def guardar_historial(historial):
    """Guardar historial de partidos"""
    with open('historial_partidos.json', 'w', encoding='utf-8') as f:
        json.dump(historial, f, ensure_ascii=False, indent=2)

def obtener_equipos_actuales():
    """Obtener equipos del último sorteo"""
    try:
        with open('equipos.json', 'r', encoding='utf-8') as f:
            equipos = json.load(f)
            return equipos.get('rojo', []), equipos.get('negro', [])
    except:
        return [], []

def agregar_resultado():
    """Agregar resultado de partido interactivamente"""
    print("🏆 Agregar Resultado de Partido")
    print("=" * 40)
    
    # Obtener datos del partido
    fecha_str = input("Fecha del partido (YYYY-MM-DD) [hoy]: ").strip()
    if not fecha_str:
        fecha_str = datetime.date.today().isoformat()
    
    hora = input("Hora del partido [21:00]: ").strip() or "21:00"
    cancha = input("Cancha [Pasto Sintético]: ").strip() or "Pasto Sintético"
    
    # Resultado
    print("\nResultado del partido:")
    try:
        goles_rojo = int(input("🔴 Goles equipo rojo: "))
        goles_negro = int(input("⚫ Goles equipo negro: "))
    except ValueError:
        print("❌ Error: Ingresa números válidos")
        return
    
    mvp = input("🏆 MVP del partido (opcional): ").strip()
    
    try:
        asistencia = int(input("👥 Asistencia (número de personas) [12]: ") or "12")
    except ValueError:
        asistencia = 12
    
    # Obtener equipos del sorteo actual
    equipo_rojo, equipo_negro = obtener_equipos_actuales()
    
    # Formatear fecha
    fecha_obj = datetime.datetime.strptime(fecha_str, '%Y-%m-%d')
    dias = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
    meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 
             'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
    
    dia_semana = dias[fecha_obj.weekday()]
    mes_nombre = meses[fecha_obj.month - 1]
    fecha_formato = f"{dia_semana} {fecha_obj.day} de {mes_nombre}"
    
    # Crear registro del partido
    nuevo_partido = {
        "id": int(datetime.datetime.now().timestamp()),
        "fecha": fecha_str,
        "fecha_formato": fecha_formato,
        "hora": hora,
        "cancha": cancha,
        "equipo_rojo": equipo_rojo,
        "equipo_negro": equipo_negro,
        "resultado": {
            "rojo": goles_rojo,
            "negro": goles_negro
        },
        "goleadores": [],  # Se puede expandir para agregar goleadores específicos
        "mvp": mvp,
        "asistencias": asistencia,
        "estado": "finalizado"
    }
    
    # Mostrar resumen
    print(f"\n📋 Resumen del partido:")
    print(f"📅 {fecha_formato} - {hora} hrs")
    print(f"🏟️ {cancha}")
    print(f"🔴 Equipo Rojo: {goles_rojo}")
    print(f"⚫ Equipo Negro: {goles_negro}")
    if mvp:
        print(f"🏆 MVP: {mvp}")
    print(f"👥 Asistencia: {asistencia}")
    
    ganador = "🔴 Equipo Rojo" if goles_rojo > goles_negro else "⚫ Equipo Negro" if goles_negro > goles_rojo else "🤝 Empate"
    print(f"🏆 Resultado: {ganador}")
    
    # Confirmar
    confirmar = input("\n¿Guardar este resultado? (s/N): ").strip().lower()
    if confirmar in ['s', 'si', 'sí', 'y', 'yes']:
        historial = cargar_historial()
        historial.append(nuevo_partido)
        guardar_historial(historial)
        print("✅ Resultado guardado correctamente!")
        
        # Mostrar estadísticas actualizadas
        mostrar_estadisticas()
    else:
        print("❌ Resultado cancelado")

def mostrar_estadisticas():
    """Mostrar estadísticas generales"""
    historial = cargar_historial()
    partidos_finalizados = [p for p in historial if p.get('estado') == 'finalizado']
    
    if not partidos_finalizados:
        print("\n📊 No hay partidos finalizados aún")
        return
    
    total = len(partidos_finalizados)
    victorias_rojo = sum(1 for p in partidos_finalizados if p['resultado']['rojo'] > p['resultado']['negro'])
    victorias_negro = sum(1 for p in partidos_finalizados if p['resultado']['negro'] > p['resultado']['rojo'])
    empates = sum(1 for p in partidos_finalizados if p['resultado']['rojo'] == p['resultado']['negro'])
    
    print(f"\n📊 Estadísticas Generales:")
    print(f"🏆 Partidos jugados: {total}")
    print(f"🔴 Victorias Equipo Rojo: {victorias_rojo}")
    print(f"⚫ Victorias Equipo Negro: {victorias_negro}")
    print(f"🤝 Empates: {empates}")
    
    if total > 0:
        print(f"📈 Porcentaje Equipo Rojo: {victorias_rojo/total*100:.1f}%")
        print(f"📈 Porcentaje Equipo Negro: {victorias_negro/total*100:.1f}%")

def mostrar_historial():
    """Mostrar historial de partidos"""
    historial = cargar_historial()
    partidos_finalizados = [p for p in historial if p.get('estado') == 'finalizado']
    
    if not partidos_finalizados:
        print("\n📅 No hay partidos en el historial")
        return
    
    print(f"\n📅 Historial de Partidos ({len(partidos_finalizados)} partidos):")
    print("=" * 60)
    
    # Ordenar por fecha (más reciente primero)
    partidos_ordenados = sorted(partidos_finalizados, key=lambda x: x['fecha'], reverse=True)
    
    for partido in partidos_ordenados:
        resultado = f"{partido['resultado']['rojo']}-{partido['resultado']['negro']}"
        ganador = "🔴" if partido['resultado']['rojo'] > partido['resultado']['negro'] else "⚫" if partido['resultado']['negro'] > partido['resultado']['rojo'] else "🤝"
        
        print(f"{partido['fecha_formato']} | {resultado} {ganador}")
        if partido.get('mvp'):
            print(f"    🏆 MVP: {partido['mvp']}")
        print()

def menu_principal():
    """Menú principal del sistema"""
    while True:
        print("\n⚽ Sistema de Estadísticas - Talaganchester United")
        print("=" * 50)
        print("1. 📝 Agregar resultado de partido")
        print("2. 📊 Ver estadísticas generales")
        print("3. 📅 Ver historial de partidos")
        print("4. 🚪 Salir")
        
        opcion = input("\nSelecciona una opción: ").strip()
        
        if opcion == '1':
            agregar_resultado()
        elif opcion == '2':
            mostrar_estadisticas()
        elif opcion == '3':
            mostrar_historial()
        elif opcion == '4':
            print("👋 ¡Hasta luego!")
            break
        else:
            print("❌ Opción no válida")

if __name__ == "__main__":
    menu_principal()
