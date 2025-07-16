# Script para mostrar equipos y promedios según sorteo actual
import json

def normaliza(s):
    return s.lower().replace(" ", "")

with open('jugadores.json', 'r', encoding='utf-8') as f:
    jugadores_db = json.load(f)

confirmados = [
    "Camilo",
    "Cristobal",
    "Francisco",
    "Ivan",
    "Pancho",
    "Maxi Vargas",
    "Pablo",
    "Enrique",
    "Diego",
    "Marco",
    "Juan R",
    "Carlos P"
]

jugadores_partido = []
for n in confirmados:
    for j in jugadores_db:
        if normaliza(n) in normaliza(j["nombre"]):
            jugadores_partido.append(j)
            break

jugadores_ordenados = sorted(jugadores_partido, key=lambda x: x['puntaje'], reverse=True)
team1, team2 = [], []
sum1, sum2 = 0, 0
for j in jugadores_ordenados:
    if len(team1) < len(jugadores_partido)//2 and (sum1 <= sum2 or len(team2) >= len(jugadores_partido)//2):
        team1.append(j)
        sum1 += j['puntaje']
    else:
        team2.append(j)
        sum2 += j['puntaje']

prom1 = sum1 / len(team1) if team1 else 0
prom2 = sum2 / len(team2) if team2 else 0

print('Equipo Rojo:')
for j in team1:
    print(f"- {j['nombre']} ({j['puntaje']})")
print(f"Promedio Rojo: {prom1:.2f}\n")

print('Equipo Negro:')
for j in team2:
    print(f"- {j['nombre']} ({j['puntaje']})")
print(f"Promedio Negro: {prom2:.2f}")
