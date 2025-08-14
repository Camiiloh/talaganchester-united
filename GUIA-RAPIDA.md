# 📝 GUÍA RÁPIDA: Actualizar Partido

## 🎯 Archivo principal: `jugadores_confirmados.txt`

Para actualizar un partido, solo edita este archivo con el formato:

```
FECHA: 2025-08-14
HORA: 22:00  
CANCHA: 1
---
Pablo
Maxi
Iván
Vicente
Ruben
Marco
Félix
Juan HG
Nel
Willians
Enrique
Diego
```

## 🚀 Pasos para actualizar:

1. **Edita `jugadores_confirmados.txt`** con la fecha, hora, cancha y jugadores
2. **Ejecuta**: `python agregar_confirmaciones.py`
3. **Ejecuta**: `python sorteo_posiciones_especificas.py`
4. **¡Listo!** Los títulos de todas las páginas se actualizan automáticamente

## 📋 Formato del archivo:

- **FECHA**: Formato YYYY-MM-DD (ej: 2025-08-14)
- **HORA**: Formato HH:MM (ej: 22:00)
- **CANCHA**: Número o nombre (ej: 1, 2, "Principal")
- **---**: Separador obligatorio
- **Jugadores**: Un jugador por línea

## ✅ Ejemplo completo:

```
FECHA: 2025-08-15
HORA: 21:30
CANCHA: 2
---
Erik
Riky
Pablo
Maxi
Nel
Willians
Enrique
Diego
Vicente
Marco
Camilo
Iván
```

**¡Solo edita el archivo y ejecuta los dos comandos!** 🎉
