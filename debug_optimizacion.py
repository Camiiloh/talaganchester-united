#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Debug específico del sorteo de posiciones - DIAGNÓSTICO
"""

import json
import random
import itertools
from datetime import datetime

def cargar_jugadores(archivo='jugadores_posiciones_especificas.json'):
    """Carga la lista de jugadores con puntajes por posición específica."""
    try:
        with open(archivo, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"❌ Error: No se encontró el archivo {archivo}")
        return []

def jugadores_confirmados(todos_jugadores):
    """Filtra jugadores confirmados basado en confirmaciones_automaticas.json"""
    try:
        with open('confirmaciones_automaticas.json', 'r', encoding='utf-8') as f:
            confirmaciones = json.load(f)
        
        fecha_hoy = datetime.now().strftime('%Y-%m-%d')
        nombres_confirmados = confirmaciones[fecha_hoy]['jugadores']
        
        confirmados = []
        for nombre in nombres_confirmados:
            jugador = next((j for j in todos_jugadores if j['nombre'].lower() == nombre.lower()), None)
            if jugador:
                confirmados.append(jugador)
        
        return confirmados
        
    except Exception as e:
        print(f"❌ Error cargando confirmaciones: {e}")
        return []

def generar_formaciones_posibles():
    """Genera todas las formaciones posibles con 6 jugadores (1 GK + 5 de campo)"""
    formaciones = []
    
    # Todas las combinaciones que sumen 5 jugadores de campo
    for lcb in range(0, 3):
        for rcb in range(0, 3):
            for lm in range(0, 3):
                for cm in range(0, 3):
                    for rm in range(0, 3):
                        for cf in range(0, 3):
                            if lcb + rcb + lm + cm + rm + cf == 5:
                                # Debe tener al menos 1 defensa, 1 mediocampo y 1 delantero
                                total_defensas = lcb + rcb
                                total_mediocampos = lm + cm + rm
                                total_delanteros = cf
                                
                                if total_defensas >= 1 and total_mediocampos >= 1 and total_delanteros >= 1:
                                    formacion = {
                                        'LCB': lcb, 'RCB': rcb, 
                                        'LM': lm, 'CM': cm, 'RM': rm,
                                        'CF': cf
                                    }
                                    formaciones.append(formacion)
    
    return formaciones

def test_optimizacion(jugadores_equipo):
    """Test de optimización con debug detallado"""
    print(f"\n🔍 TESTING OPTIMIZACIÓN - {len(jugadores_equipo)} jugadores:")
    for i, j in enumerate(jugadores_equipo):
        print(f"   {i}: {j['nombre']} - Posiciones: {j['posicion']}")
    
    if len(jugadores_equipo) != 6:
        print(f"❌ ERROR: Se esperan 6 jugadores, recibidos {len(jugadores_equipo)}")
        return None, 0, []
    
    # El primer jugador debe ser el mejor arquero
    arquero = jugadores_equipo[0]
    jugadores_campo = jugadores_equipo[1:]
    
    print(f"\n🥅 Arquero asignado: {arquero['nombre']} (GK: {arquero['puntajes_posicion']['GK']})")
    print(f"⚽ Jugadores de campo: {[j['nombre'] for j in jugadores_campo]}")
    
    formaciones_posibles = generar_formaciones_posibles()
    print(f"📋 Formaciones posibles: {len(formaciones_posibles)}")
    
    mejor_formacion = None
    mejor_puntaje = -1
    mejor_asignacion = []
    
    # Probar solo las primeras 5 formaciones para debug
    for i, formacion in enumerate(formaciones_posibles[:5]):
        print(f"\n📝 Probando formación {i+1}: {formacion}")
        
        try:
            puntaje, asignacion = asignar_flexible_debug(jugadores_campo, formacion)
            print(f"   ✅ Puntaje obtenido: {puntaje}")
            print(f"   👥 Asignación: {[(a[0], a[1]) for a in asignacion]}")
            
            if puntaje > mejor_puntaje:
                mejor_puntaje = puntaje
                mejor_formacion = formacion
                mejor_asignacion = asignacion
                print(f"   🎯 ¡Nueva mejor formación!")
        except Exception as e:
            print(f"   ❌ Error en formación {i+1}: {e}")
    
    print(f"\n🏆 MEJOR RESULTADO:")
    print(f"   Formación: {mejor_formacion}")
    print(f"   Puntaje: {mejor_puntaje}")
    print(f"   Asignación: {mejor_asignacion}")
    
    return mejor_formacion, mejor_puntaje, mejor_asignacion

def asignar_flexible_debug(jugadores_campo, formacion):
    """Asigna jugadores a posiciones con debug detallado"""
    print(f"      🔧 Asignando {len(jugadores_campo)} jugadores a formación {formacion}")
    
    posiciones_necesarias = []
    for posicion, cantidad in formacion.items():
        for _ in range(cantidad):
            posiciones_necesarias.append(posicion)
    
    print(f"      📍 Posiciones necesarias: {posiciones_necesarias}")
    
    if len(posiciones_necesarias) != len(jugadores_campo):
        raise Exception(f"Mismatch: {len(posiciones_necesarias)} posiciones vs {len(jugadores_campo)} jugadores")
    
    # Asignación simple: mejores puntajes posibles
    mejor_puntaje = 0
    mejor_asignacion = []
    
    # Probar solo las primeras 10 permutaciones para debug
    permutaciones = list(itertools.permutations(jugadores_campo))
    print(f"      🔀 Probando {min(10, len(permutaciones))} permutaciones de {len(permutaciones)} totales")
    
    for i, permutacion in enumerate(permutaciones[:10]):
        puntaje_total = 0
        asignacion_temp = []
        
        for j, jugador in enumerate(permutacion):
            posicion = posiciones_necesarias[j]
            puntaje = jugador['puntajes_posicion'][posicion]
            puntaje_total += puntaje
            asignacion_temp.append((jugador['nombre'], posicion, puntaje))
        
        if puntaje_total > mejor_puntaje:
            mejor_puntaje = puntaje_total
            mejor_asignacion = asignacion_temp
    
    print(f"      ✅ Mejor puntaje encontrado: {mejor_puntaje}")
    return mejor_puntaje, mejor_asignacion

def main():
    print("🔍 DIAGNÓSTICO DEL SORTEO DE POSICIONES ESPECÍFICAS")
    print("=" * 60)
    
    # Cargar jugadores
    jugadores = cargar_jugadores()
    if not jugadores:
        print("❌ No se pudieron cargar jugadores")
        return
    
    # Filtrar confirmados
    confirmados = jugadores_confirmados(jugadores)
    if len(confirmados) < 12:
        print(f"❌ Insuficientes jugadores confirmados: {len(confirmados)}")
        return
    
    print(f"✅ {len(confirmados)} jugadores confirmados cargados")
    
    # Separar arqueros
    arqueros = [j for j in confirmados if 'GK' in j['posicion']]
    print(f"🥅 Arqueros disponibles: {[a['nombre'] for a in arqueros]}")
    
    if len(arqueros) < 2:
        print(f"❌ Insuficientes arqueros: {len(arqueros)}")
        return
    
    # Crear un equipo de prueba
    random.shuffle(confirmados)
    mitad = len(confirmados) // 2
    equipo_test = confirmados[:mitad]
    
    # Asegurar que tenga un arquero
    if not any('GK' in j['posicion'] for j in equipo_test):
        # Intercambiar un jugador por un arquero
        for i, j in enumerate(equipo_test):
            if 'GK' not in j['posicion']:
                equipo_test[i] = arqueros[0]
                break
    
    # Mover arquero al inicio
    arquero_en_equipo = next(j for j in equipo_test if 'GK' in j['posicion'])
    equipo_test = [arquero_en_equipo] + [j for j in equipo_test if j != arquero_en_equipo]
    
    # Asegurar que tenga exactamente 6 jugadores
    equipo_test = equipo_test[:6]
    
    print(f"\n🧪 EQUIPO DE PRUEBA ({len(equipo_test)} jugadores):")
    for i, j in enumerate(equipo_test):
        print(f"   {i+1}: {j['nombre']} - {j['posicion']}")
    
    # Test de optimización
    resultado = test_optimizacion(equipo_test)
    
    if resultado[0] is None:
        print(f"\n❌ LA OPTIMIZACIÓN FALLÓ")
        print("Esto explica por qué el sorteo completo no funciona")
    else:
        print(f"\n✅ LA OPTIMIZACIÓN FUNCIONÓ")
        print("El problema debe estar en otra parte del algoritmo")

if __name__ == "__main__":
    main()
