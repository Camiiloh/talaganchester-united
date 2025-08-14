#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ejemplo de integración con WhatsApp Bot para confirmaciones automáticas
Este es un ejemplo de cómo enviar confirmaciones al servidor
"""

import requests
import json
from datetime import datetime

# URL del servidor de confirmaciones
SERVIDOR_CONFIRMACIONES = 'http://localhost:5000'

def confirmar_jugador_individual(nombre, fecha=None, fuente='WhatsApp'):
    """
    Confirma un jugador individual
    """
    if not fecha:
        fecha = datetime.now().strftime('%Y-%m-%d')
    
    data = {
        'jugador': nombre,
        'fecha': fecha,
        'fuente': fuente
    }
    
    try:
        response = requests.post(f'{SERVIDOR_CONFIRMACIONES}/confirmar-jugador', json=data)
        return response.json()
    except Exception as e:
        return {'error': str(e)}

def confirmar_lista_completa(jugadores, fecha=None, fuente='WhatsApp'):
    """
    Confirma una lista completa de jugadores
    """
    if not fecha:
        fecha = datetime.now().strftime('%Y-%m-%d')
    
    data = {
        'jugadores': jugadores,
        'fecha': fecha,
        'fuente': fuente
    }
    
    try:
        response = requests.post(f'{SERVIDOR_CONFIRMACIONES}/confirmar-lista', json=data)
        return response.json()
    except Exception as e:
        return {'error': str(e)}

def obtener_lista_confirmados(fecha=None):
    """
    Obtiene la lista de jugadores confirmados para una fecha
    """
    if not fecha:
        fecha = datetime.now().strftime('%Y-%m-%d')
    
    try:
        response = requests.get(f'{SERVIDOR_CONFIRMACIONES}/lista-jugadores/{fecha}')
        return response.json()
    except Exception as e:
        return {'error': str(e)}

# Ejemplos de uso

if __name__ == '__main__':
    print("🤖 Ejemplos de integración con WhatsApp Bot")
    print("-" * 50)
    
    # Ejemplo 1: Confirmar jugador individual
    print("\n1️⃣ Confirmando jugador individual...")
    resultado = confirmar_jugador_individual("Carlos P", fuente="WhatsApp Bot")
    print(json.dumps(resultado, indent=2, ensure_ascii=False))
    
    # Ejemplo 2: Confirmar lista completa (como si fuera de un mensaje de WhatsApp)
    print("\n2️⃣ Confirmando lista completa...")
    jugadores_whatsapp = [
        "Carlos P",
        "Diego", 
        "Erik",
        "Francisco H",
        "Iván",
        "Luisito",
        "Marco",
        "Pancho",
        "Riky",
        "Willians"
    ]
    
    resultado = confirmar_lista_completa(jugadores_whatsapp, fuente="WhatsApp Grupo")
    print(json.dumps(resultado, indent=2, ensure_ascii=False))
    
    # Ejemplo 3: Consultar lista actual
    print("\n3️⃣ Consultando lista actual...")
    lista_actual = obtener_lista_confirmados()
    print(json.dumps(lista_actual, indent=2, ensure_ascii=False))
    
    print("\n" + "="*50)
    print("💡 Ejemplos de mensajes de WhatsApp que podrían procesarse:")
    print()
    print("Mensaje: 'Confirmado para mañana: Carlos, Diego, Erik'")
    print("   → Extraer nombres y llamar confirmar_lista_completa()")
    print()
    print("Mensaje: 'Yo me anoto - Francisco H'")
    print("   → Llamar confirmar_jugador_individual('Francisco H')")
    print()
    print("Mensaje: '¿Quién va hasta ahora?'")
    print("   → Llamar obtener_lista_confirmados() y responder")
