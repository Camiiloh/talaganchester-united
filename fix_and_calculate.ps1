# Script para corregir el JSON y calcular promedios

$filePath = "jugadores_posiciones_especificas.json"

# Leer el contenido del archivo
$content = Get-Content $filePath -Raw -Encoding UTF8

# Corregir problemas de formato del JSON
$content = $content -replace '"puCB":\s*[\d.]+,\s*"\s*ntajes_posicion"', '"puntajes_posicion"'
$content = $content -replace '"puCB":\s*[\d.]+,\s*"\s*ntaje"', '"puntaje"'
$content = $content -replace '"poCB":\s*[\d.]+,\s*"\s*sicion"', '"posicion"'
$content = $content -replace '"noCB":\s*[\d.]+,\s*"\s*mbre"', '"nombre"'
$content = $content -replace '\}CB":\s*[\d.]+,\s*"\s*', '},'

# Guardar el JSON corregido
$content | Set-Content $filePath -Encoding UTF8 -NoNewline

Write-Host "JSON corregido. Cargando datos..." -ForegroundColor Green

# Parsear el JSON
$jugadores = $content | ConvertFrom-Json

Write-Host "`nCalculando promedios..." -ForegroundColor Green

# Para cada jugador, calcular el promedio de todas las posiciones
foreach ($jugador in $jugadores) {
    $posiciones = $jugador.puntajes_posicion
    
    # Asegurar que CB exista
    if (-not $posiciones.CB -and $posiciones.LCB -and $posiciones.RCB) {
        $posiciones | Add-Member -MemberType NoteProperty -Name CB -Value ([math]::Round(($posiciones.LCB + $posiciones.RCB) / 2, 2)) -Force
    }
    
    # Calcular promedio de todas las posiciones
    $valores = @($posiciones.GK, $posiciones.LCB, $posiciones.CB, $posiciones.RCB, $posiciones.LM, $posiciones.CM, $posiciones.RM, $posiciones.CF)
    $promedio = ($valores | Measure-Object -Average).Average
    $jugador.puntaje = [math]::Round($promedio, 2)
    
    Write-Host "$($jugador.nombre): $($jugador.puntaje)" -ForegroundColor Cyan
}

# Guardar el archivo actualizado
$jugadores | ConvertTo-Json -Depth 10 | Set-Content $filePath -Encoding UTF8

Write-Host "`n� Archivo actualizado correctamente con los promedios" -ForegroundColor Green
