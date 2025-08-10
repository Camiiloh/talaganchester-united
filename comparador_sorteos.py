# --- Comparador de Métodos de Sorteo ---
import json
import subprocess
import os
from datetime import datetime

class ComparadorSorteos:
    def __init__(self):
        self.resultados = {}
        self.jugadores_confirmados = self.obtener_confirmados()
    
    def obtener_confirmados(self):
        """Obtener lista de jugadores confirmados"""
        try:
            with open('confirmados.txt', 'r', encoding='utf-8') as f:
                return [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            print("⚠️  Archivo confirmados.txt no encontrado")
            return []
    
    def ejecutar_sorteo(self, script_name, nombre_metodo):
        """Ejecutar un script de sorteo y capturar resultados"""
        print(f"🔄 Ejecutando {nombre_metodo}...")
        
        try:
            # Ejecutar script
            resultado = subprocess.run(
                ["python", script_name], 
                capture_output=True, 
                text=True, 
                encoding='utf-8',
                input="\n\n\n",  # Respuestas automáticas para inputs
                timeout=30
            )
            
            if resultado.returncode == 0:
                # Cargar resultados desde equipos.json
                try:
                    with open('equipos.json', 'r', encoding='utf-8') as f:
                        datos_equipos = json.load(f)
                    
                    # Renombrar archivo para preservar resultados
                    nuevo_nombre = f"equipos_{script_name.replace('.py', '')}.json"
                    os.rename('equipos.json', nuevo_nombre)
                    
                    self.resultados[nombre_metodo] = {
                        'datos': datos_equipos,
                        'archivo': nuevo_nombre,
                        'salida': resultado.stdout,
                        'error': None
                    }
                    print(f"✅ {nombre_metodo} completado")
                    
                except Exception as e:
                    self.resultados[nombre_metodo] = {
                        'datos': None,
                        'archivo': None,
                        'salida': resultado.stdout,
                        'error': f"Error leyendo resultados: {e}"
                    }
                    print(f"⚠️  {nombre_metodo} ejecutado pero error en resultados: {e}")
            else:
                self.resultados[nombre_metodo] = {
                    'datos': None,
                    'archivo': None,
                    'salida': resultado.stdout,
                    'error': resultado.stderr
                }
                print(f"❌ Error en {nombre_metodo}: {resultado.stderr}")
                
        except subprocess.TimeoutExpired:
            self.resultados[nombre_metodo] = {
                'datos': None,
                'archivo': None,
                'salida': "",
                'error': "Timeout - El script tardó demasiado"
            }
            print(f"⏰ {nombre_metodo} cancelado por timeout")
        
        except Exception as e:
            self.resultados[nombre_metodo] = {
                'datos': None,
                'archivo': None,
                'salida': "",
                'error': f"Error ejecutando: {e}"
            }
            print(f"❌ Error ejecutando {nombre_metodo}: {e}")
    
    def comparar_resultados(self):
        """Comparar resultados de todos los métodos"""
        print("\n" + "="*80)
        print("📊 COMPARACIÓN DE MÉTODOS DE SORTEO")
        print("="*80)
        
        # Mostrar información general
        print(f"👥 Jugadores confirmados: {len(self.jugadores_confirmados)}")
        print(f"📅 Fecha de comparación: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        # Tabla comparativa
        print("📋 RESUMEN COMPARATIVO:")
        print("-" * 80)
        print(f"{'Método':<25} {'Promedio Rojo':<15} {'Promedio Negro':<15} {'Diferencia':<12} {'Estado'}")
        print("-" * 80)
        
        for metodo, resultado in self.resultados.items():
            if resultado['datos']:
                datos = resultado['datos']
                prom_rojo = datos.get('promedio_rojo', 0)
                prom_negro = datos.get('promedio_negro', 0)
                diferencia = datos.get('diferencia_promedio', abs(prom_rojo - prom_negro))
                estado = "✅ OK"
            else:
                prom_rojo = prom_negro = diferencia = 0
                estado = "❌ Error"
            
            print(f"{metodo:<25} {prom_rojo:<15.3f} {prom_negro:<15.3f} {diferencia:<12.3f} {estado}")
        
        print("-" * 80)
        
        # Análisis detallado
        print("\n📈 ANÁLISIS DETALLADO:")
        
        metodos_exitosos = {k: v for k, v in self.resultados.items() if v['datos']}
        
        if metodos_exitosos:
            # Mejor balance
            mejor_balance = min(metodos_exitosos.items(), 
                              key=lambda x: x[1]['datos'].get('diferencia_promedio', float('inf')))
            
            print(f"🎯 Mejor balance: {mejor_balance[0]} (diferencia: {mejor_balance[1]['datos'].get('diferencia_promedio', 0):.3f})")
            
            # Comparar composición de equipos
            print("\n🔍 COMPOSICIÓN DE EQUIPOS:")
            
            for metodo, resultado in metodos_exitosos.items():
                datos = resultado['datos']
                print(f"\n{metodo}:")
                print(f"  🔴 Equipo Rojo: {', '.join(datos.get('rojo', []))}")
                print(f"  ⚫ Equipo Negro: {', '.join(datos.get('negro', []))}")
                
                # Mostrar formación si está disponible
                if 'formacion' in datos:
                    print(f"  📋 Formación: {datos['formacion']}")
                
                # Mostrar información adicional
                if 'puntajes_especificos' in datos:
                    tipo_puntaje = "Específicos por posición" if datos['puntajes_especificos'] else "Calculados automáticamente"
                    print(f"  📊 Puntajes: {tipo_puntaje}")
        
        # Mostrar errores si los hay
        metodos_con_error = {k: v for k, v in self.resultados.items() if v['error']}
        if metodos_con_error:
            print("\n❌ ERRORES ENCONTRADOS:")
            for metodo, resultado in metodos_con_error.items():
                print(f"  {metodo}: {resultado['error']}")
    
    def generar_reporte(self):
        """Generar reporte detallado en archivo"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        nombre_reporte = f"reporte_comparacion_{timestamp}.txt"
        
        with open(nombre_reporte, 'w', encoding='utf-8') as f:
            f.write("REPORTE DE COMPARACIÓN DE MÉTODOS DE SORTEO\n")
            f.write("=" * 50 + "\n\n")
            f.write(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Jugadores confirmados: {len(self.jugadores_confirmados)}\n")
            f.write(f"Lista de confirmados: {', '.join(self.jugadores_confirmados)}\n\n")
            
            for metodo, resultado in self.resultados.items():
                f.write(f"MÉTODO: {metodo}\n")
                f.write("-" * 30 + "\n")
                
                if resultado['datos']:
                    datos = resultado['datos']
                    f.write(f"Estado: Exitoso\n")
                    f.write(f"Promedio Rojo: {datos.get('promedio_rojo', 0):.3f}\n")
                    f.write(f"Promedio Negro: {datos.get('promedio_negro', 0):.3f}\n")
                    f.write(f"Diferencia: {datos.get('diferencia_promedio', 0):.3f}\n")
                    f.write(f"Equipo Rojo: {', '.join(datos.get('rojo', []))}\n")
                    f.write(f"Equipo Negro: {', '.join(datos.get('negro', []))}\n")
                    
                    if 'formacion' in datos:
                        f.write(f"Formación: {datos['formacion']}\n")
                    
                    f.write(f"Archivo generado: {resultado['archivo']}\n")
                else:
                    f.write(f"Estado: Error\n")
                    f.write(f"Error: {resultado['error']}\n")
                
                f.write("\n")
            
            # Agregar salidas de los scripts si están disponibles
            f.write("\nSALIDAS DETALLADAS DE LOS SCRIPTS:\n")
            f.write("=" * 40 + "\n\n")
            
            for metodo, resultado in self.resultados.items():
                if resultado['salida']:
                    f.write(f"SALIDA DE {metodo}:\n")
                    f.write("-" * 20 + "\n")
                    f.write(resultado['salida'])
                    f.write("\n\n")
        
        print(f"📄 Reporte detallado guardado en: {nombre_reporte}")
    
    def ejecutar_comparacion_completa(self):
        """Ejecutar comparación completa de todos los métodos"""
        print("🚀 INICIANDO COMPARACIÓN COMPLETA DE MÉTODOS DE SORTEO")
        print("=" * 60)
        
        if not self.jugadores_confirmados:
            print("❌ No hay jugadores confirmados. Agrega nombres a confirmados.txt")
            return
        
        # Lista de scripts a comparar
        scripts_disponibles = [
            ('sorteo_automatico.py', 'Sorteo Automático Original'),
            ('sorteo_partido.py', 'Sorteo de Partido'),
            ('sorteo_avanzado.py', 'Sorteo Avanzado'),
            ('sorteo_especializado.py', 'Sorteo Especializado')
        ]
        
        # Filtrar scripts que existen
        scripts_a_ejecutar = []
        for script, nombre in scripts_disponibles:
            if os.path.exists(script):
                scripts_a_ejecutar.append((script, nombre))
            else:
                print(f"⚠️  Script {script} no encontrado, se omitirá")
        
        if not scripts_a_ejecutar:
            print("❌ No se encontraron scripts de sorteo para comparar")
            return
        
        print(f"📋 Scripts a comparar: {len(scripts_a_ejecutar)}")
        for script, nombre in scripts_a_ejecutar:
            print(f"   - {nombre} ({script})")
        print()
        
        # Ejecutar cada script
        for script, nombre in scripts_a_ejecutar:
            self.ejecutar_sorteo(script, nombre)
            print()  # Línea en blanco entre ejecuciones
        
        # Mostrar comparación
        self.comparar_resultados()
        
        # Generar reporte
        generar_reporte = input("\n¿Generar reporte detallado en archivo? (S/n): ").strip().lower()
        if generar_reporte not in ['n', 'no']:
            self.generar_reporte()
        
        print("\n✅ Comparación completada")

def main():
    """Función principal"""
    comparador = ComparadorSorteos()
    
    print("🔍 COMPARADOR DE MÉTODOS DE SORTEO")
    print("=" * 40)
    print("Este script ejecutará todos los métodos de sorteo disponibles")
    print("y comparará sus resultados para ayudarte a elegir el mejor.")
    print()
    
    continuar = input("¿Continuar con la comparación? (S/n): ").strip().lower()
    if continuar in ['n', 'no']:
        print("👋 Comparación cancelada")
        return
    
    comparador.ejecutar_comparacion_completa()

if __name__ == "__main__":
    main()
