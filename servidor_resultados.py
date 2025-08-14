#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Servidor simple para manejar guardado de resultados desde la interfaz web
"""

import http.server
import socketserver
import json
import urllib.parse
from pathlib import Path
import subprocess
import sys

class ResultadosHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/guardar-resultado':
            try:
                # Leer datos del POST
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                datos_partido = json.loads(post_data.decode('utf-8'))
                
                print(f"📥 Datos recibidos: {datos_partido}")
                
                # Llamar al script de guardado
                datos_json = json.dumps(datos_partido, ensure_ascii=False)
                print(f"🔄 Ejecutando script de guardado...")
                
                resultado = subprocess.run([
                    sys.executable, 'guardar_resultado_web.py', datos_json
                ], capture_output=True, text=True, cwd='.')
                
                print(f"📤 Código de salida: {resultado.returncode}")
                print(f"📝 Salida estándar: {resultado.stdout}")
                print(f"❌ Errores: {resultado.stderr}")
                
                if resultado.returncode == 0:
                    # Respuesta exitosa
                    response = {"status": "success", "message": "Resultado guardado correctamente"}
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
                    print("✅ Respuesta enviada exitosamente")
                else:
                    # Error al guardar
                    response = {"status": "error", "message": f"Error al guardar: {resultado.stderr}"}
                    self.send_response(500)
                    self.send_header('Content-Type', 'application/json')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
                    print(f"❌ Error enviado: {response}")
                    
            except Exception as e:
                print(f"💥 Excepción en el servidor: {str(e)}")
                response = {"status": "error", "message": f"Error del servidor: {str(e)}"}
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
        
        elif self.path == '/guardar-historial-completo':
            try:
                # Leer datos del POST
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                datos = json.loads(post_data.decode('utf-8'))
                
                print(f"📥 Guardando historial completo: {len(datos['historial'])} partidos")
                
                # Guardar directamente en el archivo JSON
                historial_path = Path('historial_partidos.json')
                with open(historial_path, 'w', encoding='utf-8') as f:
                    json.dump(datos['historial'], f, ensure_ascii=False, indent=2)
                
                print("✅ Historial completo guardado en historial_partidos.json")
                
                # Respuesta exitosa
                response = {"status": "success", "message": "Historial completo guardado correctamente"}
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
                
            except Exception as e:
                print(f"💥 Error al guardar historial completo: {str(e)}")
                response = {"status": "error", "message": f"Error al guardar historial: {str(e)}"}
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
        
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_OPTIONS(self):
        # Manejar preflight requests para CORS
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

if __name__ == "__main__":
    PORT = 8083  # Cambiado a 8083
    
    with socketserver.TCPServer(("", PORT), ResultadosHandler) as httpd:
        print(f"🚀 Servidor de resultados ejecutándose en http://localhost:{PORT}")
        print("📝 Endpoints disponibles:")
        print("   - POST /guardar-resultado")
        print("   - POST /guardar-historial-completo")
        print("🛑 Presiona Ctrl+C para detener")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n👋 Servidor detenido")
