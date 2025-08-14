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
    
    # Solo ejecutar si estamos en Railway (tiene DATABASE_URL)
    if not os.environ.get('DATABASE_URL'):
        print("ℹ️  No se detectó DATABASE_URL, saltando migración")
        return False
    
    db = DatabaseManager()
    
    # Verificar si ya hay datos en PostgreSQL
    try:
        historial_existente = db.get_historial_partidos()
        if historial_existente and len(historial_existente) > 0:
            print(f"✅ PostgreSQL ya tiene {len(historial_existente)} registros, saltando migración")
            return True
    except Exception as e:
        print(f"⚠️  Error verificando historial existente: {e}")
    
    # Cargar datos desde JSON
    try:
        with open('historial_partidos.json', 'r', encoding='utf-8') as f:
            datos_json = json.load(f)
        
        if not datos_json:
            print("ℹ️  No hay datos en historial_partidos.json para migrar")
            return True
            
        print(f"📦 Migrando {len(datos_json)} registros desde JSON a PostgreSQL...")
        
        # Migrar cada registro
        migrados = 0
        for registro in datos_json:
            try:
                # Guardar en PostgreSQL usando el database_manager
                exito = db.save_partido(registro)
                if exito:
                    migrados += 1
                else:
                    print(f"❌ Error migrando registro ID: {registro.get('id', 'N/A')}")
                    
            except Exception as e:
                print(f"❌ Error migrando registro {registro.get('id', 'N/A')}: {e}")
                continue
        
        print(f"✅ Migración completada: {migrados}/{len(datos_json)} registros migrados")
        return migrados > 0
        
    except FileNotFoundError:
        print("⚠️  No se encontró historial_partidos.json")
        return False
    except Exception as e:
        print(f"❌ Error durante migración: {e}")
        return False

if __name__ == "__main__":
    migrar_datos_a_postgres()
