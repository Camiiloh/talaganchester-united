# Script para calcular el promedio solo de las posiciones especificadas para cada jugador

$filePath = "jugadores_posiciones_especificas.json"

Write-Host "Cargando datos..." -ForegroundColor Green

# Leer y parsear el JSON
$jugadores = Get-Content $filePath -Raw -Encoding UTF8 | ConvertFrom-Json

Write-Host "`nCalculando promedios basados en posiciones especificas..." -ForegroundColor Green

# Para cada jugador, calcular el promedio solo de sus posiciones especificadas
foreach ($jugador in $jugadores) {
    # Obtener las posiciones especificadas y limpiarlas
    $posicionesStr = $jugador.posicion -replace ' ', ''  # Eliminar espacios
    $posicionesArray = $posicionesStr -split ','  # Separar por comas
    
    $valores = @()
    
    # Obtener el valor de cada posición especificada
    foreach ($pos in $posicionesArray) {
        $valor = $jugador.puntajes_posicion.$pos
        if ($valor -ne $null) {
            $valores += $valor
        }
    }
    
    # Calcular promedio
    if ($valores.Count -gt 0) {
        $promedio = ($valores | Measure-Object -Average).Average
        $jugador.puntaje = [math]::Round($promedio, 2)
        
        Write-Host "$($jugador.nombre) [$($jugador.posicion)]: $($jugador.puntaje)" -ForegroundColor Cyan
    }
}

# Guardar el archivo actualizado
$jugadores | ConvertTo-Json -Depth 10 | Set-Content $filePath -Encoding UTF8

Write-Host "`nArchivo actualizado correctamente!" -ForegroundColor Green
