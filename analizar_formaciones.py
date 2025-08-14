#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para analizar la diversidad de formaciones posibles
"""

import json
import itertools
from sorteo_posiciones_especificas import (
    cargar_jugadores, jugadores_confirmados, generar_formaciones_posibles,
    optimizar_posiciones_equipo, puede_jugar_posicion
)

def analizar_formaciones():
    """Analiza todas las formaciones posibles y sus puntajes"""
    
    # Cargar datos
    todos_jugadores = cargar_jugadores()
    confirmados = jugadores_confirmados(todos_jugadores)
    
    if len(confirmados) < 12:
        print(f"❌ Solo {len(confirmados)} jugadores confirmados, necesitamos al menos 12")
        return
    
    jugadores_campo = 5  # Para equipos de 6
    formaciones = generar_formaciones_posibles(jugadores_campo)
    
    print(f"📊 Analizando {len(formaciones)} formaciones posibles...")
    print(f"👥 Con {len(confirmados)} jugadores confirmados")
    
    # Dividir jugadores en dos equipos de ejemplo
    equipo1 = confirmados[:6]
    equipo2 = confirmados[6:12]
    
    print(f"\n🔴 Equipo 1: {[j['nombre'] for j in equipo1]}")
    print(f"⚫ Equipo 2: {[j['nombre'] for j in equipo2]}")
    
    # Analizar cada equipo con todas las formaciones
    print(f"\n📈 Análisis Equipo 1:")
    analizar_equipo_con_formaciones(equipo1, formaciones)
    
    print(f"\n📈 Análisis Equipo 2:")
    analizar_equipo_con_formaciones(equipo2, formaciones)

def analizar_equipo_con_formaciones(equipo, formaciones):
    """Analiza un equipo con todas las formaciones posibles"""
    
    resultados = []
    
    for i, formacion in enumerate(formaciones):
        formacion_obj, puntaje, asignacion = optimizar_posiciones_equipo(equipo)
        
        if formacion_obj:
            defensas = formacion_obj['LCB'] + formacion_obj['RCB']
            mediocampos = formacion_obj['LM'] + formacion_obj['CM'] + formacion_obj['RM']
            delanteros = formacion_obj['CF']
            formato = f"1-{defensas}-{mediocampos}-{delanteros}"
            
            resultados.append({
                'formacion': formato,
                'puntaje': puntaje,
                'formacion_dict': formacion_obj
            })
    
    # Mostrar resultados únicos ordenados por puntaje
    resultados_unicos = {}
    for r in resultados:
        key = r['formacion']
        if key not in resultados_unicos or r['puntaje'] > resultados_unicos[key]['puntaje']:
            resultados_unicos[key] = r
    
    resultados_ordenados = sorted(resultados_unicos.values(), key=lambda x: x['puntaje'], reverse=True)
    
    print(f"   Formaciones encontradas: {len(resultados_unicos)}")
    for i, r in enumerate(resultados_ordenados[:5]):  # Top 5
        print(f"   {i+1}. {r['formacion']} - Puntaje: {r['puntaje']:.2f}")

def analizar_diversidad_equipos():
    """Analiza la diversidad de equipos posibles con los jugadores actuales"""
    
    todos_jugadores = cargar_jugadores()
    confirmados = jugadores_confirmados(todos_jugadores)
    
    if len(confirmados) < 12:
        print(f"❌ Solo {len(confirmados)} jugadores confirmados")
        return
    
    print(f"\n🎲 Analizando diversidad de equipos...")
    
    # Generar varias divisiones aleatorias diferentes
    import random
    formaciones_encontradas = set()
    
    for _ in range(100):  # 100 divisiones aleatorias
        random.shuffle(confirmados)
        equipo1 = confirmados[:6]
        equipo2 = confirmados[6:12]
        
        # Optimizar cada equipo
        form1, puntaje1, _ = optimizar_posiciones_equipo(equipo1)
        form2, puntaje2, _ = optimizar_posiciones_equipo(equipo2)
        
        if form1 and form2:
            def formato_formacion(f):
                defensas = f['LCB'] + f['RCB']
                mediocampos = f['LM'] + f['CM'] + f['RM']
                delanteros = f['CF']
                return f"1-{defensas}-{mediocampos}-{delanteros}"
            
            formacion1_str = formato_formacion(form1)
            formacion2_str = formato_formacion(form2)
            
            formaciones_encontradas.add(f"{formacion1_str} vs {formacion2_str}")
    
    print(f"   Combinaciones de formaciones encontradas: {len(formaciones_encontradas)}")
    for i, combo in enumerate(sorted(formaciones_encontradas)[:10]):
        print(f"   {i+1}. {combo}")

if __name__ == '__main__':
    analizar_formaciones()
    analizar_diversidad_equipos()
