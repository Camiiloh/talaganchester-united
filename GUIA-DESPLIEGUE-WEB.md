# 🚀 GUÍA DE DESPLIEGUE WEB

## 🎯 **PROBLEMA RESUELTO**
El `servidor_resultados.py` original no funcionaba en despliegue web porque:
- ❌ Usaba subprocess (no permitido en hosting)
- ❌ Solo funcionaba en localhost
- ❌ No tenía CORS configurado

## ✅ **SOLUCIONES IMPLEMENTADAS**

### **Opción 1: Servidor Todo-en-Uno (RECOMENDADO)**
Un solo servidor que maneja TODO:
```bash
python servidor_todo_en_uno.py
```
- ✅ Sirve archivos HTML/CSS/JS
- ✅ API para guardar resultados
- ✅ Funciona en cualquier hosting
- ✅ Puerto configurable via variable de entorno

### **Opción 2: Servidor Web Mejorado**
Solo API, necesita servidor web separado:
```bash
python servidor_web.py
```

### **Opción 3: JavaScript con Fallback Automático**
El frontend detecta automáticamente dónde está la API:
- ✅ Prueba localhost:8083 primero
- ✅ Fallback a /api/ en mismo dominio
- ✅ Configuración automática

## 🌐 **DESPLIEGUE EN DIFERENTES PLATAFORMAS**

### **🔥 Heroku (Gratis)**
```bash
# 1. Crear cuenta en heroku.com
# 2. Instalar Heroku CLI
# 3. En tu proyecto:
git init
git add .
git commit -m "Deploy TalAganchester"
heroku create tu-app-name
git push heroku main
```

### **🚂 Railway (Fácil)**
```bash
# 1. Conectar GitHub a railway.app
# 2. El Procfile se detecta automáticamente
# 3. Se despliega automáticamente
```

### **▲ Vercel (Frontend + API)**
```bash
# 1. Conectar GitHub a vercel.com
# 2. Configurar build:
#    - Framework: Other
#    - Build Command: (vacío)
#    - Output: ./
```

### **🌊 Netlify (Solo Frontend)**
Para solo archivos estáticos + serverless functions

### **☁️ AWS/Google Cloud/Azure**
Usar el `servidor_todo_en_uno.py` con gunicorn

## ⚙️ **CONFIGURACIÓN DE ARCHIVOS**

### **requirements.txt** ✅
```
Flask==3.0.0
Flask-CORS==4.0.0
gunicorn==21.2.0
```

### **Procfile** ✅
```
web: python servidor_todo_en_uno.py
```

### **runtime.txt** (opcional)
```
python-3.11.0
```

## 🔧 **CONFIGURACIÓN DE PRODUCCIÓN**

### **Variables de Entorno**
```bash
PORT=8080              # Puerto del servidor
FLASK_ENV=production   # Modo producción
```

### **Para Hosting Compartido**
Si tu hosting solo permite archivos estáticos:
1. Usar GitHub Pages/Netlify para frontend
2. Usar Railway/Heroku para API
3. Configurar CORS en la API

## 🛠️ **COMANDOS ÚTILES**

### **Local (Desarrollo)**
```bash
# Servidor todo-en-uno
python servidor_todo_en_uno.py

# O servidor separados
python -m http.server 8080        # Frontend
python servidor_web.py            # API
```

### **Producción Local**
```bash
# Con gunicorn (más robusto)
pip install gunicorn
gunicorn servidor_todo_en_uno:app --bind 0.0.0.0:8080
```

### **Docker (Avanzado)**
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8080
CMD ["python", "servidor_todo_en_uno.py"]
```

## 🧪 **PRUEBAS**

### **Test Local**
```bash
python test_simple.py
```

### **Test API**
```bash
curl -X POST http://localhost:8080/api/guardar-resultado \
  -H "Content-Type: application/json" \
  -d '{"fecha":"2025-08-13","equipo_ganador":"Rojo"}'
```

### **Test Frontend**
1. Abrir http://localhost:8080/estadisticas.html
2. Hacer login como admin
3. Agregar un partido
4. Verificar que se guarde

## 🔄 **MIGRACIÓN DESDE SISTEMA ANTERIOR**

El nuevo sistema es **100% compatible**:
- ✅ Usa los mismos archivos JSON
- ✅ Misma interfaz de usuario
- ✅ Mismas funcionalidades
- ✅ + Despliegue web
- ✅ + API mejorada
- ✅ + Fallback automático

## 📈 **MONITOREO**

### **Health Check**
```
GET /api/health
```

### **Logs**
```bash
# Ver logs en tiempo real (Heroku)
heroku logs --tail

# Ver logs (Railway)
# Desde el dashboard web
```

---

## 🎉 **¡LISTO PARA PRODUCCIÓN!**

**Recomendación**: Usar `servidor_todo_en_uno.py` + Railway para despliegue más fácil.

**URL de ejemplo**: https://tu-app.railway.app
