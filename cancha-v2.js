// Configuración de posiciones (puedes personalizar para más jugadores o formaciones)
const posiciones = {
  negro: [
    { left: '10%', top: '50%' }, // arquero (de 50% a 53%)
    { left: '13%', top: '20%' },  // defensas (de 20% a 23%)
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
  return data;
}


function crearJugador(nombre, color, pos, idx) {
  const style = Object.entries(pos).map(([k, v]) => `${k}: ${v}`).join('; ');
  // Solo la imagen rota -90deg, el resto del contenido queda derecho
  return `<div class="player-v2 ${color}" style="${style}; animation-delay:${idx*0.08}s">
    <img src="fotos/${nombre}.png" alt="${nombre}" class="player-photo-v2 img-rotar-90">
  </div>`;
}

let primeraCarga = true;
let ultimoEstado = '';

function obtenerPosicionesPorFuncion(equipo, posiciones_dict, lado) {
  // Agrupar por función
  const arqueros = Object.entries(posiciones_dict).filter(([_, pos]) => pos.toLowerCase() === 'arquero').map(([n]) => n);
  const defensas = Object.entries(posiciones_dict).filter(([_, pos]) => pos.toLowerCase() === 'defensa').map(([n]) => n);
  const mediocampos = Object.entries(posiciones_dict).filter(([_, pos]) => pos.toLowerCase() === 'mediocampo').map(([n]) => n);
  const delanteros = Object.entries(posiciones_dict).filter(([_, pos]) => pos.toLowerCase() === 'delantero').map(([n]) => n);
  const sin_funcion = Object.entries(posiciones_dict).filter(([_, pos]) => !pos).map(([n]) => n);
  let x_key, x_fr;
  if (lado === 'izq') {
    x_key = 'left';
    x_fr = { arquero: 2, defensa: 15, mediocampo: 27, delantero: 37, sin_funcion: 50 };
  } else {
    x_key = 'right';
    x_fr = { arquero: 2, defensa: 15, mediocampo: 27, delantero: 37, sin_funcion: 60 };
  }
  const lineas = [
    ['arquero', arqueros],
    ['defensa', defensas],
    ['mediocampo', mediocampos],
    ['delantero', delanteros],
    ['sin_funcion', sin_funcion]
  ];
  const posiciones = {};
  for (const [funcion, grupo] of lineas) {
    const n = grupo.length;
    if (n === 0) continue;
    for (let i = 0; i < n; i++) {
      const nombre = grupo[i];
      let y;
      if (n === 1) {
        y = 50;
      } else {
        y = Math.round(15 + 70 * i / (n - 1)); // de 15% a 85%
      }
      y = y - 10; // subir 10% más arriba en total
      const x = x_fr[funcion] || 50;
      posiciones[nombre] = { [x_key]: x + '%', top: y + '%' };
    }
  }
  return posiciones;
}

async function renderCanchaV2() {
  const equipos = await cargarEquipos();
  // Actualizar encabezado con fecha, hora y cancha
  const info = document.getElementById('partido-info');
  if (info && equipos.fecha && equipos.hora && equipos.cancha) {
    info.textContent = `⚽ Partido ${equipos.fecha} - ${equipos.hora} hrs - Cancha ${equipos.cancha}`;
  }
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

// Actualización continua cada 2 segundos
setInterval(renderCanchaV2, 2000);
window.addEventListener('DOMContentLoaded', renderCanchaV2);
