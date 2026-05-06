#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para verificar la conexión a Railway desde Render
Ejecutar después de agregar las variables de entorno en Render
"""

import requests
import json
import sys
from urllib.parse import urljoin

def verificar_conexion(render_url):
    """Verifica que Render pueda conectar con Railway"""
    
    print("🔍 Verificando configuración de Render + Railway...\n")
    
    urls_a_verificar = [
        ('/api/debug-env', 'Variables de entorno'),
        ('/api/migration-status', 'Estado de migración'),
        ('/api/health', 'Health check'),
        ('/api/historial', 'Historial de partidos'),
    ]
    
    render_url = render_url.rstrip('/')
    
    for endpoint, descripcion in urls_a_verificar:
        url_completa = urljoin(render_url + '/', endpoint.lstrip('/'))
        
        print(f"📡 Verificando: {descripcion}")
        print(f"   URL: {url_completa}")
        
        try:
            response = requests.get(url_completa, timeout=10)
            
            if response.status_code == 200:
                print(f"   ✅ OK (Status: 200)")
                try:
                    datos = response.json()
                    print(f"   Respuesta: {json.dumps(datos, indent=2)[:200]}...")
                except:
                    print(f"   Respuesta: {response.text[:100]}...")
            else:
                print(f"   ❌ Error: Status {response.status_code}")
                
        except requests.exceptions.Timeout:
            print(f"   ❌ Timeout - la conexión tardó demasiado")
        except requests.exceptions.ConnectionError:
            print(f"   ❌ No se puede conectar - verifica la URL")
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
        
        print()
    
    # Verificación específica de PostgreSQL
    print("=" * 60)
    print("🗄️  VERIFICACIÓN DE POSTGRESQL\n")
    
    try:
        response = requests.get(f"{render_url}/api/debug-env", timeout=10)
        if response.status_code == 200:
            datos = response.json()
            env_vars = datos.get('env_vars', {})
            
            if env_vars.get('DATABASE_URL'):
                print("✅ DATABASE_URL configurada")
            else:
                print("❌ DATABASE_URL NO configurada")
            
            if env_vars.get('DATABASE_PUBLIC_URL'):
                print("✅ DATABASE_PUBLIC_URL configurada")
            else:
                print("⚠️  DATABASE_PUBLIC_URL NO configurada")
            
            db_available = datos.get('db_available')
            if db_available:
                print("✅ Base de datos disponible")
            else:
                print("❌ Base de datos NO disponible")
    except Exception as e:
        print(f"❌ No se puede verificar: {e}")
    
    print("\n" + "=" * 60)
    print("✨ Verificación completada\n")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("❌ Uso: python verificar_railway_render.py <URL_RENDER>")
        print("\nEjemplo:")
        print("   python verificar_railway_render.py https://talaganchester-united.onrender.com")
        print("\nObtén tu URL en: https://dashboard.render.com/services/")
        sys.exit(1)
    
    render_url = sys.argv[1]
    verificar_conexion(render_url)
