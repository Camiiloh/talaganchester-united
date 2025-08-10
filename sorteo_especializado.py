# --- Sorteo con Puntajes Específicos por Posición ---
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

class SorteoEspecializado:
    def __init__(self, usar_puntajes_especificos=True):
        self.usar_puntajes_especificos = usar_puntajes_especificos
        self.jugadores_db = self.cargar_jugadores()
        
    def cargar_jugadores(self):
        """Cargar base de datos de jugadores con puntajes específicos"""
        if self.usar_puntajes_especificos:
            try:
                with open('jugadores_avanzado.json', 'r', encoding='utf-8') as f:
                    return json.load(f)
            except FileNotFoundError:
                print("⚠️  Archivo jugadores_avanzado.json no encontrado, usando jugadores.json")
                self.usar_puntajes_especificos = False
        
        # Cargar archivo normal si no se puede usar el avanzado
        with open('jugadores.json', 'r', encoding='utf-8') as f:
            jugadores_normales = json.load(f)
            
        # Convertir al formato avanzado automáticamente
        return self.convertir_a_formato_avanzado(jugadores_normales)
    
    def convertir_a_formato_avanzado(self, jugadores_normales):
        """Convertir jugadores del formato normal al avanzado"""
        jugadores_avanzados = []
        
        for jugador in jugadores_normales:
            puntaje_base = jugador['puntaje']
            posiciones_naturales = [pos.strip().capitalize() for pos in jugador['posicion'].split(',')]
            
            # Calcular puntajes por posición
            puntajes_posicion = {}
            for posicion in ['Arquero', 'Defensa', 'Mediocampo', 'Delantero']:
                if posicion in posiciones_naturales:
                    # Posición natural - puntaje completo con ligero bonus
                    puntajes_posicion[posicion] = min(10.0, puntaje_base * 1.05)
                else:
                    # Fuera de posición - penalización
                    factor_penalizacion = 0.75 if posicion == 'Arquero' else 0.85
                    puntajes_posicion[posicion] = max(3.0, puntaje_base * factor_penalizacion)
            
            # Ajustes específicos
            if 'Arquero' in posiciones_naturales:
                puntajes_posicion['Arquero'] = min(10.0, puntaje_base * 1.15)
            else:
                puntajes_posicion['Arquero'] = max(3.0, min(6.0, puntaje_base * 0.6))
            
            jugador_avanzado = {
                "nombre": jugador['nombre'],
                "posicion": jugador['posicion'],
                "puntaje": puntaje_base,
                "puntajes_posicion": puntajes_posicion
            }
            jugadores_avanzados.append(jugador_avanzado)
        
        return jugadores_avanzados
    
    def generar_formacion_inteligente(self, jugadores):
        """
        Generar una formación que se adapte mejor a las fortalezas de los jugadores
        Garantiza: 1 arquero + al menos 1 en cada posición de campo (defensa, mediocampo, delantero)
        """
        # Verificar si hay buenos arqueros en el equipo
        mejores_arqueros = []
        for jugador in jugadores:
            puntaje_arquero = self.obtener_puntaje_posicion(jugador, 'Arquero')
            mejores_arqueros.append((jugador['nombre'], puntaje_arquero))
        
        mejores_arqueros.sort(key=lambda x: x[1], reverse=True)
        mejor_arquero_puntaje = mejores_arqueros[0][1] if mejores_arqueros else 0
        
        # Analizar las fortalezas del equipo en posiciones de campo
        fortalezas = {'Defensa': 0, 'Mediocampo': 0, 'Delantero': 0}
        
        for jugador in jugadores:
            if 'puntajes_posicion' in jugador:
                for pos in ['Defensa', 'Mediocampo', 'Delantero']:
                    fortalezas[pos] += jugador['puntajes_posicion'][pos]
            else:
                # Si no tiene puntajes específicos, usar posiciones naturales
                posiciones_naturales = [p.strip().capitalize() for p in jugador['posicion'].split(',')]
                for pos in posiciones_naturales:
                    if pos in fortalezas:
                        fortalezas[pos] += jugador['puntaje']
        
        # Ordenar posiciones por fortaleza
        posiciones_ordenadas = sorted(fortalezas.items(), key=lambda x: x[1], reverse=True)
        
        # PASO 1: Formación base garantizada - 1 arquero + al menos 1 en cada posición
        formacion = {
            'Arquero': 1,
            'Defensa': 1,
            'Mediocampo': 1, 
            'Delantero': 1
        }
        
        # Ya hemos asignado 4 jugadores (1 + 1 + 1 + 1), quedan 2 por distribuir
        jugadores_extra = 2
        
        # PASO 2: Distribuir los 2 jugadores restantes según fortalezas
        # Si tenemos un buen arquero (6.5+), podemos ser más agresivos
        factor_agresividad = 1.2 if mejor_arquero_puntaje >= 6.5 else 1.0
        
        # Distribuir los jugadores extra priorizando fortalezas
        for i, (posicion, fortaleza) in enumerate(posiciones_ordenadas):
            if jugadores_extra <= 0:
                break
                
            if i == 0:  # Posición más fuerte
                # Agregar 1-2 jugadores extra a la posición más fuerte
                if posicion == 'Delantero' and factor_agresividad > 1.0:
                    # Si somos fuertes en ataque y tenemos buen arquero, más agresivos
                    extra = min(2, jugadores_extra) if random.random() > 0.3 else 1
                else:
                    extra = min(2, jugadores_extra) if random.random() > 0.5 else 1
                    
                formacion[posicion] += extra
                jugadores_extra -= extra
                
            elif i == 1 and jugadores_extra > 0:  # Segunda posición más fuerte
                # Posibilidad de agregar 1 jugador más
                if random.random() > 0.4:
                    formacion[posicion] += 1
                    jugadores_extra -= 1
        
        # PASO 3: Si aún quedan jugadores, agregarlos a la posición más fuerte
        if jugadores_extra > 0:
            pos_fuerte = posiciones_ordenadas[0][0]
            formacion[pos_fuerte] += jugadores_extra
        
        # PASO 4: Verificación final - asegurar límites razonables
        # Ninguna posición debería tener más de 3 jugadores (excepto casos extremos)
        for pos in ['Defensa', 'Mediocampo', 'Delantero']:
            if formacion[pos] > 3:
                # Redistribuir el exceso
                exceso = formacion[pos] - 3
                formacion[pos] = 3
                
                # Buscar dónde poner el exceso
                for otra_pos in ['Defensa', 'Mediocampo', 'Delantero']:
                    if otra_pos != pos and formacion[otra_pos] < 3 and exceso > 0:
                        puede_recibir = min(exceso, 3 - formacion[otra_pos])
                        formacion[otra_pos] += puede_recibir
                        exceso -= puede_recibir
        
        # Verificación final: debe sumar exactamente 6 jugadores
        total = sum(formacion.values())
        if total != 6:
            # Ajuste de emergencia
            diferencia = 6 - total
            if diferencia > 0:
                # Faltan jugadores, agregar al mediocampo
                formacion['Mediocampo'] += diferencia
            elif diferencia < 0:
                # Sobran jugadores, quitar del mediocampo primero
                formacion['Mediocampo'] = max(1, formacion['Mediocampo'] + diferencia)
        
        return formacion
    
    def formacion_a_string(self, formacion_dict):
        """Convertir diccionario de formación a string legible"""
        defensa = formacion_dict.get('Defensa', 0)
        mediocampo = formacion_dict.get('Mediocampo', 0) 
        delantero = formacion_dict.get('Delantero', 0)
        return f"{defensa}-{mediocampo}-{delantero}"
    
    def normalizar_nombre(self, nombre):
        """Normalizar nombres para comparación"""
        nombre = nombre.lower().replace(" ", "")
        return ''.join(c for c in unicodedata.normalize('NFD', nombre) 
                      if unicodedata.category(c) != 'Mn')
    
    def obtener_confirmados(self):
        """Obtener lista de jugadores confirmados"""
        try:
            with open('confirmados.txt', 'r', encoding='utf-8') as f:
                confirmados = [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            print("⚠️  Archivo confirmados.txt no encontrado")
            return []
        
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
    
    def obtener_puntaje_posicion(self, jugador, posicion):
        """Obtener puntaje específico de un jugador en una posición"""
        if 'puntajes_posicion' in jugador:
            return jugador['puntajes_posicion'].get(posicion, jugador['puntaje'] * 0.8)
        else:
            # Fallback al puntaje general
            return jugador['puntaje']
    
    def calcular_promedio_equipo(self, equipo_asignado):
        """Calcular promedio ponderado del equipo según posiciones asignadas"""
        total_puntos = 0
        total_jugadores = 0
        
        for jugador_info, posicion in equipo_asignado.items():
            # Encontrar el jugador en la base de datos
            jugador_data = next((j for j in self.jugadores_db if j['nombre'] == jugador_info), None)
            if jugador_data:
                # Extraer posición base si es suplente
                pos_base = posicion.split('(')[1].split(')')[0] if 'Suplente' in posicion else posicion
                puntaje = self.obtener_puntaje_posicion(jugador_data, pos_base)
                total_puntos += puntaje
                total_jugadores += 1
        
        return total_puntos / total_jugadores if total_jugadores > 0 else 0
    
    def asignar_posiciones_optimas(self, jugadores, formacion_dict):
        """
        Asignar posiciones optimizando para que cada jugador esté en su mejor posición posible
        Prioriza especialmente a los mejores arqueros para la portería
        """
        if not formacion_dict:  # Formación libre
            # Asignación libre - usar directamente las mejores posiciones
            asignacion = {}
            for jugador in jugadores:
                if 'puntajes_posicion' in jugador:
                    mejor_pos = max(jugador['puntajes_posicion'].items(), key=lambda x: x[1])
                    asignacion[jugador['nombre']] = mejor_pos[0]
                else:
                    primera_pos = jugador['posicion'].split(',')[0].strip().capitalize()
                    asignacion[jugador['nombre']] = primera_pos
            return asignacion
        
        asignacion = {}
        jugadores_asignados = set()
        
        # PASO 1: Asignar arquero con la mejor puntuación en esa posición
        if formacion_dict.get('Arquero', 0) > 0:
            # Crear lista de candidatos a arquero con sus puntajes
            candidatos_arquero = []
            for jugador in jugadores:
                puntaje_arquero = self.obtener_puntaje_posicion(jugador, 'Arquero')
                candidatos_arquero.append((jugador['nombre'], puntaje_arquero))
            
            # Ordenar por puntaje de arquero descendente
            candidatos_arquero.sort(key=lambda x: x[1], reverse=True)
            
            # Asignar al mejor arquero disponible
            if candidatos_arquero:
                mejor_arquero = candidatos_arquero[0][0]
                asignacion[mejor_arquero] = 'Arquero'
                jugadores_asignados.add(mejor_arquero)
                print(f"   🥅 Arquero asignado: {mejor_arquero} ({candidatos_arquero[0][1]:.1f} pts)")
        
        # PASO 2: Crear lista de preferencias para jugadores restantes
        preferencias_jugadores = {}
        jugadores_restantes = [j for j in jugadores if j['nombre'] not in jugadores_asignados]
        
        for jugador in jugadores_restantes:
            nombre = jugador['nombre']
            preferencias = []
            # Solo considerar posiciones de campo (no arquero, ya asignado)
            for posicion in ['Defensa', 'Mediocampo', 'Delantero']:
                puntaje = self.obtener_puntaje_posicion(jugador, posicion)
                preferencias.append((posicion, puntaje))
            # Ordenar por puntaje descendente (mejor posición primero)
            preferencias.sort(key=lambda x: x[1], reverse=True)
            preferencias_jugadores[nombre] = preferencias
        
        # PASO 3: Crear lista de posiciones disponibles (sin arquero)
        posiciones_disponibles = []
        for posicion, cantidad in formacion_dict.items():
            if posicion != 'Arquero':  # Ya asignado
                posiciones_disponibles.extend([posicion] * cantidad)
        
        # PASO 4: Asignar posiciones de campo optimizando rendimiento total
        mejor_asignacion_campo = None
        mejor_puntaje_total = 0
        
        nombres_restantes = [j['nombre'] for j in jugadores_restantes]
        
        # Probar diferentes órdenes de asignación
        for _ in range(150):  # Más intentos para mejor optimización
            random.shuffle(nombres_restantes)
            posiciones_temp = posiciones_disponibles.copy()
            random.shuffle(posiciones_temp)
            
            asignacion_campo = {}
            puntaje_total = 0
            posiciones_usadas = posiciones_temp.copy()
            
            # Asignar cada jugador a su mejor posición disponible
            for nombre in nombres_restantes:
                mejor_opcion = None
                mejor_puntaje = -1
                mejor_indice = -1
                
                # Buscar la mejor posición disponible para este jugador
                for pos, puntaje in preferencias_jugadores[nombre]:
                    try:
                        indice = posiciones_usadas.index(pos)
                        if puntaje > mejor_puntaje:
                            mejor_opcion = pos
                            mejor_puntaje = puntaje
                            mejor_indice = indice
                    except ValueError:
                        continue  # Esta posición ya no está disponible
                
                if mejor_opcion:
                    asignacion_campo[nombre] = mejor_opcion
                    puntaje_total += mejor_puntaje
                    posiciones_usadas.pop(mejor_indice)
                else:
                    # Si no hay posiciones disponibles, asignar como suplente
                    mejor_pos_jugador = preferencias_jugadores[nombre][0][0]
                    asignacion_campo[nombre] = f"Suplente ({mejor_pos_jugador})"
            
            if puntaje_total > mejor_puntaje_total:
                mejor_puntaje_total = puntaje_total
                mejor_asignacion_campo = asignacion_campo.copy()
        
        # PASO 5: Combinar asignaciones
        if mejor_asignacion_campo:
            asignacion.update(mejor_asignacion_campo)
        
        return asignacion
    
    def generar_equipos_balanceados(self, jugadores_partido, intentos=10000):
        """Generar equipos balanceados con formaciones aleatorias independientes"""
        n_jugadores = len(jugadores_partido)
        if n_jugadores < 2:
            raise ValueError("Se necesitan al menos 2 jugadores para hacer equipos")
        
        tam_equipo = n_jugadores // 2
        mejor_diferencia = float('inf')
        mejor_resultado = None
        
        print(f"🔄 Generando equipos balanceados con formaciones inteligentes ({intentos} intentos)...")
        
        for intento in range(intentos):
            # Mezclar jugadores aleatoriamente
            jugadores_mezclados = jugadores_partido.copy()
            random.shuffle(jugadores_mezclados)
            
            # Dividir en dos equipos
            equipo1 = jugadores_mezclados[:tam_equipo]
            equipo2 = jugadores_mezclados[tam_equipo:2*tam_equipo]
            
            # Generar formaciones inteligentes basadas en las fortalezas de cada equipo
            formacion1 = self.generar_formacion_inteligente(equipo1)
            formacion2 = self.generar_formacion_inteligente(equipo2)
            
            # Asignar posiciones según las formaciones específicas (optimizando rendimiento)
            asignacion1 = self.asignar_posiciones_optimas(equipo1, formacion1)
            asignacion2 = self.asignar_posiciones_optimas(equipo2, formacion2)
            
            # Calcular promedios
            promedio1 = self.calcular_promedio_equipo(asignacion1)
            promedio2 = self.calcular_promedio_equipo(asignacion2)
            
            diferencia = abs(promedio1 - promedio2)
            
            if diferencia < mejor_diferencia:
                mejor_diferencia = diferencia
                mejor_resultado = {
                    'equipo1': equipo1.copy(),
                    'equipo2': equipo2.copy(),
                    'asignacion1': asignacion1.copy(),
                    'asignacion2': asignacion2.copy(),
                    'formacion1': formacion1.copy(),
                    'formacion2': formacion2.copy(),
                    'promedio1': promedio1,
                    'promedio2': promedio2,
                    'diferencia': diferencia
                }
                
                # Si encontramos una diferencia muy pequeña, podemos parar
                if diferencia < 0.05:
                    break
            
            # Mostrar progreso cada 1000 intentos
            if (intento + 1) % 1000 == 0:
                print(f"   Intento {intento + 1}/{intentos} - Mejor diferencia: {mejor_diferencia:.3f}")
        
        return mejor_resultado
    
    def mostrar_analisis_jugadores(self, jugadores_partido):
        """Mostrar análisis de puntajes por posición de los jugadores"""
        print("\n📊 ANÁLISIS DE JUGADORES POR POSICIÓN:")
        print("=" * 80)
        
        for jugador in sorted(jugadores_partido, key=lambda x: x['puntaje'], reverse=True):
            print(f"\n{jugador['nombre']} (General: {jugador['puntaje']:.1f}):")
            if 'puntajes_posicion' in jugador:
                for pos in ['Arquero', 'Defensa', 'Mediocampo', 'Delantero']:
                    puntaje_pos = jugador['puntajes_posicion'][pos]
                    es_natural = pos.lower() in jugador['posicion'].lower()
                    marca = "⭐" if es_natural else "  "
                    print(f"  {marca} {pos:12}: {puntaje_pos:.1f}")
            else:
                print("  Sin puntajes específicos por posición")
        print("=" * 80)
    
    def mostrar_resultados(self, resultado):
        """Mostrar resultados del sorteo"""
        # Obtener datos del partido
        try:
            with open('partido.txt', 'r', encoding='utf-8') as f:
                datos_partido = dict(
                    line.strip().split(':', 1) for line in f if ':' in line
                )
        except FileNotFoundError:
            datos_partido = {}
        
        fecha_str = datos_partido.get('fecha', '05/08').strip()
        hora_str = datos_partido.get('hora', '21:00').strip()
        cancha = datos_partido.get('cancha', 'Pasto Sintético').strip() or 'Pasto Sintético'
        
        # Formatear fecha
        try:
            dia, mes = map(int, fecha_str.split('/'))
            ano = datetime.datetime.now().year
            fecha_dt = datetime.datetime(ano, mes, dia)
            dia_semana = fecha_dt.strftime('%A').capitalize()
            mes_nombre = fecha_dt.strftime('%B').capitalize()
            fecha_partido = f"{dia_semana} {dia:02d} de {mes_nombre}"
        except:
            fecha_partido = fecha_str
        
        titulo = f"⚽ Partido {fecha_partido} - {hora_str} hrs - Cancha {cancha}"
        subtitulo = f"📋 Formaciones Inteligentes y Balanceadas {'(Puntajes Específicos)' if self.usar_puntajes_especificos else '(Puntajes Calculados)'}"
        
        # Obtener formaciones como strings
        form1_str = self.formacion_a_string(resultado['formacion1'])
        form2_str = self.formacion_a_string(resultado['formacion2'])
        
        print(f"\n{titulo}")
        print(subtitulo)
        print("=" * 80)
        
        # Función auxiliar para mostrar equipo
        def mostrar_equipo(nombre_equipo, equipo_jugadores, asignaciones, promedio, emoji, formacion_str):
            print(f"\n{emoji} {nombre_equipo} - Formación {formacion_str} (Promedio: {promedio:.2f}):")
            
            # Agrupar por posición
            posiciones_mostradas = set()
            for posicion_orden in ['Arquero', 'Defensa', 'Mediocampo', 'Delantero']:
                jugadores_posicion = [(j, p) for j, p in asignaciones.items() 
                                    if p == posicion_orden and j not in posiciones_mostradas]
                
                for jugador_nombre, posicion in jugadores_posicion:
                    jugador_data = next((j for j in self.jugadores_db if j['nombre'] == jugador_nombre), None)
                    if jugador_data:
                        puntaje_posicion = self.obtener_puntaje_posicion(jugador_data, posicion)
                        puntaje_general = jugador_data['puntaje']
                        es_natural = posicion.lower() in jugador_data['posicion'].lower()
                        marca = "⭐" if es_natural else "  "
                        print(f"  {marca}{posicion:12} - {jugador_nombre:15} "
                              f"({puntaje_posicion:.1f} pts en pos, {puntaje_general:.1f} general)")
                        posiciones_mostradas.add(jugador_nombre)
            
            # Mostrar suplentes
            suplentes = [(j, p) for j, p in asignaciones.items() 
                        if p.startswith('Suplente') and j not in posiciones_mostradas]
            for jugador_nombre, posicion_suplente in suplentes:
                jugador_data = next((j for j in self.jugadores_db if j['nombre'] == jugador_nombre), None)
                if jugador_data:
                    puntaje_general = jugador_data['puntaje']
                    print(f"  {posicion_suplente:12} - {jugador_nombre:15} ({puntaje_general:.1f} pts)")
        
        # Mostrar equipos
        mostrar_equipo("EQUIPO ROJO", resultado['equipo1'], resultado['asignacion1'], 
                      resultado['promedio1'], "🔴", form1_str)
        
        mostrar_equipo("EQUIPO NEGRO", resultado['equipo2'], resultado['asignacion2'], 
                      resultado['promedio2'], "⚫", form2_str)
        
        print(f"\n📊 Diferencia de promedios: {resultado['diferencia']:.3f}")
        print(f"🎲 Formaciones: Rojo {form1_str} vs Negro {form2_str}")
        print("=" * 80)
    
    def guardar_resultados(self, resultado):
        """Guardar resultados en equipos.json"""
        try:
            with open('partido.txt', 'r', encoding='utf-8') as f:
                datos_partido = dict(
                    line.strip().split(':', 1) for line in f if ':' in line
                )
        except FileNotFoundError:
            datos_partido = {}
        
        fecha_str = datos_partido.get('fecha', '05/08').strip()
        hora_str = datos_partido.get('hora', '21:00').strip()
        cancha = datos_partido.get('cancha', 'Pasto Sintético').strip() or 'Pasto Sintético'
        
        try:
            dia, mes = map(int, fecha_str.split('/'))
            ano = datetime.datetime.now().year
            fecha_dt = datetime.datetime(ano, mes, dia)
            dia_semana = fecha_dt.strftime('%A').capitalize()
            mes_nombre = fecha_dt.strftime('%B').capitalize()
            fecha_partido = f"{dia_semana} {dia:02d} de {mes_nombre}"
        except:
            fecha_partido = fecha_str
        
        # Convertir formaciones a strings legibles
        form1_str = self.formacion_a_string(resultado['formacion1'])
        form2_str = self.formacion_a_string(resultado['formacion2'])
        
        equipos_data = {
            "rojo": [j["nombre"] for j in resultado['equipo1']],
            "negro": [j["nombre"] for j in resultado['equipo2']],
            "rojo_posiciones": resultado['asignacion1'],
            "negro_posiciones": resultado['asignacion2'],
            "rojo_formacion": resultado['formacion1'],
            "negro_formacion": resultado['formacion2'],
            "rojo_formacion_str": form1_str,
            "negro_formacion_str": form2_str,
            "promedio_rojo": resultado['promedio1'],
            "promedio_negro": resultado['promedio2'],
            "diferencia_promedio": resultado['diferencia'],
            "formaciones_inteligentes_balanceadas": True,
            "puntajes_especificos": self.usar_puntajes_especificos,
            "fecha": fecha_partido,
            "hora": hora_str,
            "cancha": cancha
        }
        
        with open("equipos.json", "w", encoding="utf-8") as f:
            json.dump(equipos_data, f, ensure_ascii=False, indent=2)
        
        print(f"\n✅ Sorteo con formaciones inteligentes y balanceadas completado y guardado en equipos.json")

def main():
    """Función principal"""
    print("🚀 SORTEO ESPECIALIZADO CON PUNTAJES POR POSICIÓN")
    print("=" * 60)
    
    # Preguntar qué tipo de sorteo usar
    print("Opciones disponibles:")
    print("1. Usar puntajes específicos por posición (jugadores_avanzado.json)")
    print("2. Calcular puntajes automáticamente desde jugadores.json")
    
    try:
        opcion = input("Selecciona opción (1-2) [1]: ").strip()
        usar_especificos = opcion != "2"
    except:
        usar_especificos = True
    
    sorteo = SorteoEspecializado(usar_puntajes_especificos=usar_especificos)
    
    # Obtener jugadores confirmados
    jugadores_partido = sorteo.obtener_confirmados()
    
    if len(jugadores_partido) < 2:
        print("❌ Error: Se necesitan al menos 2 jugadores confirmados")
        return
    
    print(f"\n👥 Jugadores confirmados: {len(jugadores_partido)}")
    for j in jugadores_partido:
        print(f"   - {j['nombre']} (General: {j['puntaje']:.1f})")
    
    # Mostrar análisis si se desea
    mostrar_analisis = input("\n¿Mostrar análisis de puntajes por posición? (s/N): ").strip().lower()
    if mostrar_analisis in ['s', 'si', 'sí', 'y', 'yes']:
        sorteo.mostrar_analisis_jugadores(jugadores_partido)
    
    print(f"\n🧠 SORTEO CON FORMACIONES INTELIGENTES Y BALANCEADAS")
    print("Cada equipo tendrá una formación optimizada según las fortalezas de sus jugadores")
    print("Los jugadores serán asignados a sus mejores posiciones dentro de cada formación")
    print("Garantiza: 1 arquero + al menos 1 jugador en defensa, mediocampo y delantero")
    
    # Configurar número de intentos
    try:
        intentos_input = input("\nNúmero de intentos para optimización (1000-50000) [10000]: ").strip()
        intentos = int(intentos_input) if intentos_input else 10000
        intentos = max(1000, min(50000, intentos))
    except ValueError:
        intentos = 10000
    
    # Generar equipos con formaciones aleatorias
    resultado = sorteo.generar_equipos_balanceados(jugadores_partido, intentos=intentos)
    
    # Mostrar y guardar resultados
    sorteo.mostrar_resultados(resultado)
    sorteo.guardar_resultados(resultado)
    
    # Actualizar HTML si es posible
    try:
        import subprocess
        subprocess.run(["python", "actualizar_html.py"], check=True)
        print("✅ Archivos HTML actualizados correctamente")
    except:
        print("⚠️  No se pudo actualizar automáticamente los archivos HTML")

if __name__ == "__main__":
    main()
