# 🚀 Guía para Persistencia de Datos en Railway

## 📋 Problema
Los datos ingresados en la web (estadísticas, resultados) se pierden al hacer nuevo deploy porque Railway crea nuevos contenedores.

## ✅ Solución: PostgreSQL en Railway

### Paso 1: Agregar PostgreSQL en Railway
1. Ve a tu proyecto en Railway
2. Haz clic en "Add Service" → "Database" → "Add PostgreSQL"
3. Railway creará automáticamente la variable `DATABASE_URL`

### Paso 2: Deploy con la Nueva Funcionalidad
Los archivos ya están configurados:
- ✅ `database_manager.py` - Gestor de base de datos con fallback a JSON
- ✅ `setup_database.py` - Script de migración inicial  
- ✅ `servidor_todo_en_uno.py` - Servidor actualizado
- ✅ `requirements.txt` - Incluye `psycopg2-binary`

### Paso 3: Primera Migración (Opcional)
Si tienes datos existentes que quieres preservar:

```bash
# Localmente, ejecuta una vez:
python setup_database.py
```

Esto migrará los datos de `historial_partidos.json` a PostgreSQL.

## 🔄 Cómo Funciona

### Automático
- **Si DATABASE_URL existe**: Usa PostgreSQL (persistente)
- **Si no existe**: Usa archivos JSON (se pierden en deploy)

### Sin Interrupciones  
- El sistema funciona igual que antes
- Si PostgreSQL falla, automáticamente usa JSON como respaldo
- No hay cambios en la interfaz web

## 🎯 Beneficios

1. **Datos Persistentes**: Los resultados no se pierden nunca
2. **Escalabilidad**: PostgreSQL maneja más datos que archivos JSON
3. **Concurrencia**: Múltiples usuarios pueden agregar resultados simultáneamente
4. **Respaldo Automático**: Railway respalda la base de datos
5. **Fallback Seguro**: Si la DB falla, usa archivos JSON

## 🔧 Comandos Útiles

```bash
# Ver logs en Railway
railway logs

# Conectar a la base de datos
railway connect

# Ejecutar migración manual
railway run python setup_database.py
```

## 📊 Estructura de la Base de Datos

### Tabla: `historial_partidos`
- `id` (BIGINT) - ID único del partido
- `fecha` (DATE) - Fecha del partido
- `hora` (VARCHAR) - Hora del partido
- `cancha` (VARCHAR) - Cancha utilizada
- `jugadores_confirmados` (TEXT[]) - Array de jugadores
- `equipos` (JSONB) - Configuración de equipos
- `resultado` (JSONB) - Resultado del partido
- `mvp` (VARCHAR) - Mejor jugador
- `asistencia` (INTEGER) - Número de asistentes
- `created_at` - Timestamp de creación
- `updated_at` - Timestamp de actualización

## ⚠️ Notas Importantes

1. **Gratuito**: PostgreSQL en Railway es gratuito con límites generosos
2. **Automático**: No necesitas cambiar nada en la interfaz web
3. **Compatible**: Funciona con el código existente sin modificaciones
4. **Seguro**: Incluye respaldo automático si algo falla

## 🚀 Próximo Deploy

Simplemente haz push a GitHub y Railway:
1. Detectará las nuevas dependencias (`psycopg2-binary`)
2. Creará la base de datos automáticamente 
3. Los nuevos resultados se guardarán persistentemente

¡Los datos nunca más se perderán! 🎉
