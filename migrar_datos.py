#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para migrar datos desde JSON a la base de datos PostgreSQL en Railway
"""

import os
import json
from database_manager import DatabaseManager

def migrar_datos_a_postgres():
    """Migra datos desde historial_partidos.json a la base de datos (PostgreSQL o SQLite)"""
    
    print("🔄 Iniciando proceso de migración...")
    
    # Ejecutar tanto en Railway (PostgreSQL) como en producción con SQLite
    database_url = os.environ.get('DATABASE_URL')
    port = os.environ.get('PORT')  # Railway siempre tiene PORT
    
    if not port:
        print("ℹ️  No se detectó ambiente de producción, saltando migración")
        return False
    
    if database_url:
        print(f"🐘 DATABASE_URL detectada: {database_url[:50]}...")
    else:
        print("🗄️  No hay DATABASE_URL, usando SQLite en producción")
    
    try:
        db = DatabaseManager()
        print("✅ DatabaseManager inicializado correctamente")
    except Exception as e:
        print(f"❌ Error inicializando DatabaseManager: {e}")
        return False
    
    # Verificar si ya hay datos en PostgreSQL
    try:
        historial_existente = db.get_historial_partidos()
        print(f"📊 Historial existente en PostgreSQL: {len(historial_existente) if historial_existente else 0} registros")
        
        if historial_existente and len(historial_existente) > 0:
            print(f"✅ PostgreSQL ya tiene {len(historial_existente)} registros, saltando migración")
            return True
    except Exception as e:
        print(f"⚠️  Error verificando historial existente: {e}")
        print("🔄 Continuando con la migración...")
    
    # Cargar datos desde JSON
    try:
        if not os.path.exists('historial_partidos.json'):
            print("⚠️  No se encontró historial_partidos.json")
            return False
            
        print("📁 Cargando datos desde historial_partidos.json...")
        with open('historial_partidos.json', 'r', encoding='utf-8') as f:
            datos_json = json.load(f)
        
        print(f"📦 Datos cargados: {len(datos_json) if datos_json else 0} registros")
        
        if not datos_json:
            print("ℹ️  No hay datos en historial_partidos.json para migrar")
            return True
            
        print(f"� Iniciando migración de {len(datos_json)} registros desde JSON a PostgreSQL...")
        
        # Migrar cada registro
        migrados = 0
        errores = 0
        for i, registro in enumerate(datos_json):
            try:
                print(f"📝 Migrando registro {i+1}/{len(datos_json)}: ID {registro.get('id', 'N/A')}")
                
                # Convertir formato de equipos si es necesario
                if 'equipo_rojo' in registro and 'equipo_negro' in registro and 'equipos' not in registro:
                    registro['equipos'] = {
                        'rojo': registro.get('equipo_rojo', []),
                        'negro': registro.get('equipo_negro', [])
                    }
                    print(f"🔄 Convertido formato de equipos para registro {i+1}")
                
                # Guardar en PostgreSQL usando el database_manager
                exito = db.save_partido(registro)
                if exito:
                    migrados += 1
                    print(f"✅ Registro {i+1} migrado exitosamente")
                else:
                    errores += 1
                    print(f"❌ Error migrando registro {i+1}: ID {registro.get('id', 'N/A')}")
                    
            except Exception as e:
                errores += 1
                print(f"❌ Excepción migrando registro {i+1} {registro.get('id', 'N/A')}: {e}")
                continue
        
        print(f"📊 Migración completada:")
        print(f"   ✅ Exitosos: {migrados}")
        print(f"   ❌ Errores: {errores}")
        print(f"   📈 Total: {len(datos_json)}")
        
        if migrados > 0:
            print("🎉 Migración exitosa - datos disponibles en PostgreSQL")
        else:
            print("⚠️  No se migraron datos - revisar errores")
            
        return migrados > 0
        
    except FileNotFoundError:
        print("⚠️  No se encontró historial_partidos.json")
        return False
    except Exception as e:
        print(f"❌ Error durante migración: {e}")
        return False

if __name__ == "__main__":
    migrar_datos_a_postgres()
