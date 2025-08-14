#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para migrar datos desde JSON a la base de datos PostgreSQL en Railway
"""

import os
import json
from database_manager import DatabaseManager

def migrar_datos_a_postgres():
    """Migra datos desde historial_partidos.json a PostgreSQL"""
    
    print("🔄 Iniciando proceso de migración...")
    
    # Solo ejecutar si estamos en Railway (tiene DATABASE_URL)
    if not os.environ.get('DATABASE_URL'):
        print("ℹ️  No se detectó DATABASE_URL, saltando migración")
        return False
    
    print(f"🐘 DATABASE_URL detectada: {os.environ.get('DATABASE_URL')[:50]}...")
    
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
