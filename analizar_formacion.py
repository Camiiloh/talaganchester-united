#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Analizador de valoración de formaciones por equipo
Basado en la imagen de formación proporcionada
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
    for jugador in jugadores:
        if jugador['nombre'].lower() == nombre.lower():
            return jugador
    return None

def calcular_rating_equipo(formacion_equipo, jugadores_data):
    """Calcula el rating promedio de un equipo en sus posiciones específicas"""
    total_rating = 0
    total_jugadores = 0
    detalles = []
    
    for posicion, nombre in formacion_equipo.items():
        jugador = encontrar_jugador(nombre, jugadores_data)
        if jugador:
            # Obtener rating especifico para la posicion
            rating_posicion = jugador['puntajes_posicion'].get(posicion, jugador['puntaje'])
            total_rating += rating_posicion
            total_jugadores += 1
            detalles.append({
                'nombre': nombre,
                'posicion': posicion,
                'rating': round(rating_posicion, 1)
            })
        else:
            print(f"WARNING: Jugador '{nombre}' no encontrado en la base de datos")
    
    promedio = total_rating / total_jugadores if total_jugadores > 0 else 0
    return promedio, detalles

def main():
    print("ANALISIS DE VALORACION DE FORMACION")
    print("=" * 50)
    
    # Cargar datos de jugadores
    jugadores = cargar_jugadores()
    if not jugadores:
        return
    
    # Basado en la imagen proporcionada, interpreto la formacion:
    # Equipo superior (parece ser formacion defensiva)
    equipo_1 = {
        'GK': 'Camilo',  # Portero en el area superior
        'LCB': 'Jaime',  # Defensa central izquierdo
        'RCB': 'Maxi',   # Defensa central derecho  
        'LM': 'Carlos P', # Lateral/Medio izquierdo
        'CM': 'Willians', # Medio centro
        'RM': 'Enrique'   # Lateral/Medio derecho
    }
    
    # Equipo inferior 
    equipo_2 = {
        'LM': 'Marco',    # Medio izquierdo
        'CM': 'Turra',    # Medio centro
        'RM': 'Francisco H', # Medio derecho
        'CF': 'Diego',    # Delantero centro
        'GK': 'Willians'  # Portero (en la imagen parece haber dos porteros)
    }
    
    print("EQUIPO 1 (Superior):")
    rating_1, detalles_1 = calcular_rating_equipo(equipo_1, jugadores)
    for detalle in detalles_1:
        print(f"  {detalle['posicion']}: {detalle['nombre']} ({detalle['rating']})")
    print(f"  RATING PROMEDIO: {rating_1:.1f}")
    
    print("\nEQUIPO 2 (Inferior):")
    rating_2, detalles_2 = calcular_rating_equipo(equipo_2, jugadores)
    for detalle in detalles_2:
        print(f"  {detalle['posicion']}: {detalle['nombre']} ({detalle['rating']})")
    print(f"  RATING PROMEDIO: {rating_2:.1f}")
    
    print("\n" + "=" * 50)
    print("COMPARACION:")
    diferencia = abs(rating_1 - rating_2)
    if rating_1 > rating_2:
        print(f"Equipo 1 es mas fuerte por {diferencia:.1f} puntos")
    elif rating_2 > rating_1:
        print(f"Equipo 2 es mas fuerte por {diferencia:.1f} puntos")
    else:
        print("Los equipos estan equilibrados")
    
    print(f"Diferencia: {diferencia:.1f} puntos")
    
    # Recomendaciones
    print("\nANALISIS:")
    if diferencia < 0.5:
        print("Formacion muy equilibrada - Partido competitivo esperado")
    elif diferencia < 1.0:
        print("Formacion equilibrada - Ligera ventaja para un equipo")
    elif diferencia < 1.5:
        print("Desequilibrio notable - Considerar ajustes")
    else:
        print("Desequilibrio significativo - Se recomienda reorganizar")

if __name__ == "__main__":
    main()
