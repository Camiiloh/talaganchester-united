#!/usr/bin/env python3
"""
Script para corregir datos en PostgreSQL y verificar funcionamiento
"""
import os
import json
import psycopg2
from psycopg2.extras import RealDictCursor
from database_manager import DatabaseManager

def fix_postgres_data():
    """Corrige los datos en PostgreSQL"""
    print("🔧 Iniciando corrección de datos PostgreSQL...")
    
    # Obtener URL de PostgreSQL
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        print("❌ No se encontró DATABASE_URL")
        return False
    
    try:
        # Conectar a PostgreSQL
        conn = psycopg2.connect(database_url)
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        # Obtener todos los registros
        cur.execute('SELECT * FROM historial_partidos ORDER BY created_at DESC')
        rows = cur.fetchall()
        
        print(f"📊 Encontrados {len(rows)} registros en PostgreSQL")
        
        for row in rows:
            print(f"Registro ID: {row['id']}")
            print(f"  Fecha: {row['fecha']}")
            print(f"  Equipos tipo: {type(row['equipos'])}")
            print(f"  Resultado tipo: {type(row['resultado'])}")
            print(f"  Jugadores tipo: {type(row['jugadores_confirmados'])}")
            
            # Si equipos no es string JSON, convertirlo
            needs_update = False
            equipos = row['equipos']
            resultado = row['resultado']
            jugadores = row['jugadores_confirmados']
            
            if equipos and not isinstance(equipos, str):
                equipos = json.dumps(equipos)
                needs_update = True
                print(f"  🔄 Convirtiendo equipos a JSON")
                
            if resultado and not isinstance(resultado, str):
                resultado = json.dumps(resultado)
                needs_update = True
                print(f"  🔄 Convirtiendo resultado a JSON")
                
            if jugadores and not isinstance(jugadores, str):
                jugadores = json.dumps(jugadores)
                needs_update = True
                print(f"  🔄 Convirtiendo jugadores a JSON")
            
            if needs_update:
                cur.execute('''
                    UPDATE historial_partidos 
                    SET equipos = %s, resultado = %s, jugadores_confirmados = %s,
                        updated_at = CURRENT_TIMESTAMP
                    WHERE id = %s
                ''', (equipos, resultado, jugadores, row['id']))
                print(f"  ✅ Registro {row['id']} actualizado")
        
        conn.commit()
        
        # Verificar con DatabaseManager
        print("\n🧪 Verificando con DatabaseManager...")
        dm = DatabaseManager()
        historial = dm.get_historial()
        print(f"✅ DatabaseManager obtiene {len(historial)} registros")
        
        for i, partido in enumerate(historial):
            print(f"Partido {i+1}:")
            print(f"  Fecha: {partido.get('fecha')}")
            print(f"  Equipos: {type(partido.get('equipos'))} - {len(partido.get('equipos', {}))} items")
            if partido.get('equipos'):
                print(f"    Keys: {list(partido.get('equipos', {}).keys())}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error corrigiendo PostgreSQL: {e}")
        return False

if __name__ == "__main__":
    fix_postgres_data()
