#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Servidor de resultados mejorado para despliegue web
Compatible con hosting y servicios cloud
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import json
import os
from datetime import datetime
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Permitir requests desde cualquier origen

# Archivos de datos
HISTORIAL_FILE = 'historial_partidos.json'
EQUIPOS_FILE = 'equipos.json'

def cargar_historial():
    """Carga el historial de partidos"""
    if os.path.exists(HISTORIAL_FILE):
        try:
            with open(HISTORIAL_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            logger.error(f"Error cargando {HISTORIAL_FILE}")
            return []
    return []

def guardar_historial(historial):
    """Guarda el historial de partidos"""
    try:
        with open(HISTORIAL_FILE, 'w', encoding='utf-8') as f:
            json.dump(historial, f, indent=2, ensure_ascii=False)
        logger.info(f"Historial guardado: {len(historial)} partidos")
        return True
    except Exception as e:
        logger.error(f"Error guardando historial: {e}")
        return False

@app.route('/')
def home():
    """Página de inicio"""
    return jsonify({
        'status': 'online',
        'service': 'TalAganchester United - Servidor de Resultados',
        'version': '2.0',
        'endpoints': [
            'GET / - Estado del servidor',
            'POST /guardar-resultado - Guardar resultado de partido',
            'POST /guardar-historial-completo - Guardar historial completo',
            'GET /historial - Obtener historial de partidos',
            'GET /estadisticas - Obtener estadísticas generales'
        ]
    })

@app.route('/guardar-resultado', methods=['POST'])
def guardar_resultado():
    """Guarda un resultado de partido individual"""
    try:
        datos_partido = request.json
        
        if not datos_partido:
            return jsonify({'error': 'No se recibieron datos'}), 400
        
        # Agregar timestamp si no existe
        if 'timestamp' not in datos_partido:
            datos_partido['timestamp'] = datetime.now().isoformat()
        
        # Cargar historial actual
        historial = cargar_historial()
        
        # Agregar nuevo partido
        historial.append(datos_partido)
        
        # Guardar historial actualizado
        if guardar_historial(historial):
            logger.info(f"Partido guardado: {datos_partido.get('fecha', 'sin fecha')}")
            return jsonify({
                'success': True,
                'mensaje': 'Partido guardado exitosamente',
                'total_partidos': len(historial)
            })
        else:
            return jsonify({'error': 'Error guardando el partido'}), 500
            
    except Exception as e:
        logger.error(f"Error en guardar_resultado: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/guardar-historial-completo', methods=['POST'])
def guardar_historial_completo():
    """Reemplaza todo el historial"""
    try:
        nuevo_historial = request.json
        
        if not isinstance(nuevo_historial, list):
            return jsonify({'error': 'El historial debe ser una lista'}), 400
        
        logger.info(f"📥 Guardando historial completo: {len(nuevo_historial)} partidos")
        
        if guardar_historial(nuevo_historial):
            return jsonify({
                'success': True,
                'mensaje': 'Historial completo guardado',
                'total_partidos': len(nuevo_historial)
            })
        else:
            return jsonify({'error': 'Error guardando historial completo'}), 500
            
    except Exception as e:
        logger.error(f"Error en guardar_historial_completo: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/historial', methods=['GET'])
def obtener_historial():
    """Obtiene el historial completo de partidos"""
    try:
        historial = cargar_historial()
        return jsonify({
            'historial': historial,
            'total_partidos': len(historial),
            'ultima_actualizacion': datetime.now().isoformat()
        })
    except Exception as e:
        logger.error(f"Error obteniendo historial: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/estadisticas', methods=['GET'])
def obtener_estadisticas():
    """Obtiene estadísticas generales"""
    try:
        historial = cargar_historial()
        
        if not historial:
            return jsonify({
                'total_partidos': 0,
                'mensaje': 'No hay partidos registrados'
            })
        
        # Calcular estadísticas básicas
        total_partidos = len(historial)
        partidos_con_resultado = sum(1 for p in historial if 'equipo_ganador' in p)
        
        estadisticas = {
            'total_partidos': total_partidos,
            'partidos_con_resultado': partidos_con_resultado,
            'primer_partido': historial[0].get('fecha', 'N/A') if historial else None,
            'ultimo_partido': historial[-1].get('fecha', 'N/A') if historial else None,
            'generado_en': datetime.now().isoformat()
        }
        
        return jsonify(estadisticas)
        
    except Exception as e:
        logger.error(f"Error obteniendo estadísticas: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check para monitoreo"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'service': 'TalAganchester United API'
    })

# Servir archivos estáticos si es necesario
@app.route('/files/<path:filename>')
def serve_files(filename):
    """Servir archivos estáticos"""
    return send_from_directory('.', filename)

if __name__ == '__main__':
    # Configuración para desarrollo
    print("🚀 Servidor de resultados mejorado")
    print("=" * 40)
    print("📍 Modo: Desarrollo")
    print("🌐 Host: localhost")
    print("🔌 Puerto: 8083")
    print("📝 Endpoints disponibles:")
    print("   - POST /guardar-resultado")
    print("   - POST /guardar-historial-completo") 
    print("   - GET /historial")
    print("   - GET /estadisticas")
    print("   - GET /health")
    print("🛑 Presiona Ctrl+C para detener")
    print("=" * 40)
    
    # Ejecutar servidor
    app.run(
        host='0.0.0.0',  # Accesible desde cualquier IP
        port=int(os.environ.get('PORT', 8083)),  # Puerto configurable
        debug=True,  # Para desarrollo
        threaded=True  # Múltiples requests simultáneos
    )
