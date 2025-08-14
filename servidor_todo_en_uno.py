#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Servidor todo-en-uno para despliegue web
Sirve archivos estáticos Y maneja la API de resultados
"""

from flask import Flask, request, jsonify, send_from_directory, send_file
from flask_cors import CORS
import json
import os
from datetime import datetime
import logging
from pathlib import Path

# Importar el gestor de base de datos
try:
    from database_manager import db_manager
    DB_AVAILABLE = True
except ImportError:
    print("⚠️  database_manager no disponible, usando modo JSON")
    DB_AVAILABLE = False

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Archivos de datos
HISTORIAL_FILE = 'historial_partidos.json'

def cargar_historial():
    """Carga el historial de partidos"""
    if DB_AVAILABLE:
        return db_manager.get_historial_partidos()
    
    # Fallback a archivo JSON
    if os.path.exists(HISTORIAL_FILE):
        try:
            with open(HISTORIAL_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    return []

def guardar_historial(historial):
    """Guarda el historial de partidos"""
    if DB_AVAILABLE:
        # Con la nueva arquitectura, guardamos partido por partido
        return True  # Se maneja individualmente en save_partido
    
    # Fallback a archivo JSON
    try:
        with open(HISTORIAL_FILE, 'w', encoding='utf-8') as f:
            json.dump(historial, f, indent=2, ensure_ascii=False)
        return True
    except:
        return False

def guardar_partido(partido):
    """Guarda un partido individual"""
    if DB_AVAILABLE:
        return db_manager.save_partido(partido)
    
    # Fallback: usar método antiguo
    historial = cargar_historial()
    
    # Buscar si ya existe
    for i, p in enumerate(historial):
        if p['id'] == partido['id']:
            historial[i] = partido
            break
    else:
        historial.append(partido)
    
    return guardar_historial(historial)

# ===== API ENDPOINTS =====

@app.route('/api/guardar-resultado', methods=['POST'])
def guardar_resultado():
    """API: Guarda resultado de partido"""
    try:
        datos_partido = request.json
        if not datos_partido:
            return jsonify({'error': 'No se recibieron datos'}), 400
        
        datos_partido['timestamp'] = datetime.now().isoformat()
        
        if guardar_partido(datos_partido):
            return jsonify({'success': True, 'mensaje': 'Partido guardado'})
        else:
            return jsonify({'error': 'Error guardando'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/guardar-historial-completo', methods=['POST'])
def guardar_historial_completo():
    """API: Guarda historial completo"""
    try:
        nuevo_historial = request.json
        if not isinstance(nuevo_historial, list):
            return jsonify({'error': 'Debe ser una lista'}), 400
        
        if DB_AVAILABLE:
            # Guardar cada partido individualmente en la base de datos
            count = 0
            for partido in nuevo_historial:
                if db_manager.save_partido(partido):
                    count += 1
            return jsonify({'success': True, 'total': count})
        else:
            # Método antiguo
            if guardar_historial(nuevo_historial):
                return jsonify({'success': True, 'total': len(nuevo_historial)})
            else:
                return jsonify({'error': 'Error guardando'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/historial', methods=['GET'])
def obtener_historial():
    """API: Obtiene historial"""
    historial = cargar_historial()
    return jsonify(historial)  # Devolver directamente el array

@app.route('/api/health', methods=['GET'])
def health():
    """API: Health check"""
    return jsonify({'status': 'ok', 'timestamp': datetime.now().isoformat()})

# ===== SERVIR ARCHIVOS ESTÁTICOS =====

@app.route('/')
def index():
    """Página principal"""
    return send_file('index.html')

@app.route('/estadisticas.html')
def estadisticas():
    """Página de estadísticas"""
    return send_file('estadisticas.html')

@app.route('/cancha-v2.html')
def cancha_v2():
    """Página de cancha v2"""
    return send_file('cancha-v2.html')

@app.route('/cancha.html')
def cancha():
    """Página de cancha original"""
    return send_file('cancha.html')

@app.route('/<path:filename>')
def serve_static(filename):
    """Servir archivos estáticos"""
    try:
        return send_from_directory('.', filename)
    except:
        return "Archivo no encontrado", 404

if __name__ == '__main__':
    # Ejecutar migración automática en Railway
    if os.environ.get('DATABASE_URL'):
        print("🔄 Ejecutando migración automática de datos...")
        try:
            from migrar_datos import migrar_datos_a_postgres
            migrar_datos_a_postgres()
        except Exception as e:
            print(f"⚠️  Error en migración automática: {e}")
    
    port = int(os.environ.get('PORT', 8080))
    
    print("🚀 SERVIDOR TODO-EN-UNO - TALAGANCHESTER UNITED")
    print("=" * 50)
    print(f"🌐 Puerto: {port}")
    print("📍 URLs:")
    print(f"   • Principal: http://localhost:{port}")
    print(f"   • Estadísticas: http://localhost:{port}/estadisticas.html")
    print(f"   • Cancha v2: http://localhost:{port}/cancha-v2.html")
    print("📡 API:")
    print(f"   • POST /api/guardar-resultado")
    print(f"   • GET /api/historial")
    print("🛑 Ctrl+C para detener")
    print("=" * 50)
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=False,  # Producción
        threaded=True
    )
