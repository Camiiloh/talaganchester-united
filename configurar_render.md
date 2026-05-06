# Configuración de Render + Railway Database

## Paso 1: Accede a tu servicio en Render

1. Ve a https://dashboard.render.com
2. Selecciona tu servicio `talaganchester-united` (o similar)
3. Ve a la sección: **Environment → Environment Variables**

## Paso 2: Agrega las variables de Railway

Copia EXACTAMENTE estos valores:

### Variable 1: DATABASE_URL
```
Name: DATABASE_URL
Value: postgresql://postgres:bauAqztvgFAbwPtUZ6leIF6SvHrEogi@postgres.railway.internal:5432/railway
```

### Variable 2: DATABASE_PUBLIC_URL
```
Name: DATABASE_PUBLIC_URL
Value: postgresql://postgres:bauAqztvgFAbwPtUZ6leIF6SvHrEogi@magle.v.proxy.rlwy.net:19797/railway
```

⚠️ **IMPORTANTE**: 
- No agregues comillas
- Respeta mayúsculas/minúsculas
- Copia la contraseña EXACTAMENTE como aparece

## Paso 3: Guarda y Redeploy

1. Click en **"Save"** o **"Add"** (según sea)
2. Render automáticamente hace redeploy

## Paso 4: Verifica la conexión

Después del redeploy, abre en tu navegador:

```
https://talaganchester-united.onrender.com/api/debug-env
```

Deberías ver algo como:
```json
{
  "env_vars": {
    "DATABASE_URL": "postgresql://postgres:bauAqztvgFAbwPtUZ6leIF6...",
    "DATABASE_PUBLIC_URL": "postgresql://postgres:bauAqztvgFAbwPtUZ6leIF6..."
  },
  "db_available": true
}
```

## Paso 5: Prueba real

Ejecuta esta API para verificar datos:

```
GET https://talaganchester-united.onrender.com/api/historial
```

Debería devolverte tu historial de partidos desde Railway.

---

**Si la conexión falla**, ejecuta en tu terminal local:
```
GET https://talaganchester-united.onrender.com/api/migration-status
```

Para ver qué está pasando.

---

## Información de Conexión Railroad

**IP Pública de Railway:**
```
maglev.proxy.rlwy.net:19797
```

**URLs de Conexión:**
- Interna: `postgres.railway.internal:5432`
- Pública: `maglev.proxy.rlwy.net:19797`

**Base de datos:** railway  
**Usuario:** postgres  
**Puerto:** 5432 (interno) / 19797 (público)
