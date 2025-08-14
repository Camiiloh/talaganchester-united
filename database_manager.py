#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Módulo de base de datos para manejar estadísticas de manera persistente
"""

import os
import json
import sqlite3
import datetime

# Intentar importar PostgreSQL
try:
    import psycopg2
    from psycopg2.extras import RealDictCursor
    POSTGRES_AVAILABLE = True
except ImportError:
    POSTGRES_AVAILABLE = False

class DatabaseManager:
    def __init__(self):
        # Buscar variables de PostgreSQL de Railway
        self.database_url = (
            os.environ.get('DATABASE_URL') or 
            os.environ.get('DATABASE_PUBLIC_URL') or
            os.environ.get('DATABASE_PRIVATE_URL')
        )
        
        # También verificar si tenemos variables individuales de PostgreSQL
        if not self.database_url and os.environ.get('PGHOST'):
            pghost = os.environ.get('PGHOST')
            pgport = os.environ.get('PGPORT', '5432')
            pguser = os.environ.get('PGUSER', 'postgres')
            pgpassword = os.environ.get('PGPASSWORD')
            pgdatabase = os.environ.get('PGDATABASE', 'railway')
            
            if pgpassword:
                self.database_url = f"postgresql://{pguser}:{pgpassword}@{pghost}:{pgport}/{pgdatabase}"
        
        self.use_postgres = self.database_url is not None and POSTGRES_AVAILABLE
        self.sqlite_db = 'talaganchester.db'
        
        if self.use_postgres:
            print(f"🐘 Usando PostgreSQL: {self.database_url[:50]}...")
            self._init_postgres()
        elif os.path.exists(self.sqlite_db) or True:  # Always try SQLite for local
            print("🗄️  Usando SQLite para testing local")
            self._init_sqlite()
        else:
            print("⚠️  Usando archivos JSON como fallback")
    
    def _init_sqlite(self):
        """Inicializa la base de datos SQLite"""
        try:
            conn = sqlite3.connect(self.sqlite_db)
            cur = conn.cursor()
            
            # Crear tabla si no existe
            cur.execute('''
                CREATE TABLE IF NOT EXISTS historial_partidos (
                    id INTEGER PRIMARY KEY,
                    fecha TEXT NOT NULL,
                    fecha_formato TEXT,
                    hora TEXT,
                    cancha TEXT,
                    jugadores_confirmados TEXT,
                    equipos TEXT,
                    resultado TEXT,
                    mvp TEXT,
                    asistencia INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            print(f"❌ Error inicializando SQLite: {e}")
            return False
    
    def _init_postgres(self):
        """Inicializa la base de datos PostgreSQL"""
        try:
            conn = psycopg2.connect(self.database_url)
            cur = conn.cursor()
            
            # Crear tabla si no existe
            cur.execute('''
                CREATE TABLE IF NOT EXISTS historial_partidos (
                    id BIGINT PRIMARY KEY,
                    fecha TEXT NOT NULL,
                    fecha_formato TEXT,
                    hora TEXT,
                    cancha TEXT,
                    jugadores_confirmados TEXT,
                    equipos TEXT,
                    resultado TEXT,
                    mvp TEXT,
                    asistencia INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.commit()
            conn.close()
            print("✅ Tabla PostgreSQL inicializada correctamente")
            return True
            
        except Exception as e:
            print(f"❌ Error inicializando PostgreSQL: {e}")
            return False
    
    def get_connection(self):
        """Obtiene conexión a la base de datos"""
        if self.use_postgres:
            return psycopg2.connect(self.database_url)
        else:
            return sqlite3.connect(self.sqlite_db)
    
    def get_historial_partidos(self):
        """Obtiene el historial de partidos"""
        if self.use_postgres:
            return self._get_historial_postgres()
        elif os.path.exists(self.sqlite_db):
            return self._get_historial_sqlite()
        else:
            return self._get_historial_json()
    
    def save_partido(self, partido):
        """Guarda un partido en la base de datos"""
        if self.use_postgres:
            return self._save_partido_postgres(partido)
        elif os.path.exists(self.sqlite_db):
            return self._save_partido_sqlite(partido)
        else:
            return self._save_partido_json(partido)
    
    def update_partido(self, partido_id, partido):
        """Actualiza un partido existente"""
        if self.use_postgres:
            return self._update_partido_postgres(partido_id, partido)
        elif os.path.exists(self.sqlite_db):
            return self._save_partido_sqlite(partido)  # SQLite usa UPSERT
        else:
            return self._update_partido_json(partido_id, partido)
    
    def delete_partido(self, partido_id):
        """Elimina un partido"""
        if self.use_postgres:
            return self._delete_partido_postgres(partido_id)
        elif os.path.exists(self.sqlite_db):
            return self._delete_partido_sqlite(partido_id)
        else:
            return self._delete_partido_json(partido_id)
    
    # Métodos para SQLite
    def _get_historial_sqlite(self):
        """Obtiene historial desde SQLite"""
        try:
            conn = self.get_connection()
            cur = conn.cursor()
            cur.execute('''
                SELECT * FROM historial_partidos 
                ORDER BY fecha DESC, created_at DESC
            ''')
            
            rows = cur.fetchall()
            historial = []
            
            # Obtener nombres de columnas
            columns = [description[0] for description in cur.description]
            
            for row in rows:
                partido = dict(zip(columns, row))
                # Convertir campos JSON de vuelta a objetos Python
                if partido['jugadores_confirmados']:
                    partido['jugadores_confirmados'] = json.loads(partido['jugadores_confirmados'])
                if partido['equipos']:
                    partido['equipos'] = json.loads(partido['equipos'])
                if partido['resultado']:
                    partido['resultado'] = json.loads(partido['resultado'])
                historial.append(partido)
            
            conn.close()
            return historial
            
        except Exception as e:
            print(f"❌ Error obteniendo historial desde SQLite: {e}")
            return []
    
    def _save_partido_sqlite(self, partido):
        """Guarda partido en SQLite"""
        try:
            conn = self.get_connection()
            cur = conn.cursor()
            
            cur.execute('''
                INSERT OR REPLACE INTO historial_partidos 
                (id, fecha, fecha_formato, hora, cancha, jugadores_confirmados, 
                 equipos, resultado, mvp, asistencia)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                partido['id'],
                partido['fecha'],
                partido.get('fecha_formato'),
                partido.get('hora'),
                partido.get('cancha'),
                json.dumps(partido.get('jugadores_confirmados', [])),
                json.dumps(partido.get('equipos', {})),
                json.dumps(partido.get('resultado', {})),
                partido.get('mvp'),
                partido.get('asistencia')
            ))
            
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            print(f"❌ Error guardando partido en SQLite: {e}")
            return False
    
    def _delete_partido_sqlite(self, partido_id):
        """Elimina partido de SQLite"""
        try:
            conn = self.get_connection()
            cur = conn.cursor()
            cur.execute('DELETE FROM historial_partidos WHERE id = ?', (partido_id,))
            deleted = cur.rowcount > 0
            conn.commit()
            conn.close()
            return deleted
            
        except Exception as e:
            print(f"❌ Error eliminando partido de SQLite: {e}")
            return False

    # Métodos para PostgreSQL
    def _get_historial_postgres(self):
        """Obtiene historial desde PostgreSQL"""
        try:
            conn = self.get_connection()
            cur = conn.cursor(cursor_factory=RealDictCursor)
            cur.execute('''
                SELECT * FROM historial_partidos 
                ORDER BY fecha DESC, created_at DESC
            ''')
            
            rows = cur.fetchall()
            historial = []
            
            for row in rows:
                partido = dict(row)
                # Convertir campos JSONB de vuelta a objetos Python
                if partido['equipos']:
                    partido['equipos'] = partido['equipos']
                if partido['resultado']:
                    partido['resultado'] = partido['resultado']
                historial.append(partido)
            
            conn.close()
            return historial
            
        except Exception as e:
            print(f"❌ Error obteniendo historial desde PostgreSQL: {e}")
            return []
    
    def _save_partido_postgres(self, partido):
        """Guarda partido en PostgreSQL"""
        try:
            conn = self.get_connection()
            cur = conn.cursor()
            
            cur.execute('''
                INSERT INTO historial_partidos 
                (id, fecha, fecha_formato, hora, cancha, jugadores_confirmados, 
                 equipos, resultado, mvp, asistencia)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (id) DO UPDATE SET
                    fecha = EXCLUDED.fecha,
                    fecha_formato = EXCLUDED.fecha_formato,
                    hora = EXCLUDED.hora,
                    cancha = EXCLUDED.cancha,
                    jugadores_confirmados = EXCLUDED.jugadores_confirmados,
                    equipos = EXCLUDED.equipos,
                    resultado = EXCLUDED.resultado,
                    mvp = EXCLUDED.mvp,
                    asistencia = EXCLUDED.asistencia,
                    updated_at = CURRENT_TIMESTAMP
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
            conn.close()
            return True
            
        except Exception as e:
            print(f"❌ Error guardando partido en PostgreSQL: {e}")
            return False
    
    def _update_partido_postgres(self, partido_id, partido):
        """Actualiza partido en PostgreSQL"""
        return self._save_partido_postgres(partido)  # Usa UPSERT
    
    def _delete_partido_postgres(self, partido_id):
        """Elimina partido de PostgreSQL"""
        try:
            conn = self.get_connection()
            cur = conn.cursor()
            cur.execute('DELETE FROM historial_partidos WHERE id = %s', (partido_id,))
            deleted = cur.rowcount > 0
            conn.commit()
            conn.close()
            return deleted
            
        except Exception as e:
            print(f"❌ Error eliminando partido de PostgreSQL: {e}")
            return False
    
    # Métodos para JSON (fallback)
    def _get_historial_json(self):
        """Obtiene historial desde archivo JSON"""
        try:
            if os.path.exists('historial_partidos.json'):
                with open('historial_partidos.json', 'r', encoding='utf-8') as f:
                    return json.load(f)
            return []
        except Exception as e:
            print(f"❌ Error leyendo historial_partidos.json: {e}")
            return []
    
    def _save_partido_json(self, partido):
        """Guarda partido en archivo JSON"""
        try:
            historial = self._get_historial_json()
            
            # Buscar si ya existe
            for i, p in enumerate(historial):
                if p['id'] == partido['id']:
                    historial[i] = partido
                    break
            else:
                historial.append(partido)
            
            # Ordenar por fecha
            historial.sort(key=lambda x: x['fecha'], reverse=True)
            
            with open('historial_partidos.json', 'w', encoding='utf-8') as f:
                json.dump(historial, f, indent=2, ensure_ascii=False)
            
            return True
            
        except Exception as e:
            print(f"❌ Error guardando en historial_partidos.json: {e}")
            return False
    
    def _update_partido_json(self, partido_id, partido):
        """Actualiza partido en archivo JSON"""
        return self._save_partido_json(partido)
    
    def _delete_partido_json(self, partido_id):
        """Elimina partido de archivo JSON"""
        try:
            historial = self._get_historial_json()
            original_len = len(historial)
            historial = [p for p in historial if p['id'] != partido_id]
            
            if len(historial) < original_len:
                with open('historial_partidos.json', 'w', encoding='utf-8') as f:
                    json.dump(historial, f, indent=2, ensure_ascii=False)
                return True
            
            return False
            
        except Exception as e:
            print(f"❌ Error eliminando de historial_partidos.json: {e}")
            return False

# Instancia global del gestor de base de datos (lazy loading)
_db_manager_instance = None

def get_db_manager():
    """Obtiene la instancia del gestor de base de datos (lazy loading)"""
    global _db_manager_instance
    if _db_manager_instance is None:
        _db_manager_instance = DatabaseManager()
    return _db_manager_instance

# Para compatibilidad con código existente
db_manager = get_db_manager()
