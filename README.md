# ⚽ Talaganchester United - Sistema de Gestión de Partidos

Sistema completo para organizar partidos de fútbol con sorteo automático de equipos, visualización táctica y estadísticas históricas.

## 🚀 Características Principales

### 📋 Gestión de Jugadores
- Lista completa de jugadores con posiciones y puntajes
- Sistema de confirmación para cada partido
- Base de datos en `jugadores.json`

### 🎲 Sorteo Inteligente
- Algoritmo balanceado por promedios de puntaje
- Asignación automática de posiciones
- Garantiza arqueros y delanteros en cada equipo
- Diferencia mínima entre promedios de equipos

### 🏟️ Visualización Táctica
- **Cancha Simple**: Vista básica con nombres
- **Cancha v2**: Fotos de jugadores y diseño profesional
- Cancha rotada 90° para orientación vertical realista
- Responsive design para móviles y desktop

### 📊 Sistema de Estadísticas
- Historial completo de partidos
- Estadísticas de victorias por equipo
- Ranking de goleadores
- Sistema de MVP por partido
- Control de asistencia

## 📁 Estructura de Archivos

```
├── index.html              # Lista de jugadores y calculadora
├── cancha.html             # Vista simple de la cancha
├── cancha-v2.html          # Vista avanzada con fotos
├── estadisticas.html       # Sistema de estadísticas
├── sorteo_automatico.py    # Sorteo balanceado
├── gestionar_resultados.py # Gestión de resultados
├── jugadores.json          # Base de datos de jugadores
├── equipos.json           # Resultado del último sorteo
├── historial_partidos.json # Historial de resultados
├── confirmados.txt        # Lista de confirmados
└── partido.txt            # Datos del próximo partido
```

## 🎮 Cómo Usar

### 1. Configurar Partido
```bash
# Editar datos del partido
echo "fecha: 15/08" > partido.txt
echo "hora: 21:00" >> partido.txt
echo "cancha: Pasto Sintético" >> partido.txt
```

### 2. Confirmar Jugadores
Editar `confirmados.txt` con la lista de jugadores que van a jugar.

### 3. Ejecutar Sorteo
```bash
python sorteo_automatico.py
```

### 4. Levantar Servidor Web
```bash
python -m http.server 3000
```

### 5. Agregar Resultados
```bash
# Opción 1: Via interfaz web
# Ir a http://localhost:3000/estadisticas.html

# Opción 2: Via script Python
python gestionar_resultados.py
```

## 📊 Sistema de Estadísticas

### Funcionalidades
- ✅ Historial completo de partidos
- ✅ Victorias por equipo (Rojo vs Negro)
- ✅ Registro de empates
- ✅ Ranking de goleadores
- ✅ MVP por partido
- ✅ Control de asistencia
- ✅ Exportación de datos

---

**⚽ Talaganchester United** - Sistema completo de gestión de partidos amateur
