# --- Editor de Puntajes por Posición ---
import json
import os

class EditorPuntajes:
    def __init__(self):
        self.archivo_base = 'jugadores.json'
        self.archivo_avanzado = 'jugadores_avanzado.json'
        self.cargar_datos()
    
    def cargar_datos(self):
        """Cargar datos de jugadores"""
        try:
            with open(self.archivo_base, 'r', encoding='utf-8') as f:
                self.jugadores_base = json.load(f)
        except FileNotFoundError:
            print(f"❌ Error: No se encontró {self.archivo_base}")
            self.jugadores_base = []
        
        try:
            with open(self.archivo_avanzado, 'r', encoding='utf-8') as f:
                self.jugadores_avanzado = json.load(f)
        except FileNotFoundError:
            print(f"⚠️  {self.archivo_avanzado} no encontrado, se creará uno nuevo")
            self.jugadores_avanzado = []
    
    def generar_puntajes_automaticos(self):
        """Generar puntajes automáticos basados en el archivo base"""
        jugadores_generados = []
        
        for jugador in self.jugadores_base:
            puntaje_base = jugador['puntaje']
            posiciones_naturales = [pos.strip().capitalize() for pos in jugador['posicion'].split(',')]
            
            # Calcular puntajes automáticos
            puntajes_posicion = {}
            
            for posicion in ['Arquero', 'Defensa', 'Mediocampo', 'Delantero']:
                if posicion in posiciones_naturales:
                    # Posición natural - bonus del 5-10%
                    bonus = 1.05 if len(posiciones_naturales) > 1 else 1.1
                    puntajes_posicion[posicion] = min(10.0, puntaje_base * bonus)
                else:
                    # Fuera de posición
                    if posicion == 'Arquero':
                        # Arqueros improvisados - muy baja puntuación
                        puntajes_posicion[posicion] = max(3.0, min(6.0, puntaje_base * 0.6))
                    else:
                        # Otras posiciones - penalización moderada
                        puntajes_posicion[posicion] = max(4.0, puntaje_base * 0.85)
            
            # Ajustes específicos por características
            if 'Arquero' in posiciones_naturales:
                # Bonus extra para arqueros naturales
                puntajes_posicion['Arquero'] = min(10.0, puntaje_base * 1.15)
            
            # Crear jugador avanzado
            jugador_avanzado = {
                "nombre": jugador['nombre'],
                "posicion": jugador['posicion'],
                "puntaje": puntaje_base,
                "puntajes_posicion": puntajes_posicion
            }
            jugadores_generados.append(jugador_avanzado)
        
        return jugadores_generados
    
    def mostrar_comparacion(self, jugador_base, jugador_avanzado=None):
        """Mostrar comparación de puntajes"""
        nombre = jugador_base['nombre']
        print(f"\n📊 {nombre} (General: {jugador_base['puntaje']:.1f})")
        print(f"   Posiciones naturales: {jugador_base['posicion']}")
        
        if jugador_avanzado and 'puntajes_posicion' in jugador_avanzado:
            print("   Puntajes por posición:")
            for pos in ['Arquero', 'Defensa', 'Mediocampo', 'Delantero']:
                puntaje = jugador_avanzado['puntajes_posicion'][pos]
                es_natural = pos.lower() in jugador_base['posicion'].lower()
                marca = "⭐" if es_natural else "  "
                print(f"     {marca} {pos:12}: {puntaje:.1f}")
        else:
            print("   Sin puntajes específicos definidos")
    
    def editar_jugador(self, nombre_jugador):
        """Editar puntajes de un jugador específico"""
        # Buscar jugador en datos base
        jugador_base = next((j for j in self.jugadores_base if j['nombre'].lower() == nombre_jugador.lower()), None)
        if not jugador_base:
            print(f"❌ Jugador '{nombre_jugador}' no encontrado")
            return False
        
        # Buscar en datos avanzados
        jugador_avanzado = next((j for j in self.jugadores_avanzado if j['nombre'] == jugador_base['nombre']), None)
        
        self.mostrar_comparacion(jugador_base, jugador_avanzado)
        
        print(f"\n✏️  Editando puntajes para {jugador_base['nombre']}:")
        print("   (Presiona Enter para mantener el valor actual)")
        
        # Obtener puntajes actuales o generar automáticos
        if jugador_avanzado and 'puntajes_posicion' in jugador_avanzado:
            puntajes_actuales = jugador_avanzado['puntajes_posicion'].copy()
        else:
            # Generar automáticamente
            puntajes_actuales = self.calcular_puntajes_automaticos(jugador_base)
        
        nuevos_puntajes = {}
        
        for posicion in ['Arquero', 'Defensa', 'Mediocampo', 'Delantero']:
            valor_actual = puntajes_actuales.get(posicion, jugador_base['puntaje'])
            es_natural = posicion.lower() in jugador_base['posicion'].lower()
            marca = "⭐" if es_natural else "  "
            
            while True:
                try:
                    entrada = input(f"   {marca} {posicion:12} [{valor_actual:.1f}]: ").strip()
                    if not entrada:
                        nuevos_puntajes[posicion] = valor_actual
                        break
                    else:
                        nuevo_valor = float(entrada)
                        if 0 <= nuevo_valor <= 10:
                            nuevos_puntajes[posicion] = nuevo_valor
                            break
                        else:
                            print("     ⚠️  El puntaje debe estar entre 0 y 10")
                except ValueError:
                    print("     ⚠️  Por favor ingresa un número válido")
        
        # Actualizar o crear jugador avanzado
        if jugador_avanzado:
            # Actualizar existente
            jugador_avanzado['puntajes_posicion'] = nuevos_puntajes
        else:
            # Crear nuevo
            nuevo_jugador = {
                "nombre": jugador_base['nombre'],
                "posicion": jugador_base['posicion'],
                "puntaje": jugador_base['puntaje'],
                "puntajes_posicion": nuevos_puntajes
            }
            self.jugadores_avanzado.append(nuevo_jugador)
        
        print(f"✅ Puntajes actualizados para {jugador_base['nombre']}")
        return True
    
    def calcular_puntajes_automaticos(self, jugador_base):
        """Calcular puntajes automáticos para un jugador"""
        puntaje_base = jugador_base['puntaje']
        posiciones_naturales = [pos.strip().capitalize() for pos in jugador_base['posicion'].split(',')]
        
        puntajes = {}
        for posicion in ['Arquero', 'Defensa', 'Mediocampo', 'Delantero']:
            if posicion in posiciones_naturales:
                bonus = 1.05 if len(posiciones_naturales) > 1 else 1.1
                puntajes[posicion] = min(10.0, puntaje_base * bonus)
            else:
                if posicion == 'Arquero':
                    puntajes[posicion] = max(3.0, min(6.0, puntaje_base * 0.6))
                else:
                    puntajes[posicion] = max(4.0, puntaje_base * 0.85)
        
        if 'Arquero' in posiciones_naturales:
            puntajes['Arquero'] = min(10.0, puntaje_base * 1.15)
        
        return puntajes
    
    def guardar_datos(self):
        """Guardar datos avanzados"""
        # Asegurar que todos los jugadores base estén en el avanzado
        nombres_avanzados = {j['nombre'] for j in self.jugadores_avanzado}
        
        for jugador_base in self.jugadores_base:
            if jugador_base['nombre'] not in nombres_avanzados:
                # Generar automáticamente
                puntajes_auto = self.calcular_puntajes_automaticos(jugador_base)
                nuevo_jugador = {
                    "nombre": jugador_base['nombre'],
                    "posicion": jugador_base['posicion'],
                    "puntaje": jugador_base['puntaje'],
                    "puntajes_posicion": puntajes_auto
                }
                self.jugadores_avanzado.append(nuevo_jugador)
        
        # Ordenar por nombre
        self.jugadores_avanzado.sort(key=lambda x: x['nombre'])
        
        # Guardar archivo
        with open(self.archivo_avanzado, 'w', encoding='utf-8') as f:
            json.dump(self.jugadores_avanzado, f, ensure_ascii=False, indent=2)
        
        print(f"✅ Datos guardados en {self.archivo_avanzado}")
    
    def menu_principal(self):
        """Menú principal del editor"""
        while True:
            print("\n" + "="*60)
            print("🔧 EDITOR DE PUNTAJES POR POSICIÓN")
            print("="*60)
            print("1. Generar puntajes automáticos desde jugadores.json")
            print("2. Editar puntajes de un jugador específico")
            print("3. Mostrar todos los jugadores y sus puntajes")
            print("4. Listar jugadores disponibles")
            print("5. Guardar cambios")
            print("6. Salir")
            
            try:
                opcion = input("\nSelecciona una opción (1-6): ").strip()
                
                if opcion == "1":
                    print("🔄 Generando puntajes automáticos...")
                    jugadores_generados = self.generar_puntajes_automaticos()
                    
                    # Preguntar si sobrescribir
                    if self.jugadores_avanzado:
                        sobrescribir = input("¿Sobrescribir puntajes existentes? (s/N): ").strip().lower()
                        if sobrescribir in ['s', 'si', 'sí', 'y', 'yes']:
                            self.jugadores_avanzado = jugadores_generados
                            print("✅ Puntajes generados y sobrescritos")
                        else:
                            print("❌ Operación cancelada")
                    else:
                        self.jugadores_avanzado = jugadores_generados
                        print("✅ Puntajes generados automáticamente")
                
                elif opcion == "2":
                    nombre = input("Nombre del jugador a editar: ").strip()
                    if nombre:
                        self.editar_jugador(nombre)
                
                elif opcion == "3":
                    print("\n📋 TODOS LOS JUGADORES Y SUS PUNTAJES:")
                    for jugador_base in sorted(self.jugadores_base, key=lambda x: x['nombre']):
                        jugador_avanzado = next((j for j in self.jugadores_avanzado if j['nombre'] == jugador_base['nombre']), None)
                        self.mostrar_comparacion(jugador_base, jugador_avanzado)
                
                elif opcion == "4":
                    print("\n👥 JUGADORES DISPONIBLES:")
                    for i, jugador in enumerate(sorted(self.jugadores_base, key=lambda x: x['nombre']), 1):
                        print(f"   {i:2d}. {jugador['nombre']:20} (General: {jugador['puntaje']:.1f}, Pos: {jugador['posicion']})")
                
                elif opcion == "5":
                    self.guardar_datos()
                
                elif opcion == "6":
                    # Preguntar si guardar antes de salir
                    if input("¿Guardar cambios antes de salir? (S/n): ").strip().lower() not in ['n', 'no']:
                        self.guardar_datos()
                    print("👋 ¡Hasta luego!")
                    break
                
                else:
                    print("❌ Opción inválida")
                    
            except KeyboardInterrupt:
                print("\n\n👋 ¡Hasta luego!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")

def main():
    """Función principal"""
    editor = EditorPuntajes()
    editor.menu_principal()

if __name__ == "__main__":
    main()
