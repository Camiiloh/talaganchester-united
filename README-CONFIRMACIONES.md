# 🤖 Sistema de Confirmaciones Automáticas

Este sistema permite alimentar automáticamente las listas de jugadores confirmados desde múltiples fuentes, incluyendo bots de WhatsApp, Telegram y otras integraciones externas.

## 🚀 Características

### ✅ Fuentes de Datos Automáticas
1. **Confirmaciones Automáticas** (Prioridad 1)
   - Servidor dedicado en puerto 5000
   - API REST para recibir confirmaciones
   - Soporte para bots de WhatsApp/Telegram

2. **Último Sorteo** (Prioridad 2)
   - Lee desde `equipos.json` (último sorteo realizado)
   - Combina equipos rojo y negro

3. **Lista Manual** (Prioridad 3)
   - Lee desde `confirmados.txt`
   - Archivo de texto plano, un jugador por línea

### 🔄 Flujo Automático
- El sistema consulta las fuentes en orden de prioridad
- Carga automáticamente la primera fuente disponible
- Notifica al usuario la fuente utilizada
- Botón manual de recarga disponible

## 📋 Instalación y Configuración

### 1. Servidor de Confirmaciones
```bash
# Instalar dependencias
pip install flask flask-cors requests

# Ejecutar servidor
python servidor_confirmaciones.py
```

El servidor estará disponible en `http://localhost:5000`

### 2. Servidor Web Principal
```bash
# En otra terminal
python -m http.server 8080
```

### 3. Servidor de Resultados
```bash
# En otra terminal
python servidor_resultados.py
```

## 🌐 API Endpoints

### Confirmar Jugador Individual
```http
POST http://localhost:5000/confirmar-jugador
Content-Type: application/json

{
  "jugador": "Carlos P",
  "fecha": "2025-01-14",
  "fuente": "WhatsApp"
}
```

### Confirmar Lista Completa
```http
POST http://localhost:5000/confirmar-lista
Content-Type: application/json

{
  "jugadores": ["Carlos P", "Diego", "Erik"],
  "fecha": "2025-01-14", 
  "fuente": "WhatsApp Grupo"
}
```

### Obtener Lista de Confirmados
```http
GET http://localhost:5000/lista-jugadores/2025-01-14
```

### Estado del Servidor
```http
GET http://localhost:5000/estado
```

## 🤖 Integración con Bots

### Ejemplo WhatsApp Bot
```python
import requests

def procesar_mensaje_whatsapp(mensaje, fecha):
    # Extraer nombres del mensaje
    jugadores = extraer_nombres(mensaje)
    
    # Enviar al servidor
    data = {
        'jugadores': jugadores,
        'fecha': fecha,
        'fuente': 'WhatsApp Bot'
    }
    
    response = requests.post(
        'http://localhost:5000/confirmar-lista',
        json=data
    )
    
    return response.json()
```

### Patrones de Mensajes Soportados
- `"Confirmado: Carlos, Diego, Erik"`
- `"Me anoto - Francisco H"`
- `"Voy: Luisito, Marco, Pancho"`
- `"Para mañana: Lista de 10 jugadores..."`

## 📱 Uso desde la Interfaz Web

### Carga Automática
1. Abre `http://localhost:8080/estadisticas.html`
2. Los jugadores se cargan automáticamente al iniciar
3. El sistema muestra la fuente utilizada

### Recarga Manual
- Clic en "🔄" para recargar manualmente
- Útil cuando llegan nuevas confirmaciones

### Prioridad de Fuentes
1. **Confirmaciones automáticas**: Si hay datos del día actual
2. **Último sorteo**: Si se realizó un sorteo reciente
3. **Lista manual**: Como fallback desde confirmados.txt

## 🔧 Archivos de Configuración

### confirmaciones_automaticas.json
```json
{
  "2025-01-14": {
    "jugadores": ["Carlos P", "Diego", "Erik"],
    "timestamp": "2025-01-14T10:30:00",
    "fuentes": {
      "Carlos P": "WhatsApp",
      "Diego": "WhatsApp", 
      "Erik": "Telegram"
    }
  }
}
```

### confirmados.txt (Fallback)
```
Carlos P
Diego
Erik
Francisco H
# Comentarios con #
```

## 🛠️ Solución de Problemas

### El servidor no inicia
```bash
# Verificar puerto disponible
netstat -an | findstr :5000

# Cambiar puerto si es necesario
python servidor_confirmaciones.py --port 5001
```

### No se cargan confirmaciones automáticas
1. Verificar que el servidor esté corriendo en puerto 5000
2. Comprobar CORS habilitado
3. Verificar fecha actual vs fechas en datos

### Datos no actualizados
- Los datos se guardan automáticamente
- Usar `?_=timestamp` para evitar cache del navegador

## 📊 Monitoreo

### Logs del Servidor
```bash
# Ver logs en tiempo real
tail -f servidor_confirmaciones.log
```

### Verificar Estado
```bash
curl http://localhost:5000/estado
```

### Datos Almacenados
```bash
# Ver archivo de confirmaciones
cat confirmaciones_automaticas.json | jq
```

## 🔮 Próximas Mejoras

- [ ] Dashboard web para gestionar confirmaciones
- [ ] Notificaciones push cuando llegan nuevas confirmaciones
- [ ] Integración directa con WhatsApp Web API
- [ ] Exportación a Excel/PDF de listas
- [ ] Estadísticas de asistencia por jugador
- [ ] Recordatorios automáticos por WhatsApp

## 🆘 Soporte

Si tienes problemas:
1. Revisa los logs del servidor
2. Verifica que todos los servicios estén corriendo
3. Comprueba la conectividad entre componentes
4. Consulta los archivos de datos JSON

---

**Desarrollado para TalAganchester United** ⚽
