#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Endpoint para recibir confirmaciones automáticas de jugadores
Permite integración con bots de WhatsApp, Telegram, etc.
"""

import json
import os
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Permitir solicitudes desde el frontend

# Archivo donde se guardan las confirmaciones
CONFIRMACIONES_FILE = 'confirmaciones_automaticas.json'

def cargar_confirmaciones():
    """Carga las confirmaciones desde el archivo JSON"""
    if os.path.exists(CONFIRMACIONES_FILE):
        try:
            with open(CONFIRMACIONES_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    return {}

def guardar_confirmaciones(confirmaciones):
    """Guarda las confirmaciones en el archivo JSON"""
    with open(CONFIRMACIONES_FILE, 'w', encoding='utf-8') as f:
        json.dump(confirmaciones, f, indent=2, ensure_ascii=False)

@app.route('/confirmar-jugador', methods=['POST'])
def confirmar_jugador():
    """
    Endpoint para confirmar un jugador
    Formato: {"jugador": "Nombre", "fecha": "2025-08-14", "fuente": "WhatsApp"}
    """
    try:
        data = request.json
        jugador = data.get('jugador', '').strip()
        fecha = data.get('fecha', datetime.now().strftime('%Y-%m-%d'))
        fuente = data.get('fuente', 'Manual')
        
        if not jugador:
            return jsonify({'error': 'Nombre de jugador requerido'}), 400
        
        # Cargar confirmaciones actuales
        confirmaciones = cargar_confirmaciones()
        
        # Crear entrada para la fecha si no existe
        if fecha not in confirmaciones:
            confirmaciones[fecha] = {
                'jugadores': [],
                'timestamp': datetime.now().isoformat(),
                'fuentes': {}
            }
        
        # Agregar jugador si no está ya confirmado
        if jugador not in confirmaciones[fecha]['jugadores']:
            confirmaciones[fecha]['jugadores'].append(jugador)
            confirmaciones[fecha]['fuentes'][jugador] = fuente
            confirmaciones[fecha]['timestamp'] = datetime.now().isoformat()
            
            # Guardar cambios
            guardar_confirmaciones(confirmaciones)
            
            return jsonify({
                'success': True,
                'mensaje': f'Jugador {jugador} confirmado para {fecha}',
                'total_confirmados': len(confirmaciones[fecha]['jugadores'])
            })
        else:
            return jsonify({
                'success': False,
                'mensaje': f'Jugador {jugador} ya estaba confirmado para {fecha}'
            })
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/lista-jugadores/<fecha>', methods=['GET'])
def obtener_lista_jugadores(fecha):
    """
    Obtiene la lista de jugadores confirmados para una fecha
    """
    try:
        confirmaciones = cargar_confirmaciones()
        
        if fecha in confirmaciones:
            return jsonify({
                'fecha': fecha,
                'jugadores': confirmaciones[fecha]['jugadores'],
                'total': len(confirmaciones[fecha]['jugadores']),
                'timestamp': confirmaciones[fecha]['timestamp']
            })
        else:
            return jsonify({
                'fecha': fecha,
                'jugadores': [],
                'total': 0,
                'timestamp': None
            })
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/confirmar-lista', methods=['POST'])
def confirmar_lista_completa():
    """
    Confirma una lista completa de jugadores
    Formato: {"jugadores": ["Nombre1", "Nombre2"], "fecha": "2025-08-14", "fuente": "WhatsApp"}
    """
    try:
        data = request.json
        jugadores = data.get('jugadores', [])
        fecha = data.get('fecha', datetime.now().strftime('%Y-%m-%d'))
        fuente = data.get('fuente', 'Manual')
        
        if not jugadores:
            return jsonify({'error': 'Lista de jugadores requerida'}), 400
        
        # Cargar confirmaciones actuales
        confirmaciones = cargar_confirmaciones()
        
        # Sobrescribir lista completa para la fecha
        confirmaciones[fecha] = {
            'jugadores': jugadores,
            'timestamp': datetime.now().isoformat(),
            'fuentes': {jugador: fuente for jugador in jugadores}
        }
        
        # Guardar cambios
        guardar_confirmaciones(confirmaciones)
        
        return jsonify({
            'success': True,
            'mensaje': f'Lista completa actualizada para {fecha}',
            'total_confirmados': len(jugadores),
            'jugadores': jugadores
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/estado', methods=['GET'])
def estado_servidor():
    """Estado del servidor de confirmaciones"""
    return jsonify({
        'status': 'activo',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0'
    })

if __name__ == '__main__':
    print("🤖 Servidor de confirmaciones automáticas iniciado")
    print("📝 Endpoints disponibles:")
    print("   - POST /confirmar-jugador")
    print("   - POST /confirmar-lista") 
    print("   - GET /lista-jugadores/<fecha>")
    print("   - GET /estado")
    print("🌐 Ejecutándose en http://localhost:5000")
    print("🛑 Presiona Ctrl+C para detener")
    
    app.run(host='localhost', port=5000, debug=True)
