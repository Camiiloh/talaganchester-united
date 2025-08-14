# 📂 Estructura del Proyecto TalAganchester United

## 🌟 Archivos Principales

### 🌐 **Interfaz Web**
- `index.html` - Página principal del sitio
- `estadisticas.html` - Interfaz de gestión de partidos y estadísticas
- `cancha.html` - Visualización de la cancha (versión original)
- `cancha-v2.html` - Visualización avanzada de la cancha
- `style.css` - Estilos principales
- `cancha.css` - Estilos para visualización de cancha
- `cancha-v2.css` - Estilos avanzados para cancha v2

### ⚡ **JavaScript**
- `main.js` - Funcionalidades principales del sitio
- `estadisticas.js` - Lógica de estadísticas y gestión de partidos
- `cancha-v2.js` - Funcionalidades de la cancha v2
- `auth_simple.js` - Sistema de autenticación

### 🐍 **Python - Sistema de Sorteos**
- `sorteo_partido.py` - Sorteo básico de equipos
- `sorteo_automatico.py` - Sorteo automático con balanceado
- `sorteo_posiciones_especificas.py` - Sorteo por posiciones específicas

### 🐍 **Python - Análisis y Gestión**
- `analizar_formacion.py` - Análisis de formaciones con IA
- `calcular_formacion_especifica.py` - Cálculos de formaciones
- `editor_puntajes.py` - Editor de puntajes de jugadores
- `gestionar_resultados.py` - Gestión de resultados de partidos

### 🤖 **Sistema de Confirmaciones Automáticas**
- `servidor_confirmaciones.py` - API para confirmaciones automáticas
- `agregar_confirmaciones.py` - Script para agregar confirmaciones localmente
- `ejemplo_bot_whatsapp.py` - Ejemplo de integración con WhatsApp
- `test_confirmaciones.py` - Pruebas del sistema de confirmaciones

### 🗄️ **Servidores**
- `servidor_resultados.py` - Servidor para persistencia de datos

### 📊 **Datos**
- `jugadores.json` - Lista básica de jugadores
- `jugadores_posiciones_especificas.json` - Jugadores con puntajes por posición
- `equipos.json` - Último sorteo realizado
- `historial_partidos.json` - Historial completo de partidos
- `confirmaciones_automaticas.json` - Confirmaciones automáticas por fecha
- `confirmados.txt` - Lista manual de jugadores confirmados
- `partido.txt` - Información del partido actual
- `auth_config.json` - Configuración de autenticación

### 📁 **Recursos**
- `fotos/` - Fotos de los jugadores
- `CNAME` - Configuración de dominio personalizado
- `web.config` - Configuración del servidor web

### 📖 **Documentación**
- `README.md` - Documentación principal
- `README-NUEVO.md` - Documentación actualizada
- `README-CONFIRMACIONES.md` - Guía del sistema de confirmaciones
- `GUIA-RESULTADOS.md` - Guía de gestión de resultados
- `ESTRUCTURA-PROYECTO.md` - Este archivo

### ⚙️ **Configuración**
- `package.json` - Dependencias de Node.js
- `vite.config.js` - Configuración de Vite
- `.gitignore` - Archivos ignorados por Git

## 🗑️ **Archivos Eliminados (Limpieza)**

### ❌ **Archivos de Test Obsoletos**
- `test-auth.html`
- `test-guardar.html`
- `test-header.html`
- `test-header-v2.html`
- `debug-historial.html`
- `debug-passwords.html`
- `estadisticas-test.js`
- `test_partido.json`

### ❌ **Backups y Versiones Obsoletas**
- `cancha-v2.js.bak-v1.0`
- `cancha.bkp`
- `estadisticas_backup.js`
- `estadisticas-simple.html`
- `jugadores_avanzado.json`

### ❌ **Scripts Obsoletos**
- `actualiza-header.js`
- `actualizar_html.py`
- `debug_nombres.py`
- `guardar_resultado_web.py`
- `consultar_jugadores.py`
- `ver_equipos.py`
- `comparador_sorteos.py`
- `sorteo_avanzado.py`
- `sorteo_especializado.py`

### ❌ **CSS Obsoleto**
- `equipo-labels-left.css`

### ❌ **Cache**
- `__pycache__/` - Cache de Python

## 🚀 **Flujo de Trabajo Actual**

### 1. **Confirmación de Jugadores**
```
confirmados.txt → agregar_confirmaciones.py → confirmaciones_automaticas.json
```

### 2. **Sorteo de Equipos**
```
jugadores confirmados → sorteo_posiciones_especificas.py → equipos.json
```

### 3. **Gestión de Partidos**
```
estadisticas.html → estadisticas.js → servidor_resultados.py → historial_partidos.json
```

### 4. **Análisis de Formaciones**
```
equipos.json → analizar_formacion.py → sugerencias de formación
```

## 📈 **Estado del Proyecto**

✅ **Completado:**
- Sistema de sorteos por posiciones
- Interfaz web completa con autenticación
- Persistencia de datos
- Sistema de confirmaciones automáticas
- Análisis de formaciones con IA

🔄 **En Desarrollo:**
- Integración con bots de WhatsApp/Telegram
- Dashboard de estadísticas avanzadas

💡 **Próximas Mejoras:**
- Notificaciones push
- Exportación a PDF/Excel
- Estadísticas por temporada
