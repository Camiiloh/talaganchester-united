#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Calculador de valoración para formaciones específicas
"""

import json

def cargar_jugadores():
    """Carga los datos de jugadores con sus posiciones y puntajes"""
    try:
        with open('jugadores_posiciones_especificas.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print("No se encontro el archivo jugadores_posiciones_especificas.json")
        return []

def encontrar_jugador(nombre, jugadores):
    """Encuentra un jugador por nombre"""
    # Normalizar nombres para búsqueda
    nombre_normalizado = nombre.lower().strip()
    
    for jugador in jugadores:
        jugador_nombre = jugador['nombre'].lower().strip()
        
        # Búsqueda exacta
        if jugador_nombre == nombre_normalizado:
            return jugador
        
        # Búsqueda parcial para nombres como "Carlos P"
        if "carlos p" in nombre_normalizado and "carlos p" in jugador_nombre:
            return jugador
        if "francisco h" in nombre_normalizado and "francisco h" in jugador_nombre:
            return jugador
        if nombre_normalizado in jugador_nombre or jugador_nombre in nombre_normalizado:
            return jugador
    
    return None

def calcular_rating_equipo(formacion_equipo, jugadores_data, nombre_equipo):
    """Calcula el rating promedio de un equipo en sus posiciones específicas"""
    total_rating = 0
    total_jugadores = 0
    detalles = []
    
    print(f"\n{nombre_equipo}:")
    print("-" * 30)
    
    for posicion, nombre in formacion_equipo.items():
        jugador = encontrar_jugador(nombre, jugadores_data)
        if jugador:
            # Obtener rating específico para la posición
            rating_posicion = jugador['puntajes_posicion'].get(posicion, jugador['puntaje'])
            total_rating += rating_posicion
            total_jugadores += 1
            detalles.append({
                'nombre': nombre,
                'posicion': posicion,
                'rating': round(rating_posicion, 1)
            })
            print(f"  {posicion}: {nombre} - {rating_posicion:.1f}")
        else:
            print(f"  WARNING: Jugador '{nombre}' no encontrado")
    
    promedio = total_rating / total_jugadores if total_jugadores > 0 else 0
    print(f"\n  RATING PROMEDIO: {promedio:.1f}")
    
    return promedio, detalles

def main():
    print("CALCULO DE VALORACION - FORMACIONES ESPECIFICAS")
    print("=" * 60)
    
    # Cargar datos de jugadores
    jugadores = cargar_jugadores()
    if not jugadores:
        return
    
    # Formaciones proporcionadas por el usuario
    equipo_negro = {
        'GK': 'Nel',
        'RCB': 'Enrique',
        'LM': 'Turra',
        'RM': 'Willians',
        'CF': 'Camilo',  # Primer delantero
        'CF2': 'Jaime'   # Segundo delantero
    }
    
    equipo_rojo = {
        'GK': 'Maxi',
        'RCB': 'Marco',
        'LM': 'Carlos P',
        'RM': 'Francisco H',
        'CF': 'Fabián',  # Primer delantero
        'CF2': 'Diego'   # Segundo delantero
    }
    
    # Calcular ratings
    rating_negro, detalles_negro = calcular_rating_equipo(equipo_negro, jugadores, "EQUIPO NEGRO")
    rating_rojo, detalles_rojo = calcular_rating_equipo(equipo_rojo, jugadores, "EQUIPO ROJO")
    
    print("\n" + "=" * 60)
    print("RESUMEN COMPARATIVO:")
    print("=" * 60)
    print(f"Equipo Negro: {rating_negro:.1f}")
    print(f"Equipo Rojo:  {rating_rojo:.1f}")
    
    diferencia = abs(rating_negro - rating_rojo)
    print(f"\nDiferencia: {diferencia:.1f} puntos")
    
    if rating_negro > rating_rojo:
        print(f">>> El EQUIPO NEGRO es mas fuerte por {diferencia:.1f} puntos")
    elif rating_rojo > rating_negro:
        print(f">>> El EQUIPO ROJO es mas fuerte por {diferencia:.1f} puntos")
    else:
        print(">>> Los equipos estan perfectamente equilibrados")
    
    # Análisis de equilibrio
    print(f"\nANALISIS DE EQUILIBRIO:")
    if diferencia < 0.3:
        print("Excelente equilibrio - Partido muy competitivo")
    elif diferencia < 0.7:
        print("Buen equilibrio - Ligera ventaja para un equipo")
    elif diferencia < 1.2:
        print("Desequilibrio moderado - Diferencia notable")
    else:
        print("Desequilibrio significativo - Considerar ajustes")

if __name__ == "__main__":
    main()
