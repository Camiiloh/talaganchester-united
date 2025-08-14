#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para configurar la base de datos PostgreSQL y migrar datos existentes
"""

import os
import json
import psycopg2
from psycopg2.extras import RealDictCursor
import datetime

def get_database_url():
    """Obtiene la URL de la base de datos desde variables de entorno"""
    # Railway automáticamente provee DATABASE_URL cuando agregas PostgreSQL
    return os.environ.get('DATABASE_URL', 'postgresql://localhost:5432/talaganchester')

def create_tables():
    """Crea las tablas necesarias en PostgreSQL"""
    conn = None
    try:
        conn = psycopg2.connect(get_database_url())
        cur = conn.cursor()
        
        # Tabla para historial de partidos
        cur.execute('''
            CREATE TABLE IF NOT EXISTS historial_partidos (
                id BIGINT PRIMARY KEY,
                fecha DATE NOT NULL,
                fecha_formato VARCHAR(100),
                hora VARCHAR(10),
                cancha VARCHAR(50),
                jugadores_confirmados TEXT[],
                equipos JSONB,
                resultado JSONB,
                mvp VARCHAR(100),
                asistencia INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tabla para configuración general
        cur.execute('''
            CREATE TABLE IF NOT EXISTS configuracion (
                id SERIAL PRIMARY KEY,
                clave VARCHAR(100) UNIQUE NOT NULL,
                valor JSONB,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        print("✅ Tablas creadas exitosamente")
        
    except Exception as e:
        print(f"❌ Error creando tablas: {e}")
    finally:
        if conn:
            conn.close()

def migrate_existing_data():
    """Migra datos existentes desde archivos JSON a PostgreSQL"""
    conn = None
    try:
        # Leer historial existente
        if os.path.exists('historial_partidos.json'):
            with open('historial_partidos.json', 'r', encoding='utf-8') as f:
                historial = json.load(f)
                
            conn = psycopg2.connect(get_database_url())
            cur = conn.cursor()
            
            for partido in historial:
                # Verificar si ya existe
                cur.execute('SELECT id FROM historial_partidos WHERE id = %s', (partido['id'],))
                if cur.fetchone():
                    continue  # Ya existe
                
                cur.execute('''
                    INSERT INTO historial_partidos 
                    (id, fecha, fecha_formato, hora, cancha, jugadores_confirmados, 
                     equipos, resultado, mvp, asistencia)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ''', (
                    partido['id'],
                    partido['fecha'],
                    partido.get('fecha_formato'),
                    partido.get('hora'),
                    partido.get('cancha'),
                    partido.get('jugadores_confirmados', []),
                    json.dumps(partido.get('equipos', {})),
                    json.dumps(partido.get('resultado', {})),
                    partido.get('mvp'),
                    partido.get('asistencia')
                ))
            
            conn.commit()
            print(f"✅ Migrados {len(historial)} partidos a PostgreSQL")
        
    except Exception as e:
        print(f"❌ Error migrando datos: {e}")
    finally:
        if conn:
            conn.close()

def test_connection():
    """Prueba la conexión a la base de datos"""
    try:
        conn = psycopg2.connect(get_database_url())
        cur = conn.cursor()
        cur.execute('SELECT version()')
        version = cur.fetchone()
        print(f"✅ Conexión exitosa a PostgreSQL: {version[0]}")
        conn.close()
        return True
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False

if __name__ == '__main__':
    print("🚀 Configurando base de datos...")
    
    if test_connection():
        create_tables()
        migrate_existing_data()
        print("✅ Base de datos configurada correctamente")
    else:
        print("❌ No se pudo conectar a la base de datos")
        print("💡 En Railway, agrega PostgreSQL desde el dashboard")
