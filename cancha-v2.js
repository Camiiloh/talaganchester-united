// Configuración de posiciones (puedes personalizar para más jugadores o formaciones)
const posiciones = {
  negro: [
    { left: '10%', top: '50%' }, // arquero (de 50% a 53%)
    { left: '1%', top: '20%' },  // defensas (de 20% a 23%)
    { left: '13%', top: '80%' },  // defensas (de 80% a 83%)
    { left: '31%', top: '35%' },  // defensas (de 35% a 38%)
    { left: '31%', top: '65%' },  // defensas (de 65% a 68%)
    { left: '50%', top: '30%' },
    { left: '50%', top: '70%' }
  ],
  rojo: [
    { right: '5%', top: '50%' }, // arquero
    { right: '20%', top: '20%' },
    { right: '20%', top: '80%' },
    { right: '38%', top: '35%' },
    { right: '38%', top: '65%' },
    { right: '60%', top: '30%' },
    { right: '60%', top: '70%' }
  ]
};

// Descripciones de ejemplo (puedes personalizar por jugador)
const descripciones = {
  "Maxi": "Arquero seguro y gran atajador.",
  "Pancho": "Defensa fuerte y con gran salida.",
  "Camilo": "Delantero rápido y goleador.",
  "Carlos P": "Defensa con gran visión de juego.",
  "Marco": "Defensa férreo y líder.",
  "Erik": "Mediocampista creativo y preciso.",
  "Iván": "Mediocampista de ida y vuelta.",
  "Luisito": "Arquero ágil y valiente.",
  "Turra": "Mediocampista de gran despliegue.",
  "Riky": "Defensa rápido y seguro.",
  "Pantera": "Delantero potente y hábil.",
  "Diego": "Mediocampista con llegada al gol.",
  "Juan R": "Defensa con gran anticipo.",
  "Pablo": "Defensa con buen juego aéreo."
};

async function cargarEquipos() {
  const resp = await fetch('equipos.json?_=' + Date.now());
  const data = await resp.json();
  
  // Actualizar título de la página
  actualizarTitulo(data);
  
  return data;
}

function actualizarTitulo(equipos) {
  // Formatear fecha igual que en los scripts de Python
  let fechaTexto = equipos.fecha || 'Fecha por confirmar';
  if (fechaTexto !== 'Fecha por confirmar' && fechaTexto !== 'Por confirmar') {
    try {
      const fecha = new Date(fechaTexto + 'T00:00:00');
      const diasSemana = ['Domingo', 'Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado'];
      const meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 
                     'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'];
      
      const diaSemana = diasSemana[fecha.getDay()];
      const dia = fecha.getDate();
      const mes = meses[fecha.getMonth()];
      
      fechaTexto = `${diaSemana} ${dia} de ${mes}`;
    } catch (e) {
      // Si no se puede parsear, usar el texto original
    }
  }
  
  // Formatear hora igual que en Python
  let hora = equipos.hora || 'Por confirmar';
  if (hora !== 'Por confirmar') {
    hora = `${hora} hrs`;
  }
  
  // Formatear cancha igual que en Python
  let cancha = equipos.cancha || 'Por confirmar';
  if (cancha !== 'Por confirmar' && /^\d+$/.test(cancha.toString().trim())) {
    cancha = `Cancha ${cancha}`;
  }
  
  // Crear nuevo título con el formato exacto
  const nuevoTitulo = `⚽ Partido ${fechaTexto} - ${hora} - ${cancha}`;
  
  // Actualizar title del documento
  document.title = nuevoTitulo;
  
  // Actualizar el h1 con id partido-info
  const partidoInfo = document.getElementById('partido-info');
  if (partidoInfo) {
    partidoInfo.textContent = nuevoTitulo;
  }
  
  // Actualizar cualquier otro h1 como fallback
  const h1Element = document.querySelector('h1');
  if (h1Element && !partidoInfo) {
    h1Element.textContent = `⚽ ${nuevoTitulo}`;
  }
}


function crearJugador(nombre, color, pos, idx) {
  const style = Object.entries(pos).map(([k, v]) => `${k}: ${v}`).join('; ');
  // Las fotos se rotan con CSS, no con clase adicional
  return `<div class="player-v2 ${color}" style="${style}; animation-delay:${idx*0.08}s">
    <img src="fotos/${nombre}.png" alt="${nombre}" class="player-photo-v2">
  </div>`;
}

let primeraCarga = true;
let ultimoEstado = '';

function obtenerPosicionesPorFuncion(equipo, posiciones_dict, lado) {
  const posiciones = {};
  const x_key = lado === 'izq' ? 'left' : 'right';
  
  // Agrupar jugadores por línea
  const lineas = {
    'Arquero': [],
    'Defensa': [],
    'Mediocampo': [],
    'Delantero': []
  };
  
  for (const [nombre, posicion] of Object.entries(posiciones_dict)) {
    const linea = posicion.split('-')[0];
    if (lineas[linea]) {
      lineas[linea].push({ nombre, posicion });
    }
  }
  
  // Definir posiciones Y por línea y lado - distribución más amplia
  const posicionesY = {
    'Arquero': { y: 43 },
    'Defensa-Izq': { y: 11 },
    'Defensa-Centro': { y: 43 },
    'Defensa-Der': { y: 73 },
    'Mediocampo-Izq': { y: 9 },
    'Mediocampo-Centro': { y: 43 },
    'Mediocampo-Der': { y: 79 },
    'Delantero-Centro': { y: 43 }
  };
  
  // Posiciones X por línea - defensas y mediocampo más atrás
  const posicionesX = {
    'Arquero': 1,
    'Defensa': 13,
    'Mediocampo': 25,
    'Delantero': 38
  };
  
  // Procesar cada línea
  for (const [lineaNombre, jugadores] of Object.entries(lineas)) {
    if (jugadores.length === 0) continue;
    
    const x = posicionesX[lineaNombre] || 20;
    
    // REGLA ESPECIAL: Si hay exactamente 2 jugadores en Defensa o Mediocampo,
    // forzar posiciones Izq y Der (evitar Centro)
    if ((lineaNombre === 'Defensa' || lineaNombre === 'Mediocampo') && jugadores.length === 2) {
      // Ordenar por posición original para mantener consistencia
      jugadores.sort((a, b) => {
        const ordenPosicion = { 'Izq': 0, 'Centro': 1, 'Der': 2 };
        const ladoA = a.posicion.split('-')[1] || 'Centro';
        const ladoB = b.posicion.split('-')[1] || 'Centro';
        return (ordenPosicion[ladoA] || 1) - (ordenPosicion[ladoB] || 1);
      });
      
      // Asignar: primero a Izq, segundo a Der
      for (let i = 0; i < jugadores.length; i++) {
        const { nombre } = jugadores[i];
        let posKey = i === 0 ? `${lineaNombre}-Izq` : `${lineaNombre}-Der`;
        
        // Para equipo rojo (derecha), invertir izquierda<->derecha
        if (lado === 'der') {
          posKey = posKey.replace('-Izq', '-TEMP').replace('-Der', '-Izq').replace('-TEMP', '-Der');
        }
        
        const y = posicionesY[posKey]?.y || 50;
        posiciones[nombre] = { [x_key]: x + '%', top: y + '%' };
      }
    } else {
      // Comportamiento normal para otras configuraciones
      for (const { nombre, posicion } of jugadores) {
        let posKey = posicion;
        let y = 50;
        
        // Para equipo rojo (derecha), invertir izquierda<->derecha
        if (lado === 'der') {
          if (posicion.includes('-Izq')) {
            posKey = posicion.replace('-Izq', '-Der');
          } else if (posicion.includes('-Der')) {
            posKey = posicion.replace('-Der', '-Izq');
          }
        }
        
        // Obtener Y de la posición
        if (posicionesY[posKey]) {
          y = posicionesY[posKey].y;
        } else if (posicionesY[posicion]) {
          y = posicionesY[posicion].y;
        }
        
        posiciones[nombre] = { [x_key]: x + '%', top: y + '%' };
      }
    }
  }
  
  return posiciones;
}

async function renderCanchaV2() {
  const equipos = await cargarEquipos();
  // El título ya se actualiza en cargarEquipos() -> actualizarTitulo()
  
  const field = document.getElementById('soccer-field-v2');
  // Serializar el estado actual para evitar parpadeos innecesarios
  const estadoActual = JSON.stringify({negro: equipos.negro, rojo: equipos.rojo, negro_posiciones: equipos.negro_posiciones, rojo_posiciones: equipos.rojo_posiciones});
  if (estadoActual === ultimoEstado && !primeraCarga) return;
  ultimoEstado = estadoActual;
  // Limpiar solo los jugadores, no las líneas de la cancha
  document.querySelectorAll('.player-v2').forEach(el => el.remove());
  // Negro (izquierda, lado izq)
  const posNegro = obtenerPosicionesPorFuncion(equipos.negro, equipos.negro_posiciones, 'izq');
  equipos.negro.forEach((nombre, i) => {
    const div = document.createElement('div');
    div.innerHTML = crearJugador(nombre, 'black-team', posNegro[nombre] || {}, i);
    field.appendChild(div.firstElementChild);
  });
  // Rojo (derecha, lado der)
  const posRojo = obtenerPosicionesPorFuncion(equipos.rojo, equipos.rojo_posiciones, 'der');
  equipos.rojo.forEach((nombre, i) => {
    const div = document.createElement('div');
    div.innerHTML = crearJugador(nombre, 'red-team', posRojo[nombre] || {}, i);
    field.appendChild(div.firstElementChild);
  });
  primeraCarga = false;
}

// Animación de entrada
const style = document.createElement('style');
style.innerHTML = `.player-v2 { opacity:0; transform: scale(0.7); animation: fadeInPlayer 0.7s forwards; }
@keyframes fadeInPlayer { to { opacity:1; transform: scale(1); } }`;
document.head.appendChild(style);

// Actualización inteligente: solo actualizar si hay cambios reales
let ultimaActualizacion = 0;
const INTERVALO_VERIFICACION = 5000; // 5 segundos en lugar de 2

async function verificarYActualizar() {
  try {
    const response = await fetch('equipos.json');
    const lastModified = new Date(response.headers.get('Last-Modified') || 0).getTime();
    
    if (lastModified > ultimaActualizacion) {
      ultimaActualizacion = lastModified;
      await renderCanchaV2();
    }
  } catch (error) {
    console.log('Error verificando actualizaciones:', error);
  }
}

setInterval(verificarYActualizar, INTERVALO_VERIFICACION);
window.addEventListener('DOMContentLoaded', renderCanchaV2);
