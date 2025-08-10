# --- Sorteo Avanzado con Puntajes por Posición ---
import json
import random
import datetime
import locale
import unicodedata
from collections import defaultdict
import itertools

# Configurar localización
try:
    locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
except:
    try:
        locale.setlocale(locale.LC_TIME, 'Spanish_Spain')
    except:
        pass

class SorteoAvanzado:
    def __init__(self):
        self.jugadores_db = self.cargar_jugadores()
        self.puntajes_por_posicion = self.calcular_puntajes_posicion()
        self.formaciones = self.definir_formaciones()
        
    def cargar_jugadores(self):
        """Cargar base de datos de jugadores"""
        with open('jugadores.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def calcular_puntajes_posicion(self):
        """
        Calcular puntajes específicos por posición para cada jugador
        basado en su puntaje general y aptitud para cada posición
        """
        puntajes = {}
        
        # Factores de ajuste por posición según especialización
        factores_especializacion = {
            'Arquero': 1.0,      # Sin ajuste si es arquero natural
            'Defensa': 1.0,      # Sin ajuste si es defensa natural  
            'Mediocampo': 1.0,   # Sin ajuste si es mediocampo natural
            'Delantero': 1.0     # Sin ajuste si es delantero natural
        }
        
        # Penalizaciones por jugar fuera de posición natural
        penalizacion_fuera_posicion = 0.8  # 20% de reducción
        
        for jugador in self.jugadores_db:
            nombre = jugador['nombre']
            puntaje_base = jugador['puntaje']
            posiciones_naturales = [pos.strip().capitalize() for pos in jugador['posicion'].split(',')]
            
            puntajes[nombre] = {}
            
            # Calcular puntaje para cada posición
            for posicion in ['Arquero', 'Defensa', 'Mediocampo', 'Delantero']:
                if posicion in posiciones_naturales:
                    # Posición natural - puntaje completo
                    puntajes[nombre][posicion] = puntaje_base
                else:
                    # Fuera de posición - aplicar penalización
                    puntajes[nombre][posicion] = puntaje_base * penalizacion_fuera_posicion
            
            # Ajustes específicos por características del jugador
            # Arqueros: priorizar a los arqueros naturales
            if 'Arquero' in posiciones_naturales:
                puntajes[nombre]['Arquero'] = puntaje_base * 1.1  # Bonus arqueros naturales
            else:
                # Arqueros improvisados: preferir menor puntaje general
                puntajes[nombre]['Arquero'] = max(3.0, puntaje_base * 0.6)
        
        return puntajes
    
    def definir_formaciones(self):
        """Definir diferentes formaciones tácticas para equipos de 6 jugadores (1 arquero + 5 de campo)"""
        return {
            '2-2-1': {'Arquero': 1, 'Defensa': 2, 'Mediocampo': 2, 'Delantero': 1},  # Equilibrado
            '3-1-1': {'Arquero': 1, 'Defensa': 3, 'Mediocampo': 1, 'Delantero': 1},  # Defensivo
            '2-1-2': {'Arquero': 1, 'Defensa': 2, 'Mediocampo': 1, 'Delantero': 2},  # Ofensivo
            '1-3-1': {'Arquero': 1, 'Defensa': 1, 'Mediocampo': 3, 'Delantero': 1},  # Control medio
            '1-2-2': {'Arquero': 1, 'Defensa': 1, 'Mediocampo': 2, 'Delantero': 2},  # Ataque intenso
            '2-3-0': {'Arquero': 1, 'Defensa': 2, 'Mediocampo': 3, 'Delantero': 0},  # Solo mediocampo
        }
    
    def normalizar_nombre(self, nombre):
        """Normalizar nombres para comparación"""
        nombre = nombre.lower().replace(" ", "")
        return ''.join(c for c in unicodedata.normalize('NFD', nombre) 
                      if unicodedata.category(c) != 'Mn')
    
    def obtener_confirmados(self):
        """Obtener lista de jugadores confirmados"""
        # Leer confirmados
        with open('confirmados.txt', 'r', encoding='utf-8') as f:
            confirmados = [line.strip() for line in f if line.strip()]
        
        # Mapear a nombres oficiales
        jugadores_partido = []
        no_encontrados = []
        
        for nombre_confirmado in confirmados:
            encontrado = False
            for jugador in self.jugadores_db:
                if self.normalizar_nombre(nombre_confirmado) == self.normalizar_nombre(jugador["nombre"]):
                    jugadores_partido.append(jugador)
                    encontrado = True
                    break
            
            if not encontrado:
                no_encontrados.append(nombre_confirmado)
        
        if no_encontrados:
            print("⚠️  ATENCIÓN: Nombres no encontrados en la base de datos:")
            for nombre in no_encontrados:
                print(f"    - {nombre}")
            print()
        
        return jugadores_partido
    
    def calcular_promedio_equipo(self, equipo_asignado, formacion='4-4-2'):
        """
        Calcular promedio ponderado del equipo según formación y posiciones asignadas
        """
        total_puntos = 0
        total_jugadores = 0
        
        for jugador, posicion in equipo_asignado.items():
            puntaje_posicion = self.puntajes_por_posicion[jugador][posicion]
            total_puntos += puntaje_posicion
            total_jugadores += 1
        
        return total_puntos / total_jugadores if total_jugadores > 0 else 0
    
    def asignar_posiciones_optimas(self, jugadores, formacion='4-4-2'):
        """
        Asignar posiciones óptimas según la formación y maximizando el rendimiento
        """
        nombres_jugadores = [j['nombre'] for j in jugadores]
        posiciones_requeridas = []
        
        # Crear lista de posiciones requeridas según formación
        for posicion, cantidad in self.formaciones[formacion].items():
            posiciones_requeridas.extend([posicion] * cantidad)
        
        # Si hay más jugadores que posiciones, agregar como suplentes
        while len(posiciones_requeridas) < len(nombres_jugadores):
            posiciones_requeridas.append('Suplente')
        
        # Encontrar la mejor asignación usando optimización
        mejor_asignacion = None
        mejor_puntaje = 0
        
        # Probar diferentes permutaciones (limitado para rendimiento)
        for asignacion in itertools.permutations(posiciones_requeridas[:len(nombres_jugadores)]):
            puntaje_total = 0
            asignacion_actual = {}
            
            for i, jugador in enumerate(nombres_jugadores):
                posicion = asignacion[i]
                if posicion != 'Suplente':
                    puntaje_total += self.puntajes_por_posicion[jugador][posicion]
                    asignacion_actual[jugador] = posicion
                else:
                    # Para suplentes, usar la mejor posición del jugador
                    mejor_pos = max(self.puntajes_por_posicion[jugador].items(), key=lambda x: x[1])
                    asignacion_actual[jugador] = f"Suplente ({mejor_pos[0]})"
            
            if puntaje_total > mejor_puntaje:
                mejor_puntaje = puntaje_total
                mejor_asignacion = asignacion_actual.copy()
        
        return mejor_asignacion
    
    def generar_equipos_balanceados(self, jugadores_partido, formacion='2-2-1', intentos=5000):
        """
        Generar equipos balanceados considerando puntajes por posición
        """
        n_jugadores = len(jugadores_partido)
        if n_jugadores < 2:
            raise ValueError("Se necesitan al menos 2 jugadores para hacer equipos")
        
        tam_equipo = n_jugadores // 2
        mejor_diferencia = float('inf')
        mejor_equipo1 = None
        mejor_equipo2 = None
        mejor_asignacion1 = None
        mejor_asignacion2 = None
        
        print(f"🔄 Generando equipos balanceados ({intentos} intentos)...")
        
        for intento in range(intentos):
            # Mezclar jugadores aleatoriamente
            jugadores_mezclados = jugadores_partido.copy()
            random.shuffle(jugadores_mezclados)
            
            # Dividir en dos equipos
            equipo1 = jugadores_mezclados[:tam_equipo]
            equipo2 = jugadores_mezclados[tam_equipo:2*tam_equipo]
            
            # Asignar posiciones óptimas a cada equipo
            asignacion1 = self.asignar_posiciones_optimas(equipo1, formacion)
            asignacion2 = self.asignar_posiciones_optimas(equipo2, formacion)
            
            # Calcular promedios
            promedio1 = self.calcular_promedio_equipo(asignacion1, formacion)
            promedio2 = self.calcular_promedio_equipo(asignacion2, formacion)
            
            diferencia = abs(promedio1 - promedio2)
            
            if diferencia < mejor_diferencia:
                mejor_diferencia = diferencia
                mejor_equipo1 = equipo1.copy()
                mejor_equipo2 = equipo2.copy()
                mejor_asignacion1 = asignacion1.copy()
                mejor_asignacion2 = asignacion2.copy()
                
                # Si encontramos una diferencia muy pequeña, podemos parar
                if diferencia < 0.1:
                    break
        
        return {
            'equipo1': mejor_equipo1,
            'equipo2': mejor_equipo2,
            'asignacion1': mejor_asignacion1,
            'asignacion2': mejor_asignacion2,
            'promedio1': self.calcular_promedio_equipo(mejor_asignacion1, formacion),
            'promedio2': self.calcular_promedio_equipo(mejor_asignacion2, formacion),
            'diferencia': mejor_diferencia
        }
    
    def mostrar_resultados(self, resultado, formacion='2-2-1'):
        """Mostrar resultados del sorteo"""
        # Obtener datos del partido
        with open('partido.txt', 'r', encoding='utf-8') as f:
            datos_partido = dict(
                line.strip().split(':', 1) for line in f if ':' in line
            )
        
        fecha_str = datos_partido.get('fecha', '05/08').strip()
        hora_str = datos_partido.get('hora', '21:00').strip()
        cancha = datos_partido.get('cancha', 'Pasto Sintético').strip() or 'Pasto Sintético'
        
        # Formatear fecha
        dia, mes = map(int, fecha_str.split('/'))
        ano = datetime.datetime.now().year
        fecha_dt = datetime.datetime(ano, mes, dia)
        dia_semana = fecha_dt.strftime('%A').capitalize()
        mes_nombre = fecha_dt.strftime('%B').capitalize()
        fecha_partido = f"{dia_semana} {dia:02d} de {mes_nombre}"
        
        titulo = f"⚽ Partido {fecha_partido} - {hora_str} hrs - Cancha {cancha}"
        print(f"\n{titulo}")
        print(f"📋 Formación: {formacion}")
        print("=" * 80)
        
        # Mostrar Equipo Rojo
        print(f"\n🔴 EQUIPO ROJO (Promedio: {resultado['promedio1']:.2f}):")
        posiciones_orden = ['Arquero', 'Defensa', 'Mediocampo', 'Delantero']
        
        for posicion in posiciones_orden:
            jugadores_posicion = [j for j, p in resultado['asignacion1'].items() 
                                if p.startswith(posicion)]
            for jugador in jugadores_posicion:
                puntaje_posicion = self.puntajes_por_posicion[jugador][posicion]
                puntaje_general = next(j['puntaje'] for j in self.jugadores_db if j['nombre'] == jugador)
                print(f"  {posicion:12} - {jugador:15} ({puntaje_posicion:.1f} pts en posición, {puntaje_general:.1f} general)")
        
        # Mostrar suplentes si los hay
        suplentes1 = [j for j, p in resultado['asignacion1'].items() if p.startswith('Suplente')]
        for jugador in suplentes1:
            posicion_suplente = resultado['asignacion1'][jugador]
            puntaje_general = next(j['puntaje'] for j in self.jugadores_db if j['nombre'] == jugador)
            print(f"  {posicion_suplente:12} - {jugador:15} ({puntaje_general:.1f} pts)")
        
        # Mostrar Equipo Negro
        print(f"\n⚫ EQUIPO NEGRO (Promedio: {resultado['promedio2']:.2f}):")
        
        for posicion in posiciones_orden:
            jugadores_posicion = [j for j, p in resultado['asignacion2'].items() 
                                if p.startswith(posicion)]
            for jugador in jugadores_posicion:
                puntaje_posicion = self.puntajes_por_posicion[jugador][posicion]
                puntaje_general = next(j['puntaje'] for j in self.jugadores_db if j['nombre'] == jugador)
                print(f"  {posicion:12} - {jugador:15} ({puntaje_posicion:.1f} pts en posición, {puntaje_general:.1f} general)")
        
        # Mostrar suplentes si los hay
        suplentes2 = [j for j, p in resultado['asignacion2'].items() if p.startswith('Suplente')]
        for jugador in suplentes2:
            posicion_suplente = resultado['asignacion2'][jugador]
            puntaje_general = next(j['puntaje'] for j in self.jugadores_db if j['nombre'] == jugador)
            print(f"  {posicion_suplente:12} - {jugador:15} ({puntaje_general:.1f} pts)")
        
        print(f"\n📊 Diferencia de promedios: {resultado['diferencia']:.2f}")
        print("=" * 80)
    
    def guardar_resultados(self, resultado, formacion='2-2-1'):
        """Guardar resultados en equipos.json"""
        with open('partido.txt', 'r', encoding='utf-8') as f:
            datos_partido = dict(
                line.strip().split(':', 1) for line in f if ':' in line
            )
        
        fecha_str = datos_partido.get('fecha', '05/08').strip()
        hora_str = datos_partido.get('hora', '21:00').strip()
        cancha = datos_partido.get('cancha', 'Pasto Sintético').strip() or 'Pasto Sintético'
        
        # Formatear fecha
        dia, mes = map(int, fecha_str.split('/'))
        ano = datetime.datetime.now().year
        fecha_dt = datetime.datetime(ano, mes, dia)
        dia_semana = fecha_dt.strftime('%A').capitalize()
        mes_nombre = fecha_dt.strftime('%B').capitalize()
        fecha_partido = f"{dia_semana} {dia:02d} de {mes_nombre}"
        
        equipos_data = {
            "rojo": [j["nombre"] for j in resultado['equipo1']],
            "negro": [j["nombre"] for j in resultado['equipo2']],
            "rojo_posiciones": resultado['asignacion1'],
            "negro_posiciones": resultado['asignacion2'],
            "promedio_rojo": resultado['promedio1'],
            "promedio_negro": resultado['promedio2'],
            "diferencia_promedio": resultado['diferencia'],
            "formacion": formacion,
            "fecha": fecha_partido,
            "hora": hora_str,
            "cancha": cancha,
            "puntajes_por_posicion": True  # Indicador de que se usó el sistema avanzado
        }
        
        with open("equipos.json", "w", encoding="utf-8") as f:
            json.dump(equipos_data, f, ensure_ascii=False, indent=2)
        
        print(f"\n✅ Sorteo avanzado completado y guardado en equipos.json")

def main():
    """Función principal"""
    print("🚀 SORTEO AVANZADO CON PUNTAJES POR POSICIÓN")
    print("=" * 50)
    
    sorteo = SorteoAvanzado()
    
    # Obtener jugadores confirmados
    jugadores_partido = sorteo.obtener_confirmados()
    
    if len(jugadores_partido) < 2:
        print("❌ Error: Se necesitan al menos 2 jugadores confirmados")
        return
    
    print(f"👥 Jugadores confirmados: {len(jugadores_partido)}")
    for j in jugadores_partido:
        print(f"   - {j['nombre']} (General: {j['puntaje']:.1f})")
    print()
    
    # Seleccionar formación
    formaciones_disponibles = list(sorteo.formaciones.keys())
    print("📋 Formaciones disponibles:")
    for i, form in enumerate(formaciones_disponibles, 1):
        distribución = sorteo.formaciones[form]
        desc = f"{distribución['Defensa']}-{distribución['Mediocampo']}-{distribución['Delantero']}"
        print(f"   {i}. {form} ({desc})")
    
    try:
        seleccion = input(f"\nSelecciona formación (1-{len(formaciones_disponibles)}) [1]: ").strip()
        if not seleccion:
            seleccion = "1"
        indice = int(seleccion) - 1
        if 0 <= indice < len(formaciones_disponibles):
            formacion_elegida = formaciones_disponibles[indice]
        else:
            formacion_elegida = '2-2-1'
            print("⚠️  Selección inválida, usando 2-2-1")
    except ValueError:
        formacion_elegida = '2-2-1'
        print("⚠️  Selección inválida, usando 2-2-1")
    
    print(f"✅ Formación seleccionada: {formacion_elegida}")
    
    # Generar equipos
    resultado = sorteo.generar_equipos_balanceados(
        jugadores_partido, 
        formacion=formacion_elegida
    )
    
    # Mostrar y guardar resultados
    sorteo.mostrar_resultados(resultado, formacion_elegida)
    sorteo.guardar_resultados(resultado, formacion_elegida)
    
    # Actualizar HTML si es posible
    try:
        import subprocess
        subprocess.run(["python", "actualizar_html.py"], check=True)
        print("✅ Archivos HTML actualizados correctamente")
    except:
        print("⚠️  No se pudo actualizar automáticamente los archivos HTML")

if __name__ == "__main__":
    main()
