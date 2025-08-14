@echo off
chcp 65001 >nul
echo.
echo ⚽ ========================================
echo    TALAGANCHESTER UNITED - SISTEMA COMPLETO
echo ========================================
echo.
echo 🚀 Iniciando servidores del sistema...
echo.

echo 📡 1. Iniciando servidor web (puerto 8080)...
start "Servidor Web" cmd /k "python -m http.server 8080"
timeout /t 2 >nul

echo 💾 2. Iniciando servidor de resultados (puerto 8083)...
start "Servidor Resultados" cmd /k "python servidor_resultados.py"
timeout /t 2 >nul

echo 🤖 3. Iniciando servidor de confirmaciones (puerto 5000)...
start "Servidor Confirmaciones" cmd /k "python servidor_confirmaciones.py"
timeout /t 3 >nul

echo.
echo ✅ Todos los servidores iniciados!
echo.
echo 🌐 URLs disponibles:
echo    • Página principal:     http://localhost:8080
echo    • Estadísticas:         http://localhost:8080/estadisticas.html  
echo    • Cancha v2:           http://localhost:8080/cancha-v2.html
echo    • Cancha original:     http://localhost:8080/cancha.html
echo.
echo 💡 Comandos útiles:
echo    • Sorteo:              python sorteo_posiciones_especificas.py
echo    • Confirmaciones:      python agregar_confirmaciones.py
echo    • Análisis:            python analizar_formacion.py
echo    • Test del sistema:    python test_simple.py
echo.
echo 🛑 Para detener: Cierra las ventanas de comando abiertas
echo.

echo 🌍 ¿Abrir navegador automáticamente? (S/N)
set /p abrir="Respuesta: "
if /i "%abrir%"=="S" (
    echo 🚀 Abriendo navegador...
    start http://localhost:8080
)

echo.
echo 🎉 ¡Sistema listo para usar!
pause
