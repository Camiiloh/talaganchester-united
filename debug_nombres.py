#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json

# Cargar jugadores
with open('jugadores_posiciones_especificas.json', 'r', encoding='utf-8') as f:
    jugadores = json.load(f)

print("Jugadores en JSON:")
for j in jugadores:
    print(f"  - {repr(j['nombre'])}")

print("\n" + "="*50)

# Cargar confirmados
with open('confirmados.txt', 'r', encoding='utf-8') as f:
    confirmados = [line.strip() for line in f if line.strip()]

print("Jugadores confirmados:")
for c in confirmados:
    print(f"  - {repr(c)}")

print("\n" + "="*50)

print("Búsqueda:")
for nombre_conf in confirmados:
    encontrado = any(j['nombre'].lower() == nombre_conf.lower() for j in jugadores)
    print(f"  {nombre_conf}: {'✅' if encontrado else '❌'}")
