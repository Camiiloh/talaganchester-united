# TalAganchester United - Script de inicio del sistema
# PowerShell version

Write-Host ""
Write-Host "⚽ ========================================" -ForegroundColor Green
Write-Host "   TALAGANCHESTER UNITED - SISTEMA COMPLETO" -ForegroundColor Green  
Write-Host "========================================" -ForegroundColor Green
Write-Host ""

Write-Host "🚀 Iniciando servidores del sistema..." -ForegroundColor Yellow
Write-Host ""

# Función para verificar si un puerto está ocupado
function Test-Port {
    param([int]$Port)
    try {
        $listener = [System.Net.Sockets.TcpListener]::new([System.Net.IPAddress]::Any, $Port)
        $listener.Start()
        $listener.Stop()
        return $false
    }
    catch {
        return $true
    }
}

# Verificar puertos
$puertos = @{8080="Servidor Web"; 8083="Servidor Resultados"; 5000="Servidor Confirmaciones"}
foreach ($puerto in $puertos.Keys) {
    if (Test-Port $puerto) {
        Write-Host "⚠️  Puerto $puerto ocupado por otro proceso ($($puertos[$puerto]))" -ForegroundColor Yellow
    }
}

Write-Host "📡 1. Iniciando servidor web (puerto 8080)..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "python -m http.server 8080"
Start-Sleep 2

Write-Host "💾 2. Iniciando servidor de resultados (puerto 8083)..." -ForegroundColor Cyan  
Start-Process powershell -ArgumentList "-NoExit", "-Command", "python servidor_resultados.py"
Start-Sleep 2

Write-Host "🤖 3. Iniciando servidor de confirmaciones (puerto 5000)..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "python servidor_confirmaciones.py"
Start-Sleep 3

Write-Host ""
Write-Host "✅ Todos los servidores iniciados!" -ForegroundColor Green
Write-Host ""

Write-Host "🌐 URLs disponibles:" -ForegroundColor White
Write-Host "   • Página principal:     http://localhost:8080" -ForegroundColor Gray
Write-Host "   • Estadísticas:         http://localhost:8080/estadisticas.html" -ForegroundColor Gray
Write-Host "   • Cancha v2:           http://localhost:8080/cancha-v2.html" -ForegroundColor Gray
Write-Host "   • Cancha original:     http://localhost:8080/cancha.html" -ForegroundColor Gray
Write-Host ""

Write-Host "💡 Comandos útiles:" -ForegroundColor White
Write-Host "   • Sorteo:              python sorteo_posiciones_especificas.py" -ForegroundColor Gray
Write-Host "   • Confirmaciones:      python agregar_confirmaciones.py" -ForegroundColor Gray
Write-Host "   • Análisis:            python analizar_formacion.py" -ForegroundColor Gray
Write-Host "   • Test del sistema:    python test_simple.py" -ForegroundColor Gray
Write-Host ""

Write-Host "🛑 Para detener: Cierra las ventanas de PowerShell abiertas" -ForegroundColor Red
Write-Host ""

$abrir = Read-Host "🌍 ¿Abrir navegador automáticamente? (S/N)"
if ($abrir -eq "S" -or $abrir -eq "s") {
    Write-Host "🚀 Abriendo navegador..." -ForegroundColor Green
    Start-Process "http://localhost:8080"
}

Write-Host ""
Write-Host "🎉 ¡Sistema listo para usar!" -ForegroundColor Green
Write-Host ""
Write-Host "Presiona cualquier tecla para continuar..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
